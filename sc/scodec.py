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

class SpatialCodec:
    def __init__(self, resolution:int, dim:int):
        self.log = logging.getLogger(__name__)
        # ensure input space can be filled
        self.visualizer = Visualizer()
        self.res = resolution
        self.s = [2**x for x in range(self.res)]
        self.log.info("s vector: %s", self.s)
        # dimension 
        if dim == 2:
            inputs = [self.encode(x) for x in range(self.res)]
            self.visualizer.line(inputs)
        elif dim == 3:
            inputs = [self.encode3d(x) for x in range(self.res)]
            self.visualizer.plot_3d(inputs)

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

    def encode3d(self, i:int) -> tuple:
        """
        convert bit index to (x,y,z)
        """
        # initial coordinates
        x,y,z = 0,0,0
        for index,s in enumerate(self.s):
            self.log.debug("starting iteration %s",index)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            # if i == 0:
            #     # optimization for starting case
            #     if x == y == z: break
            #     # compute last flip (if odd flip if even keep)
            #     x,y,z = (y,x,z) if (self.res-index) & 1 else (x,y,z) 
            #     break
            # parity checks on last bits
            r_x = 1 & (i >> 2)  # is index/4 odd?
            r_y = 1 & (i >> 1 ^ r_x)
            r_z = 1 & (i ^ r_x ^ r_y)
            # if r_z == 0:
            #     if r_y == 0:
            #         if r_x == 1: x,y,z = s-1 - x, s-1 - y, s-1 - z
            #         # x,y,z = x,y,z
            # else:
            #    if r_y == 0:
            #         if r_x == 1: x,y,z = s-1 - x, s-1 - y, s-1 - z
            #         x,y,z = x,y,z
            # coordinates offsets by region
            x,y,z = self.transform(r_x,r_y,r_z,x,y,z,s)
            x += s * r_x
            y += s * r_y
            z += s * r_z
            i = i >> 3 # regions of seperations (8 verticies)
            self.log.info("i:%s s:%s | rx:%s ry:%s rz:%s | x:%s y:%s z:%s", i, s, r_x, r_y, r_z, x, y, z)
        self.log.info("resolved i:%s -> x:%s y:%s z:%s", i, x,y,z)
        return x,y,z

    def transform(self, r_x:int,r_y:int,r_z:int, x:int, y:int, z:int, s:int) -> Tuple[int,int,int]:
        if r_z == 0:
            if r_y == 1:
                if r_x == 1: x,y,z = s-1 - x, s-1 - y, s-1 - z
        return x,y,z

    def encode(self, i:int) -> tuple:
        """
        convert bit index to (x,y)
        |-----|-----|
        |     |     |
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
            r_x = 1 & (i >> 1) # is index/2 odd?
            r_y = 1 & (i ^ r_x) # is index/2 odd and index odd?
                              # is index/2 even and index even?
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

