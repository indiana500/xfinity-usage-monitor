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
your Xfinity-Usage Monitor
"""
HIGH_LEVEL_EMAIL_START = """Hello,
You current usage level is projected to be abov 90% for the month.

You currently have used.
"""
HIGH_LEVEL_MAIL_END = """ GB

Regards,
your Xfinity-Usage Monitor
"""
