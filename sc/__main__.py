import sys
import getopt
import logging

from sc.n3 import N3
from sc.n2 import N2


def main(argv) -> None:
    # defaults
    dimension = 0
    resolution = 0
    input_stream = bytes("default", 'utf-8')
    mpl = False
    # parse opts
    try:
        opts, _ = getopt.getopt(argv, "s:d:v:", ["string=", "dimension=", "verbose="])
    except getopt.GetoptError:
        logging.exception("python -m sc -s $STRING -d $DIMENSION -v=")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--string"):
            input_stream = bytes(arg,'utf-8')
            # compute bit resolution of stream
            resolution = len(input_stream) * 8
        elif opt in ("-d", "--dimension"):
            dimension = int(arg)
        elif opt in ('-v, --verbose'):
            mpl = True
    logging.info("Input stream: %s", input_stream)
    logging.info("Bit resolution: %s", resolution)
    logging.info("Encoding dimension: %s", dimension)
    logging.info("MPL Visualizer: %s", mpl)
    # N2/N3 impl split
    if dimension == 2:
        n2_sc = N2(resolution)
        encode_stream = n2_sc.stream_encode(input_stream,mpl=mpl)
        bytestream = n2_sc.stream_decode(encode_stream,len(input_stream))
    elif dimension == 3:
        n3_sc = N3(resolution)
        encode_stream = n3_sc.stream_encode(input_stream,mpl=mpl)
        bytestream = n3_sc.stream_decode(encode_stream,len(input_stream))
    else:
        raise ValueError("Spatial codec is only defined for 2D and 3D space filling curves")
    print(bytestream.decode('utf-8'))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(sys.argv[1:])
