# -*- coding: utf-8 -*-
"""
N2 Spatial Codec™
=================
Contributors: Christian Sargusingh
Updated: 2020-07
Repoitory: https://github.com/cSDes1gn/spatial-codec
README availble in repository root
Version: 1.0

Take in an input set and generate a hilberts curve that will pass through each of the input points.

https://www.desmos.com/calculator/hpzbeqkqc1

Dependancies
------------

Copyright © 2020 Christian Sargusingh
"""

import logging
from typing import Tuple
from sc.visualizer import Visualizer
from sc.scodec import SpatialCodec

class N2(SpatialCodec):
    def __init__(self, resolution:int, dim:int):
        self.log = logging.getLogger(__name__)
        # ensure input space can be filled
        
        self.res = resolution
        self.s = [2**x for x in range(self.res)]
        self.log.info("s vector: %s", self.s)
        # dimension 
        inputs = [self.encode(x) for x in range(self.res)]
        self.visualizer.line(inputs)

    def decode(self, n:int, x:int, y:int) -> int:
        """
        convert (x,y) to d
        """
        d = 0
        s = n >> 1
        while s > 0:
            rx = (x & s) > 0
            ry = (y & s) > 0
            d += 2 * s * ((3 * rx) ^ ry)
            if ry == 0:
                if rx == 1:
                    x,y = s-1 - x, s-1 - y
                x,y = y,x
            s = s >> 1
            self.log.debug("i:%s s:%s \t|\trx:%s ry:%s\t|\tx:%s y:%s", i, s, rx, ry, x, y)
        return d

    def iterator(self, i:int) -> Tuple[int,int]:
        """
        Defines base iterator function for n2 spatial codec algorithm

        :param i: [description]
        :type i: int
        :return: [description]
        :rtype: Tuple[int,int]
        """
        r_x = 1 & (i >> 1)
        r_y = 1 & (i ^ r_x)
        return r_x, r_y

    def encode(self, i:int) -> tuple:
        """
        convert bit index to (x,y)
        |-----|-----|
        |  1  |     |
        |-----|-----|
        |     |     |
        |-----|-----|
        """
        self.log.info("Computing coordinate at bit: %s", i)
        # initial coordinates
        x,y = 0,0
        for level, cells in enumerate(self.s):
            self.log.info("starting level %s",level)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # we are done
                if x == y: break
                # compute last flip (i required for forcasting)
                x,y = (y,x) if (self.res-level) & 1 else (x,y)
                break
            # parity checks on last bits rx and ry can only be 1 or 0

            # grid rotation function for this region
            if r_y == 0:
                if r_x == 1: x,y = cells-1 - x, cells-1 - y
                x,y = y,x
            # assign x and y to 
            x += cells * r_x # x = x + (s or 0)
            y += cells * r_y # y = y + (s or 0)
            i = i >> 2 # regions of seperation (4 verticies)
            self.log.info("i:%s cells:%s | i/2 odd:%s i/2 odd and i odd:%s -> x:%s y:%s", i, cells, r_x, r_y, x, y)
        self.log.info("resolved i:%s -> x:%s y:%s", i, x, y) 
        return x,y

