#include <Servo.h> 

#define SERIAL_ADDRESS 250000
#define SERVO_PIN 3

//Positions
#define MOTOR_OFF 0
#define MOTOR_ON 40
#define MOTOR_MAX 180

Servo servo;

int motorSpeed = 0;

int speedMultiplier = (180 - MOTOR_ON)/100;

int testSpeeds[] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 50, 20, -1};

int current = 0;

int currentAngle = 180;

int startTime = 0;

int currentTime = 0;

void setup() { 
  Serial.begin(SERIAL_ADDRESS); 
  servo.attach(SERVO_PIN);

  servo.write(180);
  currentAngle = 180;
  motorSpeed = MOTOR_OFF;
}
void loop(){
  if (Serial.available()) {
    Serial.println("Motor Speed: ");
    Serial.print(motorSpeed);
    motorSpeed = Serial.read() - '0';
    setMotorSpeed(motorSpeed);
    startTime = millis();
  }

  // if (current != sizeof(testSpeeds)) {
  //   Serial.println("Motor Speed: ");
  //   Serial.print(testSpeeds[current]);
  //   setMotorSpeed(testSpeeds[current]);
  //   current++;
  // }
  // delay(2000);

  currentTime = millis();
  if (currentTime - startTime > 2000 && currentAngle > 15) {
    turnOff();
  }
}

void setMotorSpeed(int speed) {
  int angle = 0;
  if (speed == -1) {
    angle = 180 - MOTOR_OFF;
  } else if (speed > 100) {
    angle = 180 - MOTOR_OFF;
  } else if (speed < -1) {
    angle = 180 - MOTOR_OFF;
  } else {
    angle = int(180 - MOTOR_ON - (speed * speedMultiplier));
  }

  Serial.println("Angle: ");
  Serial.print(angle);

  servo.write(angle);

  delay((150/60) * abs(currentAngle - angle));

  currentAngle = angle;
}

void turnOff() {
  setMotorSpeed(-1);
}

void turnOn() {
  setMotorSpeed(MOTOR_ON);
}
