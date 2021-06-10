# -*- coding: utf-8 -*-
"""
Visualizer
==========
Contributors: Christian Sargusingh
Updated: 2021-05

Interactive spatial codec rendering using mpl api.

Dependancies
------------
```
from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import CheckButtons
```
Copyright © 2021 LEAP. All Rights Reserved.
"""

from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.widgets import CheckButtons


class Visualizer:
    def __init__(self) -> None:
        plt.style.use("dark_background")
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.curves = []
        self.cube_max = 0

    def add_n3_curve(
        self, d: List[Tuple[int, int, int]], marker: str, label: str, clr: str
    ) -> None:
        x = list(map(lambda x: x[0], d))
        y = list(map(lambda x: x[1], d))
        z = list(map(lambda x: x[2], d))
        # Update cube max
        self.cube_max = max(max(x), max(y), max(z), self.cube_max)
        # Don't mess with the limits!
        (l,) = self.ax.plot(x, y, z, visible=True, marker=marker, color=clr, label=label)
        self.curves.append(l)

    def add_n2_curve(self, d: List[Tuple[int, int]], marker: str, label: str, clr: str) -> None:
        x = list(map(lambda x: x[0], d))
        y = list(map(lambda x: x[1], d))
        # Update cube max
        self.cube_max = max(max(x), max(y), self.cube_max)
        # Don't mess with the limits!
        (l,) = self.ax.plot(x, y, visible=True, marker=marker, color=clr, label=label)
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
        self.ax.set_xlim(0, self.cube_max)
        self.ax.set_ylim(0, self.cube_max)
        plt.autoscale(False)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_zlim(0, self.cube_max)
        plt.subplots_adjust(left=0.2)
        check.on_clicked(func)
        plt.show()
