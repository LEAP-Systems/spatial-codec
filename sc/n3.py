# -*- coding: utf-8 -*-
"""
N3 Spatial Codec
================
Contributors: Christian Sargusingh
Updated: 2021-05

Encode an n1 block of data in n3 space using a pseudo hilbert space filling curve 

Dependancies
------------
```
from typing import List, Tuple

from sc.scodec import SpatialCodec
from sc.iterators import Iterators
```
Copyright © 2020 Christian Sargusingh
"""
from typing import List, Tuple

from sc.scodec import SpatialCodec
from sc.iterators import Iterators

class N3(SpatialCodec):
    def __init__(self, resolution:int):
        if resolution > 8:
            raise NotImplementedError('This version supports single iteration (max 8 bit resolution) curves in 3D space')
        # spatial codec init
        super().__init__(resolution=resolution)

    def stream_encode(self, bytestream:bytes, mpl:bool=False) -> List[Tuple[int,int,int]]:
        """
        Encode a stream of bytes in n3 space.

        :param bytestream: 
        :type bytestream: bytes
        :param mpl: flag to enable mpl visualizer, defaults to False
        :type mpl: bool, optional
        :return: encoded stream
        :rtype: List[Tuple[int,int,int]]
        """
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

    def decode(self, n:int, x:int, y:int) -> int: ...

    def encode(self, i:int) -> Tuple[int,int,int]:
        """
        Compute coordinate tuple of an n3 hilbert curve at index i. Normally this
        applies iterative mapping to n3 space to constuct hilberts curve @ resolution
        (the iterative solution is not supported therefore the encode function only
        supports the base resolution: 8)

        :param i: bit index
        :type i: int
        :return: coordinate tuple @ bit index i
        :rtype: Tuple[int,int,int]
        """
        # initial coordinates
        x,y,z = self.iterator(i)
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
        """
        Transform base iterator by applying a reflection about a plane or axis

        :param r_x: x component of iterator coordinate
        :type r_x: int
        :param r_y: y component of iterator coordinate
        :type r_y: int
        :param r_z: z component of iterator coordinate
        :type r_z: int
        :param o: iterator variant selector 
        :type o: Tuple[str,str,str]
        :return: transformed coordinate tuple
        :rtype: Tuple[int,int,int]
        """
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
        """
        Render MPL visualizer of index iterator and stream overlay

        :param stream: encoded stream
        :type stream: List[Tuple[int,int,int]]
        """
        index = [self.encode(i) for i in range(self.resolution)]
        self.log.debug("index: %s", index)
        self.log.debug("stream: %s", stream)
        self.visualizer.add_n3_curve(index, marker='', label='index', clr='k')
        self.visualizer.add_n3_curve(stream, marker='o', label='stream', clr='r')
        self.visualizer.show()

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