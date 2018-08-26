#include <Servo.h> 

#define SERIAL_ADDRESS 9600
#define SERVO_PIN 9

Servo servo;

int currentAngle = 0;

void setup() { 
  Serial.begin(SERIAL_ADDRESS); 
  servo.attach(SERVO_PIN);

  servo.write(0);
  currentAngle = 0;
}

void loop(){
  if (currentAngle > 180) {
    currentAngle = 0;
  }
  Serial.println(currentAngle);
  servo.write(currentAngle);
  delay(200);
  currentAngle = currentAngle + 20;
}

