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
from sc.visualizer import Visualizer
```
Copyright © 2020 Christian Sargusingh
"""

import math
import logging
from typing import List, Tuple
from abc import ABC, abstractmethod
from sc.visualizer import Visualizer


class SpatialCodec(ABC):

    def __init__(self, resolution:int) -> None:
        self.log = logging.getLogger(__name__)
        # compute codec resolution (next power of 2)
        self.resolution = 4 ** math.ceil(math.log(resolution,4))
        self.log.info("Codec resolution: %s", self.resolution)
        self.s = [2**x for x in range(self.resolution)]
        self.log.info("s vector: %s", self.s)
        self.visualizer = Visualizer()
        super().__init__()

    @abstractmethod
    def stream_encode(self, bytestream:bytes) -> None: ...

    @abstractmethod
    def stream_decode(self, coor:List[Tuple], byte_size:int) -> bytes: ...

    @abstractmethod
    def decode(self, coor:Tuple) -> int: ...

    @abstractmethod
    def encode(self, i:int): ...

    @abstractmethod
    def render(self, coors:List[Tuple]): ...

    @abstractmethod
    def transform(self): ...

    @abstractmethod
    def iterator(self, i:int) -> Tuple: ...
