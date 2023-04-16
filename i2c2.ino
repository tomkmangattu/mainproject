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
 
// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    byte c = Wire.read(); // receive byte as a character
    Serial.println(c);
  }
}
void loop() {
  delay(100);
}
