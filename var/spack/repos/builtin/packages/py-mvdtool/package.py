# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMvdtool(PythonPackage):
    """Python bindings for the MVD3 neuroscience file format parser and tool
    """

    homepage = "https://github.com/BlueBrain/MVDTool"
    url      = "https://github.com/BlueBrain/MVDTool.git"
    git      = "https://github.com/BlueBrain/MVDTool.git"

    version('develop', branch='master', submodules=True, clean=False)
    version('2.3.0', tag='v2.3.0', submodules=True, clean=False)
    version('2.2.1', tag='v2.2.1', submodules=True, clean=False)
    version('2.2.0', tag='v2.2.0', submodules=True, clean=False)
    version('2.1.0', tag='v2.1.0', submodules=True, clean=False)
    version('2.0.0', tag='v2.0.0', submodules=True, clean=False)

    variant('mpi', default=True, description='Build with support for MPI')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('cmake@3.2:', type='build')
    depends_on('py-numpy', type='run')

    depends_on('mpi', when='+mpi')
    depends_on('hdf5+mpi', type=('build', 'run'), when="+mpi")
    depends_on('hdf5~mpi', type=('build', 'run'), when="~mpi")
    depends_on('libsonata~mpi', type=('build', 'run'), when='~mpi@2.1:')
    depends_on('libsonata+mpi', type=('build', 'run'), when='+mpi@2.1:')
    depends_on('highfive~mpi', type='build', when='~mpi')
    depends_on('highfive+mpi', type='build', when='+mpi')

    @when('+mpi')
    @run_before('build')
    def configure(self):
        env['CC'] = self.spec['mpi'].mpicc
        env['CXX'] = self.spec['mpi'].mpicxx
