"""
Spatial Codec __init___
===================================

Initialization for spatial codec

Copyright © 2021 LEAP. All Rights Reserved.
"""

import yaml
from pathlib import Path
import logging
import logging.config

from scodec.__version__ import __version__


# cleanup all previous logs for new runtime environment
CONFIG_PATH = Path(__file__).parent.joinpath("config/log.yaml")

# check for existance of config.yaml
if not CONFIG_PATH.exists(): raise FileNotFoundError

# configure the logger
with open(CONFIG_PATH) as file:
    logging.config.dictConfig(yaml.full_load(file))

_log = logging.getLogger(__name__)
_log.info("scodec version: %s", __version__)
