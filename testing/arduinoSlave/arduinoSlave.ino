#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x04
#define SERIAL_ADDRESS 9600

int motorSpeed = 0;

const int csPin = 10;
const int sckPin = 13;

void setup() {
  pinMode(sckPin, OUTPUT);
  pinMode (csPin, OUTPUT);
  
  Serial.begin(SERIAL_ADDRESS); // start serial for output
  // initialize i2c as slave
  SPI.begin();
  
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
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
