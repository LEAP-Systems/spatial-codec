# -*- coding: utf-8 -*-
"""
Spatial Codec™ ABC
==================

Abstract base class implemented by n2 and n3 spatial codec algorithms

Dependancies
------------
```
import logging
from typing import List, Tuple
from abc import ABC, abstractmethod
from sc.visualizer import Visualizer
```
Copyright © 2020 Christian Sargusingh
"""

import logging
from typing import List, Tuple
from abc import ABC, abstractmethod
from sc.visualizer import Visualizer


class SpatialCodec(ABC):

    def __init__(self, resolution:int) -> None:
        self.log = logging.getLogger(__name__)
        self.resolution = resolution
        self.s = [2**x for x in range(self.resolution)]
        self.log.info("s vector: %s", self.s)
        self.visualizer = Visualizer()
        super().__init__()

    @abstractmethod
    def stream_encode(self, bytestream:bytes) -> None: ...

    @abstractmethod
    def stream_decode(self, coor:List[Tuple]) -> bytes: ...

    @abstractmethod
    def decode(self) -> int: ...

    @abstractmethod
    def encode(self): ...

    @abstractmethod
    def render(self, coors:List[Tuple]): ...

    @abstractmethod
    def transform(self): ...

    @abstractmethod
    def iterator(self, i:int) -> Tuple: ...
