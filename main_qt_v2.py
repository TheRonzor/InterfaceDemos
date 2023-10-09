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

# Other general python libraries
import sys
from typing import Callable

# Libraries for the PyQt5 interface
#from PyQt5 import QtGui as qtg
#from PyQt5.QtCore import Qt as qt
from PyQt5 import QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MyInterface_Qt:
    def __init__(self,
                 geometry = None # Unused
                 ):
        
        # The engine is for the math/analysis
        self.engine = RandomDataAnalysis()
        
        # The display is for the plot        
        self.display = SimpleScatter()
        
        # A separate method to initialize the plot
        # This was removed from the SimpleScatter contstructor
        # due to an issue with tk
        self.display.init_scatter()
        
        # Layout the figure and the buttons
        self.configure_main_window(geometry)
        
        # Show the window and run the app
        self.main_window.show()
        sys.exit(self.app.exec_())
        return

    def configure_main_window(self, 
                              geometry
                              ):
        
        # Application
        self.app = qtw.QApplication([])

        # Main window
        self.main_window = qtw.QWidget()
        self.main_window.setWindowTitle('Example interface using PyQt5')

        # The main layout is a vertical container
        #   The top part will be the figure, the bottom will be the buttons
        self.main_layout = qtw.QVBoxLayout()
        self.main_window.setLayout(self.main_layout)

        # For the figure, we first create a canvas
        self.canvas = FigureCanvasQTAgg(self.display.fig)
        # Then we add it to the main_layout
        self.main_layout.addWidget(self.canvas)

        # Two rows of buttons, each is a horizontal container
        self.button_row1 = qtw.QHBoxLayout()
        self.button_row2 = qtw.QHBoxLayout()

        # Put those two button rows in their own vertical container
        self.button_rows = qtw.QVBoxLayout()
        self.button_rows.addLayout(self.button_row1)
        self.button_rows.addLayout(self.button_row2)
        # Put the button row container in the main_layout
        self.main_layout.addLayout(self.button_rows)

        ### Creating the actual buttons
        self.button_generate_random_data = \
            self.__create_button(text = "Generate Random Data",
                                 command = self.make_random_data,
                                 layout = self.button_row1
                                 )

        # Repeat for the rest of the buttons
        self.button_load_data = \
            self.__create_button(text = "Load a file",
                                 command = self.load_data,
                                 layout = self.button_row1
                                 )
        self.button_save_data = \
            self.__create_button(text = "Save data to file",
                                 command = self.engine.output_data,
                                 layout = self.button_row2
                                 )
        self.button_save_figure = \
            self.__create_button(text = "Save Figure",
                                 command = self.display.save_plot,
                                 layout = self.button_row2
                                 )
        return
    
    def __create_button(self,
                        text:       str,
                        command:    Callable,
                        layout:     qtw.QLayout
                        ) -> qtw.QPushButton:
        button = qtw.QPushButton(text)
        button.clicked.connect(command)
        layout.addWidget(button)
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
        filename,_ = qtw.QFileDialog.getOpenFileName(self.main_window,
                                                     "Select file",
                                                     "./data/")
        try:
            self.engine.load_data(filename)
            self.update_plot()
        except Exception as e:
            print('Problem loading data. File name was: ' + str(filename))
        return
    
if __name__ == '__main__':
    MyInterface_Qt()