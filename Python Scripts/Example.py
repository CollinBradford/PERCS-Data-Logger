'''
Created on Mar 4, 2020

@author: Collin Bradford for PERCS
'''

import Arduino
import Run
import time
from DataLogger import DataLogger

COM_PORT = "COM4"
BAUD_RATE = 115200

mainBoard = Arduino.Arduino(COM_PORT, BAUD_RATE)
mainBoard.printConnectionInformaion()

print()
print("Starting tests...")
print()

print("Setting sample size to 6")
mainBoard.setChannelCount(6)
print("Sample size set. Message from board: " + mainBoard.readLine())

print("Setting sample frequency to 50")
mainBoard.setSampleFrequency(50)
print("Sample frequency set. Message from board: " + mainBoard.readLine())

print("Setting sample average size to 1")
mainBoard.setSampleAverageSize(1)
print("Sample average set. Message from board: " + mainBoard.readLine())

print("Setting device report rate to 1000")
mainBoard.setDeviceReportFrequency(1000)
print("Device report rate set. Message from board: " + mainBoard.readLine())

print("Setting device sample enabled bit to 1")
mainBoard.setSampleEnable(1)
print("Device sample enabled set. Message from board: " + mainBoard.readLine())

print()
print("Starting board read: ")
print()

headers = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']
logger = DataLogger('run1.xlsx', 7, headers)

sampleRun = Run.Run(mainBoard, logger)
sampleRun.start()

time.sleep(16)

print("Run Successful!")
print("Number of Samples: " + str(sampleRun.stop()))
