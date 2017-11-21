#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x06
#define SERIAL_ADDRESS 9600
#define pwmPin 3
#define dirPin 2

int currentVal = -1;
int changedVal = 0;
int newVal = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(pwmPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  currentVal = -1;
  setActuatorValue(50);
//  digitalWrite(dirPin, HIGH);
//    analogWrite(pwmPin, 255);
//    delay((300/100) * 25);
//    analogWrite(pwmPin, 0);

  Serial.begin(SERIAL_ADDRESS);
  SPI.begin();
  
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void setActuatorValue(int value) {
//  if (value > 0) {
//    digitalWrite(dirPin, HIGH);
//    analogWrite(pwmPin, 255);
////    Serial.println("A");
//    delay((3000/1000) * (value*10));
////    Serial.println("B");
//    analogWrite(pwmPin, 0); 
//  }
//  else if (value < 0) {
//    digitalWrite(dirPin, LOW);
//    analogWrite(pwmPin, 255);
//    delay((3000/1000) * (value * -10));
//    analogWrite(pwmPin, 0); 
//  }
  if (value >= 0 && value <= 100) {
    if (value > 50) {
      digitalWrite(dirPin, HIGH);
      analogWrite(pwmPin, 255);
      delay((300/100) * 50);
      analogWrite(pwmPin, 0);
      currentVal = 1;
    }
    else if (value < 50) {
      digitalWrite(dirPin, LOW);
      analogWrite(pwmPin, 255);
      delay((300/100) * 50);
      analogWrite(pwmPin, 0);
      currentVal = -1;
    }
    else {
      if (currentVal == -1) {
        digitalWrite(dirPin, HIGH);
        analogWrite(pwmPin, 255);
        delay((300/100) * 50);
        analogWrite(pwmPin, 0); 
      }
      else if (currentVal == 1) {
        digitalWrite(dirPin, LOW);
        analogWrite(pwmPin, 255);
        delay((300/100) * 50);
        analogWrite(pwmPin, 0); 
      }
      currentVal = 0;
    }
    delay(5);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
//  Serial.println(changedVal);
//  changedVal = newVal - currentVal;
//  Serial.println("A");
//  setActuatorValue(changedVal);
//  Serial.println("B");
//  currentVal = newVal;
  setActuatorValue(newVal);
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    newVal = Wire.read();
  }
}

// callback for sending data
void sendData() {
  Wire.write(currentVal);
}
