"""
Spatial Codec™
------------------------------------------------------------
Author: Christian Sargusingh
Date: 2020-01-09
Repoitory: https://github.com/cSDes1gn/spatial-encoding
LICENSE and README availble in repository
Version: 1.0

#TODO:  Include 3D array of `SpatialBit` objects in `Frame`
        Optimize decode() algorithm in `SpatialCodec`
        Introduce Spatial Encryption™ scheme to Frame object

Copyright © 2020 Christian Sargusingh
"""

from progress.bar import IncrementalBar
from progress.spinner import Spinner

lb = IncrementalBar('Importing argparse', max=8)

#include status of imports via progress bar
import argparse
lb.next()
lb.message = 'Importing random'
import random
lb.next()
lb.message = 'Importing time'
import time
lb.next()
lb.message = 'Importing Thread'
from threading import Thread
lb.next()
lb.message = 'Importing numpy'

import numpy as np
lb.next()
lb.message = 'Importing pandas'
import pandas as pd
lb.next()
lb.message = 'Importing plotly'
import plotly.graph_objects as go
lb.next()
lb.message = 'Importing bitarray'
from bitarray import bitarray
lb.next()


class SpatialBit:
    """Class `SpatialBit` creates a bit with a tuple (x,y,z).

    This object defines the base information unit in the 3D spatial dimension. Each `SpatialBit` is defined by a position tuple
    which has an x y and z coordinate representing a `True` bit in 3D space.

    Attributes:
        _pos (`tuple(x,y,z)`): `_pos` defines the x, y and z coordinates of a `True` bit in 3D space
    """
    def __init__(self, pos):
        """Initializes `_pos` with an x, y and z coordinate.
        
        Raises:
            TypeError: ensures pos parameter has a length of 3 for (x,y,z) and is of type `tuple`
        """
        # ensure the type of pos is an (x,y,z) tuple
        if type(pos) != tuple or len(pos) != 3:
            raise TypeError
        else:
            self._pos = pos
    
    def read(self):
        """Returns the stored `_pos` tuple within this instance of `SpatialBit`

        Returns:
            Returns the `_pos` tuple (x,y,z).
        """
        return self._pos

class Frame:
    """Class `Frame` is a collection of `SpatialBit` objects contained within a single matrix frame.

    This object defines the emergence of `SpatialBit` objects storing them in a list. The x, y and z attributes are removable
    and are included for easily adding a new 3D Scatter. Therefore they are not included in the docstring.

    Attributes:
        _spatial_map (:list:`SpatialBit`): `_spatial_map` is a list of `SpatialBit` objects within instance of `Frame`
    """
    def __init__(self):
        """Initializes empty `_spatial_map` list. The length of this list will always be less than the allowed number of `SpatialBit`
        objects per frame.
        
        Raises:
            TypeError: ensures pos parameter has a length of 3 for (x,y,z) and is of type `tuple`
        """
        self.x = list()
        self.y = list()
        self.z = list()
        self._spatial_map = list()

    def fill(self, sb):
        """Appends a new `SpatialBit` object to the `_spatial_map` list within this instance of `Frame`. Updates internal `x`, `y` and `z`
        lists with `SpatialBit` parameters.

        Args:
            sb (`SpatialBit`): `sb` is a `SpatialBit` object.

        Raises:
            TypeError: checks that `sb` parameter is of type `SpatialBit`
        """
        if type(sb) != SpatialBit:
            raise TypeError
        else:
            self._spatial_map.append(sb)

            # update hidden class attributes for 3D Scatter trace
            x,y,z = sb.read()
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
    
    def read(self):
        """Returns the stored `_spatial_map` list within this instance of `Frame`

        Returns:
            Returns the `_spatial_map` list of `SpatialBit` objects.
        """
        return self._spatial_map

