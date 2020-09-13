'''
Created on Jul 1, 2018

@author: Michael Walden
'''
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from settings import DEBUG
from email_settings import *

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

def email_status(num_activations):
    '''
    Send Email with number of activations
    '''
    msg_from = Address(display_name='Raspberry Pi 3', username=FROM_ADDR['username'], domain=FROM_ADDR['domain'])
    msg_to = Address(username=STATUS_TO_ADDR['username'], domain=STATUS_TO_ADDR['domain'])
    msg_body = STATUS_EMAIL_START + str(num_activations) + STATUS_MAIL_END
    msg_subject = 'Sump Pump Activation Weekly Summary'
    if SEND_EMAIL:
        send_email(msg_from, msg_to, msg_subject, msg_body)
    
def email_high_level(ctr):
    '''
    Send email to indicate water level is high, which
    might indicate pump is not activating
    '''
    msg_from = Address(display_name='Raspberry Pi 3', username=FROM_ADDR['username'], domain=FROM_ADDR['domain'])
    msg_to = Address(username=STATUS_TO_ADDR['username'], domain=STATUS_TO_ADDR['domain'])
    msg_body = HIGH_LEVEL_EMAIL_START + str(ctr) + HIGH_LEVEL_MAIL_END
    msg_subject = 'SUMP WATER LEVEL HIGH'
    if SEND_EMAIL:
        send_email(msg_from, msg_to, msg_subject, msg_body)
    