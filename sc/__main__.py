from sc.n3 import N3
from sc.n2 import N2
import sys
import getopt
import logging
from sc.scodec import SpatialCodec

def main(argv) -> None:
    dimension = 0
    resolution = 0
    try:
        opts, _ = getopt.getopt(argv, "r:d:", ["resolution=", "dimension="])
    except getopt.GetoptError:
        logging.exception("python -m sc -r $RESOLUTION -d $DIMENSION")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-r", "--resolution"):
            resolution = int(arg)
        elif opt in ("-d", "--dimension"):
            dimension = int(arg)
    # N2/N3 impl split
    if dimension == 2:
        sc = N2(resolution=resolution)
    elif dimension == 3:
        sc = N3(resolution=resolution)
    else:
        raise ValueError("Spatial codec algorithm defined for 2D and 3D space filling curves")
    sc.stream_encode(b'\xffffffff')

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(sys.argv[1:])
