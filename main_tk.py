import os
import time
import numpy as np
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from datetime import datetime as dt
from sklearn.linear_model import LinearRegression as LR
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Write random data to a file

# Select a file to import

# Plot the data and fit a line

# Output the figure

# Keep the functional and display aspects separate

class MyProgram:
    PATH_DATA = './data/'
    # Does all the data stuff
    def __init__(self):
        self.check_directories()
        return
    
    def check_directories(self):
        if not os.path.exists(self.PATH_DATA):
            os.mkdir(self.PATH_DATA)
        return
    
    def timestamp(self) -> str:
        return str(dt.now()).replace(':', '.').replace(' ', '-')

    def make_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6,6), 
                                         dpi=100)
        
        self.scat = self.ax.scatter(self.data['x'], self.data['y'])
        return
    
    def update_plot(self):
        self.scat.set_offsets(self.data.values)
        return

    def get_plot(self):
        return self.fig, self.ax
    
    def show_plot(self):
        plt.show()
        return

    def output_data(self):
        file_name = self.PATH_DATA + 'data_' + self.timestamp() + '.csv'
        self.data.to_csv(file_name, index=False)
        return
    
    def load_data(self, 
                  file_name: str
                  ):
        self.data = pd.read_csv(file_name)
        return

    def make_random_data(self, 
                         num_points=10
                         ):
        self.data = pd.DataFrame(np.random.normal(size=(num_points,2)), 
                                 columns=['x','y'])
        return
    
class MyInterface:
    # Does all the display stuff
    def __init__(self):
        pass
        return
    
if __name__ == '__main__':
    m = MyProgram()
    print(m.timestamp())
    m.make_random_data()
    m.make_plot()
    time.sleep(1)
    m.make_random_data()
    
    