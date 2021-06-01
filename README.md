# Spatial Codec
[![ci](https://github.com/LEAP-Systems/spatial-codec/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/LEAP-Systems/spatial-codec/actions/workflows/ci.yaml)
Modified: 2021-05

<p align="center">
  <img src="docs/img/LEAP_INS_WHITE.png"/>
</p>

## Navigation
  1. [About](#about)
  2. [Quickstart](#quickstart)
  3. [Dev](#dev)
  4. [License](#license)

## About
Spatial codec is a spatial encoding and decoding algorithm developed for mapping a bytes to a 3D matrix at a target voxel resolution. The algorithm maps according to [Hilbert's Space Filling Curve](https://en.wikipedia.org/wiki/Hilbert_curve) which preserves the relative localization of bits in 3D independant of the matrix dimension which is a convienient property for error correction and scalable network policies.

## Quickstart
Install python dependancies
```bash
python3 -m pip install -r requirements.txt
...
```
Run the algorithm for a specified data block `-s` / `--string` and dimension `-d` / `--dimension` (2 or 3). The MPL visualizer can be enabled with the `-v=` flag.
```bash
# exec n2 algorithm
python3 -m sc -s "Hello World" -d 2 -v=
...
# exec n3 algorithm
python3 -m sc -s "H" -d 3 -v=
```

## Dev
Setup on M1 macs requires some additional configuration. I have automated the installation:
```bash
./scripts/m1-setup.sh
```

## License
BSD 2-Clause License available [here](LICENSE)
