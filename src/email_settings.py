'''
Created on Jul 15, 2018

@author: Mike & Joan
'''

'''
email information
'''
SEND_EMAIL = True

from email_account_settings import *


STATUS_EMAIL = """Hello,

This is your weekly status email.

Currently, your xfinity account has used {usage} of {allotment} GB for {month} {year}.
This puts you at a {usage_rate}% estimated usage rate.

Regards,
your Xfinity-Usage Monitor
"""

SUMMARY_EMAIL = """Hello,

For the month of {month} {year}, your xfinity account has used {usage} of {allotment} GB.

(note this may be off by what was used in the last few  hours of the month)

Regards,
your Xfinity-Usage Monitor
"""


HIGH_LEVEL_EMAIL = """Hello,
You current usage level is projected to be above 90% for the month.

You currently have used {usage} GB.  Based on the remaining time in the month, your total data
usage is projected to be {percentage}% of your allotment.

Regards,
your Xfinity-Usage Monitor
"""
