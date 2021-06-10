import sys
import getopt
import logging

from codec.n3 import N3
from codec.n2 import N2


def main(argv) -> None:
    # defaults
    be = "utf-8"
    dimension = 0
    block = 0
    input_stream = bytes("default", be)
    mpl = False
    # parse opts
    try:
        opts, _ = getopt.getopt(
            argv, "n:b:d:v:", ["dimension=", "block=", "data=", "verbose="])
    except getopt.GetoptError:
        logging.exception("python -m sc -n 2 -b 32 -s test -v=")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--data"):
            input_stream = bytes(arg, be)
        elif opt in ("-n", "--dimension"):
            dimension = int(arg)
        elif opt in ("-v, --verbose"):
            mpl = True
        elif opt in ("-b, --block"):
            block = int(arg)
    logging.info("Input stream: %s", input_stream)
    logging.info("Byte Encoding: %s", be)
    logging.info("Block size: %s", block)
    logging.info("Encoding dimension: %s", dimension)
    logging.info("MPL Visualizer: %s", mpl)
    # N2/N3 impl split
    if dimension == 2:
        n2_sc = N2(block)
        encode_stream = n2_sc.stream_encode(input_stream, mpl=mpl)
        bytestream = n2_sc.stream_decode(encode_stream, len(input_stream))
    elif dimension == 3:
        n3_sc = N3(block)
        encode_stream = n3_sc.stream_encode(input_stream, mpl=mpl)
        bytestream = n3_sc.stream_decode(encode_stream, len(input_stream))
    else:
        raise ValueError("Spatial codec is only defined for 2D and 3D space filling curves")
    print(bytestream.decode("utf-8"))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(sys.argv[1:])
