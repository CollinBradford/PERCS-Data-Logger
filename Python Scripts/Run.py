'''
Created on Mar 4, 2020

@author: Collin Bradford for PERCS
'''
import threading

class Run(threading.Thread):
    '''
    This object manages the sample run. When the start() function is called, it continues
    to listen to the arduino for any input and records it to the logging file. 
    To stop the run, call the stop() function. 
    '''


    def __init__(self, arduino, dataLogger):
        '''
        Constructor
        @param arduino: Arduino object that reports data for the run
        @param dataLogger: DataLogger object that will be used to write the data
        '''
        threading.Thread.__init__(self)
        self.arduino = arduino
        self.dataLogger = dataLogger
    
    def run(self):
        '''
        Call the start() function to start this thread instead of run()
        
        This is the main function for the run manager. It simply listens to the Arduino
        and records the incoming info into the data logger spreadsheet. 
        '''
        self.active = True
        while self.active:
            samples = self.arduino.getSampleSet()
            self.dataLogger.saveEntrySet(samples)
        self.dataLogger.writeDataToFile()
        self.numSamples = self.dataLogger.getNumberSampleSets()
        
    
    def stop(self):
        '''
        Stops the run and saves data to the file. 
        @return: Returns the number of samples taken during the run as an int.
        '''
        self.active = False
        self.join();
        return self.numSamples