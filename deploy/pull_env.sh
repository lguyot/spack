#!/bin/sh

DEPLOYMENT_ROOT="/gpfs/bbp.cscs.ch/apps/hpc/jenkins"

usage() {
    echo "$0 pull/PR STAGE"
}

pr=$1
stage=$2

[ -z "$pr" ] && usage
[ -z "$stage" ] && usage

tmpdir=$(mktemp -d ${PWD}/spack_${pr//\//-}_XXXXXX)
spack=$(readlink -f "${DEPLOYMENT_ROOT}/${pr}/spack")
deployment=$(readlink -f "${DEPLOYMENT_ROOT}/${pr}/deploy/${stage}/latest")

if [ -z "${spack}" ]; then
    echo 'echo unable to find PR!'
    exit 1
fi

mkdir -p ${tmpdir}/install

cp -Rp ${deployment}/data/{.spack,*} ${tmpdir}
cp -Rp ${deployment}/.spack-db ${tmpdir}/install

cat <<EOF
export SOFTS_DIR_PATH=${tmpdir}/install;
export MODS_DIR_PATH=${tmpdir}/modules;
export HOME=${tmpdir};
alias spacktivate="source ${spack}/share/spack/setup-env.sh";
echo "use the command 'spacktivate' to source the spack of the PR";
EOF
