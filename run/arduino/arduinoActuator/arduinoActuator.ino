#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x06
#define SERIAL_ADDRESS 9600
#define pwmPin 3
#define dirPin 2

int stickVal = 50;
int actuatorVal = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(pwmPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  setActuatorValue(50);

  Serial.begin(SERIAL_ADDRESS);
  SPI.begin();
  
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void setActuatorValue(int value) {
  if (value >= 0 && value <= 100) {
    int movement = (value - actuatorVal);
    if (movement > 0) {
      digitalWrite(dirPin, HIGH);
      analogWrite(pwmPin, 255);
      delay((300/100) * movement/2);
      analogWrite(pwmPin, 0);
    }
    else if (movement < 0) {
      digitalWrite(dirPin, LOW);
      analogWrite(pwmPin, 255);
      delay((300/100) * ((movement * -1)/2));
      analogWrite(pwmPin, 0);
    }
    
    actuatorVal = value;
    delay(5);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  setActuatorValue(stickVal);
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    stickVal = Wire.read();
    delay(5);
  }
}

// callback for sending data
void sendData() {
  Wire.write(actuatorVal);
}
