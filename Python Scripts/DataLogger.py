'''
Created on Mar 4, 2020

@author: Collin Bradford for PERCS
'''

import xlsxwriter
from datetime import datetime

class DataLogger(object):
    
    def __init__(self, fileName="run.xlsx", channelCount=1, headers=['A0']):
        '''
        Constructor
        @param fileName: The name of the file to write to. Make sure this is not a file currently used! 
        @param channelCount: The number of channels that are being recorded from the arduino. 
        @param headers: The header names that the data will be stored in.

        DataLogger automatically adds a time stamp to each sample set. 
        '''
        self.fileName = fileName
        self.channelCount = channelCount
        self.data = []
        headers.append('SampleTime')
        self.headers = headers
    
    def saveEntrySet(self, data):
        '''
        Saves the given sample set to the RAM buffer. 
        IMPORTANT: This does NOT save the file. You must call the writeDataToFile() function to save data! 
        @param data: The data to be saved to the temporary buffer.
        '''
        curTime = datetime.now().strftime('%H:%M:%S')
        data.append(curTime)
        self.data.append(data)
    
    def getNumberSampleSets(self):
        '''
        Returns the size of the internal buffer.
        '''
        return len(self.data)
    
    def writeDataToFile(self, worksheetName='Run Data'):
        '''
        Saves all the data in the current buffer to a file. 
        @param worksheetName: The name of the current worksheet.
        '''
        workbook = xlsxwriter.Workbook(self.fileName)
        worksheet = workbook.add_worksheet(worksheetName)
        row = 0
        col = 0
        worksheet.write_row(row, col, self.headers)
        row += 1
        for i in self.data:
            worksheet.write_row(row, col, i)
            row += 1;
        workbook.close()