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
        variations = [
            (('x','y','z'),'k'),
            (('x','-y','z'),'r'),
            (('x','y','-z'),'b'),
            (('x','z','y'),'g'),
            (('x','-z','y'),'y'),
            (('x','z','-y'),'c'),
            (('x','-y','-z'),'m'),
            (('x','-z','-y'),'blueviolet'),
            # (('-x','y','z'),'k'),
            # (('-x','-y','z'),'r'),
            # (('-x','y','-z'),'b'),
            # (('-x','z','y'),'g'),
            # (('-x','-z','y'),'y'),
            # (('-x','z','-y'),'c'),
            # (('-x','-y','-z'),'m'),
            # (('-x','-z','-y'),'blueviolet'),
            (('y','x','z'),'k'),
            # (('y','-x','z'),'r'),
            (('y','x','-z'),'b'),
            (('y','z','x'),'g'),
            (('y','-z','x'),'y'),
            # (('y','z','-x'),'c'),
            # (('y','-x','-z'),'m'),
            # (('y','-z','-x'),'blueviolet'),
            (('-y','x','z'),'k'),
            # (('-y','-x','z'),'r'),
            (('-y','x','-z'),'b'),
            (('-y','z','x'),'g'),
            (('-y','-z','x'),'y'),
            # (('-y','z','-x'),'c'),
            # (('-y','-x','-z'),'m'),
            # (('-y','-z','-x'),'blueviolet'),
            (('z','x','y'),'k'),
            # (('z','-x','y'),'r'),
            (('z','x','-y'),'b'),
            (('z','y','x'),'g'),
            (('z','-y','x'),'y'),
            # (('z','y','-x'),'c'),
            # (('z','-x','-y'),'m'),
            # (('z','-y','-x'),'blueviolet'),
            (('-z','x','y'),'k'),
            # (('-z','-x','y'),'r'),
            (('-z','x','-y'),'b'),
            (('-z','y','x'),'g'),
            (('-z','-y','x'),'y'),
            # (('-z','y','-x'),'c'),
            # (('-z','-x','-y'),'m'),
            # (('-z','-y','-x'),'blueviolet'),
        ]
        self.log.info(len(variations))
        for curve in variations:
            order, clr = curve
            index = [self.iterator(i,order) for i in range(self.resolution)]
            # self.render(index)
            self.visualizer.add_curve(index, str(order),clr)
            self.log.info("Added curve %s with label %s", index, str(order))
        self.visualizer.show()
        # index = [self.encode(i) for i in range(self.resolution)]
        # self.log.info(index)
        # self.render(index)

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
        for index,s in enumerate(self.s):
            self.log.debug("starting iteration %s",index)
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # optimization for starting case, flipping does not do anything
                if x == y == z: break
            #     # compute last flip (if odd flip if even keep)
            #     x,y,z = (y,x,z) if (self.res-index) & 1 else (x,y,z) 
            #     break
            # compute region selector bits
            # coordinates offsets by region
            r_x,r_y,r_z = self.iterator(i, ('x','z','y'))
            # regions of seperation (8 verticies)
            i = i >> 3
            x,y,z = self.transform(r_x,r_y,r_z,x,y,z,s)
            self.log.info("i:%s s:%s | rx:%s ry:%s rz:%s | x:%s y:%s z:%s", i, s, r_x, r_y, r_z, x, y, z)
        self.log.info("resolved i:%s -> x:%s y:%s z:%s", i, x,y,z)
        return x,y,z

    def transform(self, r_x:int,r_y:int,r_z:int, x:int, y:int, z:int, s:int) -> Tuple[int,int,int]:
        # region selection and transform application
        # lambda x,y,z: (x + (s * r_x), y + (s * r_y), z + (s * r_z))
        if (r_x,r_y,r_z) == (0,0,0):
            x,y,z = y,x,z
        elif (r_x,r_y,r_z) == (0,1,0) or (0,1,1):
            x,y,z = z,y,x
        elif (r_x,r_y,r_z) == (0,0,1) or (1,0,1):
            x,y,z = x,-y,-z
        elif (r_x,r_y,r_z) == (1,1,1) or (1,1,0):
            x,y,z = -z,y,x
        else:
            x,y,z = -z,x,y
        # translate base iterator
        x += s * r_x # x = x + (s | 0)
        y += s * r_y # y = y + (s | 0)
        z += s * r_z # z = z + (s | 0)
        return x,y,z

    def iterator(self, i:int, o:Tuple[str,str,str]) -> Tuple[int,int,int]:
        """
        Base iterator for N3 algorithm    

        :param i: probe index
        :type i: int
        :return: base cartesian coordinate of bit @ index i
        :rtype: Tuple[int,int,int]
        """
        r_t = 0,0,0
        r_x = 1 & (i >> 2)
        r_y = 1 & (i >> 1 ^ r_x)
        r_z = 1 & (i ^ r_x ^ r_y)
        # iterator variant selector
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

    def render(self, coors: List[Tuple[int,int,int]]) -> None:
        self.visualizer.plot_3d(coors)