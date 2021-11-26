import math
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

POPULATION = 8
BLOCK = 16
DIM = 1000

_SV = [2**x for x in range(BLOCK)]


def transform(x: int, y: int, r_x: int, r_y: int, c: int) -> Tuple[int, int]:
    # rotation function for this region
    if r_y == 0:
        if r_x == 1:
            x, y = c - 1 - x, c - 1 - y
        x, y = y, x
    return x, y


def iterator(i: int) -> Tuple[int, int]:
    r_x = 1 & (i >> 1)
    r_y = 1 & (i ^ r_x)
    return r_x, r_y


def encode(i: int) -> Tuple[int, int]:
    index = i
    # initial coordinates
    x, y = 0, 0
    for level, c in enumerate(_SV):
        # Once the index reaches 0 the x and y bits are latched and alternate between each other
        # before converging before we exceed the range boundary n
        if i == 0:
            # we are done
            if x == y:
                break
            # compute last flip (i required for forcasting)
            x, y = (y, x) if (BLOCK - level) & 1 else (x, y)
            break
        # generate base iterator
        r_x, r_y = iterator(i)
        x, y = transform(x, y, r_x, r_y, c)
        # translate base iterator
        x += c * r_x  # x = x + (s or 0)
        y += c * r_y  # y = y + (s or 0)
        i = i >> 2  # regions of seperation (4 verticies)
    return x, y


def stream_encode(bytestream: bytes, mpl: bool = False) -> List[Tuple[int, int]]:
    # remove excess bytes if word exceeds resolution
    bitstream = int(bytestream.hex(), base=16) & (2 ** BLOCK - 1)
    print("bitstream: ", bin(bitstream))
    bits = [bitstream >> i & 0x1 for i in range(BLOCK)]
    index = list(filter(None, [encode(i) if b else None for i, b in enumerate(bits)]))
    print("index: ", index)
    return index


print(bytes([0xff, 0xff]))
hra = stream_encode(bytes([0xff, 0xff]))
x = np.array(list(map(lambda a: float(a[0]), hra)))
y = np.array(list(map(lambda a: float(a[1]), hra)))
hc = np.array([x, y])
print(hc)

size = np.array([DIM, DIM])

x = np.random.randint(0, DIM, size=POPULATION)
y = np.random.randint(0, DIM, size=POPULATION)

divisor = DIM / math.log2(BLOCK)
square = size / math.log2(BLOCK)
print("Quantile: ", square)

xv, yv = np.meshgrid(
    np.linspace(
        divisor / 2, DIM - divisor / 2, int(math.log2(BLOCK))
    ),
    np.linspace(
        divisor / 2, DIM - divisor / 2, int(math.log2(BLOCK))
    )
)

# data = np.random.rand(int(math.log2(BLOCK)), int(math.log2(BLOCK))) * 2
# compute population per tile
tile_populations = np.array([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 0],
])
print(tile_populations)
# create discrete colormap
cmap = colors.ListedColormap(['none', 'r'], N=2)
bounds = [0, 1]
norm = colors.BoundaryNorm(bounds, cmap.N)  # type: ignore


print(xv, yv)
major_ticks = np.linspace(0, DIM, int(math.log2(BLOCK)) + 1)
fig, axes = plt.subplots(figsize=(10, 10))
axes.set_xlim(0, DIM)
axes.set_ylim(0, DIM)
axes.set_xticks(major_ticks)
axes.set_yticks(major_ticks)
axes.set_title("Frame")
axes.imshow(tile_populations, cmap=cmap, norm=norm, extent=[0, DIM, 0, DIM], zorder=0)
axes.grid()
plt.plot(xv, yv, 'ko')
# draw hilberts curve
hc *= divisor
hc = hc + (divisor / 2)
print(hc)

plt.plot(hc[0], hc[1], 'k')
plt.plot(x, y, 'bo')
plt.grid(color='grey', linestyle='--', linewidth=0.5)
plt.show()
#
