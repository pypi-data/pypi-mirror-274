#!/usr/bin/env bash
# `argrelay` integration file: https://github.com/argrelay/argrelay

# Define with `s` in value to debug:
if [[ "${ARGRELAY_DEBUG-}" == *s* ]]
then
    set -x
    set -v
fi

# FS_36_17_84_44: check_env script:
# This script runs basic checks in shell just to
# pass control to Python for majority of checks implemented via plugins.

# Debug: Print commands before execution:
#set -x
# Debug: Print commands after reading from a script:
#set -v
# Return non-zero exit code from commands within a pipeline:
set -o pipefail
# Exit on non-zero exit code from a command:
set -e
# Inherit trap on ERR by sub-shells:
set -E
# Error on undefined variables:
set -u

script_source="${BASH_SOURCE[0]}"
# The dir of this script:
script_dir="$( cd -- "$( dirname -- "${script_source}" )" &> /dev/null && pwd )"
# FS_29_54_67_86 dir_structure: `@/exe/` -> `@/`:
argrelay_dir="$( dirname "${script_dir}" )"

########################################################################################################################

success_color="\e[42m"
failure_color="\e[41m"
reset_color="\e[0m"

# Indicate success|failure by color:
function color_failure_and_success {
    exit_code="${?}"
    if [[ "${exit_code}" == "0" ]]
    then
        # Only if this script is NOT sourced by another:
        if [[ "${0}" == "${BASH_SOURCE[0]}" ]]
        then
            echo -e "${success_color}SUCCESS:${reset_color} ${BASH_SOURCE[0]}" 1>&2
        fi
    else
        echo -e "${failure_color}FAILURE:${reset_color} ${BASH_SOURCE[0]}: exit_code: ${exit_code}" 1>&2
        exit "${exit_code}"
    fi
}

trap color_failure_and_success EXIT

########################################################################################################################

# Ensure it is `argrelay_dir` layout which contain `@/exe/` dir:
test -d "${argrelay_dir}/exe/"

# Run bootstrap to activate venv only (bootstrap should be run from `argrelay_dir`):
cd "${argrelay_dir}"
source "${argrelay_dir}/exe/bootstrap_dev_env.bash" activate_venv_only_flag

# Source it after ensuring that bootstrap was finished:
source "${argrelay_dir}/exe/argrelay_common_lib.bash"
