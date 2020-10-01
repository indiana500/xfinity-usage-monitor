'''
Created on Apr 30, 2018

@author: Michael Walden
'''

from calendar import monthlen
from datetime import datetime
from time import *
import csv

class EventLog(object):
    '''
    Class to control logging of data to files
    
    inputs: data_path is file path to store the log file
            headers is a list ctaining the text headers
            log_refresh_time is the frequency to start a new log file
            when updating the log file with a fresh data point, a list is provided.  The initial
            list parameter is assumed to be an epoch time stamp, which is converted to a date/time value
            If the file already exists, then the data can be read.  Check file_already_exists()
    '''
    
    def __init__(self, data_path, headers):
        '''
        Create an event log or find the current one
        
        '''
        self.log_start_time = 0
        self.data_path = data_path
        self.headers = headers
        self.filename = self.data_path + 'Log_file_' + strftime('%Y-%m') + '.csv'
        self.file_dict = {}
        self.file_already_exists = False
        
        try: # if file already exists then read data in
            with open(self.filename, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for key in reader.fieldnames:
                    self.file_dict[key] = []
                for row in reader:
                    for key in row:
                        self.file_dict[key].append(int(row[key]))
            self.file_already_exists = True
        except Exception:
            print(self.filename, 'file will be created')
            self.init_logfile()
    
    def init_logfile(self):
        '''
        open and initialize a logfile
        '''
        
        with open(self.filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.headers)
        self.log_start_time = time()
    
    def get_file_exists(self):
        '''
        get boolean indicated the file was found
        '''
        return self.file_already_exists
    
    def read_logfile_dict(self):
        
        return self.file_dict
        
    def print_time(self, in_time):
        '''
        Change time from epoch to print format
        '''
        return datetime.fromtimestamp(int(in_time))
    
    
    def log_data(self, curr_reading):
        '''
        write to log file.  Writes a time, and then data
        
        input: curr_reading, a list of the data with the first value of type epoch time.
        '''
        with open(self.filename, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(curr_reading)
