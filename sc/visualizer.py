

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
class Visualizer:

    @staticmethod
    def plot_3d(coordinates:tuple) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        hcx, hcy, hcz, = list(), list(), list()
        # plot hilberts curve
        for x,y,z in coordinates:
            hcx.append(x)
            hcy.append(y)
            hcz.append(z)
        plt.plot(hcx, hcy, hcz, marker='o')
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
