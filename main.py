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

from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt as qt
from PyQt5 import QtWidgets as qtw

class MyPlot:
    '''
    Class handles all aspects of figure creation, updating, output
    '''
    __SLOTS__ = ('fig', 
                 'ax', 
                 'scat')
    
    PATH_FIGURES = './figures/'
    
    def __init__(self):
        self.fig = None
        self.check_directories()
        return
    
    def check_directories(self):
        if not os.path.exists(self.PATH_FIGURES):
            os.mkdir(self.PATH_FIGURES)
        return

    def init_scatter(self):
        # Note: There is an issue with tk,
        #  do not create a figure before calling tk.Tk()
        self.fig, self.ax = plt.subplots(figsize=(2,2),
                                         dpi = 72)
        self.scat = self.ax.scatter([],[], 
                                    s=10)
        return
    
    def update_scatter(self, 
                       scatter_data: pd.DataFrame
                       ):
        '''
        scatter_data should be a pandas DataFrame with columns
        labeled 'x' and 'y'
        '''
        self.scat.set_offsets(scatter_data.values)
        self.ax.set_xlim([min(scatter_data['x']),
                          max(scatter_data['x'])
                          ])
        self.ax.set_ylim([min(scatter_data['y']),
                          max(scatter_data['y'])
                          ])
        return
    
    def save_plot(self):
        self.fig.savefig(self.PATH_FIGURES + 'figure.pdf', 
                         bbox_inches='tight')
        return

class MyEngine:
    '''
    This class does all the data/math/etc stuff.
    It does NONE of the visualization/interface stuff.

    It can be used by another class that defines an interface,
    and that class should ask this class to do any math/computation/data stuff.
    '''

    PATH_DATA = './data/'
    PATH_FIGURES = './figures/'

    def __init__(self):
        self.check_directories()
        return
    
    def check_directories(self):
        if not os.path.exists(self.PATH_DATA):
            os.mkdir(self.PATH_DATA)
        if not os.path.exists(self.PATH_FIGURES):
            os.mkdir(self.PATH_FIGURES)
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
    
class MyInterface_Tk:
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
        
        # The engine is for the math/analysis
        self.engine = MyEngine()
        # The display is for the plot        
        self.display = MyPlot()
        # Layout the figure and the buttons
        self.configure_main_window(geometry)

        # The mainloop() runs the application
        self.main_window.mainloop()
        return

    def configure_main_window(self,
                              geometry: str
                              ):
        
        # Function defines and places all the buttons.
        # Could not include the placement of the plot here
        # due to a mysterious "unrecognized selector" error, so
        # the plot is constructed after this function is called
        
        self.main_window = tk.Tk()
        self.main_window.geometry(geometry)
        self.main_window.title('Example interface using tkinter')

        # Create the interface area,
        # which will be a container for the plot and the buttons
        self.interface_area = tk.Frame(self.main_window)

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
                                  command       = self.display.save_plot,
                                  text          = 'Save Figure',
                                  wraplength    = self.BTN_WRAPLEN,
                                  height        = self.BTN_HEIGHT,
                                  width         = self.BTN_WIDTH
                                  )
        btn_save_plot.grid(row=2, column=1)

        ### Set up the figure
        self.display.init_scatter()
        # The canvas object to link the figure to the interface
        self.canvas = FigureCanvasTkAgg(self.display.fig,
                                        master = self.interface_area)
        self.canvas.get_tk_widget().grid(row=0,        # Place the canvas in the top row
                                         columnspan=2, # Based on how many buttons we defined
                                         sticky=tk.E + tk.W)

        # Pack the interface
        self.interface_area.pack()
        return
    
    def update_plot(self):
        self.display.update_scatter(self.engine.data)
        self.canvas.draw()
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

class MyInterface_Qt:
    def __init__(self):
        
        # Application
        self.app = qtw.QApplication([])

        # Main window
        self.main_window = qtw.QWidget()
        self.main_window.setWindowTitle('Example interface using PyQt5')

        # The main layout
        self.main_layout = qtw.QVBoxLayout()

        # The figure
        # self.fig, self.ax = 


        return

if __name__ == '__main__':
    MyInterface_Tk()
    #MyInterface_Qt()