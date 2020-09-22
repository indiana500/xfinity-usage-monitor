'''
Created on Sep 1, 2020

@author: Michael Walden
'''
import os
from time import sleep
from datetime import date
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
    curr_data_point = UsageReading()
    curr_month = curr_data_point.get_month()
    curr_weekday = curr_data_point.get_weekday()
    
    log_it = EventLog(DATA_PATH, DATA_HEADERS, 'month')
    log_it.log_data(curr_data_point.get_list())
    print(curr_data_point.get_list())
    
    month_data = MonthUsage(curr_data_point.get_list())
    print(month_data.get_dict())
    
    rec_data = None
    x_scrape = XfinityUsage(USERNAME, XPASSWORD, browser_name='firefox-headless', debug=False)
    retries = 0
    print('finished setup')

    while True:
        try:
            rec_data = x_scrape.run()
        except Exception:
            print(Exception)
            retries += 1
            print('retries: ', retries)
            if retries >= NUM_OF_RETRIES:
                assert "Number of retries exceeded ({})".format(NUM_OF_RETRIES)
            cycle_time = RETRY_CYCLE_TIME
        else: 
            # data value was obtained.  Update current data point with new data
            retries = 0       
            curr_data_point.update(rec_data['data_timestamp'], rec_data['used'], rec_data['total'] )
            print(curr_data_point)
            
            # log the data
            log_it.log_data(curr_data_point.get_list())
            
            # email status on Sunday Morning (weekday = 6)
            if curr_weekday == curr_data_point.get_weekday(): # change to !=
                if curr_data_point.get_weekday() != 6: # change to ==
                    email_status(curr_data_point.get_data_used(),
                                 curr_data_point.get_allotment(),
                                 curr_data_point.current_date())
                    curr_weekday = curr_data_point.get_weekday()
            
            # Update the dictionary with this months data (create new month and email summary if necessary)
            if curr_data_point.get_month() == curr_month: # change to !=
                email_summary(month_data.get_usage_list()[-1], 
                             month_data.get_allotment_list()[-1], 
                             date.fromtimestamp(month_data.get_time_list()[-1]))
#                 month_data.reinit_dict(curr_data_point.get_list()) # uncomment
                month_data.update(curr_data_point.get_list()) # delete this line
                curr_month = curr_data_point.get_month()
            else:
                month_data.update(curr_data_point.get_list())
            
            # Notify user if you are above the alarm limit
            if curr_data_point.get_data_used() >= curr_data_point.get_current_alarm_level(): # change settings back to 0.9
                print('you may be on the way to exceeding your quota')
                email_high_level(curr_data_point.get_data_used(), 
                             int(100 * curr_data_point.projected_usage() / curr_data_point.get_allotment()))
            
            # plot the data
            month_data.plot_data()
            
            # set cycle time for next reading
            cycle_time = CYCLE_TIME

            print(month_data.get_dict())

        sleep(cycle_time)

        