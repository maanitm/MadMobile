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
}

void loop() {
  if (Serial.available()) {
    int readSpeed = Serial.read() - '0';
    motorSpeed = readSpeed;
    if (motorSpeed < 129) {
      // digitalPotWrite(motorSpeed);
      Serial.println("Drive: ");
      Serial.print(motorSpeed);
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
