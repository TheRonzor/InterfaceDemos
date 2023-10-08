##########################################################################
#                                                                        #
#      May you do good and not evil                                      #
#      May you find forgiveness for yourself and forgive others          #
#      May you share freely, never taking more than you give.            #
#                                                                        #
##########################################################################

# My libraries
from my_plots import SimpleScatter
from my_analysis import RandomDataAnalysis

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
        try:
            self.engine.load_data(filename)
            self.update_plot()
        except Exception as e:
            print('Problem loading data. File name was: ' + str(filename))
        return

if __name__ == '__main__':
    MyInterface_Tk()