# Spatial Codec™

## Navigation
  1. [About](#about)
  2. [Quickstart](#quickstart)
  5. [License](#license)

## About
<p align="center">
  <img src="docs/img/3DFractal.gif"/>
</p>

Spatial codec is a spatial encoding and decoding algorithm developed for mapping a bytes to a 3D matrix at a target voxel resolution. The algorithm maps according to [Hilbert's Space Filling Curve](https://en.wikipedia.org/wiki/Hilbert_curve) which preserves the relative localization of bits in 3D independant of the matrix dimension which is a convienient property for error correction and scalable network policies.

<p align="center">
  <img src="docs/img/Codec.gif" width="900" height="450"/>
</p>

## Quickstart
Install python dependancies
```bash
python3 -m pip install -r requirments.txt
...
```
Run the algorithm for a specified resolution `n`
```bash
./scodec.sh 1024
```

## License
BSD 2-Clause License available [here](LICENSE)
