# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyNeurodamus(PythonPackage):
    """The BBP simulation control suite, Python API
    """

    homepage = "https://bbpteam.epfl.ch/project/spaces/display/BGLIB/Neurodamus"
    git      = "ssh://bbpcode.epfl.ch/sim/neurodamus-py"

    version('develop', branch='master')
    version('0.8.0',   tag='0.8.0')
    version('0.7.2',   tag='0.7.2')

    # We depend on Neurodamus but let the user decide which one
    depends_on('python@3.4:',      type=('build', 'run'))
    depends_on('py-setuptools',    type=('build', 'run'))
    depends_on('py-h5py',          type='run')
    depends_on('py-numpy',         type='run')
    depends_on('py-lazy-property', type='run')
    depends_on('py-docopt',        type='run')
    depends_on('py-six',           type='run')
    depends_on('py-scipy',         type='run')

    @run_after('install')
    def install_scripts(self):
        mkdirp(self.prefix.share)
        for script in ('init.py', '_debug.py'):
            copy(script, self.prefix.share)

    def setup_run_environment(self, env):
        PythonPackage.setup_run_environment(self, env)
        env.set('NEURODAMUS_PYTHON', self.prefix.share)
