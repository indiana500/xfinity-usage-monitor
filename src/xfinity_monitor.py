'''
Created on Sep 1, 2020

@author: Michael Walden

Python program to grab xfinity internet usage data, add to a log file for 
the month, and plot

This program grabs one data point and if an issue exists with a data point, 
will retry at a ten minute rate for up to 4 additiona retries

The program will create a plot of the month's data, and notify the user if
usage is projected to be above 90% for the month.  Usage is projected throughout
the month based on where in the month the data point is taken

Additionally, an email is sent out with the first data point on Sunday morning
to notify the user of the current status

The expectation is to execute this program at an appropriate rate, 2 hours
suggested, via a cron job

'''
import os
from time import sleep
from datetime import datetime
from xfinity_usage.xfinity_usage import XfinityUsage
from xfinity_account_settings import *
from settings import *
from usage_reading import UsageReading
from event_log import EventLog
from month_usage import MonthUsage
from email_status import *


if __name__ == '__main__':
    '''
    initialize
    '''
    os.chdir(DATA_PATH)
    
    curr_data_point = UsageReading()
    curr_weekday = curr_data_point.get_weekday()
    
    log_it = EventLog(DATA_PATH, DATA_HEADERS)
    
    # if current month log file already exists, grab the data.  Otherwise, 
    # initialize and write start of month data
    if log_it.get_file_exists():
        month_data = MonthUsage(log_it.read_logfile_dict())
        print('log file exists')
    else:
        month_data = MonthUsage()
        month_data.init_dict(curr_data_point.get_list())
        log_it.log_data(curr_data_point.get_list())
    print(month_data.get_dict())
        
    rec_data = None
    x_scrape = XfinityUsage(USERNAME, XPASSWORD, browser_name='firefox-headless', debug=False)
    retries = 0

    while retries <= NUM_OF_RETRIES:
        try:
            rec_data = x_scrape.run()
        except Exception as e:
            print(e)
            retries += 1
            print('retries: ', retries)
            cycle_time = RETRY_CYCLE_TIME
            sleep(cycle_time)
        else:
            retries = 100
            # data value was obtained.  Update current data point with new data
            curr_data_point.update(rec_data['data_timestamp'], rec_data['used'], rec_data['total'] )
            print(curr_data_point) 
             
            # log the data
            log_it.log_data(curr_data_point.get_list())
             
            # email status on Sunday Morning (weekday = 6)
            if datetime.fromtimestamp(month_data.get_dict()['Date and Time'][-1]).weekday() != curr_data_point.get_weekday():
                print('emailing Sunday status')
                print(datetime.fromtimestamp(month_data.get_dict()['Date and Time'][-1]).weekday())
                if curr_data_point.get_weekday() == 6: 
                    email_status(curr_data_point.get_data_used(),
                                 curr_data_point.get_allotment(),
                                 int(100 * curr_data_point.projected_usage() / curr_data_point.get_allotment()),
                                 curr_data_point.current_date())
             
            # Update the dictionary with this months data (create new month and email summary if necessary)
            month_data.update(curr_data_point.get_list())
             
            # Notify user if you are above the alarm limit
            if curr_data_point.get_data_used() >= curr_data_point.get_current_alarm_level():
                email_high_level(curr_data_point.get_data_used(), 
                                 int(100 * curr_data_point.projected_usage() / curr_data_point.get_allotment()))
             
            # plot the data
            month_data.plot_data()
 
        

        