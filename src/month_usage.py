'''
Created on Sep 2, 2020

@author: Michael Walden
'''

from settings import *


class MonthUsage(object):
    '''
    keeps a dictionary of data for the month
    '''
    
    def __init__(self, in_data):
        self.init_dict(in_data)
    
    def init_dict(self, in_data):
        '''
        initialize dictionary from list values
        '''
        self.usage_data = dict(zip(DATA_KEYS, [list(x) for x in zip(in_data)]))
        return
    
    def reinit_dict(self, in_data):
        '''
        re-initializes the dictionary, dropping the old data
        '''
        self.init_dict(in_data)
        return
        
    def update(self, in_data):
        '''
        update dictionary with a new data point
        '''
        for key, x in zip(self.usage_data.keys(), in_data):
            self.usage_data[key].append(x)
        return
    
    def get_dict(self):
        return self.usage_data
    
    def plot_data(self):
        return
    
        