class SpatialCodec:
    """Class `SpatialCodec` defines the codec for spatial encoding and decoding based on Hilbert's space filling curve.

    This object defines the codec for  of `SpatialBit` objects storing them in a list. The x, y and z attributes are removable
    and are included for easily adding a new 3D Scatter. Therefore they are not included in the docstring.

    Attributes:
        size (`int`): `size` attribute defines the number of allowable SpatialBit objects per Frame
        _hilbert_master (:list:`tuple (x,y,z)`): list of tuple (x,y,z) coordinates defined by the internal recursive function `hilbert_curve`
        fig (`dict`): `fig` is a dictionary containing the figure attribute initialization for a graphic object rendering spatial mapping in plotly
    """
    def __init__(self, dim):
        """Initializes empty `_hilbert_master` list. Defines `size` attribute which is the upper limit of `SpatialBit`
        objects per frame. Intializes graphic object `fig` for rendering spatial mapping

        Args:
            dim (`int`): `dim` is the dimension of the 3D matrix. Hilbert's space filling algorithm restricts this dimension to powers of 2.
        
        Raises:
            IndexError: ensures the internal `hilbert_curve` definition generates a `_hilbert_master` size that matches the expected size
            based on the specified dimension `dim`.
        """
        self.size = pow(dim,3)
        self._hilbert_master = list()
        self.fig = go.Figure(
            layout = go.Layout(title="3D Spatial Mapping of Randomly Generated 1D Bitarray using Hilberts Space Filling Curve.")
        )

        # ensures dim parameter is a power of 2
        if  np.log2(self.size) % 1 != 0:
            raise ValueError

        print("\nGenerating Hilbert Curve...")
        self.hilbert_curve(dim,0,0,0,1,0,0,0,1,0,0,0,1)
        print("Recursive hilbert algorithm completed successfully.")
        
            

    def hilbert_curve(self, dim, x, y, z, dx, dy, dz, dx2, dy2, dz2, dx3, dy3, dz3):
        """Recursively generates a set of coordinates for a hilbert space filling curve with 3D resolution `dim`
        Algorithm based on solution by user:kylefinn @ https://stackoverflow.com/questions/14519267/algorithm-for-generating-a-3d-hilbert-space-filling-curve-in-python
        """
        if(dim==1):
            # save as an immutable tuple
            self._hilbert_master.append((x,y,z))
        else:
            dim/=2
            if(dx<0): 
                x -= dim*dx
            if(dy<0): 
                y -= dim*dy
            if(dz<0): 
                z -= dim*dz
            if(dx2<0): 
                x -= dim*dx2
            if(dy2<0): 
                y -= dim*dy2
            if(dz2<0): 
                z -= dim*dz2
            if(dx3<0): 
                x -= dim*dx3
            if(dy3<0): 
                y -= dim*dy3
            if(dz3<0): 
                z -= dim*dz3
            self.hilbert_curve(dim, x, y, z, dx2, dy2, dz2, dx3, dy3, dz3, dx, dy, dz)
            self.hilbert_curve(dim, x+dim*dx, y+dim*dy, z+dim*dz, dx3, dy3, dz3, dx, dy, dz, dx2, dy2, dz2)
            self.hilbert_curve(dim, x+dim*dx+dim*dx2, y+dim*dy+dim*dy2, z+dim*dz+dim*dz2, dx3, dy3, dz3, dx, dy, dz, dx2, dy2, dz2)
            self.hilbert_curve(dim, x+dim*dx2, y+dim*dy2, z+dim*dz2, -dx, -dy, -dz, -dx2, -dy2, -dz2, dx3, dy3, dz3)
            self.hilbert_curve(dim, x+dim*dx2+dim*dx3, y+dim*dy2+dim*dy3, z+dim*dz2+dim*dz3, -dx, -dy, -dz, -dx2, -dy2, -dz2, dx3, dy3, dz3)
            self.hilbert_curve(dim, x+dim*dx+dim*dx2+dim*dx3, y+dim*dy+dim*dy2+dim*dy3, z+dim*dz+dim*dz2+dim*dz3, -dx3, -dy3, -dz3, dx, dy, dz, -dx2, -dy2, -dz2)
            self.hilbert_curve(dim, x+dim*dx+dim*dx3, y+dim*dy+dim*dy3, z+dim*dz+dim*dz3, -dx3, -dy3, -dz3, dx, dy, dz, -dx2, -dy2, -dz2)
            self.hilbert_curve(dim, x+dim*dx3, y+dim*dy3, z+dim*dz3, dx2, dy2, dz2, -dx3, -dy3, -dz3, -dx, -dy, -dz)

    def encode(self, ba):
        """Encodes a 1D bitarray into a `Frame` object consisting of a collection of `SpatialBit` objects.

        Args:
            ba (`bitarray`): `ba` is the target `bitarray` object for encoding.

        Returns:
            frame (`Frame`): `frame` object built from a bitarray `ba` converted into a collection of `SpatialBit` objects
        """
        frame = Frame()
        # construct spatial map by including only True bits
        for i in range(len(self._hilbert_master)):
            if ba[i]:
                frame.fill(SpatialBit(self._hilbert_master[i]))
            else:   # included for structural clarity
                pass
        return frame

    def decode(self, frame):
        """Decodes a `Frame` object into a 1D bitarray.

        Args:
            frame (`Frame`): `frame` object built from a bitarray `ba` converted into a collection of `SpatialBit` objects

        Returns:
            ba (`bitarray`): `ba` is the decoded 1D `bitarray` object from .
        """
        # bitarray defined with 0's with a length equal to the masterlist (has dim encoded by masterlist length) for 1 bit replacement
        ba = bitarray(len(self._hilbert_master))
        ba.setall(False)
        spatial_bitmap = frame.read()

        # adjust bitarray true values based on spatial_bitmap
        for i in range(len(spatial_bitmap)):
            try:
                ba[self._hilbert_master.index(spatial_bitmap[i].read())] = True
            except ValueError:
                pass
        return ba
    
    def render(self, ba_list):
        """Renders a list of `bitarray` objects to a 3D scatter rendered using `plotly`

        Args:
            ba_list (:list:`bitarray`): `ba_list` is a list (size args.frames) of randomly generated bits (size args.dim^3)
        """
        # initialized for storing figure labels with decoded hex values
        decoded_hex = list()

        print("Rendering Spatial Bitmaps:")
        spin = Spinner()

        for steps in range(len(ba_list)):
            # encode bitarray into list of Spatial bits
            frame = self.encode(ba_list[steps])
            spin.message = 'Encoded frame: ' + str(steps) + ' '
            # Add the new trace to the scatter
            tx = frame.x
            ty = frame.y
            tz = frame.z
            self.fig.add_trace(go.Scatter3d(visible=True, x=tx,y=ty,z=tz))

            # decode Frame object back into bitarray
            ba = self.decode(frame)
            # append decoded bitarray to decoded hex list for figure labelling
            decoded_hex.append(ba.tobytes().hex())
            spin.message = 'Decoded frame: ' + str(steps) + ' '

            # clear arrays for next frame
            tx.clear()
            ty.clear()
            tz.clear()

            spin.next()

        steps = []

        for i in range(len(self.fig.data)):
            spin.message = 'Drawing to plotly '
            step = dict(
                method="restyle",
                args=["visible", [False] * len(self.fig.data)],
                label=decoded_hex[i],
            )
            step["args"][1][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)
            spin.next()

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Frame: "},
            pad={"t": 50},
            steps=steps
        )]

        self.fig.update_layout(
            sliders=sliders,
        )

        self.fig.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates a sequence of 3D spatially encoded frames from sequence of 1D bitarrays.')
    parser.add_argument('dim', metavar='dim', type=int, help='matrix dimension (must be a power of 2)')
    parser.add_argument('frames', metavar='frames',type=int, help='number of frames to generate.')
    parser.add_argument('bitarray', nargs='?', default=None, metavar='bitarray',type=str, help='custom hex definition. If arg specified script ignores previous frame argument.')
    args = parser.parse_args()

    # size parameter is important for describing the voxel (3D pixel) resolution per frame 
    # ex/. for a 4x4x4 matrix the resolution is 64. In other words, there are 64 bits of information that can be encoded per frame
    size = pow(args.dim,3)
    ba_list = list()

    # check for specified bitarray argument otherwise generate random bitarrays for each new frame
    if args.bitarray:
        # ensure bitarray length matches matrix dimension argument
        if len(args.bitarray) != size/4:
            raise ValueError("Mis-match of bitarray length and matrix dimension arguments.")

        b = bitarray(bin(int(args.bitarray, base=16)).lstrip('0b'))

        # re append MSB cutoff of 0 bits by python bin() definition
        if len(b) != 64:
            bn = bitarray()
            for i in range(64-len(b)):
                bn.append(False)
            bn.extend(b)
            ba_list.append(bn)
        else:
            ba_list.append(b)
        
        
    else:
        # generate 'args.frames' number random bitarray with a length 'size'
        for j in range(args.frames):  
            ba = bitarray()
            for i in range(size):
                ba.append(bool(random.getrandbits(1)))
            ba_list.append(ba)

    try:
        sc = SpatialCodec(args.dim)
    except ValueError:
        print("Argument dim must be a power of 2. Exiting.")
        exit(0)
    
    sc.render(ba_list)
