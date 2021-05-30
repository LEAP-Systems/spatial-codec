# -*- coding: utf-8 -*-
"""
N3 Spatial Codec
================
Contributors: Christian Sargusingh
Updated: 2021-05

https://www.desmos.com/calculator/hpzbeqkqc1

Dependancies
------------

Copyright © 2020 Christian Sargusingh
"""
from sc.scodec import SpatialCodec
from typing import List, Tuple
from sc.visualizer import Visualizer

class N3(SpatialCodec):
    def __init__(self, resolution:int):
        # spatial codec init
        super().__init__(resolution=resolution)

    def stream_encode(self, bytestream:bytes) -> None:
        # index = [self.encode(i) for i in range(self.resolution)]
        for curve in [(('x','y','z'),'r'),(('x','z','y'),'b'),(('y','x','z'),'g'),(('y','z','x'),'y'),(('z','x','y'),'c'),(('z','y','x'),'m')]:
            order, clr = curve
            index = [self.iterator(i,order) for i in range(self.resolution)]
            # self.render(index)
            self.visualizer.add_curve(index, str(order),clr)
            self.log.info("Added curve %s with label %s", index, str(order))
        self.visualizer.show()

    def stream_decode(self, coor:List[Tuple[int,int,int]]) -> bytes: ...

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
        r_x,r_y,r_z = 0,0,0
        for index,s in enumerate(self.s):
            self.log.debug("starting iteration %s",index)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            # if i == 0:
            #     # optimization for starting case, flipping does not do anything
            #     if x == y == z: break
            #     # compute last flip (if odd flip if even keep)
            #     x,y,z = (y,x,z) if (self.res-index) & 1 else (x,y,z) 
            #     break
            # compute region selector bits
            r_x,r_y,r_z = self.iterator(i)
            # coordinates offsets by region
            x,y,z = self.transform(r_x,r_y,r_z,x,y,z,s)
            x += s * r_x
            y += s * r_y
            z += s * r_z
            self.log.info("i:%s s:%s | rx:%s ry:%s rz:%s | x:%s y:%s z:%s", i, s, r_x, r_y, r_z, x, y, z)
        self.log.info("resolved i:%s -> x:%s y:%s z:%s", i, x,y,z)
        return x,y,z

    def transform(self, r_x:int,r_y:int,r_z:int, x:int, y:int, z:int, s:int) -> Tuple[int,int,int]:
        # region selection and transform application
        # fn = s-1 - x, s-1 - y, s-1 - z 
        # fn = x,y,z
        # fn = x,z,y 
        # fn = y,x,z 
        # fn = y,z,x 
        # fn = z,x,y 
        # fn = z,y,x 
        # if r_z == 0:
        #     if r_y == 0:
        #         if r_x == 1: x,y,z = z,s-1-y,s-1-x
        #         else: x,y,z = z,y,x
        #     else:
        #         if r_x == 1: x,y,z =  y,z,x
        #         else: x,y,z = s-1-y,z,s-1-x
        # else:
        #     if r_y == 0:
        #         if r_x == 1: x,y,z = z,s-1-y,s-1-x
        #         else: x,y,z = z,x,y
        #     else:
        #         if r_x == 1: x,y,z = y,z,x
        #         else: x,y,z = x,y,z
        if r_z == 0:
            if r_y == 0:
                if r_x == 1: x,y,z = x,s-1-y,s-1-z
                x,y,z = y,x,z
            x,y,z = z,x,y
        return x,y,z

    def iterator(self, i:int, o:Tuple[str,str,str]) -> Tuple[int,int,int]:
        """
        Base iterator for N3 algorithm    

        :param i: probe index
        :type i: int
        :return: base cartesian coordinate of bit @ index i
        :rtype: Tuple[int,int,int]
        """
        # x,y,z
        # x,z,y
        # y,x,z
        # y,z,x
        # z,y,x
        # z,x,y
        r_x = 1 & (i >> 2)
        r_y = 1 & (i >> 1 ^ r_x)
        r_z = 1 & (i ^ r_x ^ r_y)
        # regions of seperation (8 verticies)
        i = i >> 3
        if o[0] == 'x':
            if o[1] == 'y': r_t = r_x, r_y, r_z
            else: r_t = r_x, r_z, r_y
        elif o[0] == 'y':
            if o[1] == 'x': r_t = r_y, r_x, r_z
            else: r_t = r_y, r_z, r_x
        else:
            if o[1] == 'x': r_t = r_z, r_x, r_y
            else: r_t = r_z, r_y, r_x 
        return r_t

    def render(self, coors: List[Tuple[int,int,int]]) -> None:
        self.visualizer.plot_3d(coors)