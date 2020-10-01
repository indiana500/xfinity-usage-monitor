'''
Created on Oct 1, 2020

@author: Michael Walden

Python program to grab read in previously recorded xfinity internet usage 
data, and create a plot.

This program would normally be used to create a plot of a previous month's
data.  

'''
import sys
import os
from datetime import datetime, timedelta
from settings import *
from event_log import EventLog
from month_usage import MonthUsage

def print_help():
    print('format: python3 xfinitiy_plot.py [YYYY-MM]')
    print('')
    print('Program looks in data directory for Log_file_YYYY-MM.csv to create a plot named YYYY-MM.png')
    print('If YYYY-MM is omitted, the program will automatically use last month.')
    print('python3 xfinity_plot.py help to get this help file')
    quit()

def cleanup_end_of_month(month_data):
    '''
    remove 0 GB data points from end of month data to account for exfinity ending month early.
    only allow up to half of the data or 10 points to be removed in case it's all 0's
    '''
    len_of_data = len(month_data.get_time_list())
    lines_removed = 0
    while month_data.get_usage_list()[-1] == 0:
        lines_removed += 1
        month_data.remove_last_data_point()
        if lines_removed >= (len_of_data/2):
            break
    return

if __name__ == '__main__':
    '''
    initialize
    '''
    args = sys.argv[1:]

    if args==[]:
        plot_month = datetime.today() - timedelta(days=datetime.today().day)
        month_string =plot_month.strftime('%Y-%m')
    elif args[0] == 'help':
        print_help()
    else:
        month_string = args[0]
    
    try:
        log_it = EventLog(DATA_PATH, DATA_HEADERS, filedate=month_string, init=False)
    except Exception as e:
        print('Exception: ', e)
        print_help()

    if log_it.get_file_exists():
        month_data = MonthUsage(log_it.read_logfile_dict())
        cleanup_end_of_month(month_data)
        month_data.plot_data(plot_name=month_string)
    else:
        print('Data File does not exist')
