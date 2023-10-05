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

    # Don't build any plot objects here, let the interface do that
    #  # #  ## # # #####  # ## # # # 
    

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
        data = np.random.normal(size=(num_points,2))
        data[:,1] = data[:,0] + 0.1*data[:,1]
        self.data = pd.DataFrame(data, 
                                 columns=['x','y'])
        return
    
class MyInterface:
    # Does all the display stuff
    def __init__(self,
                 geometry = '640x480'
                 ):
        
        self.configure_main_window()
        self.make_plot()

        print('entering main loop')
        self.main_window.mainloop()
        print('main loop done')
        return
    
    def configure_main_window(self,
                              geometry: str = '640x480'
                              ):
        self.main_window = tk.Tk()
        self.main_window.geometry(geometry)
        self.main_window.title('Example interface using tkinter')

        # Split the main_window into two rows (top for plot, bottom for buttons)
        self.interface_area = tk.Frame(self.main_window)
        self.interface_area.rowconfigure(0, weight=1) # The plot area
        self.interface_area.rowconfigure(1, weight=1) # The buttons area

        
        # A button
        print('button stuff')
        a_button = tk.Button(master=self.interface_area,
                             command = lambda: print(1),
                             text = 'a button'
                             )
        a_button.grid(row=1, column=0)

        # Pack it up
        self.interface_area.pack()
        return
    
    def make_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(2,2), 
                                         dpi=72)
        #self.scat = self.ax.scatter(self.data['x'], self.data['y'])
        self.scat = self.ax.scatter([1,2,3],[4,5,6])
        self.canvas = FigureCanvasTkAgg(self.fig, 
                                        master=self.interface_area)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0)
        return
    
    def update_plot(self):
        self.scat.set_offsets(self.data.values)
        return
    
if __name__ == '__main__':
    m = MyProgram()
    print(m.timestamp())
    MyInterface()