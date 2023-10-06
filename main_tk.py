##########################################################################
#                                                                        #
#      May you do good and not evil                                      #
#      May you find forgiveness for yourself and forgive others          #
#      May you share freely, never taking more than you give.            #
#                                                                        #
##########################################################################

# Comment out the below (not recommended) to not print The Zen of Python
print('\n')
import this
print('\n')

# Pardon the order of my imports, 
# it would be more logical to group them by functionality,
# but I like them to look like a mountainside ;-)
import os
import time
import numpy as np
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from datetime import datetime as dt
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    

class MyEngine:
    '''
    This class does all the data/math/etc stuff.
    It does NONE of the visualization/interface stuff.

    It can be used by another class that defines an interface,
    and that class should ask this class to do any math/computation/data stuff.
    '''

    PATH_DATA = './data/'
    def __init__(self):
        self.check_directories()
        return
    
    def check_directories(self):
        if not os.path.exists(self.PATH_DATA):
            os.mkdir(self.PATH_DATA)
        return
    
    def timestamp(self) -> str:
        '''
        Returns a unique timestamp as a string
        '''
        return str(dt.now()).replace(':', '.').replace(' ', '-')

    def output_data(self):
        '''
        Output the currently loaded data as a .csv file with a default naming convention
        '''
        file_name = self.PATH_DATA + 'data_' + self.timestamp() + '.csv'
        self.data.to_csv(file_name, index=False)
        return
    
    def load_data(self, 
                  file_name: str
                  ):
        '''
        Load a data file
        '''
        self.data = pd.read_csv(file_name)
        return

    def make_random_data(self, 
                         num_points=10
                         ):
        '''
        Generate some random data
        '''
        data = np.random.normal(size=(num_points,2))
        data[:,1] = data[:,0] + 0.5*data[:,1]
        self.data = pd.DataFrame(data, 
                                 columns=['x','y'])
        return
    
class MyInterface:
    '''
    This class does all of the interface/visualization stuff.
    It does NONE of the math/data stuff (it has a MyEngine component for those parts)
    '''

    BTN_HEIGHT  = 2
    BTN_WIDTH   = 10
    BTN_WRAPLEN = 100

    def __init__(self,
                 geometry = '600x480'
                 ):
        
        # Favor composition over inheritence
        self.engine = MyEngine()
        
        self.configure_main_window(geometry)
        self.make_plot()

        self.main_window.mainloop()
        return

    def configure_main_window(self,
                              geometry: str
                              ):
        self.main_window = tk.Tk()
        self.main_window.geometry(geometry)
        self.main_window.title('Example interface using tkinter')

        # Split the main_window into two rows (top for plot, bottom for buttons)
        self.interface_area = tk.Frame(self.main_window)
        
        # Not needed since we are using .grid below, but leaving it as a reminder
        #self.interface_area.rowconfigure(0, weight=1) # The plot area
        #self.interface_area.rowconfigure(1, weight=1) # The buttons area

        ### Buttons
        #  Make random data button
        btn_make_random_data = tk.Button(master      = self.interface_area,
                                         command     = self.make_random_data,
                                         text        = 'Generate Random Data',
                                         wraplength  = self.BTN_WRAPLEN,
                                         height      = self.BTN_HEIGHT,
                                         width       = self.BTN_WIDTH
                                         )
        btn_make_random_data.grid(row=1, column=0)

        #  Load data button
        btn_load_data = tk.Button(master        = self.interface_area,
                                  command       = self.load_data,
                                  text          = 'Load a file',
                                  wraplength    = self.BTN_WRAPLEN,
                                  height        = self.BTN_HEIGHT,
                                  width         = self.BTN_WIDTH
                                  )
        btn_load_data.grid(row=1, column=1)

        #  Output data button
        btn_output_data = tk.Button(master      = self.interface_area,
                                    command     = self.engine.output_data,
                                    text        = 'Save data to file',
                                    wraplength  = self.BTN_WRAPLEN,
                                    height      = self.BTN_HEIGHT,
                                    width       = self.BTN_WIDTH
                                    )
        btn_output_data.grid(row=2, column=0)
        
        # Save plot button
        btn_save_plot = tk.Button(master        = self.interface_area,
                                  command       = self.save_plot,
                                  text          = 'Save Figure',
                                  wraplength  = self.BTN_WRAPLEN,
                                  height      = self.BTN_HEIGHT,
                                  width       = self.BTN_WIDTH
                                  )
        btn_save_plot.grid(row=2, column=1)

        # Pack it up
        self.interface_area.pack()
        return
    
    def make_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(2,2), 
                                         dpi=72)
        
        self.scat = self.ax.scatter([],[], 
                                    s= 10)
        
        self.canvas = FigureCanvasTkAgg(self.fig, 
                                        master=self.interface_area)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, 
                                         columnspan=3,
                                         sticky=tk.E + tk.W)
        return
    
    def update_plot(self):
        self.scat.set_offsets(self.engine.data.values)
        self.ax.set_xlim([min(self.engine.data['x']),
                          max(self.engine.data['x'])
                          ])
        self.ax.set_ylim([min(self.engine.data['y']),
                          max(self.engine.data['y'])
                          ])
        self.canvas.draw()
        return
    
    def save_plot(self):
        self.fig.savefig('figure.pdf', bbox_inches='tight')
        return
    
    def make_random_data(self):
        self.engine.make_random_data()
        self.update_plot()
        return
    
    def load_data(self):
        filename = fd.askopenfilename()
        self.engine.load_data(filename)
        self.update_plot()
        return
    
if __name__ == '__main__':
    MyInterface()