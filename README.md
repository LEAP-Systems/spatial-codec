# Spatial Codec
[![PyPI version](https://badge.fury.io/py/scodec.svg)](https://badge.fury.io/py/scodec)
[![ci](https://github.com/LEAP-Systems/spatial-codec/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/LEAP-Systems/spatial-codec/actions/workflows/ci.yaml)

Modified: 2021-06

<p align="center">
  <img src="docs/img/LEAP_INS_WHITE.png"/>
</p>

## Navigation
  1. [About](#about)
  2. [Quickstart](#quickstart)
  3. [Dev](#dev)
  4. [License](#license)

## About
Spatial codec is a spatial encoding and decoding algorithm developed for iteratively mapping any number of bytes to a 3D (N3 space) matrix. The algorithm uses a psuedo variant of [Hilbert's Space Filling Curve](https://en.wikipedia.org/wiki/Hilbert_curve) which preserves the relative localization of bits in 3D independant of the matrix dimension which is a convienient property for error correction and scalable network policies.

## Quickstart
Install `scodec` from the package index
```bash
python3 -m pip install --upgrade pip
...
python3 -m pip install scodec
```
### API
Spatial codec provides an api for interacting in 2 (`N2`) and 3 (`N3`) dimensional space. Below is an example of using the `N2` space api:
```python
from scodec.n2 import N2

# configure a 2D spatial codec using a 64 bit block size
sc = N2(block_size=64)
# encode utf-8 string and enable matplotlib visualizer
space_encode = sc.stream_encode(bytes("Hello World", "utf-8"), mpl=True)
# feed spatial encode stream back into stream decode
bytestream = sc.stream_decode(space_encode)
```

### CLI Tool
The codec provides a cli tool for ease of use. Run the algorithm for a specified block size `-b` / `--block`, with a data stream `-d` / `--data` and dimension `-n` / `--dimension` (2 or 3). The MPL visualizer can be enabled with the `-v=` flag.
```bash
# n2 codec invocation
python3 -m codec -n 2 -b 512 -d "Hello World" -v=
...
# n3 codec invocation 
python3 -m codec -n 3 -b 8 -d "H" -v=
```

## License
BSD 2-Clause License available [here](LICENSE)
