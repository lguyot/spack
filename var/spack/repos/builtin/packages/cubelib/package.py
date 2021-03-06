# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cubelib(AutotoolsPackage):
    """Component of CubeBundle: General purpose C++ library and tools """

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url = "http://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubelib-4.4.tar.gz"

    version('4.4.4', sha256='adb8216ee3b7701383884417374e7ff946edb30e56640307c65465187dca7512')
    version('4.4.3', sha256='bcd4fa81a5ba37194e590a5d7c3e6c44b448f5e156a175837b77c21206847a8d')
    version('4.4.2', sha256='843335c7d238493f1b4cb8e07555ccfe99a3fa521bf162e9d8eaa6733aa1f949')
    version('4.4',   sha256='77548e1732fa5e82b13cc8465c8a21349bf42b45a382217d2e70d18576741d5c')

    depends_on('pkgconfig', type='build')
    depends_on('zlib')

    def url_for_version(self, version):
        url = 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubelib-{1}.tar.gz'
        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec

        configure_args = ['--enable-shared']

        if spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')
        elif spec.satisfies('%pgi'):
            configure_args.append('--with-nocross-compiler-suite=pgi')
        elif spec.satisfies('%clang'):
            configure_args.append('--with-nocross-compiler-suite=clang')

        return configure_args

    def install(self, spec, prefix):
        make('install', parallel=False)
