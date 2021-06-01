import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.widgets import CheckButtons
class Visualizer:

    def __init__(self) -> None:
        plt.style.use('dark_background')
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.curves = []
        self.cube_max = 0

    def add_curve(self, d:List[Tuple[int,int,int]], label:str, clr:str) -> None:
        x = list(map(lambda x : x[0], d))
        y = list(map(lambda x : x[1], d))
        z = list(map(lambda x : x[2], d))
        # Update cube max
        self.cube_max = max([max(x), max(y), max(z)])
        # Don't mess with the limits!
        l, = self.ax.plot(x, y, z, visible=False, marker='o', color=clr, label=label)
        self.curves.append(l)

    def show(self) -> None:
        def func(label):
            index = labels.index(label)
            self.curves[index].set_visible(not self.curves[index].get_visible())
            plt.draw()
        # Make checkbuttons with all plotted lines with correct visibility
        rax = plt.axes([0.05, 0.1, 0.2, 0.7])
        labels = [str(curve.get_label()) for curve in self.curves]
        visibility = [bool(curve.get_visible()) for curve in self.curves]
        check = CheckButtons(rax, labels, visibility)
        plt.xlim(0, self.cube_max)
        plt.ylim(0, self.cube_max)
        plt.autoscale(False)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_zlim(0, self.cube_max)
        plt.subplots_adjust(left=0.2)
        check.on_clicked(func)
        plt.show()

    def plot_3d(self, d:List[Tuple[int,int,int]]) -> None:
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
        plt.plot(x, y, z, marker='o', color='red')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_zlim(0, cube_max)
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
        sq_max = max(max(x), max(y))
        plt.xlim(0, sq_max)
        plt.ylim(0, sq_max)
        # Don't mess with the limits!
        plt.autoscale(False)
        plt.plot(x, y, linewidth=3, color='black')
        x = list(map(lambda x : x[0], coor))
        y = list(map(lambda x : x[1], coor))
        plt.plot(x, y, marker='o', color='red') 
        plt.show()
