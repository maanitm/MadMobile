#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x06
#define SERIAL_ADDRESS 9600
#define pwmPin 3
#define dirPin 2

int currentVal = 0;
int changedVal = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(pwmPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  setActuatorValue(currentVal);

  Serial.begin(SERIAL_ADDRESS);
  SPI.begin();
  
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void setActuatorValue(int value) {
  if (value > 0) {
    digitalWrite(dirPin, HIGH);
    analogWrite(pwmPin, 255);
    Serial.println("A");
    delay((3000/1000) * (value*10));
    Serial.println("B");
    analogWrite(pwmPin, 0); 
  }
  else if (value < 0) {
    digitalWrite(dirPin, LOW);
    analogWrite(pwmPin, 255);
    delay((3000/1000) * (value * -10));
    analogWrite(pwmPin, 0); 
  }
  else {
    digitalWrite(dirPin, HIGH);
    analogWrite(pwmPin, 0);
  }
  delay(5);
}

void loop() {
  // put your main code here, to run repeatedly:
  setActuatorValue(changedVal);
  Serial.println(changedVal);
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    int newVal = Wire.read();
    if (newVal <= 200) {
      changedVal = newVal - currentVal;
      currentVal = newVal;
    }
  }
}

// callback for sending data
void sendData() {
  Wire.write(currentVal);
}
