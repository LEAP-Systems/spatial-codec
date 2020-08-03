

import matplotlib.pyplot as plt

class Visualizer:

    def __init__(self, frame:tuple):
        plt.figure(figsize=frame)
        plt.axis('equal')
        # plt.fill(x, y)
        plt.show()