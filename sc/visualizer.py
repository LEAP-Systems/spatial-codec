

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
class Visualizer:

    @staticmethod
    def plot_3d(data_set, decoder):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xs, ys, zs, = list(), list(), list()
        for coor, neuron in data_set.items():
            label = f"({neuron.x},{neuron.y})"
            ax.text(coor[0],coor[1],coor[2], label, size=6, zorder=1, color='k') 
            xs.append(coor[0])
            ys.append(coor[1])
            zs.append(coor[2])
        ax.scatter(xs, ys, zs, marker='o')
        hcx, hcy, hcz, = list(), list(), list()
        # plot hilberts curve
        for coor in decoder.hc:
            hcx.append(coor[0])
            hcy.append(coor[1])
            hcz.append(coor[2])
        plt.plot(hcx, hcy, hcz, marker='o')
        # plt.plot(hcx,hcy,hcz)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
    
    @staticmethod        
    def render() -> None:
        plt.axis('off')
        plt.grid(b=False)
        plt.show()

    @staticmethod
    def line(d:list) -> None:
        x = list(map(lambda x : x[0], d))
        y = list(map(lambda x : x[1], d))
        plt.plot(x, y, linewidth=1, color='black')
