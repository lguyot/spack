# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DocsInternalUpload(PythonPackage):
    """Documentation upload utility for internal use"""

    homepage = "https://bbpcode.epfl.ch/code/#/projects/common/docs-internal-upload,dashboards/project:overview"
    git      = "ssh://matwolf@bbpcode.epfl.ch/common/docs-internal-upload"
    url      = "ssh://matwolf@bbpcode.epfl.ch/common/docs-internal-upload"

    version('develop', branch='master')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-packaging', type='run')
