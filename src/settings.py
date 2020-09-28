'''
Created on May 7, 2018

Constants file

@author: Michael Walden
'''
from constants import SEC_PER_MIN, SEC_PER_DAY, SEC_PER_HOUR
import os

CYCLE_TIME = 2 * SEC_PER_HOUR - 70
RETRY_CYCLE_TIME = 10 * SEC_PER_MIN
NUM_OF_RETRIES = 4

USAGE_ALARM_LEVEL = 0.9  # if this is updated, updated header and key names as well

# DATA_KEYS = ['time', 'usage', 'allotment', 'projected usage', '100% Usage', '90% Usage']
DATA_HEADERS = ['Date and Time', 'Usage Month to Date (GB)', 'Alloted Usage (GB)', 
                'Projected Usage (GB)', '100% Usage (GB)', '90% Usage (GB)']

# Set LOG_REFRESH_TIME to 'year', 'quarter', 'month', 'week', or 'day'
LOG_REFRESH_TIME = 'month'

'''
path for raspbian
'''
# dir_path = os.getcwd()
# DATA_PATH = os.path.dirname(dir_path) + '/data/'
DATA_PATH = '/home/pi/Public/xfinity-monitor/data/'

'''
path for windows
'''
# DATA_PATH = 'C:\\Users\\admin\\python-workspace\\Xfinity_usage\\data\\' 


DEBUG = False
