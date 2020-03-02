##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from spack.pkg.builtin.sim_model import SimModel
import shutil
import os
import llnl.util.tty as tty

# Definitions
_CORENRN_MODLIST_FNAME = "coreneuron_modlist.txt"
_BUILD_NEURODAMUS_FNAME = "build_neurodamus.sh"
_LIB_SUFFIX = "_nd"


class NeurodamusModel(SimModel):
    """An 'abstract' base package for Simulation Models. Therefore no version.
       Eventually in the future Models are independent entities,
       not tied to neurodamus
    """
    # NOTE: Several variants / dependencies come from SimModel
    variant('synapsetool', default=True,  description="Enable SynapseTool reader (for edges)")
    variant('mvdtool',     default=True,  description="Enable MVDTool reader (for nodes)")
    variant('common_mods', default='default', description="Source of common mods. '': no change, other string: alternate path")
    # Note: We dont request link to MPI so that mpicc can do what is best
    # and dont rpath it so we stay dynamic.
    # 'run' mode will load the same mpi module
    depends_on("mpi", type=('build', 'run'))
    depends_on('neurodamus-core', type='build')
    depends_on('neurodamus-core@develop', type='build', when='@develop')
    depends_on("hdf5+mpi")
    depends_on('reportinglib')
    depends_on('reportinglib+profile', when='+profile')
    depends_on('synapsetool+mpi', when='+synapsetool')
    depends_on('py-mvdtool+mpi', type='run', when='+mvdtool')

    # NOTE: With Spack chain we no longer require support for external libs.
    # However, in some setups (notably tests) some libraries might still be
    # specificed as external and, if static,
    # and we must bring their dependencies.
    depends_on('zlib')  # for hdf5

    phases = ['setup_common_mods', 'build_model', 'merge_hoc_mod', 'build', 'install']

    def setup_common_mods(self, spec, prefix):
        """Setup common mod files if provided through variant.
        """
        # If specified common_mods then we must change the source
        # Particularly useful for CI of changes to models/common
        if spec.variants['common_mods'].value != 'default':
            shutil.move('common', '_common_orig')
            force_symlink(spec.variants['common_mods'].value, 'common')

    def build_model(self, spec, prefix):
        """Build and install the bare model.
        """
        SimModel._build_mods(self, 'mod', dependencies=[])  # No dependencies
        # Dont install intermediate src.
        SimModel.install(self, spec, prefix, install_src=False)

    def merge_hoc_mod(self, spec, prefix):
        """Add hocs and mods from neurodamus-core.

        This routine simply adds the additional mods to existing dirs
        so that incremental builds can actually happen.
        """
        core_prefix = spec['neurodamus-core'].prefix


        # If we shall build mods for coreneuron,
        # only bring from core those specified
        if spec.satisfies("+coreneuron"):
            shutil.copytree('mod', 'mod_core', True)
            with open(core_prefix.lib.mod.join(_CORENRN_MODLIST_FNAME))\
                    as core_mods:
                for aux_mod in core_mods:
                    mod_fil = core_prefix.lib.mod.join(aux_mod.strip())
                    if os.path.isfile(mod_fil):
                        shutil.copy(mod_fil, 'mod_core')

        copy_all(core_prefix.lib.hoc, 'hoc', make_link)
        copy_all(core_prefix.lib.mod, 'mod', make_link)

    def build(self, spec, prefix):
        """ Build mod files from with nrnivmodl / nrnivmodl-core.
            To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        # NOTE: sim-model now attempts to build all link and
        # include flags from the dependencies
        # link_flag += ' '
        #         + spec['synapsetool'].package.dependency_libs(spec).joined()

        self.mech_name += _LIB_SUFFIX  # Final lib name
        if spec.satisfies('+synapsetool'):
            base_include_flag = "-DENABLE_SYNTOOL"
        else:
            base_include_flag = ""

        include_flag, link_flag = self._build_mods('mod', "",
                                                   base_include_flag,
                                                   'mod_core')

        # Create rebuild script
        with open(_BUILD_NEURODAMUS_FNAME, "w") as f:
            f.write(
                _BUILD_NEURODAMUS_TPL.format(nrnivmodl=str(which('nrnivmodl')),
                                             incflags=include_flag,
                                             loadflags=link_flag))
        os.chmod(_BUILD_NEURODAMUS_FNAME, 0o770)

    def install(self, spec, prefix):
        """Install phase.

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        python/ If neurodamus-core comes with python, create links
        """
        # base dest dirs already created by model install
        # We install binaries normally, except lib has a suffix
        self._install_binaries()

        # Install mods/hocs, and a builder script
        self._install_src(prefix)
        shutil.move(_BUILD_NEURODAMUS_FNAME, prefix.bin)

        # Create mods links in share
        force_symlink(spec['neurodamus-core'].prefix.lib.mod,
                      prefix.share.mod_neurodamus)
        force_symlink(prefix.lib.mod, prefix.share.mod_full)

        filter_file(r'UNKNOWN_NEURODAMUS_MODEL', r'%s' % spec.name,
                    prefix.lib.hoc.join('defvar.hoc'))
        filter_file(r'UNKNOWN_NEURODAMUS_VERSION', r'%s' % spec.version,
                    prefix.lib.hoc.join('defvar.hoc'))

        try:
            commit_hash = self.fetcher[0].get_commit()
        except Exception as e:
            tty.warn(e)
        else:
            filter_file(r'UNKNOWN_NEURODAMUS_HASH', r"'%s'" % commit_hash[:8],
                        prefix.lib.hoc.join('defvar.hoc'))

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        for libnrnmech_name in find(self.prefix.lib, 'libnrnmech*.so',
                                    recursive=False):
            # We have the two libs and must export them in different vars
            #  - NRNMECH_LIB_PATH the combined lib (used by neurodamus-py)
            #  - BGLIBPY_MOD_LIBRARY_PATH is the pure mechanism
            #        (used by bglib-py)
            if '_nd.' in libnrnmech_name:
                env.set('NRNMECH_LIB_PATH', libnrnmech_name)
            else:
                env.set('BGLIBPY_MOD_LIBRARY_PATH', libnrnmech_name)


_BUILD_NEURODAMUS_TPL = """#!/bin/sh
set -e
if [ "$#" -eq 0 ]; then
    echo "******* Neurodamus builder *******"
    echo "Syntax:"
    echo "$(basename $0) <mods_dir> [add_include_flags] [add_link_flags]"
    echo
    echo "NOTE: mods_dir is literally passed to nrnivmodl."
    echo "If you only have the mechanism mods"
    echo " and wish to build neurodamus you need to include"
    echo " the neurodamus-specific mods."
    echo " Under \\$NEURODAMUS_ROOT/share you'll find the whole set"
    echo " of original mod files, as"
    echo " well as the neurodamus-specific mods alone."
    echo " You may copy/link them into your directory."
    exit 1
fi

# run with nrnivmodl in path
set -x
'{nrnivmodl}' -incflags '{incflags} '"$2" -loadflags '{loadflags} '"$3" "$1"
"""
