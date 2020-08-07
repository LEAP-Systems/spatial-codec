import os
from sc.scodec import SpatialCodec

# inputs = ((10,3), (5,4), (2,6), (4,6), (1,9))

if os.environ['SC_ENV'] == 'dev':
    sc = SpatialCodec(2,2, dev=True,optimize=False)
else:
    sc = SpatialCodec(2,2, dev=False, optimize=True)
# sc.visualizer.populate(inputs)
sc.visualizer.render()
