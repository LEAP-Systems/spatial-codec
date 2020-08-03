

import matplotlib.pyplot as plt

class Visualizer:

    def __init__(self, frame:tuple):
        plt.figure(figsize=(8,8))
        rx, ry = frame
        plt.axis([0, rx, 0, ry])
        
    def render(self):
        plt.show()
    
    def populate(self, targets:set):
        plt.scatter(
            list(map( lambda x : x[0], targets)),
            list(map( lambda x : x[1], targets)),
        )