'''
Created on Sep 1, 2020

@author: Michael Walden
'''
import os
from xfinity_usage.xfinity_usage import XfinityUsage
from xfinity_account_settings import *
from settings import *
from time import sleep, time
from usage_reading import UsageReading
from event_log import EventLog
from month_usage import MonthUsage


if __name__ == '__main__':
    '''
    initialize
    '''
    curr_data_point = UsageReading()
    curr_month = curr_data_point.get_month()
    
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
            
            # Update the dictionary with this months data (create new month if necessary)
            if curr_data_point.get_month() != curr_month:
                month_data.reinit_dict(curr_data_point.get_list())
                curr_month = curr_data_point.get_month()
            else:
                month_data.update(curr_data_point.get_list())
            
            # Notify user if you are above the alarm limit
            if curr_data_point.get_data_used() >= curr_data_point.get_current_alarm_level():
                print('you may be on the way to exceeding your quota')
            
            # plot the data
            month_data.plot_data()
            
            # set cycle time for next reading
            cycle_time = CYCLE_TIME

            print(month_data.get_dict())

        sleep(cycle_time)



def data_point_to_dict(data_point):
    '''
    converts a data point to a dictionary type
    where the keys are DATA_HEADERS
    '''
    return {DATA_HEADERS[0]: [data_point.get_timestamp()], 
            DATA_HEADERS[1]: [data_point.get_data_used()],
            DATA_HEADERS[2]: [data_point.get_allotment()],
            DATA_HEADERS[3]: [data_point.projected_usage()],
            DATA_HEADERS[4]: [int(data_point.current_percent_of_month() * data_point.get_allotment())],
            DATA_HEADERS[5]: [int(data_point.current_percent_of_month() * data_point.get_allotment() * 0.9)]
            }

        
        