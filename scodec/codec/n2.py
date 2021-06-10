# -*- coding: utf-8 -*-
"""
N2 Spatial Codec
================
Updated: 2021-06

Encode an n1 block of data in n2 space using a pseudo hilbert space filling curve

Dependancies
------------
```
from typing import List, Tuple
from scodec.codec.base import SpatialCodec
```
Copyright © 2021 LEAP. All Rights Reserved.
"""

from typing import List, Tuple
from scodec.codec.base import SpatialCodec


class N2(SpatialCodec):

    BASE_BLOCK_SIZE = 4   # block size of base iterator

    def __init__(self, block_size: int):
        super().__init__(block_size, self.BASE_BLOCK_SIZE)
        self.log.info("Configured %s codec with block size: %s", __name__, self.block_size)

    def stream_encode(self, bytestream: bytes, mpl: bool = False) -> List[Tuple[int, int]]:
        """
        Encode a stream of bytes in n2 space.

        :param bytestream: block of data for encoding
        :type bytestream: bytes
        :param mpl: flag to enable mpl visualizer, defaults to False
        :type mpl: bool, optional
        :return: encoded stream
        :rtype: List[Tuple[int,int]]
        """
        # remove excess bytes if word exceeds resolution
        bitstream = int(bytestream.hex(), base=16) & (2 ** self.block_size - 1)
        self.log.debug("bitstream: %s", bin(bitstream))
        bits = [bitstream >> i & 0x1 for i in range(self.block_size)]
        index = list(filter(None, [self.encode(i) if b else None for i, b in enumerate(bits)]))
        self.log.info("index: %s", index)
        if mpl: self.render(index)
        return index

    def stream_decode(self, stream: List[Tuple[int, int]]) -> bytes:
        """
        Decode a stream of coordinates encoded in n2 space into bytes.

        :param stream: stream of n2 space coordinate mapping
        :type stream: List[Tuple[int,int]]
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

    def decode(self, coor: Tuple[int, int]) -> int:
        """
        Compute bit index from a coordinate tuple encoded from an n2 hilbert curve.
        This method iteratively applies the inverse operation of the n2 space encoding.

        :param coor: n2 space coordinate mapping
        :type coor: Tuple[int,int]
        :return: bit index of coor
        :rtype: int
        """
        d = 0
        s = self.block_size >> 1
        x, y = coor
        self.log.debug("n: %s x: %s y: %s", self.block_size, x, y)
        while s > 0:
            rx = (x & s) > 0
            ry = (y & s) > 0
            d += s ** 2 * ((3 * rx) ^ ry)
            x, y = self.transform(x, y, rx, ry, self.block_size)
            self.log.debug("s: %s rx: %s ry:%s x:%s y:%s", s, rx, ry, x, y)
            s = s >> 1  # divide by 2 each iteration
        self.log.debug("d: %s x: %s y: %s", d, x, y)
        index = 0x1 << d
        self.log.debug("computed index: %s", bin(index))
        return index

    def encode(self, i: int) -> Tuple[int, int]:
        """
        Compute coordinate tuple of an n2 hilbert curve at index i. This applies
        iterative mapping to n2 space to constuct hilberts curve @ resolution

        :param i: bit index
        :type i: int
        :return: coordinate tuple @ bit index i
        :rtype: Tuple[int,int]
        """
        index = i
        self.log.debug("Computing coordinate at bit: %s", i)
        # initial coordinates
        x, y = 0, 0
        for level, c in enumerate(self._sv):
            # Once the index reaches 0 the x and y bits are latched and alternate between each other
            # before converging before we exceed the range boundary n
            if i == 0:
                # we are done
                if x == y:
                    break
                # compute last flip (i required for forcasting)
                x, y = (y, x) if (self.block_size - level) & 1 else (x, y)
                break
            # generate base iterator
            r_x, r_y = self.iterator(i)
            x, y = self.transform(x, y, r_x, r_y, c)
            # translate base iterator
            x += c * r_x  # x = x + (s or 0)
            y += c * r_y  # y = y + (s or 0)
            i = i >> 2  # regions of seperation (4 verticies)
            self.log.debug(
                "i:%s cells:%s | i/2 odd:%s i/2 odd and i odd:%s -> x:%s y:%s",
                i,
                c,
                r_x,
                r_y,
                x,
                y,
            )
        self.log.debug("resolved i:%s -> x:%s y:%s", index, x, y)
        return x, y

    def transform(self, x: int, y: int, r_x: int, r_y: int, c: int) -> Tuple[int, int]:
        """
        Transform base iterator by applying a reflection about an axis or line by cell selector c

        :param x: x translation to cell index c
        :type x: int
        :param y: y translation to cell index c
        :type y: int
        :param r_x: x component of base iterator coordinate
        :type r_x: int
        :param r_y: y component of base iterator coordinate
        :type r_y: int
        :param s: cell index
        :type s: int
        :return: transformed coordinate tuple from cell c
        :rtype: Tuple[int,int]
        """
        # rotation function for this region
        if r_y == 0:
            if r_x == 1:
                x, y = c - 1 - x, c - 1 - y
            x, y = y, x
        return x, y

    def iterator(self, i: int) -> Tuple[int, int]:
        """
        Base iterator for N2 algorithm

        :param i: probe index
        :type i: int
        :return: base cartesian coordinate of bit @ index i
        :rtype: Tuple[int,int]
        """
        r_x = 1 & (i >> 1)
        r_y = 1 & (i ^ r_x)
        return r_x, r_y

    def render(self, stream: List[Tuple[int, int]]) -> None:
        """
        Render MPL visualizer of index iterator and stream overlay

        :param stream: encoded stream
        :type stream: List[Tuple[int,int]]
        """
        index = [self.encode(i) for i in range(self.block_size)]
        self.log.debug("index: %s", index)
        self.log.debug("stream: %s", stream)
        self.visualizer.add_n2_curve(index, marker="", label="index", clr="k")
        self.visualizer.add_n2_curve(stream, marker="o", label="stream", clr="r")
        self.visualizer.show()
