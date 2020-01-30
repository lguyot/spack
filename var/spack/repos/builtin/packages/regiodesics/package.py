# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Regiodesics(CMakePackage):

    git = "ssh://bbpcode.epfl.ch/viz/Regiodesics"

    version('0.1.0', tag='0.1.0', submodules=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('ninja', type='build')
    depends_on('bbptestdata')
    depends_on('boost@1.65.0')
    depends_on('openscenegraph')
