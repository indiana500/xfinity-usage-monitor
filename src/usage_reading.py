'''
Created on Sep 2, 2020

@author: Michael Walden
'''

from time import localtime, time, mktime
from datetime import date
from calendar import monthlen
from constants import SEC_PER_DAY
from settings import DATA_HEADERS, USAGE_ALARM_LEVEL

class UsageReading(object):
    '''
    classdocs
    '''

    def __init__(self, time_in = None, data_in = None, allotment_in = None):
        '''
        Constructor
        '''
        if time_in is None:
            self.timestamp = int(time())
            self.timestamp = int(self.start_of_month_timestamp())
        else:
            self.timestamp = time_in
        if data_in is None:
            self.data_used = 0
        else:
            self.data_used = int(data_in)
        if allotment_in is None:
            self.allotment = 0
        else:
            self.allotment = int(allotment_in)
    
    def get_struct_time (self):
        '''
        Return structured time value
        '''
        return localtime(self.timestamp)
    
    def update(self, timestamp = None, data_used = None, allotment = None, new_reading = None):
        '''
        Update method to update usage_reading
    
        Input: either individual values for usage_reading or another usage_reading
    
        Results: updates values 
        '''
        if new_reading is None:
            self.timestamp = int(timestamp)
            self.data_used = int(data_used)
            self.allotment = int(allotment)
        elif isinstance(new_reading, UsageReading):
            self.timestamp = int(new_reading.get_timestamp())
            self.data_used = int(new_reading.get_data_used())
            self.allotment = int(new_reading.get_allotment())
        
        
    def get_day(self):
        return date.fromtimestamp(self.timestamp).day
    
    def get_weekday(self):
        return date.fromtimestamp(self.timestamp).weekday()
    
    def get_month(self):
        return date.fromtimestamp(self.timestamp).month
    
    def get_year(self):
        return date.fromtimestamp(self.timestamp).year
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_data_used(self):
        return self.data_used
    
    def get_allotment(self):
        return self.allotment
    
    def start_of_month_timestamp(self):
        '''
        Return epoch time for first day of month for timestamp
        '''
        start_of_month = date.fromtimestamp(self.timestamp).replace(day=1)
        return mktime(start_of_month.timetuple())
    
    def current_date(self):
        '''
        return current date, without time, in date format
        (year, month, date)
        '''
        return date.fromtimestamp(self.timestamp)
    
    def days_in_month(self):
        '''
        return number of days in the current month
        '''
        return monthlen(self.get_year(), self.get_month())
    
    def end_of_month_timestamp(self):
        '''
        Return epoch time for end of last day of month for timestamp
        '''
        end_of_month_date = self.current_date().replace(day=self.days_in_month())
        return mktime(end_of_month_date.timetuple()) + SEC_PER_DAY
    
    def current_percent_of_month(self):
        '''
        Return percentage of month that has been completed, between 0 and 1
        '''
        return ((self.timestamp - self.start_of_month_timestamp()) /
                (self.end_of_month_timestamp() - self.start_of_month_timestamp()))
    
    def get_current_allotment(self):
        '''
        Return usage allotment based on how far we are through the month
        '''
        return int(self.allotment * self.current_percent_of_month())
    
    def get_current_alarm_level(self):
        '''
        Return alarm level based on how far we are through the month
        '''
        return int(self.current_percent_of_month() * self.allotment * USAGE_ALARM_LEVEL)
    
    def projected_usage(self):
        '''
        Uses rate from beginning of month to report projected usage for the month
 
            usage * (days in month * seconds per day)
        =  ------------------------------------------
            seconds from start of month until now
 
        Returns: in indicated GB projected to be used for the month
           
        '''
        if self.timestamp == self.start_of_month_timestamp():
            return 0
        else:
            return int(self.data_used * self.days_in_month() * SEC_PER_DAY / 
                    (self.timestamp - self.start_of_month_timestamp()) )
             
    def get_list(self):
        '''
        returns a list of the values to store in a log
        '''
        return [self.timestamp, 
                self.data_used, 
                self.allotment,
                self.projected_usage(),
                self.get_current_allotment(),
                self.get_current_alarm_level()]
        
    def __str__(self):
        return 'Time: {0}\nData Used: {1:0.2f} GB\nAlloted: {2:0.1f} GB'.format(self.get_struct_time(), self.get_data_used(), self.get_allotment())
    