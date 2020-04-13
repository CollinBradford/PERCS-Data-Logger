#include <Arduino.h>

//Program setup variables
int sampleSize = 1; //Number of channels to sample (1-6) apply to analog channels.
int sampleFrequency = 100; //Frequency of samples (before average) in milliseconds.
int sampleAverageSize = 10; //Set the size of the sample average.
int sampleReportFrequency = 1000; //Set the frequency at which to send averaged samples in milliseconds.
int sampleEnabled = 0; //Set whether the device is currently sampling and reporting to the computer.

//Timing variables
unsigned long lastSampleTime = 0;
unsigned long lastReportTime = 0;
int reportNumber = 0; //TODO: remove testing counter

//Constants
const int DEVICE_ID = 0; //Could be changed according to digital pins to give addressing capability, but this functionality is not implemented.
const int BUFFER_SIZE = 100;
const int NUMBER_SAMPLE_CHANELS = 6;

//Data variables
int dataBuffer[NUMBER_SAMPLE_CHANELS][BUFFER_SIZE]; //Main data buffer.
int bufferPlace = 0; //Circular buffer placeholder. Increments every time we add to the buffer.
bool bufferInitialized = false; //Sets to true once we have a full buffer so that we don't try to read from the buffer before the first set of data has been read.

//Commands (sent to the device)
const int SET_SAMPLE_SIZE = 1;
const int SET_SAMPLE_FREQUENCY = 2;
const int SET_SAMPLE_AVERAGE = 3;
const int SET_REPORT_FREQUENCY = 4;
const int SET_SAMPLE_ENABLE = 5;

//Function declarations
int readCommandDataBlock();
void checkForCommand();
void report();
void sample();
void eraseDataBuffer();
void getChanelAverages(double[]);

void setup() {
  Serial.begin(115200);
  Serial.println("Connected to device: " + String(DEVICE_ID));
  lastSampleTime = millis();
  eraseDataBuffer();
}

void loop() {
  checkForCommand();
  if(sampleEnabled == 1 && millis() - lastSampleTime >= sampleFrequency){
    sample();
    lastSampleTime = millis();
  }
  if(sampleEnabled == 1 && millis() - lastReportTime >= sampleReportFrequency){
    report();
    lastReportTime = millis();
  }
}

void sample(){
  for(int i = 0; i < sampleSize; i++){
    dataBuffer[i][bufferPlace] = analogRead(i);
    //dataBuffer[i][bufferPlace] = i;
  }
  bufferPlace++;
  if(bufferPlace == sampleAverageSize){
    bufferPlace = 0;
    bufferInitialized = true;
  }
}

void report(){
  double sampleAverages[NUMBER_SAMPLE_CHANELS];
  getChanelAverages(sampleAverages);
  for(int i = 0; i < sampleSize; i++){
    Serial.println(sampleAverages[i]);
  }
}

void getChanelAverages(double averages[NUMBER_SAMPLE_CHANELS]){
  for(int i = 0; i < sampleSize; i++){
    averages[i] = 0;
    if(bufferInitialized){
      for(int j = 0; j < sampleAverageSize; j++){
        averages[i] += dataBuffer[i][j];
      }
      averages[i] = averages[i] / sampleAverageSize;
    } else {
      for(int j = 0; j < bufferPlace; j++){
        averages[i] += dataBuffer[i][j];
      }
      averages[i] = averages[i] / bufferPlace;
    }
  }
}

void eraseDataBuffer(){
  for(int i = 0; i < BUFFER_SIZE; i++){
    for(int j = 0; j < 6; j++){
      dataBuffer[j][i] = 0;
    }
  }
}

void checkForCommand(){
  if(Serial.available() > 0){
    int command = Serial.read();
    switch(command){
    case SET_SAMPLE_SIZE:
      sampleSize = readCommandDataBlock();
      Serial.println("Sample size: " + String(sampleSize));
      break;
    case SET_SAMPLE_FREQUENCY:
      sampleFrequency = readCommandDataBlock();
      Serial.println("Sample frequency: " + String(sampleSize));
      break;
    case SET_SAMPLE_AVERAGE:
      sampleAverageSize = readCommandDataBlock();
      Serial.println("Sample average size: " + String(sampleAverageSize));
      break;
    case SET_REPORT_FREQUENCY:
      sampleReportFrequency = readCommandDataBlock();
      Serial.println("Sample report size: " + String(sampleReportFrequency));
      break;
    case SET_SAMPLE_ENABLE:
      sampleEnabled = readCommandDataBlock();
      Serial.println("Sample enabled bit set to: " + String(sampleEnabled));
    }
  }
}

int readCommandDataBlock(){
  int commandData = Serial.parseInt();
  return commandData;
}
