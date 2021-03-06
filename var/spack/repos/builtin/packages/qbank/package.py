# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Qbank(Package):
    """QBank is a unique dynamic reservation-based allocation management system
    that manages the utilization of computational resources in a multi-project
    environment. It is used in conjunction with a resource management system
    allowing an organization to guarantee greater fairness and enforce mission
    priorities by associating a charge with the use of computational resources
    and allocating resource credits which limit how much of the resources may
    be used at what time and by whom. It tracks resource utilization and allows
    for insightful planning."""

    # QBank is so old that it no longer has (never had?) a homepage
    # but it was developed at Pacific Northwest National Laboratory
    # by Scott Jackson <Scott.Jackson@pnl.gov>
    homepage = "http://www.pnnl.gov/"
    url      = "file://{0}/qbank-2.10.4.tar.gz".format(os.getcwd())
    manual_download = True

    version('2.10.4', '0820587353e63d32ddb49689dd4289e7')

    variant('doc', default=False, description='Build documentation')

    depends_on('openssl')

    depends_on('perl@5.6:5.16',  type=('build', 'run'))
    depends_on('perl-dbi@1.00:', type=('build', 'run'))

    phases = ['configure', 'build', 'install']

    def configure_args(self):
        prefix = self.prefix

        config_args = [
            '--prefix', prefix,
            '--logdir', join_path(prefix, 'var', 'log', 'qbank')
        ]

        return config_args

    def configure(self, spec, prefix):
        perl = which('perl')
        perl('configure', *self.configure_args())

    def build(self, spec, prefix):
        make()

        if '+doc' in spec:
            make('docs')

    def install(self, spec, prefix):
        make('install')

        if '+doc' in spec:
            install_tree('doc', join_path(prefix, 'doc'))

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        prefix = self.prefix

        if '+doc' in spec:
            run_env.prepend_path('MANPATH', join_path(prefix, 'doc'))
