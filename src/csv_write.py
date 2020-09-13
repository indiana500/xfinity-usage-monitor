'''
Created on May 2, 2018

@author: Michael Walden
'''
import csv

class csv_writer(object):
    '''
    csv_writer implements writing procedures for csv files
    
    '''

    def __init__(self, path, headers=None):
        '''
        Constructor for csv_write class
        
        path (string): path and filename
        headers (optional list): header row for csv file
        
        '''
        self.path = path
        with open(self.path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
        
    def append_row(self, rows):
        '''
        used to write out one or more rows of data to the end of the file
        
        row (list): data to be written to file in csv format
        '''
        with open(self.path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
        
    