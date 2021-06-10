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

# region selection and transform application
# lambda x,y,z: (x + (s * r_x), y + (s * r_y), z + (s * r_z))
# if (r_x,r_y,r_z) == (0,0,0):
#     x,y,z = y,x,z
# elif (r_x,r_y,r_z) == (0,1,0) or (0,1,1):
#     x,y,z = z,y,x
# elif (r_x,r_y,r_z) == (0,0,1) or (1,0,1):
#     x,y,z = x,-y,-z
# elif (r_x,r_y,r_z) == (1,1,1) or (1,1,0):
#     x,y,z = -z,y,x
# else:
#     x,y,z = -z,x,y
# x += s * r_x # x = x + (s | 0)
# y += s * r_y # y = y + (s | 0)
# z += s * r_z # z = z + (s | 0)


# for index,s in enumerate(self.s):
#     self.log.debug("starting iteration %s",index)
#     # Once the index reaches 0 the x and y bits are latched and alternate between each other
#     # before converging before we exceed the range boundary n
#     if i == 0:
#         # optimization for starting case, flipping does not do anything
#         if x == y == z: break
#         # compute last flip (if odd flip if even keep)
#         x,y,z = (y,x,z) if (self.res-index) & 1 else (x,y,z) 
#         break
#     # compute region selector bits
#     # coordinates offsets by region
#     # the iterator changes with different i values
#     r_x,r_y,r_z = self.iterator(i, ('x','z','y'))
#     # regions of seperation (8 verticies)
#     i = i >> 3
#     x,y,z = self.transform(r_x,r_y,r_z,x,y,z,s)
#     self.log.info("i:%s s:%s | rx:%s ry:%s rz:%s | x:%s y:%s z:%s", i, s, r_x, r_y, r_z, x, y, z)