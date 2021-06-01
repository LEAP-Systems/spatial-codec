# -*- coding: utf-8 -*-
"""
N3 Spatial Codec
================
Contributors: Christian Sargusingh
Updated: 2021-05


Dependancies
------------

Copyright © 2020 Christian Sargusingh
"""

from sc.scodec import SpatialCodec
from typing import List, Tuple
from sc.iterators import Iterators

class N3(SpatialCodec):
    def __init__(self, resolution:int):
        if resolution > 8:
            raise NotImplementedError('This version supports single iteration (max 8 bit resolution) curves in 3D space')
        # spatial codec init
        super().__init__(resolution=resolution)

    def stream_encode(self, bytestream:bytes, mpl:bool=False) -> List[Tuple[int,int,int]]:
        # remove excess bytes if word exceeds an 8 bit number
        bitstream = int(bytestream.hex(), base=16) & 0xff
        self.log.debug("bitstream: %s", bin(bitstream))
        # stretch bistream into iterable of single bits
        bits = [bitstream >> i & 0x1 for i in range(self.resolution)]
        # generate index by encoding each set bit sequentially
        stream = list(filter(None, [self.encode(i) if b else None for i,b in enumerate(bits)]))
        self.log.debug("stream: %s", stream)
        if mpl: self.render(stream)
        return stream 

    def stream_decode(self, coor:List[Tuple[int,int,int]]) -> bytes: ...

    def show_iterators(self) -> None:
        """
        Interactive visualizer for iteration variations
        """
        # variation iterator
        for curve in Iterators.variations:
            order, clr = curve
            self.visualizer.add_n3_curve(
                d=[self.transform(*self.iterator(i), order) for i in range(8)],
                marker='o',
                label=str(order),
                clr=clr
            )
        self.visualizer.show()

    def decode(self, n:int, x:int, y:int) -> int:
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

    def encode(self, i:int) -> Tuple[int,int,int]:
        # initial coordinates
        x,y,z = 0,0,0
        # for index,s in enumerate(self.s):
        #     self.log.debug("starting iteration %s",index)
        #     # Once the index reaches 0 the x and y bits are latched and alternate between each other
        #     # before converging before we exceed the range boundary n
        #     if i == 0:
        #         # optimization for starting case, flipping does not do anything
        #         if x == y == z: break
        #         # compute last flip (if odd flip if even keep)
        #         x,y,z = (y,x,z) if (self.res-index) & 1 else (x,y,z) 
        #         break
        #     # compute region selector bits
        #     # coordinates offsets by region
        #     # the iterator changes with different i values
        #     r_x,r_y,r_z = self.iterator(i, ('x','z','y'))
        #     # regions of seperation (8 verticies)
        #     i = i >> 3
        #     x,y,z = self.transform(r_x,r_y,r_z,x,y,z,s)
        #     self.log.info("i:%s s:%s | rx:%s ry:%s rz:%s | x:%s y:%s z:%s", i, s, r_x, r_y, r_z, x, y, z)
        self.iterator(i)
        self.log.info("resolved i:%s -> x:%s y:%s z:%s", i, x,y,z)
        return x,y,z

    def iterator(self, i:int) -> Tuple[int,int,int]:
        """
        Base iterator for N3 algorithm

        :param i: probe index
        :type i: int
        :return: base cartesian coordinate of bit @ index i
        :rtype: Tuple[int,int,int]
        """
        r_x = 1 & (i >> 2)
        r_y = 1 & (i >> 1 ^ r_x)
        r_z = 1 & (i ^ r_x ^ r_y)
        return r_x,r_y,r_z

    def transform(self, r_x:int, r_y:int, r_z:int, o:Tuple[str,str,str]) -> Tuple[int,int,int]:
        # region selection and transform application
        # lambda x,y,z: (x + (s * r_x), y + (s * r_y), z + (s * r_z))
        # if (r_x,r_y,r_z) == (0,0,0):
        #     x,y,z = y,x,z
        # elif (r_x,r_y,r_z) == (0,1,0) or (0,1,1):
        #     x,y,z = z,y,x
        # elif (r_x,r_y,r_z) == (0,0,1) or (1,0,1):
        #     x,y,z = x,-y,-z
        # elif (r_x,r_y,r_z) == (1,1,1) or (1,1,0):
        #     x,y,z = -z,y,x
        # else:
        #     x,y,z = -z,x,y
        # x += s * r_x # x = x + (s | 0)
        # y += s * r_y # y = y + (s | 0)
        # z += s * r_z # z = z + (s | 0)
        # translate base iterator
        # iterator variant selector (-x and x are somehow the same?)
        r_t = r_x, r_y, r_z
        if o[0] == 'x':
            if o[1] == 'y':
                if o[2] == 'z': r_t = r_x, r_y, r_z
                else: r_t = r_x, r_y, 1-r_z 
            elif o[1] == '-y':
                if o[2] == 'z': r_t = r_x, 1-r_y, r_z
                else: r_t = r_x, 1-r_y, 1-r_z 
            elif o[1] == 'z':
                if o[2] == 'y': r_t = r_x, r_z, r_y
                else: r_t = r_x, r_z, 1-r_y
            else:
                if o[2] == 'y': r_t = r_x, 1-r_z, r_y
                else: r_t = r_x, 1-r_z, 1-r_y
        elif o[0] == '-x':
            if o[1] == 'y':
                if o[2] == 'z': r_t = 1-r_x, r_y, r_z
                else: r_t = 1-r_x, r_y, 1-r_z 
            elif o[1] == '-y':
                if o[2] == 'z': r_t = 1-r_x, 1-r_y, r_z
                else: r_t = 1-r_x, 1-r_y, 1-r_z
            elif o[1] == 'z':
                if o[2] == 'y': r_t = 1-r_x, r_z, r_y
                else: r_t = 1-r_x, r_z, 1-r_y
            else:
                if o[2] == 'y': r_t = 1-r_x, 1-r_z, r_y
                else: r_t = 1-r_x, 1-r_z, 1-r_y
        elif o[0] == 'y':
            if o[1] == 'x':
                if o[2] == 'z': r_t = r_y, r_x, r_z
                else: r_t = r_y, r_x, 1-r_z 
            elif o[1] == '-x':
                if o[2] == 'z': r_t = r_y, 1-r_x, r_z
                else: r_t = r_y, 1-r_x, 1-r_z 
            elif o[1] == 'z':
                if o[2] == 'x': r_t = r_y, r_z, r_x
                else: r_t = r_y, r_z, 1-r_x
            else:
                if o[2] == 'x': r_t = r_y, 1-r_z, r_x
                else: r_t = r_y, 1-r_z, 1-r_x
        elif o[0] == '-y':
            if o[1] == 'x':
                if o[2] == 'z': r_t = 1-r_y, r_x, r_z
                else: r_t = 1-r_y, r_x, 1-r_z 
            elif o[1] == '-x':
                if o[2] == 'z': r_t = 1-r_y, 1-r_x, r_z
                else: r_t = 1-r_y, 1-r_x, 1-r_z 
            elif o[1] == 'z':
                if o[2] == 'x': r_t = 1-r_y, r_z, r_x
                else: r_t = 1-r_y, r_z, 1-r_x
            else:
                if o[2] == 'x': r_t = 1-r_y, 1-r_z, r_x
                else: r_t = 1-r_y, 1-r_z, 1-r_x
        elif o[0] == 'z':
            if o[1] == 'x':
                if o[2] == 'y': r_t = r_z, r_x, r_y
                else: r_t = r_z, r_x, 1-r_y 
            elif o[1] == '-x':
                if o[2] == 'y': r_t = r_z, 1-r_x, r_y
                else: r_t = r_z, 1-r_x, 1-r_y 
            elif o[1] == 'y':
                if o[2] == 'x': r_t = r_z, r_y, r_x
                else: r_t = r_z, r_y, 1-r_x
            else:
                if o[2] == 'x': r_t = r_z, 1-r_y, r_x
                else: r_t = r_z, 1-r_y, 1-r_x
        elif o[0] == '-z':
            if o[1] == 'x':
                if o[2] == 'y': r_t = 1-r_z, r_x, r_y
                else: r_t = 1-r_z, r_x, 1-r_y
            elif o[1] == '-x':
                if o[2] == 'y': r_t = 1-r_z, 1-r_x, r_y
                else: r_t = 1-r_z, 1-r_x, 1-r_y 
            elif o[1] == 'y':
                if o[2] == 'x': r_t = 1-r_z, r_y, r_x
                else: r_t = 1-r_z, r_y, 1-r_x
            else:
                if o[2] == 'x': r_t = 1-r_z, 1-r_y, r_x
                else: r_t = 1-r_z, 1-r_y, 1-r_x
        return r_t 

    def render(self, stream:List[Tuple[int,int,int]]) -> None:
        index = [self.encode(i) for i in range(self.resolution)]
        self.log.debug("index: %s", index)
        self.log.debug("stream: %s", stream)
        self.visualizer.add_n3_curve(index, marker='', label='index', clr='k')
        self.visualizer.add_n3_curve(stream, marker='o', label='stream', clr='k')