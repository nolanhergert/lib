
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque



class Plotter():
    '''
    A 1D timeseries plotter
    '''
    
    def __init__(self, width=5):
        '''
        Nothing for now
        
        Parameters
        ----------
        width : float
            Width in seconds of data to show
            
        '''
        self.fig, self.ax = plt.subplots()
        self.queue = deque(np.random.randn(100))
        self.line, = self.ax.plot(self.list)
        plt.show(block=False)
        self.tstart = time.time()
    
    def Update(self, data):
        list.append(data)
        list.
        self.line.set_ydata(data)
        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.time()


if __name__ == '__main__':
    p = Plotter()
    for i in range(100):
        p.Update(np.random.randn(100))
