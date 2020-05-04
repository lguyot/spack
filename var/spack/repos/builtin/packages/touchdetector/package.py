##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Touchdetector(CMakePackage):
    """Detects autaptic touches between branches
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/TouchDetector"
    url      = "ssh://bbpcode.epfl.ch/building/TouchDetector"
    git      = "ssh://bbpcode.epfl.ch/building/TouchDetector"

    version('develop', submodules=True)
    version('5.4.0', tag='5.4.0', submodules=True)
    version('5.3.4', tag='5.3.4', submodules=True)
    version('5.3.3', tag='5.3.3', submodules=True)
    version('5.3.2', tag='5.3.2', submodules=True)
    version('5.3.1', tag='5.3.1', submodules=True)
    version('5.3.0', tag='5.3.0', submodules=True)
    version('5.2.0', tag='5.2.0', submodules=True)
    version('5.1.0', tag='5.1.0', submodules=True)
    version('5.0.1', tag='5.0.1', submodules=True)
    version('5.0.0', tag='5.0.0', submodules=True)
    version('4.4.2', tag='4.4.2', submodules=True)
    version('4.4.1', tag='4.4.1', submodules=True)
    version('4.3.3', tag='4.3.3', submodules=True)

    variant('openmp', default=False, description='Enables OpenMP support')

    depends_on('cmake', type='build')
    depends_on('boost@1.50:')
    depends_on('catch~single_header', when='@5.0.2:')
    depends_on('eigen', when='@4.5:')
    depends_on('fmt', when='@4.5:')
    depends_on('morphio@2.0.8:', when='@4.5:5.1')
    depends_on('morpho-kit', when='@5.2:')
    depends_on('mvdtool@2.1.0:', when='@5.1.1:')
    depends_on('mvdtool@1.5.1:2.0.0', when='@4.5:5.1')
    depends_on('mpi')
    depends_on('pugixml', when='@4.5:')
    depends_on('random123', when='@5.3.3:')
    depends_on('range-v3@:0.4', when='@5.0.2:5.3.2')
    depends_on('range-v3', when='@5.3.3:')
    depends_on('highfive+mpi', when='@5.3.0:')
    depends_on('nlohmann-json', when='@5.3.3:')

    # Old dependencies
    depends_on('hpctools~openmp', when='~openmp@:4.4')
    depends_on('hpctools+openmp', when='+openmp@:4.4')
    depends_on('libxml2', when='@:4.4')
    depends_on('zlib', when='@:4.4')

    patch("no-wall.patch", when='@5:')

    def cmake_args(self):
        args = [
            '-DUSE_OPENMP:BOOL={0}'.format('+openmp' in self.spec),
            '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx)
        ]
        return args
