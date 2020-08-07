

import matplotlib.pyplot as plt

class Visualizer:

    def __init__(self, frame:tuple):
        # plt.figure(figsize=(8,8))
        self.rx, self.ry = frame
        # plt.axis([0, self.rx-1, 0, self.ry-1])
        # draw dividers
        # plt.plot([self.rx/2, self.rx/2], [0,self.ry],linewidth=1, linestyle='dashed', color='red')
        # plt.plot([0, self.rx], [self.ry/2,self.ry/2],linewidth=1, linestyle='dashed', color='red')
        # plt.plot([0, self.rx], [0,self.ry],linewidth=1, color='red')
        
    def render(self):
        plt.axis('off')
        plt.grid(b=False)
        plt.show()
    
    def populate(self, targets:set):
        plt.scatter(
            list(map( lambda x : x[0], targets)),
            list(map( lambda x : x[1], targets)),
        )

    def line(self, d:list):
        # creating 4 equivalent sectors
        # offset = self.rx/2
        # draw curve
        # plt.plot()
        x = list(map(lambda x : x[0], d))
        y = list(map(lambda x : x[1], d))
        plt.plot(x, y, linewidth=1, color='black')
        plt.scatter(x,y)
