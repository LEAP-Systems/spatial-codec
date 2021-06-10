# -*- coding: utf-8 -*-
"""
Spatial Codec™ ABC
==================

Abstract base class implemented by n2 and n3 spatial codec algorithms

Dependancies
------------
```
import math
import logging
from typing import List, Tuple
from abc import ABC, abstractmethod
from scodec.plt.visualizer import Visualizer
```
Copyright © 2021 LEAP. All Rights Reserved.
"""

import math
import logging
from typing import List, Tuple
from abc import ABC, abstractmethod
from scodec.plt.visualizer import Visualizer


class SpatialCodec(ABC):
    def __init__(self, block_size: int, base_block_size: int) -> None:
        self.log = logging.getLogger(__name__)
        # compute codec resolution (next power of 2)
        self.visualizer = Visualizer()
        super().__init__()
        # validate block size
        if not math.log(block_size, base_block_size).is_integer():
            raise ValueError("{} block size must be a power of {}".format(
                __name__, base_block_size))
        self.block_size = block_size
        self._sv = [2**x for x in range(block_size)]
        self.log.debug("s vector: %s", self._sv)

    @abstractmethod
    def stream_encode(self, bytestream: bytes) -> None:
        ...

    @abstractmethod
    def stream_decode(self, coor: List[Tuple], byte_size: int) -> bytes:
        ...

    @abstractmethod
    def decode(self, coor: Tuple) -> int:
        ...

    @abstractmethod
    def encode(self, i: int):
        ...

    @abstractmethod
    def render(self, coors: List[Tuple]):
        ...

    @abstractmethod
    def transform(self):
        ...

    @abstractmethod
    def iterator(self, i: int) -> Tuple:
        ...
