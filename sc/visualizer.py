

import matplotlib.pyplot as plt

class Visualizer:

    def __init__(self, frame:tuple):
        plt.figure(figsize=(8,8))
        self.rx, self.ry = frame
        plt.axis([0, self.rx, 0, self.ry])
        # draw dividers
        plt.plot([self.rx/2, self.rx/2], [0,self.ry],linewidth=1, linestyle='dashed', color='red')
        plt.plot([0, self.rx], [self.ry/2,self.ry/2],linewidth=1, linestyle='dashed', color='red')
        
    def render(self):
        self.line()
        plt.show()
    
    def populate(self, targets:set):
        plt.scatter(
            list(map( lambda x : x[0], targets)),
            list(map( lambda x : x[1], targets)),
        )

    def line(self):
        # creating 4 equivalent sectors
        offset = self.rx/2
        
        # draw curve
        # plt.plot()