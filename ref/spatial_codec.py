"""
Spatial Codec™
==============
Contributors: Christian Sargusingh
Updated: 2020-07
Repoitory: https://github.com/cSDes1gn/spatial-codec
README availble in repository root
Version: 2.0

Dependancies
------------
>>> import argparse
>>> import random
>>> import time
>>> import numpy as np
>>> import plotly.graph_objects as go
>>> from bitarray import bitarray

Sample Runs
-----------
>>> python spatial_codec.py 4 1 ffffffffffffffff
>>> python spatial_codec.py 8 64

Copyright © 2020 Christian Sargusingh
"""

#include status of imports via progress bar
import argparse
import random
import time
import numpy as np
import plotly.graph_objects as go
from bitarray import bitarray

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Frame:
    """Class `Frame` represents a 1D bitarray as a 3D matrix of specified size.

    `Frame` is a wrapper for an encoded 3D spatially encoded bitarray. It includes a `read` method for returning the spatial map `_SM`
    and a `compact` method for reducing the `x`,`y`,`z` attributes into a format that is readable to the plotly renderer.

    Attributes:
      * _SM (`np.matrix`): `_SM` is a 3D matrix of integers.
      * x (`list`): `x` is a list of x components for 'on' bits within the frame.
      * y (`list`): `y` is a list of y components for 'on' bits within the frame.
      * z (`list`): `z` is a list of z components for 'on' bits within the frame.
    """
    def __init__(self, dim):
        """Initializes a dim^3 dimensional 3D matrix of zeroes."""
        self._SM = np.zeros((dim,dim,dim), dtype=int)
        # components are initialized to an empty list so that the components can be entered in the order which they appear according to
        # Hilberts space filling curve
        self.x = [None for _ in range(pow(dim,3))]
        self.y = [None for _ in range(pow(dim,3))]
        self.z = [None for _ in range(pow(dim,3))]
        
    def read(self):
        """Returns stored `_SM` matrix within this instance of `Frame`.

        Returns:
          * Returns the `_SM` matrix.
        """
        return self._SM

    def write(self, x, y, z, bit=1):
        """Writes bit to spatial map matrix `_SM` within this instance of `Frame`.

        Args:
          * x (`int`): x component of spatial mapping tuple.
          * y (`int`): y component of spatial mapping tuple.
          * z (`int`): z component of spatial mapping tuple.
          * bit (`int`): bit value
        """
        self._SM[x][y][z] = bit

    def compact(self):
        """Formats the component lists by removing the leftover `None` type objects so component lists can be used by plotly renderer."""
        # each list corresponds to a component of a coordinate set so the first time None is not found for one component will make it
        # true for all other components
        while True:
            try:
                self.x.remove(None)
                self.y.remove(None)
                self.z.remove(None)
            except ValueError:
                break
                    

