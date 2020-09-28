'''
Created on May 2, 2018

@author: Michael Walden
'''
import csv


class csv_writer(object):
    '''
    csv_writer implements writing procedures for csv files
    
    '''
    self.file_exists = False
    
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
        
class csv_reader(object):
    '''
    csv_reader implements reading procedures for csv file
    '''
    def __init__(self, path):
        '''
        constructor for csv_reader class
        
        path (string): path and filename
        first line of file contains the key values
        '''
        self.path = path
        out_dict = {}
    
    def get_csv_dict(self):
        '''
        retrieve data in the csv file into a dictionary of lists
        '''
        with open(self.path, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for key in reader.fieldnames:
                out_dict[key] = []
            for row in reader:
                for key in row:
                    if key != 'Date and Time':
                        out_dict[key].append(int(row[key]))
                    else:
                        out_dict[key].append(row[key]) 
        return out_dict

from settings import DATA_PATH
path = DATA_PATH + 'Log_file 2020-09.csv'
data_file = csv_reader(path)
