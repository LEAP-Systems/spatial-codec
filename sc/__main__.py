import sys
import getopt
import logging
from sc.scodec import SpatialCodec

def main(argv) -> None:
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
    SpatialCodec(resolution, dimension)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(sys.argv[1:])
