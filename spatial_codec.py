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

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Method by user:Greenstick @ https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

#include status of imports via progress bar
import argparse
printProgressBar(1,8,prefix="Importing argparse             ")
import random
printProgressBar(2,8,prefix="Importing random               ")
import time
printProgressBar(3,8,prefix="Importing time                 ")
from threading import Thread
printProgressBar(4,8,prefix="Importing Thread               ")

import numpy as np
printProgressBar(5,8,prefix="Importing numpy                ")
import pandas as pd
printProgressBar(6,8,prefix="Importing pandas               ")
import plotly.graph_objects as go
printProgressBar(7,8,prefix="Importing plotly.graph_objects ")
from bitarray import bitarray
printProgressBar(8,8,prefix="Importing bitarray             ")


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
    """
    def __init__(self, dim):
        """Initializes empty `_hilbert_master` list. Defines `size` attribute which is the upper limit of `SpatialBit`
        objects per frame. 

        Args:
            dim (`int`): `dim` is the dimension of the 3D matrix. Hilbert's space filling algorithm restricts this dimension to powers of 2.
        
        Raises:
            IndexError: ensures the internal `hilbert_curve` definition generates a `_hilbert_master` size that matches the expected size
            based on the specified dimension `dim`.
        """
        self.size = pow(dim,3)
        self._hilbert_master = list()

        # ensures dim parameter is a power of 2
        if  np.log2(self.size) % 1 != 0:
            raise ValueError

        print("Generating Hilbert Curve...")
        # execute space filling algorithm for size dim
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
        # construct spatial map by including only
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
        #define a bitarray defined with 0's with a length equal to the masterlist (has dim encoded by masterlist length)
        ba = bitarray(len(self._hilbert_master))
        ba.setall(False)
        spatial_bitmap = frame.read()
        #Adjust bitarray true values based on spatial_bitmap
        for i in range(len(spatial_bitmap)):
            # fix for printprogressBar div by 0
            if len(spatial_bitmap) <= 1:
                print("Single iteration required.")
            else:
                printProgressBar(i, len(spatial_bitmap)-1, prefix = 'Decoding Spatial Bitmap:    ', suffix = '', length = 50)
            
            # replace spatial_bitmap elements in bitarray
            if spatial_bitmap[i].read() in self._hilbert_master:
                ba[self._hilbert_master.index(spatial_bitmap[i].read())] = True
        return ba



# Argument Parsing
parser = argparse.ArgumentParser(description='Generates a sequence of 3D spatially encoded frames from sequence of 1D bitarrays.')
parser.add_argument('dim', metavar='dim', type=int, help='matrix dimension (must be a power of 2)')
parser.add_argument('frames', metavar='frames',type=int, help='number of frames to generate.')
args = parser.parse_args()

# define a 3D cube of SpatialBits given a cube dimension using Hilberts space filling curve
size = pow(args.dim,3)

# create figure with base layout
fig = go.Figure(
    layout = go.Layout(title="3D Spatial Mapping of Randomly Generated 1D Bitarray using Hilberts Space Filling Curve.")
)

decoded_hex = list()

# Initialize spatial codec using hilberts space filling curve for a 'dim' dimensional 3D matric
try:
    sc = SpatialCodec(args.dim)
except ValueError:
    print("Argument dim must be a power of 2. Exiting.")
    exit(0)

# generate frame traces
for steps in range(args.frames):
    # define empty bitarray
    ba = bitarray()

    # generate a random bitarray with length of cube size
    for i in range(size):
        ba.append(bool(random.getrandbits(1)))

    # encode bitarray into list of Spatial bits
    frame = sc.encode(ba)
    print("Encoded frame: " + str(steps))
    
    # Add the new trace to the scatter
    tx = frame.x
    ty = frame.y
    tz = frame.z
    fig.add_trace(go.Scatter3d(visible=True, x=tx,y=ty,z=tz))

    # decode Frame object back into bitarray
    ba2 = sc.decode(frame)
    print("Decoded frame: " + str(steps))
    # append decoded bitarray to decoded hex list for figure labelling
    decoded_hex.append(ba2.tobytes().hex())
    
    # clear arrays for next frame
    tx.clear()
    ty.clear()
    tz.clear()
    ba = bitarray()

steps = []
print("Rendering 3D Scatter...")

for i in range(len(fig.data)):
    step = dict(
        method="restyle",
        args=["visible", [False] * len(fig.data)],
        label=decoded_hex[i],
    )
    step["args"][1][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Frame: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders,
)

fig.show()
