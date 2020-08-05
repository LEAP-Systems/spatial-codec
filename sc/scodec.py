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

Dependancies
------------

Copyright © 2020 Christian Sargusingh
"""
import math
from sc.visualizer import Visualizer

class SpatialCodec:
    def __init__(self, fx:int, fy:int):
        # ensure input space can be filled
        # TODO: deprecate
        if fx != fy or fx < 0 or fy < 0:
            raise ValueError
        self.frame = (fx,fy)
        self.visualizer = Visualizer(self.frame)
        self.iteration = 0
        self.scale = 1
        n = fx
        # for 2D
        self.res = n**2
        # self.encode(10)
        self.s = [2**x for x in range(int(math.sqrt(self.res)))]
        inputs = [self.encode(x) for x in range(self.res)]
        self.visualizer.line(inputs)


    def sectorize(self, n=0):
        pass
        # s1 ((0,0),()
        # s1 = ((0,self.ry), (self.rx/2, self.ry), (self.rx/2,self.ry/2), (0, self.ry/2))
        # s2 = ((0+offset,self.ry), (self.rx/2+offset, self.ry), (self.rx/2+offset,self.ry/2), (0+offset, self.ry/2))
        # s3 = ((0,self.ry-offset), (self.rx/2, self.ry-offset), (self.rx/2,self.ry/2-offset), (0, self.ry/2-offset))
        # s4 = ((0+offset,self.ry-offset), (self.rx/2+offset, self.ry-offset), (self.rx/2+offset,self.ry/2-offset), (0+offset, self.ry/2-offset))

    def decode(self, n:int, x:int, y:int) -> int:
        """
        convert (x,y) to d
        """
        d=0
        s = int(n/2)
        while s > 0:
            rx = (x & s) > 0
            ry = (y & s) > 0
            d += 2 * s * ((3 * rx) ^ ry)
            if ry == 0:
                self.rot(n, x, y, rx)
            s = int(s/2)
        return d

    def encode(self, index:int) -> tuple:
        """
        convert d to (x,y)
        """
        if index == 0:
            return 0,0
        x,y = 0,0
        # np.linspace(1,self.res,)
        for s in self.s:
            # print(s)
            if index == 0 and x == y:
                break
            # parity checks on last bits
            rx = 1 & (int(index/2))
            ry = 1 & (index ^ rx)
            # input("rx:{} ry:{}".format(rx,ry))
            if ry == 0:
                x,y = self.rot(s, x, y, rx)
            x += s * rx
            y += s * ry
            # input("x:{} y:{}".format(x,y))
            index = int(index/4)
            # input("index:{} s:{}".format(index,s))
        # input("returning x:{} y:{}".format(x,y))
        return x,y

    @staticmethod
    def rot(n:int, x:int, y:int ,rx:int) -> tuple:
        """
        rotate/flip a quadrant appropriately
        """
        if rx == 1:
            x,y = n-1 - x, n-1 - y
        # Swap x and y
        return y,x
