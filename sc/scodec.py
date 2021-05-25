# -*- coding: utf-8 -*-
"""
Spatial Codec™ ABC
==================

Dependancies
------------
```
```

Copyright © 2020 Christian Sargusingh
"""

from typing import Tuple
from abc import ABC, abstractmethod
from sc.visualizer import Visualizer

class SpatialCodec(ABC):

    def __init__(self, resolution:int, dim:int) -> None:
        self.resolution = resolution
        self.dim = dim
        self.s = [2**x for x in range(self.resolution)]
        self.visualizer = Visualizer()
        super().__init__()

    @abstractmethod
    def stream_encode(self): ...

    @abstractmethod
    def stream_decode(self): ...
    
    @abstractmethod
    def transform(self): ...

    @abstractmethod
    def iterator(self, i:int) -> Tuple: ...
    
    @abstractmethod
    def decoder(self): ...
    
    @abstractmethod
    def encoder(sefl): ...

    @abstractmethod
    def render(self): ...