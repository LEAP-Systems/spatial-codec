import getopt
import sys

"""
rx, ry table
========
0 >> 2 = 0 (even) -> 0 | 00 ^ 00 = 00 & 1 -> 0
1 >> 2 = 0 (even) -> 0 | 01 ^ 00 = 01 & 1 -> 1
2 >> 2 = 1 (odd)  -> 1 | 10 ^ 01 = 11 & 1 -> 1
3 >> 2 = 1 (odd)  -> 1 | 11 ^ 01 = 10 & 1 -> 0
"""

def iterator2d(iterations:int) -> None:
    for i in range(iterations):
        r_x = 1 & (i >> 1)  # is index/2 odd?
        r_y = 1 & (i ^ r_x) # 
        print(r_x,r_y)

def iterator3d(iterations:int) -> None:
    for i in range(iterations):
        r_x = 1 & (i >> 2)  # is index/4 odd?
        r_y = 1 & ((i >> 1) ^ r_x)
        r_z = 1 & (i ^ r_x ^ r_y)
        print(r_x, r_y, r_z)

def main(argv) -> None:
    try:
        opts, _ = getopt.getopt(argv, "i:d:", ["index=", "dimension="])
    except getopt.GetoptError:
        print("python base.py -i $INDEX -d $DIMENSION")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--iterations"):
            i = int(arg)
        elif opt in ("-d", "--dimension"):
            d = int(arg)
    if d == 2:
        iterator2d(iterations=i)
    elif d == 3:
        iterator3d(iterations=i) 

if __name__  == "__main__":
    main(sys.argv[1:])