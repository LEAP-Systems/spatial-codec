

from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
class Visualizer:

    @staticmethod
    def plot_3d(d:List[Tuple[int,int,int]]) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = list(map(lambda x : x[0], d))
        y = list(map(lambda x : x[1], d))
        z = list(map(lambda x : x[2], d))
        # plot hilberts curve
        plt.plot(x, y, z, marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
    
    @staticmethod
    def line(d:List[Tuple]) -> None:
        x = list(map(lambda x : x[0], d))
        y = list(map(lambda x : x[1], d))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.plot(x, y, linewidth=1, color='black')
        plt.show()
