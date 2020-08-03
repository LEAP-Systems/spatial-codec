#!/usr/bin/env python

"""
N2 Spatial Codec™
=================
Contributors: Christian Sargusingh
Updated: 2020-07
Repoitory: https://github.com/cSDes1gn/spatial-codec
README availble in repository root
Version: 1.0

Dependancies
------------
Sample Runs
-----------

Copyright © 2020 Christian Sargusingh
"""

from N2.plot import Visualizer

class N2:
    def __init__(self, fx:int, fy:int):
        self.frame = (fx,fy)
        self.targets = set()
        self.visualizer = Visualizer(self.frame)
    
    def populate(self, targets:set):
        self.targets = targets

    
