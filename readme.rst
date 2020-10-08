xfinity-monitor
=============


Python script designed for raspberry pi to get Xfinity bandwidth usage from Xfinity MyAccount website. 
This uses the `python API <https://github.com/jantman/xfinity-usage/>`_ originally created 
by @jantman to access the xfinity website and pull down the data used, month to date. 
xfinity-monitor stores this data in a file and generates a graph showing current usage along with a 
100% usage line, and an alarm line set at 90% of the monthly allotment.  In addition, the program 
will send out a weekly status email, and also an email should the alarm line ever be crossed.


Requirements
------------

-  Python (tested with 3.7)
-  matplotlib
-  smtplib
-  firefox
-  `xfinity-usage <https://github.com/jantman/xfinity-usage/>`_  Python package
-  `selenium <http://selenium-python.readthedocs.io/>`_  
-  `geckodriver <https://github.com/mozilla/geckodriver/>`_  download from `here <https://github.com/mozilla/geckodriver/releases/>`_

   -  Based on testing done after xfinity website changes, geckodriver (firefox) seemed to be the optimum browser to use to access the xfinity website
   -  I used v0.23.0, the last one released as a compiled version for the raspberry pi
  

Usage
-----

Install xfinity-usage from github website.  Note - as of now, using pip to 
download and install xfinity-usage pulls an older version of the file, which
does not currently work with the xfinity website.  So, either make sure to grab the
github version up make the updates to the downloaded package.

Edit the email_account_settings.py and xfinity_account_settings.py files 
with you usernames and passwords.  Edit the settings.py file with a 
pointer to the directory to store your data files and graph. 

I set up a cron job to execute a shell script file to run the python program every x
hours.  Selenium had some issues running from a cron job so in the end, this seemed
the best way to execute it.  Geckodriver also does not fully suppress all output
and it also needed some coaxing to get to run this way.  My crontab commands are
included in the cron_list file.  I included a command in the cron table to copy
the updated usage figure to a directory where it can be accessed via a webpage from
elsewhere in my network.

Note, as stated elsewhere, this screen-scrapes the xfinity site; it's likely to break with a
redesign.



Note About Reliability
----------------------

In short: xfinity's site isn't terribly reliable. I have been running this
script every other hour via cron, so 12 times a day, every day. The script
has a retry scheme, but still may fail for various failures, mostly on 
the part of xfinity - elements missing
from the page, connection resets, blank pages, server-side error
messages, etc. Keep that in mind. If the site isn't available, you just don't
have that data point, and it will pick it up at the next time.

Rationale
---------

Xfinity began implementing a data cap last year, and a month ago I was 
near going over.  I wasn't notified until most of the way through the month
when I reached 90% of total monthly allotment, with more than 10% of the 
month remaining.  I started to use a raspberry pi to scape the website for 
usage data when I found @jantman's xfinity-usage project.  I wanted to 
have a pi monitor the usage and notify me via email if I ever reached a 
trajectory that suggests that I would be above 90% at the end of the month.
The figure that is plotted allows me to check the status at any time, and 
get an idea of when the data is being used.  


Disclaimer
----------

I have no idea what Xfinity's terms of use for their account management website
are, or if they claim to have an issue with automating access. They modified access
methods in July of 2020 that then required some changes to xfinity-usage.  It could
change again. So... use this at your own risk.

License
-------

This package is licensed under the `GNU AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`_.


