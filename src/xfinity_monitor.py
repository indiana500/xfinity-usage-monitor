'''
Created on Sep 1, 2020

@author: Mike & Joan
'''
import os
from xfinity_usage.xfinity_usage import XfinityUsage
from xfinity_account_settings import *
from settings import *
from time import sleep, time
from usage_reading import UsageReading
from sample_data import *
from event_log import EventLog

if __name__ == '__main__':
    '''
    initialize
    '''
    prev_data_point = UsageReading()
    curr_data_point = UsageReading()
    log_it = EventLog()
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
            if retries >= NUM_OF_RETRIES:
                assert "Number of retries exceeded ({})".format(NUM_OF_RETRIES)
            cycle_time = RETRY_CYCLE_TIME
        else: 
            retries = 0       
            prev_data_point.update(new_reading = curr_data_point)
            curr_data_point.update(rec_data['data_timestamp'], rec_data['used'], rec_data['total'] )
            print(prev_data_point)
            print(curr_data_point)
            log_it.log_usage(curr_data_point, prev_data_point, send_email = False)
            cycle_time = CYCLE_TIME

        sleep(cycle_time)
        
        