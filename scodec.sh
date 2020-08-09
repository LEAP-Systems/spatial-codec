#!/bin/bash

# dev mode enable
export SC_N=$1
export SC_ENV=$2

# for flask visualizer interface
export FLASK_ENV=development

# run in background
nohup python3 -m sc &