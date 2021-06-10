#!/bin/bash

source .env

# handle all non-zero exit status codes with a slack notification
trap 'handler $? $LINENO' ERR

handler () {
    printf "%b" "${FAIL} ✗ ${NC}${0##*/} failed on line $2 with exit status $1\n"
}

# clean old distributions
printf "%b" "${OKB}Cleaning previous distributions${NC}\n"
rm -f dist/*
printf "%b" "${OKG} ✓ ${NC}complete\n"

# build package
printf "%b" "${OKB}Building package distribution${NC}\n"
python setup.py sdist bdist_wheel
printf "%b" "${OKG} ✓ ${NC}complete\n"