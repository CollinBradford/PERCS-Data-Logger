'''
Created on Mar 4, 2020

@author: Collin Bradford for PERCS
'''

import serial

class Arduino(object):
    
    #Command codes that control the Arduino
    SET_SAMPLE_SIZE = 1
    SET_SAMPLE_FREQUENCY = 2
    SET_SAMPLE_AVERAGE = 3
    SET_REPORT_FREQUENCY =  4
    SET_SAMPLE_ENABLE = 5
    
    NUMBER_SAMPLE_CHANELS = 6 #Maximum number of sample channels supported by device
    MAX_BUFFER_SIZE = 100 #Maximum buffer size supported by device
    
    def __init__(self, port, baudRate):
        '''
        Constructor
        @param port: String representation of the port
        @param baudRate: Integer representation of the baud rate (9600 or 115200 is common). Must match baud rate set on board.
        '''
        self.port = port
        self.baudRate = baudRate
        self.deviceID = -1
        self.channelCount = 1
        self.sampleAverageSize = 10
        self.deviceReportFrequency = 1000
        self.sampleFrequency = 100
        self.sampleEnabled = 0
        self.initiateConnection()
    
    def initiateConnection(self):
        '''
        Initiates the connection to the board. Called by the constructor. 
        '''
        self.serialConnection = serial.Serial(self.port, self.baudRate)
        deviceStatus = self.readLine()
        self.deviceID = int(deviceStatus[len(deviceStatus) - 1]) #Only works for single-digit board ID's. 
        
    def readLine(self):
        '''
        Reads one line of data from the board, decodes it, and removes any newline characters.
        @return: The values returned from the board.
        '''
        inputData = self.serialConnection.readline()
        inputData = inputData.decode('utf-8')
        inputData = inputData[:len(inputData) - 2] #Remove the two newline characters
        return inputData
    
    def flushInput(self):
        '''
        Flush the input buffer.
        '''
        self.serialConnection.flushInput()
    
    def printConnectionInformaion(self):
        '''
        Prints connection information to verify connectivity.
        @return: Boolean value representing a successful connection
        '''
        if self.serialConnection.isOpen():
            print("Connection confirmed. ")
            print("Device connected to: " + str(self.port))
            print("Baud rate: " + str(self.baudRate))
            print("Board ID: " + str(self.deviceID))
            print("Sample size: " + str(self.channelCount))
            print("Sample frequency: " + str(self.sampleFrequency))
            print("Sample average size: " + str(self.sampleAverageSize))
            print("Sample report frequency: " + str(self.deviceReportFrequency))
            if(self.sampleEnabled == 0):
                print("Sampling disabled")
            else:
                print("Sampling enabled")
            return True
        else:
            print("No connection")
            return False
    
    def setChannelCount(self, inputChannelCount):
        '''
        Sets the number of input channels to be sampled. Number starts at A0. For example, 3 input channels would sample A0-A2
        @param inputChannelCount: Number of input channels to sample
        '''
        self.channelCount = inputChannelCount
        if inputChannelCount > self.NUMBER_SAMPLE_CHANELS:
            print("Max sample size is " + str(self.NUMBER_SAMPLE_CHANELS) + ".")
            print("Sample size set to " + str(self.NUMBER_SAMPLE_CHANELS + "."))
            self.channelCount = self.NUMBER_SAMPLE_CHANELS
        self.sendCommand(self.SET_SAMPLE_SIZE, self.channelCount)
    
    def setSampleFrequency(self, sampleFrequency):
        '''
        Sets the sample frequency (different from the report frequency.
        @param sampleFrequency: The delay in milliseconds between samples. 
        '''
        self.sampleFrequency = sampleFrequency
        self.sendCommand(self.SET_SAMPLE_FREQUENCY, self.sampleFrequency)
    
    def setSampleAverageSize(self, sampleAverageSize):
        '''
        Sets the size of the data buffer that will be averaged before being sent to the computer.
        If the buffer size requested is too large, an error message will be printed.
        @param sampleAverageSize: Size of the sample buffer that will be averaged. 
        '''
        self.sampleAverageSize = sampleAverageSize
        if sampleAverageSize > self.MAX_BUFFER_SIZE:
            print("Maximum average size is " + str(self.MAX_BUFFER_SIZE) + ".")
            print("Average size set to " + str(self.MAX_BUFFER_SIZE) + ".")
            self.sampleAverageSize = self.MAX_BUFFER_SIZE
        self.sendCommand(self.SET_SAMPLE_AVERAGE, self.sampleAverageSize)
    
    def setDeviceReportFrequency(self, deviceReportFrequency):
        '''
        Sets the frequency at which the arduino will send the average of all the samples in the 
        sample buffer.
        @param deviceReportFrequency: The delay in milliseconds between samples sent to the computer.
        '''
        self.deviceReportFrequency = deviceReportFrequency
        self.sendCommand(self.SET_REPORT_FREQUENCY, self.deviceReportFrequency)
    
    def setSampleEnable(self, sampleEnabled):
        '''
        When the sample enable bit is set, the arduino will start sending samples.
        @param sampleEnabled: Sets the sample enabled bit in the arduino. If true, the arduino
        will send samples to the computer. If false, it will stop.
        '''
        self.sampleEnabled = sampleEnabled;
        self.sendCommand(self.SET_SAMPLE_ENABLE, self.sampleEnabled)
    
    def sendCommand(self, command, value):
        self.serialConnection.write(command.to_bytes(1, 'big'))
        self.serialConnection.write((str(value) + "/n").encode('utf-8'))
    
    def getSample(self):
        return float(self.readLine())
    
    def getSampleSet(self):
        '''
        Returns the sample set representing the averaged samples for the number of channels being used.
        '''
        samples = []
        for i in range(self.channelCount):
            samples.append(self.getSample())
        return samples