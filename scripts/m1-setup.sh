#!/bin/bash

set -e

# cli
OKG="\033[92m"
WARN="\033[93m"
FAIL="\033[91m"
OKB="\033[94m"
UL="\033[4m"
NC="\033[0m"

trap 'handler $? $LINENO' ERR

function handler() {
    if [ "$1" != "0" ]; then
        printf "%b" "${FAIL} ✗ ${NC} ${0##*/} failed on line $2 with status code $1\n"
        exit "$1"
    fi
}

PYTHON_INT=$(which python3)
printf "%b" "${OKB}Setting up dependancies for dev on M1 using python interpreter located in ${OKG}$PYTHON_INT\n"
python3 -m pip install Cython
# install numpy circumventing pep517 assertion bug
python3 -m pip install --no-binary :all: --no-use-pep517 numpy
# install external mpl dependancy
brew install libjpeg

printf "%b" "${OKB}Installing python requirements${NC}\n"
python3 -m pip install -r requirements.txt 
printf "%b" "${OKG} ✓ ${NC} complete\n"