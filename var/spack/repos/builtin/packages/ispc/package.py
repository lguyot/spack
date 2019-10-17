# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack import *


class Ispc(Package):
    """ispc is a compiler for a variant of the C programming language, with
    extensions for single program, multiple data programming mainly aimed at CPU
    SIMD platforms."""

    homepage = "https://github.com/ispc/ispc/"
    url      = "https://sourceforge.net/projects/ispcmirror/files/v1.9.2/ispc-v1.9.2-linux.tar.gz"

    version('1.9.2', sha256='6ec8d47af5ad1cf4448f64be539a9a3d216eb7c2')

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/ispcmirror/files/v{0}/ispc-v{0}-{1}.tar.gz"

        system = platform.system()
        if system == 'Darwin':
            checksums = {
                Version('1.9.2'): '5205e0fca11361f8527d3489ee1503fd79ab8511db6399830c052ccf210cc3b7',
            }
            self.versions[version] = {'checksum': checksums[version]}
            if self.spec.satisfies('@1.9.2:'):
                return url.format(version, 'MacOs')
            else:
                return url.format(version, 'osx')
        else:  # linux
            return url.format(version, 'linux')

    def install(self, spec, prefix):
        for d in ['bin', 'examples']:
            if os.path.isdir(d):
                install_tree(d, join_path(self.prefix, d))
