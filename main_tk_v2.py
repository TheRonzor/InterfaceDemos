##########################################################################
#                                                                        #
#      May you do good and not evil                                      #
#      May you find forgiveness for yourself and forgive others          #
#      May you share freely, never taking more than you give.            #
#                                                                        #
##########################################################################


# Step 1 of refactoring - group the logic for creating buttons into a function


# My libraries
from my_plots import SimpleScatter
from my_analysis import RandomDataAnalysis

# Other generic libraries
from typing import Callable

# Libraries for the tkinter interface
import tkinter as tk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.engine = RandomDataAnalysis()
        # The display is for the plot        
        self.display = SimpleScatter()
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
        self.button_make_random_data = \
            self.__create_button(text = 'Generate Random Data',
                                 row = 1,
                                 column = 0,
                                 command = self.make_random_data
                                 )
        #  Load data button
        self.button_load_data = \
            self.__create_button(text = 'Load a file',
                                 row = 1,
                                 column = 1,
                                 command = self.load_data
                                 )
        #  Output data button
        self.button_output_data = \
            self.__create_button(text = 'Save data to file',
                                 row = 2,
                                 column = 0,
                                 command = self.engine.output_data
                                 )
        # Save plot button
        self.button_save_plot = \
            self.__create_button(text = 'Save Figure',
                                 row = 2,
                                 column = 1,
                                 command = self.display.save_plot
                                 )
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
    
    def __create_button(self,
                        text:       str,
                        row:        int,
                        column:     int,
                        command:    Callable,
                        master:     tk.Frame    = None, # Default to self.interface_area
                        wraplength: int         = BTN_WRAPLEN,
                        height:     int         = BTN_HEIGHT,
                        width:      int         = BTN_WIDTH,
                        ) -> tk.Button:
        if master is None:
            master = self.interface_area
        
        button = tk.Button(master       = master,
                           command      = command,
                           text         = text,
                           wraplength   = wraplength,
                           height       = height,
                           width        = width
                           )
        button.grid(row=row, column=column)
        return button
    
    def make_random_data(self):
        self.engine.make_random_data()
        self.update_plot()
        return
    
    def update_plot(self):
        self.display.update_scatter(self.engine.data)
        self.canvas.draw()
        return
    
    def load_data(self):
        filename = fd.askopenfilename()
        try:
            self.engine.load_data(filename)
            self.update_plot()
        except Exception as e:
            print('Problem loading data. File name was: ' + str(filename))
        return

if __name__ == '__main__':
    MyInterface_Tk()