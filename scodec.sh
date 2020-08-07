#!/bin/bash

# dev mode enable
export SC_ENV=$1
export SC_N=$2
# for flask visualizer interface
export FLASK_ENV=development

python3 -m sc