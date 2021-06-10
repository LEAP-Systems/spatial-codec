#!/bin/bash
source .env

# handle all non-zero exit status codes with a slack notification
trap 'handler $? $LINENO' ERR

handler () {
    printf "%b" "${FAIL} ✗ ${NC} twine publish failed on line $2 with exit status $1\n"
}

usage() {
  cat <<EOF
Usage:  ./publish.sh testpypi OR
        ./publish.sh pypi
Publish package to testpypi or pypi service
EOF
}

if [ "$#" -ne 1 ]; then
    printf "%b" "${FAIL}Missing required arguments${NC}\n"
    printf "%b" "$(usage)\n"
    exit 1
fi

SERVICE=$1

printf "%b" "${OKB}Uploading package distribution${NC}\n"
python3 -m twine upload -r "$SERVICE" dist/* --verbose
printf "%b" "${OKG} ✓ ${NC}complete\n"