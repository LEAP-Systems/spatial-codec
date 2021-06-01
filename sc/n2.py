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

from typing import List, Tuple
from sc.scodec import SpatialCodec

class N2(SpatialCodec):

    def __init__(self, resolution:int):
        super().__init__(resolution=resolution)

    def stream_encode(self, bytestream:bytes, mpl:bool=False) -> List[Tuple[int,int]]:
        # remove excess bytes if word exceeds resolution
        bitstream = int(bytestream.hex(), base=16) & (2**self.resolution - 1)
        self.log.debug("bitstream: %s", bin(bitstream))
        bits = [bitstream >> i & 0x1 for i in range(self.resolution)]
        self.log.debug("%s",bits )
        index =list(filter(None,[self.encode(i) if b else None for i,b in enumerate(bits)]))
        self.log.debug("index: %s", index)
        if mpl: self.render(index)
        return index

    def stream_decode(self, coor:List[Tuple[int,int]]) -> bytes: ...

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

    def encode(self, i:int) -> Tuple[int,int]:
        index = i
        self.log.debug("Computing coordinate at bit: %s", i)
        # initial coordinates
        x,y = 0,0
        for level, c in enumerate(self.s):
            self.log.debug("starting level %s",level)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # we are done
                if x == y: break
                # compute last flip (i required for forcasting)
                x,y = (y,x) if (self.resolution-level) & 1 else (x,y)
                break
            # generate base iterator 
            r_x,r_y = self.iterator(i)
            x,y = self.transform(x,y,r_x,r_y,c)
            i = i >> 2 # regions of seperation (4 verticies)
            self.log.debug("i:%s cells:%s | i/2 odd:%s i/2 odd and i odd:%s -> x:%s y:%s", i, c, r_x, r_y, x, y)
        self.log.debug("resolved i:%s -> x:%s y:%s", index, x, y) 
        return x,y

    def transform(self, x:int, y:int, r_x:int, r_y:int, c:int) -> Tuple[int,int]:
        """
        Rotate and translate base iterator by cell selector c

        :param x: computed x coordinate state @ cell iteration c
        :type x: int
        :param y: computed y coordinate state @ cell iteration c
        :type y: int
        :param r_x: [description]
        :type r_x: int
        :param r_y: [description]
        :type r_y: int
        :param s: cell index
        :type s: int
        :return: transformed coordinate tuple from cell c
        :rtype: Tuple[int,int]
        """
        # rotation function for this region
        if r_y == 0:
            if r_x == 1: x,y = c-1 - x, c-1 - y
            x,y = y,x
        # translate base iterator
        x += c * r_x # x = x + (s or 0)
        y += c * r_y # y = y + (s or 0)
        return x,y

    def iterator(self, i:int) -> Tuple[int,int]:
        """
        Base iterator for N2 algorithm

        :param i: probe index
        :type i: int
        :return: base cartesian coordinate of bit @ index i
        :rtype: Tuple[int,int]
        """
        r_x = 1 & (i >> 1)
        r_y = 1 & (i ^ r_x)
        return r_x,r_y

    def render(self, stream:List[Tuple[int,int]]) -> None:
        index = [self.encode(i) for i in range(self.resolution)]
        self.log.debug("index: %s", index)
        self.log.debug("stream: %s", stream)
        self.visualizer.add_n2_curve(index, marker='', label='index', clr='k')
        self.visualizer.add_n2_curve(stream, marker='o', label='stream', clr='r')
        self.visualizer.show()