#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x04
#define SERIAL_ADDRESS 9600
int manualSpeed = 0;
int state = 0;
long duration;
int distance;
bool manual = true;

const int trigPin = 2;
const int echoPin = 3;

const int csPin = 10;
const int sckPin = 13;

int currentSpeed = 75;

int zeroSpeed = 75;
int speedIncrement = 3;
int topSpeed = 102;

int minStopDistance = 50;
int maxStopDistance = 400;

void setup() {
  pinMode(sckPin, OUTPUT);
  pinMode (csPin, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode (echoPin, INPUT);
  
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
  if (!manual) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    distance= duration*0.034/2;
    // Prints the distance on the Serial Monitor
    Serial.print("Distance: ");
    Serial.println(distance);
  
    //REFLECT LIGHT BASED ON DISTANCE HERE
    int stopDif = maxStopDistance - minStopDistance;
    int stopDistance = (currentSpeed - zeroSpeed) * 14.8148148148;
    if (stopDistance < minStopDistance) {
      stopDistance = minStopDistance;
    }
    if (stopDistance > maxStopDistance) {
      stopDistance = maxStopDistance;
    }
    
    if (distance < stopDistance) {
      currentSpeed = zeroSpeed + 1;
      
    }
    else if (distance <= 400 && distance > stopDistance) {
      currentSpeed = int(distance/30) + zeroSpeed;
    }
    else {
      if (currentSpeed + speedIncrement < topSpeed) {
        currentSpeed += speedIncrement;  
      }
    }
    Serial.print("Voltage: ");
    Serial.println(currentSpeed);
    digitalPotWrite(currentSpeed);
    delay(50);
  }
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    manualSpeed = Wire.read();
    if (manualSpeed == 130) {
      if (manual) {
        manual = false;
      }
      else {
        manual = true;
      }
    }
    else if (manual) {
      if (manualSpeed < 129) {
        digitalPotWrite(manualSpeed);
        delay(50);
      }
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
  Wire.write(manualSpeed);
}
