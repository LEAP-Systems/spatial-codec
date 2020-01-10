# Spatial Codec™

1. [ About ](#about)
2. [ Version ](#version)
3. [ Setup ](#setup)
4. [ Run ](#run)
5. [ License ](#lic)


<a name="about"></a>

## 1. About

This script is a visual demonstration of a specialized spatial encoding and decoding algorithm developed for mapping a 1D bitarray to a 3D matrix with a specified voxel (3D pixel) resolution. The encoder takes a 1D bitarray and translates each True bit to an equivalent set of `SpatialBit` objects consisting of a coordinate tuple `(x,y,z)`. 

The spatial encoder maps according to Hilbert's space filling curve (https://en.wikipedia.org/wiki/Hilbert_curve) which preserves localized bits in 1D to geometry in 3D independant of the matrix dimension. The encoder generates a `Frame` object which is a collection of `SpatialBit` objects. The result is a list of coordinate tuples with variable length. The spatial decoder takes a `Frame` object and uses a comparative algorithm to map each `SpatialBit` back to its correct index in the 1D `bitarray` mapping.

This mapping allows for consistent network packing/unpacking protocols independent of the cube dimensions. Furthermore it ensures that if a particular localized region of the 3D space is obstructed or is unreadable then the corresponding bit data errors will be localized to a set of neighbouring bits in 1D space which effectively reduces the severity of error across the whole message.


<a name="version"></a>

## 2. Version
This repository is staged: Version 1.0


<a name="setup"></a>

## Setup
Python3 is recommended for optimum results. Install the following modules to enable plotting functionality:
```
pip install plotly
```
```
pip install pandas
```
Install the following module to enable the `bitarray` generation:
```
pip install bitarray
```


<a name="run"></a>

## Run

The script takes in 2 input arguments: the first is the matrix dimension (must be a power of 2) and the second is for the number of random 1D `bitarray` frames the algorithm will generate.

The following example will generate 32 frames on a 4x4x4 matrix map:
```
python spatial_encoder.py 4 32
```
Once the script completes it will generate a `plotly` figure using your native browser. The initial frame will show a superposition of spatial bit mapping for all generated frames. Using the slider you can view a specific frames spatial mapping. Each point represents a bit that is has a `state=True`. The connecting lines follow the sequence in which the 1D bitarray constructs the 3D spatial bit map. By default mapping of the MSB of the bitarray is at `(0,0,0)` with the corresponding LSB at `(0,0,dim-1)` where `dim` is the user specified matrix dimension.


<a name="lic"></a>

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
