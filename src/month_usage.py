'''
Created on Sep 2, 2020

@author: Michael Walden
'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from settings import *
from datetime import datetime


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
        '''
        create and save a png of the plot of data use and allotment for the current month
        '''
        # initialization
        plot_x_series = [datetime.fromtimestamp(x) for x in self.usage_data['time']]
        print(plot_x_series)
        days = mdates.DayLocator(interval=1)
        day_fmt = mdates.DateFormatter('%D')
        
        # create figure from data
        fig, ax = plt.subplots(figsize=(12,8), tight_layout=True)
        ax.plot(plot_x_series, self.usage_data['usage'], '-b2', label='Actual Usage')
        ax.plot(plot_x_series, self.usage_data['100% Usage'], '-', color='gray', linewidth=5, label='100% Allocation Line')
        ax.plot(plot_x_series, self.usage_data['90% Usage'], ':', color='gray', linewidth=0.75, label='Alarm Line')
        fig.autofmt_xdate()
        
        # annotate
        ax.set_title("Xfinity Usage for Current Month")
        ax.legend()
        ax.xaxis.set_major_locator(days)
        ax.xaxis.set_major_formatter(day_fmt)
        ax.xaxis.set_label_text('Time')
        ax.yaxis.set_label_text('Usage, GB')
        
        # add usage information text
        current_percent_string = ('Currently running at: ' + 
                                  '{:.1f}'.format(100 * self.usage_data['usage'][-1] / self.usage_data['100% Usage'][-1]) 
                                  + '%')
        usage_string = ('Current Estimated Monthly Usage: ' + 
                        str(self.usage_data['projected usage'][-1]) + 
                        ' GB of ' + str(self.usage_data['allotment'][-1]) + ' GB allowed') 
        if self.usage_data['projected usage'][-1] >= self.usage_data['allotment'][-1]:
            font_color = "red"
        else:
            font_color = 'black'
        plt.figtext(0.97,0.15, current_percent_string, horizontalalignment='right', fontweight='bold', color=font_color, fontsize='large')
        plt.figtext(0.97,0.12, usage_string, horizontalalignment='right', fontweight='bold', color=font_color, fontsize='large')
        
        # show or save the plot depending which line is commented out
#         plt.show()
        plt.savefig(DATA_PATH + 'curr_month_plot.png')

        return
    
        