import plotly.graph_objects as go
import pandas as pd
from bitarray import bitarray
import random
import argparse


class SpatialBit:

    def __init__(self, x, y, z, state):
        self.pos = [x,y,z]
        #any non-zero state value is collapsed to true
        self.state = bool(state)
        self.next = None
    
    def read(self):
        return self.pos, self.state

class SpatialMap:
    def __init__(self, size, xm, ym, zm, ba):
        self.head = None
        #build linked list from the last frame to the first in order to have the head start at first indice
        for i in reversed(range(size)):
            sb = SpatialBit(xm[i],ym[i],zm[i],ba[i])
            sb.next = self.head
            self.head = sb

    def next(self):
        if self.head == None:
            raise ValueError("Traversed to end of hilbert spatial map.")
        
        current = self.head
        self.head = current.next
        return current


#define masterlists for x,y and z coordinates
xm = list()
ym = list()
zm = list()

def hilbert_curve(dim, x, y, z, dx, dy, dz, dx2, dy2, dz2, dx3, dy3, dz3):
    if(dim==1):
        xm.append(x)
        ym.append(y)
        zm.append(z)
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
        
        hilbert_curve(dim, x, y, z, dx2, dy2, dz2, dx3, dy3, dz3, dx, dy, dz)
        hilbert_curve(dim, x+dim*dx, y+dim*dy, z+dim*dz, dx3, dy3, dz3, dx, dy, dz, dx2, dy2, dz2)
        hilbert_curve(dim, x+dim*dx+dim*dx2, y+dim*dy+dim*dy2, z+dim*dz+dim*dz2, dx3, dy3, dz3, dx, dy, dz, dx2, dy2, dz2)
        hilbert_curve(dim, x+dim*dx2, y+dim*dy2, z+dim*dz2, -dx, -dy, -dz, -dx2, -dy2, -dz2, dx3, dy3, dz3)
        hilbert_curve(dim, x+dim*dx2+dim*dx3, y+dim*dy2+dim*dy3, z+dim*dz2+dim*dz3, -dx, -dy, -dz, -dx2, -dy2, -dz2, dx3, dy3, dz3)
        hilbert_curve(dim, x+dim*dx+dim*dx2+dim*dx3, y+dim*dy+dim*dy2+dim*dy3, z+dim*dz+dim*dz2+dim*dz3, -dx3, -dy3, -dz3, dx, dy, dz, -dx2, -dy2, -dz2)
        hilbert_curve(dim, x+dim*dx+dim*dx3, y+dim*dy+dim*dy3, z+dim*dz+dim*dz3, -dx3, -dy3, -dz3, dx, dy, dz, -dx2, -dy2, -dz2)
        hilbert_curve(dim, x+dim*dx3, y+dim*dy3, z+dim*dz3, dx2, dy2, dz2, -dx3, -dy3, -dz3, -dx, -dy, -dz)


#Argument Parsing
parser = argparse.ArgumentParser(description='Generates a sequence of 3D spatially encoded frames from sequence of 1D bitarrays.')
parser.add_argument('dim', metavar='dim', type=int,
    help='matrix dimension (must be a power of 2)')
parser.add_argument('frames', metavar='frames',type=int,
    help='number of frames to generate.')
args = parser.parse_args()

#define a 3D cube of SpatialBits given a cube dimension using Hilberts space filling curve
size = pow(args.dim,3)
ba = bitarray()

#execute space filling algorithm for size dim
hilbert_curve(args.dim,0,0,0,1,0,0,0,1,0,0,0,1)

#we should finish the algorithm with dim^3 length arrays.
if  not all([len(xm), len(ym), len(zm)]) or len(xm) != size:
    raise IndexError

tx = list()
ty = list()
tz = list()

#create figure with base layout
fig = go.Figure(
    layout = go.Layout(title="3D Spatial Mapping of Randomly Generated 1D Bitarray using Hilberts Space Filling Curve.")
)

spatial_maps = list()

#generate frame traces
for steps in range(args.frames):
    #generate a random bitarray with length of cube size
    for i in range(size):
        ba.append(bool(random.getrandbits(1)))

    spatial_maps.append(SpatialMap(size, xm, ym, zm, ba))
    #print only bits with an on state.
    for i in range(size):
        [x,y,z], state = spatial_maps[steps].next().read()
        if state:
            tx.append(x)
            ty.append(y)
            tz.append(z)
    fig.add_trace(go.Scatter3d(visible=True, x=tx,y=ty,z=tz))
    #clear arrays
    tx.clear()
    ty.clear()
    tz.clear()
    ba = bitarray()


steps = []
for i in range(len(fig.data)):
    step = dict(
        method="restyle",
        args=["visible", [False] * len(fig.data)],
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
    sliders=sliders
)

fig.show()