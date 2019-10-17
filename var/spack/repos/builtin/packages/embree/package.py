# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Embree(CMakePackage):
    """High-performance ray tracing kernel"""

    homepage = "https://embree.github.io/"
    url = "https://github.com/embree/embree/archive/v3.6.1.tar.gz"
    generator = 'Ninja'

    version('3.6.1', sha256='d3ccbc54fe1a3eb1c373036fb146757082773735')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('ispc', type='build')
    depends_on('ninja', type='build')
    depends_on('tbb')

    def cmake_args(self):
        return ['-DEMBREE_TUTORIALS=OFF', '-DEMBREE_IGNORE_INVALID_RAYS=ON']
