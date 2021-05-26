
from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
class Visualizer:

    @staticmethod
    def plot_3d(d:List[Tuple[int,int,int]]) -> None:
        plt.style.use('dark_background')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = list(map(lambda x : x[0], d))
        y = list(map(lambda x : x[1], d))
        z = list(map(lambda x : x[2], d))
        # Set the limits of the plot
        cube_max = max([max(x), max(y), max(z)])
        plt.xlim(0, cube_max)
        plt.ylim(0, cube_max)
        # Don't mess with the limits!
        plt.autoscale(False)
        # plot hilberts curve
        plt.plot(x, y, z, marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_zlim(0,cube_max)
        plt.show()
    
    @staticmethod
    def d2(coor:List[Tuple], base:List[Tuple[int,int]]) -> None:
        plt.style.use('dark_background')
        x = list(map(lambda x : x[0], base))
        y = list(map(lambda x : x[1], base))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        # Set the limits of the plot
        sq_max = max(y) if max(y) > max(x) else max(x)
        plt.xlim(0, sq_max)
        plt.ylim(0, sq_max)
        # Don't mess with the limits!
        plt.autoscale(False)
        plt.plot(x, y, linewidth=3, color='black')
        x = list(map(lambda x : x[0], coor))
        y = list(map(lambda x : x[1], coor))
        plt.plot(x, y, marker='o', color='red') 
        plt.show()
