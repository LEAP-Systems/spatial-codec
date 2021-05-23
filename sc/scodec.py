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
from sc.visualizer import Visualizer

class SpatialCodec:
    def __init__(self, n:int):
        self.log = logging.getLogger(__name__)
        # ensure input space can be filled
        self.visualizer = Visualizer()
        self.iteration = 0
        self.scale = 1
        # for 2D
        self.res = n
        self.s = [2**x for x in range(n)]
        self.log.info("s vector: %s", self.s)
        inputs = [self.encode(x) for x in range(self.res)]
        # inputs = [self.encode3d(x) for x in range(self.res)]
        # self.visualizer.plot_3d(inputs)
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

    def encode3d(self, i:int) -> tuple:
        """
        convert bit index to (x,y,z)
        """
        # initial coordinates
        x,y,z = 0,0,0
        for index,s in enumerate(self.s):
            self.log.info("starting iteration %s",index)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # optimization for starting case
                if x == y: break
                # compute last flip (if odd flip if even keep)
                x,y,z = (y,x,z) if (self.res-index) & 1 else (x,y,z) 
                break
            # parity checks on last bits
            rx = 1 & (i >> 1) # is i/2 odd?
            ry = 1 & (i ^ rx) # is i/2 odd and i odd?
                              # is i/2 even and i even?
            if ry == 0:
                if rx == 1: x,y,z = s-1 - x, s-1 - y, z
                x,y,z = y,x,z
            x += s * rx
            y += s * ry
            i = i >> 2 # log2i (reverse of s vector)
            self.log.debug("i:%s s:%s | rx:%s ry:%s rz: | x:%s y:%s z:%s", i, s, rx, ry, x, y, z)
        self.log.info("resolved i:%s -> x:%s y:%s z:%s", i, x,y,z)
        return x,y,z

    def encode(self, i:int) -> tuple:
        """
        convert bit index to (x,y)
        """
        # initial coordinates
        x,y = 0,0
        for index,s in enumerate(self.s):
            self.log.info("starting iteration %s",index)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # we are done
                if x == y: break
                # compute last flip (i required for forcasting)
                x,y = (y,x) if (self.res-index) & 1 else (x,y)
                break
            # parity checks on last bits rx and ry can only be 1 or 0
            rx = 1 & (i >> 1) # is index/2 odd?
            ry = 1 & (i ^ rx) # is index/2 odd and index odd?
                              # is index/2 even and index even?
            if ry == 0:
                if rx == 1: x,y = s-1 - x, s-1 - y
                x,y = y,x
            # cumulative scores may represent 
            x += s * rx # x = x + (s or 0)
            y += s * ry # y = y + (s or 0)
            i = i >> 2 # log2i (inverse of 2^n)
            self.log.info("i:%s s:%s | i/2 odd:%s i/2 odd and i odd:%s -> x:%s y:%s", i, s, rx, ry, x, y)
        self.log.info("resolved i:%s -> x:%s y:%s", i, x, y) 
        return x,y

