from sc.n3 import N3
from sc.n2 import N2
import sys
import getopt
import logging
from sc.scodec import SpatialCodec

def main(argv) -> None:
    dimension = 0
    resolution = 0
    stream = "default"
    try:
        opts, _ = getopt.getopt(argv, "s:d:", ["string=", "dimension="])
    except getopt.GetoptError:
        logging.exception("python -m sc -s $STRING -d $DIMENSION")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--string"):
            resolution = len(arg)
            stream = arg
        elif opt in ("-d", "--dimension"):
            dimension = int(arg)
    # N2/N3 impl split
    if dimension == 2: sc = N2(resolution)
    elif dimension == 3: sc = N3(resolution)
    else: raise ValueError("Spatial codec is only defined for 2D and 3D space filling curves")
    sc.stream_encode(bytes(stream, 'utf-8'))

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(sys.argv[1:])
