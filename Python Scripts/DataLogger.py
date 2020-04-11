'''
Created on Mar 4, 2020

@author: Collin Bradford for PERCS
'''

import xlsxwriter

class DataLogger(object):
    
    def __init__(self, fileName, channelCount, headers):
        self.fileName = fileName
        self.channelCount = channelCount
        self.data = []
        self.headers = headers
    
    def saveEntrySet(self, data):
        self.data.append(data)
    
    def getNumberSampleSets(self):
        return len(self.data)
    
    def writeDataToFile(self, worksheetName='Run Data'):
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