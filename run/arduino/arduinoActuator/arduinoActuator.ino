#define SERIAL_ADDRESS 250000
#define PWM_PIN 3
#define DIR_PIN 2
#define POT_PIN A0

#define LEFT 455
#define RIGHT 755

int stickVal = 50;
int actuatorVal = 0;
int setpoint = 0;

int testPoints[] = {10, 40, 80, 70, 90, 30, 0, 8, 32, 80};

void setup() {
  // put your setup code here, to run once:
  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  actuatorVal = analogRead(POT_PIN);
  
  actuatorVal = int((actuatorVal - LEFT)/3);

  setpoint = actuatorVal;

  Serial.begin(SERIAL_ADDRESS);

  Serial.println("Ready!");
  Serial.println(actuatorVal);
}

void loop() {
  actuatorVal = analogRead(POT_PIN);
  actuatorVal = int((actuatorVal - LEFT)/3);
  
  if (Serial.available()) {
    setpoint = Serial.read() - '0';

    Serial.println(Serial.read());
    Serial.println(Serial.read() - '0');

    Serial.println("Setpoint: ");
    Serial.println(setpoint);

    Serial.println("ActuatorVal: ");
    Serial.println(actuatorVal);
  }

  if (setpoint != actuatorVal) {
      if (actuatorVal < setpoint - 10) {
        digitalWrite(DIR_PIN, LOW);
        analogWrite(PWM_PIN, 255);
      } else if (actuatorVal > setpoint + 10) {
        digitalWrite(DIR_PIN, HIGH);
        analogWrite(PWM_PIN, 255);
      } else {
        analogWrite(PWM_PIN, 0);
      }
  }
  else {
    analogWrite(PWM_PIN, 0);
  }
  
}
