'''
Created on Jul 15, 2018

@author: Mike & Joan
'''
'''
email information
'''
SEND_EMAIL = True

from email_account_settings import *


STATUS_EMAIL_START = """Hello,
This is the total number of activations this week (SUN to SAT):
"""
STATUS_MAIL_END = """

Regards,
your Sump Pump Monitor
"""
HIGH_LEVEL_EMAIL_START = """Hello,
The water level in the sump pit may have reached a high level
without pump activation.

Please check the sump pump at your earliest convenience.

High level has been active for
"""
HIGH_LEVEL_MAIL_END = """ seconds

Regards,
your Sump Pump Monitor
"""
