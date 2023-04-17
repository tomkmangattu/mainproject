/*
  Arduino Slave for Raspberry Pi Master
  i2c_slave_ard.ino
  Connects to Raspberry Pi via I2C
  
  DroneBot Workshop 2019
  https://dronebotworkshop.com
*/
 
// Include the Wire library for I2C
#include <Wire.h>
 
// LED on pin 13
const int ledPin = 13; 
 
void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x10);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600);
}

int myArray[4];
int idx = 0;

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  Serial.println("started");
  while (Wire.available()) { // loop through all but the last
    byte b = Wire.read(); // receive byte as a character
    if (b != 1){
      int value = (int)b;
      Serial.println(value);
      myArray[idx++] = value;
      if(idx == 4){
        idx = 0;
      }
    }
  }
}
void loop() {
  delay(100);
}
