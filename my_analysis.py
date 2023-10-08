##########################################################################
#                                                                        #
#      May you do good and not evil                                      #
#      May you find forgiveness for yourself and forgive others          #
#      May you share freely, never taking more than you give.            #
#                                                                        #
##########################################################################

import os
import numpy as np
import pandas as pd
from datetime import datetime as dt

class RandomDataAnalysis:
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
                         num_points:int = 10
                         ):
        '''
        Generate some random data
        '''
        data = np.random.normal(size=(num_points,2))
        data[:,1] = data[:,0] + 0.5*data[:,1]
        self.data = pd.DataFrame(data, 
                                 columns=['x','y'])
        return