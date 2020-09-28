'''
Created on Apr 30, 2018

@author: Michael Walden
'''

from calendar import monthlen
from datetime import datetime
from time import *
# from csv_write import csv_writer, csv_reader
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
        self.filename = self.data_path + 'Log_file ' + strftime('%Y-%m') + '.csv'
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
        write to log file.  Writes a formatted time, and then data
        
        if the time to refresh the file has been reached, a new file is started and initialized
        
        input: curr_reading, a list of the data with the first value of type epoch time.
        '''
 
         # First check to see if a new log file needs to be started
#         if self.log_refresh_time == "year":
#             if localtime(self.log_start_time).tm_year != localtime(time()).tm_year:
#                 self.init_logfile()
#         if self.log_refresh_time == "quarter":
#             if localtime(self.log_start_time).tm_mon != localtime(time()).tm_mon:
#                 if (localtime(time()).tm_mon % 3) == 1:
#                     self.init_logfile()
#         if self.log_refresh_time == "month":
#             if localtime(self.log_start_time).tm_mon != localtime(time()).tm_mon:
#                 self.init_logfile()
#         if self.log_refresh_time == "week":
#             if localtime(self.log_start_time).tm_mday != localtime(time()).tm_mday:
#                 if localtime(time()).tm_wday == 0:
#                     self.init_logfile()
#         if self.log_refresh_time == "day":
#             if localtime(self.log_start_time).tm_mday != localtime(time()).tm_mday:
#                 self.init_logfile()
#         if self.log_refresh_time == "hour":
#             if localtime(self.log_start_time).tm_hour != localtime(time()).tm_hour:
#                 self.init_logfile()
#         if self.log_refresh_time == "minute":
#             if localtime(self.log_start_time).tm_min != localtime(time()).tm_min:
#                 self.init_logfile()
        
        # Update the log file with latest datapoint after adjusting time value to a string
#         outdata = curr_reading.copy()
#         outdata[0] = self.print_time(curr_reading[0])
        with open(self.filename, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(curr_reading)

#         self.data_file.append_row([outdata])

