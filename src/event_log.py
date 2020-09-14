'''
Created on Apr 30, 2018

@author: Michael Walden
'''
# from time import ctime, strftime, localtime, time
from usage_reading import UsageReading
from settings import *
from calendar import monthrange
from datetime import date
from time import *

from email_settings import SEND_EMAIL
from csv_write import csv_writer

if SEND_EMAIL:
    import smtplib
    from email.mime import multipart, text

class EventLog(object):
    '''
    event tracks on cycle to determine the total on time
    '''
    
    def __init__(self):
        ''' 
        Create an event with by providing a start time 
        
        state: RUNNING or IDLE
        '''
        self.log_start_time = 0
        self.init_logfile()
     
        
    def init_logfile(self):
        '''
        open and initialize a logfile
        '''
        headers = ['Date and Time', 'Usage Month to Date (GB)', 'Alloted Usage (GB)', 'Projected (last reading)', 'Projected (month to date)']
        filename = DATA_PATH + 'Log_file ' + strftime('%Y-%m-%d %H-%M',localtime(time())) + '.csv'
        self.data_file = csv_writer(filename, headers)
        self.log_start_time = time()
        if DEBUG:
            print('log file initialized', localtime(self.log_start_time))
        
        
    def print_time(self, in_time):
        '''
        Change time from epoch to print format
        '''
        return strftime('%m/%d/%Y %H:%M:%S', localtime(in_time))
    
    
    def log_usage(self, curr_reading, prev_reading, send_email = False):
        '''
        write to log file.  Writes start_time, usage information
        '''
        def projected_usage_month ():
            '''
            Uses rate from beginning of month to report projected usage for the month
    
                usage * (days in month * seconds per day)
            =  ------------------------------------------
                seconds from start of month until now
    
            Returns: in indicated GB projected to be used for the month
              
            '''
            days_in_month = monthrange(curr_reading.get_year(), curr_reading.get_month())[1]
        
            return int(curr_reading.get_data_used() * days_in_month * SEC_PER_DAY / 
                    (curr_reading.get_timestamp() - curr_reading.start_of_month_timestamp()) )
        
        def projected_usage_last_reading():
            '''
            Uses rate from last reading to report projected usage for the month
    
                                  usage since last reading * (seconds remaining in the current month)
            =  current usage +  ---------------------------------------------------------------------
                                  seconds since the last reading
    
            Returns: in indicated GB projected to be used for the month
    
            '''
            if curr_reading.get_timestamp() == prev_reading.get_timestamp():
                return 0
            else:
                usage_rate = ((curr_reading.get_data_used() - prev_reading.get_data_used()) / 
                              (curr_reading.get_timestamp() - prev_reading.get_timestamp()))
                return int(curr_reading.get_data_used() + 
                           usage_rate * (curr_reading.end_of_month_timestamp() - curr_reading.get_timestamp()))
 
         # First check to see if a new log file needs to be started
        if LOG_REFRESH_TIME == "Year":
            if localtime(self.log_start_time).tm_year != localtime(time()).tm_year:
                self.init_logfile()
        if LOG_REFRESH_TIME == "Quarter":
            if localtime(self.log_start_time).tm_mon != localtime(time()).tm_mon:
                if (localtime(time()).tm_mon % 3) == 1:
                    self.init_logfile()
        if LOG_REFRESH_TIME == "Month":
            if localtime(self.log_start_time).tm_mon != localtime(time()).tm_mon:
                self.init_logfile()
        if LOG_REFRESH_TIME == "Week":
            if localtime(self.log_start_time).tm_mday != localtime(time()).tm_mday:
                if localtime(time()).tm_wday == 0:
                    self.init_logfile()
        if LOG_REFRESH_TIME == "Day":
            if localtime(self.log_start_time).tm_mday != localtime(time()).tm_mday:
                self.init_logfile()
        if LOG_REFRESH_TIME == "Hour":
            if localtime(self.log_start_time).tm_hour != localtime(time()).tm_hour:
                self.init_logfile()
        if LOG_REFRESH_TIME == "Minute":
            if localtime(self.log_start_time).tm_min != localtime(time()).tm_min:
                self.init_logfile()
        
        #Update the log file with latest datapoint
        self.data_file.append_row([[self.print_time(curr_reading.get_timestamp()), 
                                    str(curr_reading.get_data_used()), str(curr_reading.get_allotment()),
                                    str(projected_usage_last_reading()), projected_usage_month()]])
        if DEBUG:
            print('log updated')
    
    
# in_key = None
# event1 = EventLog(IDLE)
# print('filename: ', event1.data_file.path)
# while in_key != 'q':
#     in_key = input('press enter when sump sump_monitor turns on')
#     event1.update_state(RUNNING)
#     print('sump is ', event1.curr_state)
#     input('press enter when sump sump_monitor turns off')
#     event1.update_state(IDLE)
#     print('sump is ', event1.curr_state)
#     print('total run time was:', event1.run_time(), 'sec')
#     print('total run time was:', event1.stop_time - event1.start_time, 'sec')
#    
