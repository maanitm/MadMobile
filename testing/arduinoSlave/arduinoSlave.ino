#include <Wire.h>
#include <SPI.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

void setup() {
  pinMode(13, OUTPUT);
  pinMode (10, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  SPI.begin();
  
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

// callback for received data
void receiveData(int byteCount) {
  while(Wire.available()) {
    number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);
    
    if (number < 129) {
      digitalPotWrite(number);
      delay(50);
    }
  }
}

int digitalPotWrite(int value) {
  digitalWrite(10, LOW);
  SPI.transfer(0x00);
  SPI.transfer(value);
  digitalWrite(10, HIGH);
}

// callback for sending data
void sendData() {
  Wire.write(number);
}
