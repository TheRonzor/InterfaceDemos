##########################################################################
#                                                                        #
#      May you do good and not evil                                      #
#      May you find forgiveness for yourself and forgive others          #
#      May you share freely, never taking more than you give.            #
#                                                                        #
##########################################################################

import os
import pandas as pd
import matplotlib.pyplot as plt

class SimpleScatter:
    '''
    A basic scatter plot, based on a pandas DataFrame
    '''
    __slots__ = ('fig', 
                 'ax', 
                 'scat')
    
    PATH_FIGURES = './figures/'
    
    def __init__(self):
        # Note: Due to an issue with tk,
        #  initializing the fig object to None
        #  and creating it later via self.init_scatter()
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