class SpatialCodec:
    """Class `SpatialCodec` defines the codec for spatial encoding and decoding based on Hilbert's space filling curve.

    `SpatialCodec` has two primary definitions `encode` & `decode` for converting `bitarray` objects into `Frame` objects and vice-versa.
    This class also has two secondary functions `remap` & `render`. `remap` is a defintion specifically designed for the LEAP™ project. It
    is a protected definition which can only be called by `TransmissionControlUnit` objects which allows the Transmission Control Software
    to change the Hilbert space filling curve mapping to project the encoded frame to different access points (directions). The receiving
    unit will always decode the frame according to a standardized method. `render` renders the encoded spatial map into a 3D matrix for the
    purposes of validation testing and demonstration.

    Attributes:
      * dim (`int`): `dim` attribute defines the dimension of the the 3D matrix spatial map.
      * orient (`int`): `orient` defines the orientation of the hilbert curve mapping. The default orientation is 0 followed by 1>2>3>0 in CW rotation
      * fig (`dict`): `fig` is a dictionary containing the figure attribute initialization for a graphic object rendering spatial mapping in plotly
      * HC (`np.matrix`): Holds `bitarray` index numbers in a 3D matrix defined by the hilberts space filling curve and shape is described by `dim`.
      * J (`np.matrix`): Defines an 2D anti-diagonal identity matrix for rotating each layer (xy plane) of a `Frame`.
      * bit_index (`int`): `bit_index` is a temporary attribute used to hold the running bit index count for `hilberts_curve`.  
    """
    def __init__(self, dim):
        """Initializes empty `HC` 3D matrix with resolution defined by `dim` and orientation by `orient`. Intializes graphic object `fig` for 
        rendering spatial mapping. Generates a spatial map using `HC` via Hilbert's space filling curve. Defines anti-diagonal identity matrix 
        `J` for rotational transformations by `Frame` layer.

        Args:
          * dim (`int`): `dim` is the dimension of the 3D matrix. Hilbert's space filling algorithm restricts this dimension to powers of 2.
        
        Raises:
          * `ValueError`: Raised if the parameter `dim` is not a power of 2.
        """
        self.dim = dim
        self.orient = 0 # default to 0
        self.bit_index = 0
        self.fig = go.Figure(
            layout = go.Layout(title="3D Spatial Mapping of Randomly Generated 1D Bitarray using Hilbert's Space Filling Curve.")
        )
        
        # entry check to hilberts_curve to ensure dim parameter is a power of 2
        if np.log2(self.dim) % 1 != 0:
            raise ValueError
            
        # Generate a 3D matrix of size dim that maps 1D bitarray indices to Hilberts space filling curve 
        print("\nGenerating Hilbert Curve...")
        self.HC = np.zeros((self.dim,self.dim,self.dim), dtype=int)
        self.hilbert_curve(dim,0,0,0,1,0,0,0,1,0,0,0,1)
        print(bcolors.OKGREEN + "Hilbert curve matrix (HC) attribute successfully initialized." + bcolors.ENDC)

        # dereference bit_index counter for HC
        del self.bit_index

        # construct anti-diagonal identity matrix J
        self.J = np.eye(self.dim)
        for i in range(int(self.dim/2)):
            self.J[:,[0+i,self.dim-1-i]] = self.J[:,[self.dim-1-i,0+i]]

    def hilbert_curve(self, dim, x, y, z, dx, dy, dz, dx2, dy2, dz2, dx3, dy3, dz3):
        """Recursively generates a set of coordinates for a hilbert space filling curve with 3D resolution `dim`
        Algorithm based on solution by user:kylefinn @ https://stackoverflow.com/questions/14519267/algorithm-for-generating-a-3d-hilbert-space-filling-curve-in-python
        """
        if dim == 1:
            # Recursively fill matrix indices using temp SpatialCodec attribute bit_index
            self.HC[int(z)][int(x)][int(y)] = self.bit_index
            self.bit_index += 1
        else:
            dim /= 2
            if(dx < 0): 
                x -= dim*dx
            if(dy < 0): 
                y -= dim*dy
            if(dz < 0): 
                z -= dim*dz
            if(dx2 < 0): 
                x -= dim*dx2
            if(dy2 < 0): 
                y -= dim*dy2
            if(dz2 < 0): 
                z -= dim*dz2
            if(dx3 < 0): 
                x -= dim*dx3
            if(dy3 < 0): 
                y -= dim*dy3
            if(dz3 < 0): 
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
        """Encodes a 1D bitarray into a `Frame` object consisting of a 3D matrix containing indices corresponding to its spatial mapping.

        Args:
          * ba (`bitarray`): `ba` is the input `bitarray` object for encoding.

        Returns:
          * frame (`Frame`): `frame` object built from input bitarray `ba`
        """
        frame = Frame(self.dim)
        # construct spatial map matrix
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    if ba[self.HC[i][j][k]] == 1:
                        frame.write(i,j,k)
                        # update frame components for rendering
                        frame.x[self.HC[i][j][k]] = j
                        frame.y[self.HC[i][j][k]] = k
                        frame.z[self.HC[i][j][k]] = i
                    else:
                        pass
        print(frame.read())
        # component condensing setup for rendering
        frame.compact()
        return frame

    def decode(self, frame):
        """Decodes a `Frame` object into a 1D bitarray.

        Args:
          * frame (`Frame`): `frame` object built from a bitarray `ba`

        Returns:
          * ba (`bitarray`): `ba` is the decoded 1D `bitarray` from `Frame` object.
        """
        # bitarray defined with 0's with a length equal to the masterlist (has dim encoded by masterlist length) for 1 bit replacement
        ba = bitarray(pow(self.dim,3))
        ba.setall(False)
        SM = frame.read()

        # adjust bitarray true values based on spatial_bitmap
        bit_index = 0
        for i in range(self.dim):
            # adding 1 to each HC element allows element multiplication of SM to HC to yield non-zero bit indices defining positions for decoded bits
            SML = np.multiply(SM[i][:][:],self.HC[i][:][:]+1)
            for j in range(self.dim):
                for k in range(self.dim):
                    if SML[j][k] != 0:
                        # subtracting 1 from each element reverts the indices to the true index number
                        ba[SML[j][k]-1] = 1
        print(ba)
        return ba
    
    def remap(self, dest):
        """Protected definition. Modifies `SpatialCodec` Hilbert curve by translating about the Z axis.

        Args:
          * dest (`int`): `dest` defines a target direction to remap to. Defined by directions [0>1>2>3] in clockwise direction

        Raises:
          * `ValueError`: Raised if destination is not defined by integers in the range [0,3]
        """
        # assume default direction is 0
        if self.orient == dest:
            return
        elif dest not in [0,1,2,3]:
            raise ValueError
        
        # the following if statements categorize 3 matrix transformations: mirror, CW and CCW rotations. Depending on the destination index the
        # algorithm will select the operation that will yield the destination via a single transformation.
        if np.abs(self.orient+dest)%2 == 0:
            print("Mirror translation:")
            # to perform a mirror transformation matrix multiply anti-diagonal identity J to HC twice for each layer of HC: J*HC[x]*J 
            for i in range(self.dim):
                self.HC[i][:][:] = np.matmul(self.J, np.matmul(self.HC[i][:][:],self.J))
        else:
            # determine the 
            if ((dest - self.orient) <= 0 and (dest - self.orient) >= -1) or ((dest - self.orient) > 1):
                # perform a CCW rotation transformation by matrix multiply the anti-diagonal identity J to the transpose of each layer of HC: J*HC[x]^T
                print("CCW translation:")
                for i in range(self.dim):
                    self.HC[i][:][:] = np.matmul(self.J,self.HC[i][:][:].T)
            else:
                # perform a CW rotation transformation by matrix multiply the transpose of each layer of HC to the anti-diagonal identity J: HC[x]^T*J
                print("CW translation:")
                for i in range(self.dim):
                    self.HC[i][:][:] = np.matmul(self.HC[i][:][:].T,self.J)
        
        # update codec orientation attribute
        self.orient = dest
        print(self.HC)

    def render(self, ba_list):
        """Renders a list of `bitarray` objects to a 3D scatter rendered using `plotly`

        Args:
          * ba_list (:list:`bitarray`): `ba_list` is a list (size args.frames) of randomly generated bits (size args.dim^3)
        """
        # initialized for storing figure labels with decoded hex values
        decoded_hex = list()

        print("Rendering Spatial Bitmaps:")

        for steps in range(len(ba_list)):
            # encode bitarray into list of Spatial bits
            frame = self.encode(ba_list[steps])
            print("Encoded frame: " + str(steps))
            # Add the new trace to the scatter
            tx = frame.x
            ty = frame.y
            tz = frame.z
            self.fig.add_trace(go.Scatter3d(visible=True, x=tx,y=ty,z=tz))

            # decode Frame object back into bitarray
            ba = self.decode(frame)
            # append decoded bitarray to decoded hex list for figure labelling
            decoded_hex.append(ba.tobytes().hex())
            print("Decoded frame: " + str(steps))

            # clear arrays for next frame
            tx.clear()
            ty.clear()
            tz.clear()

        steps = []

        for i in range(len(self.fig.data)):
            step = dict(
                method="restyle",
                args=["visible", [False] * len(self.fig.data)],
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
    # sc.remap(3)
    # Step 2: Encode
    # Step 3 Decode always at default
    # NOTE: TCU has the ability to rotate and track its rotation with the hilbert curve. IRIS only knows one configuration of HC and simply decodes according to that
    sc.render(ba_list)
