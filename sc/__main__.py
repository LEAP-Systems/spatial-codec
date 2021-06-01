import sys
import getopt
import logging

from sc.n3 import N3
from sc.n2 import N2


def main(argv) -> None:
    # defaults
    dimension = 0
    resolution = 0
    stream = bytes("default", 'utf-8')
    mpl = False
    # parse opts
    try:
        opts, _ = getopt.getopt(argv, "s:d:v:", ["string=", "dimension=", "verbose="])
    except getopt.GetoptError:
        logging.exception("python -m sc -s $STRING -d $DIMENSION -v=")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--string"):
            stream = bytes(arg,'utf-8')
            # compute bit resolution of stream
            resolution = len(stream) * 8
        elif opt in ("-d", "--dimension"):
            dimension = int(arg)
        elif opt in ('-v, --verbose'):
            mpl = True
    print("resolution: {}".format(resolution))
    print("dimension: {}".format(dimension))
    print("mpl: {}".format(mpl))
    # N2/N3 impl split
    if dimension == 2: sc = N2(resolution)
    elif dimension == 3: sc = N3(resolution)
    else: raise ValueError("Spatial codec is only defined for 2D and 3D space filling curves")
    sc.stream_encode(stream,mpl=mpl)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(sys.argv[1:])
