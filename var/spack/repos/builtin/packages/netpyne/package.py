# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install example
#
# You can edit this file again by typing:
#
#     spack edit example
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Netpyne(PythonPackage):
    """Netpyne: A python package to facilitate the development, parallel simulation, 
    optimization and analysis of multiscale biological neuronal networks in NEURON."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.netpyne.org/"
    git      = "https://github.com/Neurosim-lab/netpyne.git"

    # FIXME: Add proper versions and checksums here.
    version('develop', git=git, branch='master')
    version('coreneuron', git=git, branch='coreneuron')
    version('0.9.3.1', git=git, tag='v0.9.3.1')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-future', type='run')
    depends_on('py-matplotlib@2.2:', type='run')
    depends_on('py-matplotlibscalebar', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-scipy', type='run')

    # FIXME: Add dependencies if required.
    depends_on('python@3.6:')
    depends_on('neuron+coreneuron+python')
    depends_on('coreneuron', when='@coreneuron')
    
