#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x06
#define SERIAL_ADDRESS 9600
#define pwmPin 3
#define dirPin 2

int currentVal = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(pwmPin,OUTPUT);
  pinMode(dirPin,OUTPUT);

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
    analogWrite(pwmPin, 255);
    
    digitalWrite(dirPin, HIGH);
    delay((300/100) * value);
    analogWrite(pwmPin, 0); 
  }
  else if (value < 0) {
    analogWrite(pwmPin, 255);
    
    digitalWrite(dirPin, LOW);
    delay((300/100) * value * -1);
    analogWrite(pwmPin, 0); 
  }
  else {
    analogWrite(pwmPin, 0);
  }
  delay(5);
}

void loop() {
  // put your main code here, to run repeatedly:
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    int newVal = Wire.read();
    if (newVal <= 200) {
      if (newVal > 100) {
        newVal = (newVal + 100) - (newVal * 2);
      }
      int change = newVal - currentVal;
      Serial.println(newVal);
      setActuatorValue(change);
      currentVal = newVal;  
    }
  }
}

// callback for sending data
void sendData() {
  Wire.write(currentVal);
}
