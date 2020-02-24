#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python -m virtualenv .env --prompt "[cortex] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install protobuf-to-dict
    .env/bin/pip install flask
    .env/bin/pip install pika --upgrade
    .env/bin/pip install -r requirements.txt
}


main "$@"
