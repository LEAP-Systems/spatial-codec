#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Spatial Codec Logging Configuration
===================================

Copyright © 2021 LEAP. All Rights Reserved.
"""
import logging.config
import os
from pathlib import Path

import yaml


def config():
    # cleanup all previous logs for new runtime environment
    cwd = os.getcwd()
    os.chdir(Path(__file__).parent)

    logs = list(
        filter(lambda file: os.path.isfile(file) and file.split(".")[1] == "log", os.listdir())
    )
    for log in logs:
        os.remove(log)
    os.chdir(cwd)

    CONFIG_PATH = Path(__file__).parent.joinpath("config.yaml")

    # check for existance of config.yaml
    if not CONFIG_PATH.exists():
        raise FileNotFoundError

    # configure the logger
    with open(CONFIG_PATH) as file:
        logging.config.dictConfig(yaml.full_load(file))
