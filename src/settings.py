'''
Created on May 7, 2018

Constants file

@author: Michael Walden
'''
from constants import SEC_PER_MIN, SEC_PER_DAY, SEC_PER_HOUR
import os

CYCLE_TIME = 2 * SEC_PER_HOUR - 70
RETRY_CYCLE_TIME = 10 * SEC_PER_MIN
NUM_OF_RETRIES = 3

# Set LOG_REFRESH_TIME to 'Year', 'Quarter', 'Month', 'Week', or 'Day'
LOG_REFRESH_TIME = 'Quarter'

'''
path for raspbian
'''
dir_path = os.getcwd()
DATA_PATH = os.path.dirname(dir_path) + '/data/'

'''
path for windows
'''
# DATA_PATH = 'C:\\Users\\admin\\python-workspace\\Xfinity_usage\\data\\' 


DEBUG = True
