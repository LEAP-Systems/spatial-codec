#!/usr/bin/env python

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
import logging.config
import math
from sc.visualizer import Visualizer

class SpatialCodec:
    def __init__(self, n:int, dev=False):
        self.log = logging.getLogger(__name__)
        # env vars
        self.dev = dev
        
        # ensure input space can be filled
        # TODO: deprecate
        if n < 0 :
            raise ValueError
        self.frame = (n,n)
        self.visualizer = Visualizer(self.frame)
        self.iteration = 0
        self.scale = 1

        # for 2D
        self.res = n
        # self.encode(10)
        self.s = [2**x for x in range(n)]
        self.log.info("s vector: {}".format(self.s))
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
            if self.dev:
                self.log.debug("i:%s s:%s \t|\trx:%s ry:%s\t|\tx:%s y:%s", i, s, rx, ry, x, y)
        # if self.dev:
        #     self.log.debug("returned x:%s y:%s @ iteration %s", x,y,index)
        return d

    def encode(self, i:int) -> tuple:
        """
        convert bit index to (x,y)
        """
        x,y = 0,0
        for index,s in enumerate(self.s):
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # we are done
                if x == y:
                    break
                # compute last flip (i required for forcasting)
                x,y = (lambda x,y : ((y,x) if ((len(self.s)-index) & 1) else (x,y)))(x,y)
                break
            # parity checks on last bits
            rx = 1 & (i >> 1) # is index/2 odd?
            ry = 1 & (i ^ rx) # is index/2 odd and index odd?
                              # is index/2 even and index even?
            
            if ry == 0:
                if rx == 1:
                    x,y = s-1 - x, s-1 - y
                x,y = y,x
            x += s * rx
            y += s * ry
            i = i >> 2
            if self.dev:
                self.log.debug("i:%s s:%s \t|\trx:%s ry:%s\t|\tx:%s y:%s", i, s, rx, ry, x, y)
        if self.dev:
            self.log.debug("returned x:%s y:%s @ iteration %s", x,y,index)
        return x,y

    @staticmethod
    def transform(n:int, x:int, y:int ,rx:int) -> tuple:
        """
        rotate/flip a quadrant appropriately
        """
        if rx == 1:
            x,y = n-1 - x, n-1 - y
        # Swap x and y
        return y,x
