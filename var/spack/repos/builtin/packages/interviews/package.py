# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Interviews(AutotoolsPackage):
    """GUI package for NEURON Simulator"""

    homepage = "https://www.neuron.yale.edu/"
    url      = "https://neuron.yale.edu/ftp/neuron/versions/v7.7/iv-19.tar.gz"

    version('19', sha256='9db9ead5f011dbf524a852be6e85f69ce9728fa891c1c5f57fb9e3050637c80f')

    depends_on("libxcomposite")
    depends_on('libxext')
    depends_on('libx11')

    def configure_args(self):
        return [
            '--with-x',
            '--x-includes={0}'.format(self.spec['libx11'].prefix.include),
            '--x-libraries={0}'.format(self.spec['libx11'].prefix.lib),
        ]
