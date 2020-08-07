import os
from sc.scodec import SpatialCodec

# inputs = ((10,3), (5,4), (2,6), (4,6), (1,9))

INPUT_SPACE = int(os.environ['SC_N'])

if os.environ['SC_ENV'] == 'dev':
    sc = SpatialCodec(INPUT_SPACE, dev=True)
else:
    sc = SpatialCodec(INPUT_SPACE, dev=False)
# sc.visualizer.populate(inputs)
sc.visualizer.render()
