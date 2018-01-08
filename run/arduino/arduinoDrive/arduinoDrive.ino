#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x04
#define SERIAL_ADDRESS 9600
#define csPin 10
#define sckPin 13

int motorSpeed = 0;

void setup() {
  pinMode(sckPin, OUTPUT);
  pinMode (csPin, OUTPUT);
  
  Serial.begin(SERIAL_ADDRESS);
  SPI.begin();
  
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void loop() {
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    motorSpeed = Wire.read();
    if (motorSpeed < 129) {
      Serial.println(motorSpeed);
      digitalPotWrite(motorSpeed);
      delay(50);
    }
    delay(100);
  }
}

int digitalPotWrite(int value) {
  digitalWrite(csPin, LOW);
  SPI.transfer(0x00);
  SPI.transfer(value);
  digitalWrite(csPin, HIGH);
}

// callback for sending data
void sendData() {
  Wire.write(motorSpeed);
}
