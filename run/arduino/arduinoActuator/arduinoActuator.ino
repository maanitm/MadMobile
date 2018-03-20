#define SERIAL_ADDRESS 250000
#define PWM_PIN 3
#define DIR_PIN 2
#define POT_PIN A0

int stickVal = 50;
int actuatorVal = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  actuatorVal = analogRead(POT_PIN);

  Serial.begin(SERIAL_ADDRESS);
  SPI.begin();

  Serial.println("Ready!");
}

void loop() {
  actuatorVal = analogRead(POT_PIN);
  
  if (Serial.available()) {
    int setpoint = Serial.read() - '0';
    
    if (setpoint != actuatorVal) {
      if (setpoint > actuatorVal) {
        digitalWrite(DIR_PIN, HIGH);
        while (actuatorVal < setpoint) {
          actuatorVal = analogRead(POT_PIN);
          analogWrite(PWM_PIN, 255);
        }
      } else if (setpoint < actuatorVal) {
        digitalWrite(DIR_PIN, LOW);
        while (actuatorVal > setpoint) {
          actuatorVal = analogRead(POT_PIN);
          analogWrite(PWM_PIN, 255);
        }
      }
      analogWrite(PWM_PIN, 0);
    }
  }
}
