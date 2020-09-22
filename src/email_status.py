'''
Created on Jul 1, 2018

@author: Michael Walden
'''
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from settings import DEBUG
from email_settings import *
from datetime import date

def send_email(msg_from, msg_to, msg_subject, msg_body):

    msg = EmailMessage()
    msg['Subject'] = msg_subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    msg_body = msg_body
    msg.set_content(msg_body)
    
    s = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
    if DEBUG:
        s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.login(Address(username=FROM_ADDR['username'], domain=FROM_ADDR['domain']), PWD)
    s.send_message(msg)

def email_status(usage, allotment, status_date):
    '''
    Send Email with current status
    
    inputs: usage: int
            allotment: int
            status_date: datetime.date
    '''
    msg_from = Address(display_name='Raspberry Pi 1', 
                       username=FROM_ADDR['username'], 
                       domain=FROM_ADDR['domain'])
    msg_to = Address(username=STATUS_TO_ADDR['username'], 
                     domain=STATUS_TO_ADDR['domain'])
    msg_body = STATUS_EMAIL.format(usage=usage, 
                                   allotment=allotment, 
                                   month=status_date.strftime("%B"), 
                                   year=status_date.strftime("%Y"))
    msg_subject = 'Xfinitiy usage status email'
    if SEND_EMAIL:
        send_email(msg_from, msg_to, msg_subject, msg_body)
    
def email_summary(usage, allotment, status_date):
    '''
    Send Email with current status
    
    inputs: usage: int
            allotment: int
            status_date: datetime.date
    '''
    msg_from = Address(display_name='Raspberry Pi 1', 
                       username=FROM_ADDR['username'], 
                       domain=FROM_ADDR['domain'])
    msg_to = Address(username=STATUS_TO_ADDR['username'], 
                     domain=STATUS_TO_ADDR['domain'])
    msg_body = SUMMARY_EMAIL.format(usage=usage, 
                                    allotment=allotment, 
                                    month=status_date.strftime("%B"), 
                                    year=status_date.strftime("%Y"))
    msg_subject = 'Xfinitiy usage summary email {month} {year}'.format(month=status_date.strftime("%B"), 
                                                                       year=status_date.strftime("%Y"))
    if SEND_EMAIL:
        send_email(msg_from, msg_to, msg_subject, msg_body)
    
def email_high_level(usage, projection):
    '''
    Send email to indicate usage is high

    inputs: usage: int
            allotment: int
            status_date: datetime.date
    '''
    msg_from = Address(display_name='Raspberry Pi 1', 
                       username=FROM_ADDR['username'], 
                       domain=FROM_ADDR['domain'])
    msg_to = Address(username=STATUS_TO_ADDR['username'], 
                     domain=STATUS_TO_ADDR['domain'])
    msg_body = HIGH_LEVEL_EMAIL.format(usage=usage, 
                                       percentage=projection)
    msg_subject = 'Xfinitiy usage high level email'
    if SEND_EMAIL:
        send_email(msg_from, msg_to, msg_subject, msg_body)

if __name__ == '__main__':
    msg_from = Address(display_name='Raspberry Pi 1', 
                       username=FROM_ADDR['username'], 
                       domain=FROM_ADDR['domain'])
    msg_to = Address(username=STATUS_TO_ADDR['username'], 
                     domain=STATUS_TO_ADDR['domain'])
    msg_body = TEST_EMAIL.format(a=10, b=20)
    msg_subject = 'Test'
    print(msg_body)
    if SEND_EMAIL:
        send_email(msg_from, msg_to, msg_subject, msg_body)
   