# -*- coding: utf-8 -*-
"""
N3 Spatial Codec
================
Updated: 2021-06

Encode an n1 block of data in n3 space using a pseudo hilbert space filling curve

Dependancies
------------
```
from typing import List, Tuple
from scodec.codec.base import SpatialCode
```
Copyright © 2021 LEAP. All Rights Reserved.
"""

from typing import List, Tuple
from scodec.codec.base import SpatialCodec


class N3(SpatialCodec):

    BASE_BLOCK_SIZE = 8   # block size of base iterator

    def __init__(self, block_size: int):
        # check if the block_size is greater than the base block size
        if block_size > self.BASE_BLOCK_SIZE:
            raise NotImplementedError(
                "This version only supports first order\
                (max 8 bit block_size) curves in 3D space"
            )
        super().__init__(block_size, self.BASE_BLOCK_SIZE)
        self.log.info("Configured %s codec with block size: %s", __name__, self.block_size)

    def stream_encode(self, bytestream: bytes, mpl: bool = False) -> List[Tuple[int, int, int]]:
        """
        Encode a stream of bytes in n3 space.

        :param bytestream: block of data for encoding
        :type bytestream: bytes
        :param mpl: flag to enable mpl visualizer, defaults to False
        :type mpl: bool, optional
        :return: encoded stream
        :rtype: List[Tuple[int,int,int]]
        """
        # remove excess bytes if word exceeds an 8 bit number
        bitstream = int(bytestream.hex(), base=16) & 0xFF
        self.log.debug("bitstream: %s", bin(bitstream))
        # unpacked bistream into iterable of single bits
        bits = [bitstream >> i & 0x1 for i in range(self.block_size)]
        # generate index by encoding each set bit sequentially
        stream = list(filter(None, [self.encode(i) if b else None for i, b in enumerate(bits)]))
        self.log.info("stream: %s", stream)
        if mpl: self.render(stream)
        return stream

    def stream_decode(self, stream: List[Tuple[int, int, int]]) -> bytes:
        """
        Decode a stream of coordinates encoded in n3 space into bytes.

        :param stream: stream of n3 space coordinate mapping
        :type stream: List[Tuple[int, int, int]]
        :return: decoded bytestream
        :rtype: bytes
        """
        bitstream = 0x0
        for coor in stream:
            bitstream |= self.decode(coor)
        self.log.info("decoded bitstream: %s", bin(bitstream))
        bytestream = bitstream.to_bytes(self.block_size, byteorder="big", signed=False)
        self.log.info("bytestream: %s", bytestream)
        return bytestream

    def decode(self, coor: Tuple[int, int, int]) -> int:
        """
        Compute bit index from a coordinate tuple encoded from an n3 first order hilbert curve.
        This method simply computes the

        :param coor: n3 space coordinate mapping
        :type coor: Tuple[int, int, int]
        :return: bit index of coordinate
        :rtype: int
        """
        x, y, z = coor
        x, y, z = 1 & x, 1 & y, 1 & z
        d = (x << 2) ^ (x ^ y << 1) ^ (x ^ y ^ z)
        index = 0x1 << d
        self.log.debug("computed index: %s", bin(index))
        return index

    def encode(self, i: int) -> Tuple[int, int, int]:
        """
        Compute coordinate tuple of an n3 hilbert curve at index i. Normally this
        applies iterative mapping to n3 space to constuct hilberts curve @ block_size
        (the iterative solution is not supported therefore the encode function only
        supports the base block_size: 8)

        :param i: bit index
        :type i: int
        :return: coordinate tuple @ bit index i
        :rtype: Tuple[int,int,int]
        """
        # initial coordinates
        x, y, z = self.iterator(i)
        self.log.info("resolved i:%s -> x:%s y:%s z:%s", i, x, y, z)
        return x, y, z

    def iterator(self, i: int) -> Tuple[int, int, int]:
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
        return r_x, r_y, r_z

    def transform(
        self, r_x: int, r_y: int, r_z: int, o: Tuple[str, str, str]
    ) -> Tuple[int, int, int]:
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
        if o[0] == "x":
            if o[1] == "y":
                if o[2] == "z":
                    r_t = r_x, r_y, r_z
                else:
                    r_t = r_x, r_y, 1 - r_z
            elif o[1] == "-y":
                if o[2] == "z":
                    r_t = r_x, 1 - r_y, r_z
                else:
                    r_t = r_x, 1 - r_y, 1 - r_z
            elif o[1] == "z":
                if o[2] == "y":
                    r_t = r_x, r_z, r_y
                else:
                    r_t = r_x, r_z, 1 - r_y
            else:
                if o[2] == "y":
                    r_t = r_x, 1 - r_z, r_y
                else:
                    r_t = r_x, 1 - r_z, 1 - r_y
        elif o[0] == "-x":
            if o[1] == "y":
                if o[2] == "z":
                    r_t = 1 - r_x, r_y, r_z
                else:
                    r_t = 1 - r_x, r_y, 1 - r_z
            elif o[1] == "-y":
                if o[2] == "z":
                    r_t = 1 - r_x, 1 - r_y, r_z
                else:
                    r_t = 1 - r_x, 1 - r_y, 1 - r_z
            elif o[1] == "z":
                if o[2] == "y":
                    r_t = 1 - r_x, r_z, r_y
                else:
                    r_t = 1 - r_x, r_z, 1 - r_y
            else:
                if o[2] == "y":
                    r_t = 1 - r_x, 1 - r_z, r_y
                else:
                    r_t = 1 - r_x, 1 - r_z, 1 - r_y
        elif o[0] == "y":
            if o[1] == "x":
                if o[2] == "z":
                    r_t = r_y, r_x, r_z
                else:
                    r_t = r_y, r_x, 1 - r_z
            elif o[1] == "-x":
                if o[2] == "z":
                    r_t = r_y, 1 - r_x, r_z
                else:
                    r_t = r_y, 1 - r_x, 1 - r_z
            elif o[1] == "z":
                if o[2] == "x":
                    r_t = r_y, r_z, r_x
                else:
                    r_t = r_y, r_z, 1 - r_x
            else:
                if o[2] == "x":
                    r_t = r_y, 1 - r_z, r_x
                else:
                    r_t = r_y, 1 - r_z, 1 - r_x
        elif o[0] == "-y":
            if o[1] == "x":
                if o[2] == "z":
                    r_t = 1 - r_y, r_x, r_z
                else:
                    r_t = 1 - r_y, r_x, 1 - r_z
            elif o[1] == "-x":
                if o[2] == "z":
                    r_t = 1 - r_y, 1 - r_x, r_z
                else:
                    r_t = 1 - r_y, 1 - r_x, 1 - r_z
            elif o[1] == "z":
                if o[2] == "x":
                    r_t = 1 - r_y, r_z, r_x
                else:
                    r_t = 1 - r_y, r_z, 1 - r_x
            else:
                if o[2] == "x":
                    r_t = 1 - r_y, 1 - r_z, r_x
                else:
                    r_t = 1 - r_y, 1 - r_z, 1 - r_x
        elif o[0] == "z":
            if o[1] == "x":
                if o[2] == "y":
                    r_t = r_z, r_x, r_y
                else:
                    r_t = r_z, r_x, 1 - r_y
            elif o[1] == "-x":
                if o[2] == "y":
                    r_t = r_z, 1 - r_x, r_y
                else:
                    r_t = r_z, 1 - r_x, 1 - r_y
            elif o[1] == "y":
                if o[2] == "x":
                    r_t = r_z, r_y, r_x
                else:
                    r_t = r_z, r_y, 1 - r_x
            else:
                if o[2] == "x":
                    r_t = r_z, 1 - r_y, r_x
                else:
                    r_t = r_z, 1 - r_y, 1 - r_x
        elif o[0] == "-z":
            if o[1] == "x":
                if o[2] == "y":
                    r_t = 1 - r_z, r_x, r_y
                else:
                    r_t = 1 - r_z, r_x, 1 - r_y
            elif o[1] == "-x":
                if o[2] == "y":
                    r_t = 1 - r_z, 1 - r_x, r_y
                else:
                    r_t = 1 - r_z, 1 - r_x, 1 - r_y
            elif o[1] == "y":
                if o[2] == "x":
                    r_t = 1 - r_z, r_y, r_x
                else:
                    r_t = 1 - r_z, r_y, 1 - r_x
            else:
                if o[2] == "x":
                    r_t = 1 - r_z, 1 - r_y, r_x
                else:
                    r_t = 1 - r_z, 1 - r_y, 1 - r_x
        return r_t

    def render(self, stream: List[Tuple[int, int, int]]) -> None:
        """
        Render MPL visualizer of index iterator and stream overlay

        :param stream: encoded stream
        :type stream: List[Tuple[int,int,int]]
        """
        index = [self.encode(i) for i in range(self.block_size)]
        self.log.debug("index: %s", index)
        self.log.debug("stream: %s", stream)
        self.visualizer.add_n3_curve(index, marker="", label="index", clr="k")
        self.visualizer.add_n3_curve(stream, marker="o", label="stream", clr="r")
        self.visualizer.show()

    def show_iterators(self) -> None:
        """
        Interactive visualizer for iteration variations
        """
        # variation iterator
        # for curve in Iterators.variations:
        #     order, clr = curve
        #     self.visualizer.add_n3_curve(
        #         d=[self.transform(*self.iterator(i), order) for i in range(8)],
        #         marker='o',
        #         label=str(order),
        #         clr=clr
        #     )
        # self.visualizer.show()
