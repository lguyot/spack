# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Openscenegraph(CMakePackage):
    """OpenSceneGraph is an open source, high performance 3D graphics toolkit
       that's used in a variety of visual simulation applications."""

    homepage = "http://www.openscenegraph.org"
    url      = "https://github.com/openscenegraph/OpenSceneGraph/archive/OpenSceneGraph-3.2.3.zip"

    version('3.2.3', sha256='1e15f2c92e2e4a396f42fd4a8b64b31a65d2036b9fb5d1555a798a81598a533d')
    version('3.1.5', sha256='1ca3f16ec023486686087c832e64e54da81cc12344549ba26ededfd9295572bc')

    variant('shared', default=True, description='Builds a shared version of the library')

    patch('relwithdebinfo_postfix.patch')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('qt@4: +opengl')
    depends_on('zlib')

    def cmake_args(self):
        spec = self.spec

        shared_status = 'ON' if '+shared' in spec else 'OFF'

        args = [
            '-DDYNAMIC_OPENSCENEGRAPH={0}'.format(shared_status),
            '-DDYNAMIC_OPENTHREADS={0}'.format(shared_status),
            '-DZLIB_INCLUDE_DIR={0}'.format(spec['zlib'].prefix.include),
            '-DZLIB_LIBRARY={0}/libz.{1}'.format(spec['zlib'].prefix.lib,
                                                 dso_suffix),
            '-DBUILD_OSG_APPLICATIONS=OFF',
            '-DOSG_NOTIFY_DISABLED=ON',
            '-DLIB_POSTFIX=',
        ]

        # NOTE: This is necessary in order to allow OpenSceneGraph to compile
        # despite containing a number of implicit bool to int conversions.
        if spec.satisfies('%gcc'):
            args.extend([
                '-DCMAKE_C_FLAGS=-fpermissive',
                '-DCMAKE_CXX_FLAGS=-fpermissive',
            ])

        return args
