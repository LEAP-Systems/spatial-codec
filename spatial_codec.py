"""
Spatial Codec™
------------------------------------------------------------
Author: Christian Sargusingh
Date: 2020-02-12
Repoitory: https://github.com/cSDes1gn/spatial-encoding
LICENSE and README availble in repository
Version: 2.0

#TODO:  Optimize decode() algorithm in `SpatialCodec`
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

class Frame:
    """Class `Frame` is a collection of `SpatialBit` objects contained within a single matrix frame.

    This object defines the emergence of `SpatialBit` objects storing them in a list. The x, y and z attributes are removable
    and are included for easily adding a new 3D Scatter. Therefore they are not included in the docstring.

    Attributes:
        _spatial_map (:list:`SpatialBit`): `_spatial_map` is a list of `SpatialBit` objects within instance of `Frame`
    """
    def __init__(self, dim):
        """Initializes empty `_spatial_map` list. The length of this list will always be less than the allowed number of `SpatialBit`
        objects per frame.
        
        Raises:
            TypeError: ensures pos parameter has a length of 3 for (x,y,z) and is of type `tuple`
        """
        self.x = [None for _ in range(pow(dim,3))]
        self.y = [None for _ in range(pow(dim,3))]
        self.z = [None for _ in range(pow(dim,3))]
        self.SM = np.zeros((dim,dim,dim), dtype=int)
    
    def read(self):
        """Returns the stored `_spatial_map` list within this instance of `Frame`

        Returns:
            Returns the `_spatial_map` list of `SpatialBit` objects.
        """
        return self.SM

    def condense_components(self):
        # each list corresponds to a component of a coordinate set so the first time None is not found for one component will make it true for all other components
        while True:
            try:
                self.x.remove(None)
                self.y.remove(None)
                self.z.remove(None)
            except ValueError:
                break
                    

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
        self.dim = dim
        self.orient = 0 # default to 0
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

        # convert master list to a master matrix
        self.HC = np.zeros((self.dim,self.dim,self.dim), dtype=int)
        bit_index = 0
        for i in range(len(self._hilbert_master)):
            x,y,z = self._hilbert_master[i]
            self.HC[int(z)][int(x)][int(y)] = bit_index
            bit_index += 1
            
        # construct anti-diagonal identity matrix J
        self.J = np.eye(self.dim)
        for i in range(int(self.dim/2)):
            self.J[:,[0+i,self.dim-1-i]] = self.J[:,[self.dim-1-i,0+i]]

    def hilbert_curve(self, dim, x, y, z, dx, dy, dz, dx2, dy2, dz2, dx3, dy3, dz3):
        """Recursively generates a set of coordinates for a hilbert space filling curve with 3D resolution `dim`
        Algorithm based on solution by user:kylefinn @ https://stackoverflow.com/questions/14519267/algorithm-for-generating-a-3d-hilbert-space-filling-curve-in-python
        """
        if(dim==1):
            # save as an immutable tuple
            self._hilbert_master.append((int(x),int(y),int(z)))
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
        frame = Frame(self.dim)
        # construct spatial map matrix by including only True bits
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    if ba[self.HC[i][j][k]] == 1:
                        frame.SM[i][j][k] = 1
                        # update frame components for rendering
                        frame.x[self.HC[i][j][k]] = j
                        frame.y[self.HC[i][j][k]] = k
                        frame.z[self.HC[i][j][k]] = i
                    else:
                        pass
        print(frame.SM)
        # component condensing setup for rendering
        frame.condense_components()
        return frame

    def decode(self, frame):
        """Decodes a `Frame` object into a 1D bitarray.

        Args:
            frame (`Frame`): `frame` object built from a bitarray `ba` converted into a collection of `SpatialBit` objects

        Returns:
            ba (`bitarray`): `ba` is the decoded 1D `bitarray` object from .
        """
        # bitarray defined with 0's with a length equal to the masterlist (has dim encoded by masterlist length) for 1 bit replacement
        ba = bitarray(self.size)
        ba.setall(False)
        SM = frame.SM

        # adjust bitarray true values based on spatial_bitmap
        bit_index = 0
        for i in range(self.dim):
            SML = np.multiply(SM[i][:][:],self.HC[i][:][:]+1)
            for j in range(self.dim):
                for k in range(self.dim):
                    if SML[j][k] != 0:
                        ba[SML[j][k]-1] = 1
        print(ba)
        return ba
    
    def translate(self, dest):
        """Translates the Hilbert master curve about the Z axis"""
        # assume default direction is 0
        if self.orient == dest:
            return
        elif dest not in [0,1,2,3]:
            raise ValueError

        if np.abs(self.orient+dest)%2 == 0:
            print("Mirror translation:")
            # perform mirror
            for i in range(self.dim):
                self.HC[i][:][:] = np.matmul(self.J, np.matmul(self.HC[i][:][:],self.J))
        else:
            if ((dest - self.orient) <= 0 and (dest - self.orient) >= -1) or ((dest - self.orient) > 1):
                # to rotate the curve CCW multiply the anti-diagonal identity J to the transpose of each layer of HC: J*HC[x]^T
                print("CCW translation:")
                for i in range(self.dim):
                    self.HC[i][:][:] = np.matmul(self.J,self.HC[i][:][:].T)
            else:
                # to rotate the curve CW multiply the transpose of each layer of HC to the anti-diagonal identity J: HC[x]^T*J
                print("CW translation:")
                for i in range(self.dim):
                    self.HC[i][:][:] = np.matmul(self.HC[i][:][:].T,self.J)
                
        self.orient = dest
        print(self.orient)
        print(self.HC)

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

    print(sc.HC)

    # Step 1: Translate HC
    sc.translate(3)
    # Step 2: Encode
    # Step 3 Decode always at default
    # NOTE: TCU has the ability to rotate and track its rotation with the hilbert curve. IRIS only knows one configuration of HC and simply decodes according to that
    sc.render(ba_list)
