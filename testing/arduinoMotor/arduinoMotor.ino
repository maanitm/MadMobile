#include <SPI.h>

byte address = 0x00;
int CS= 10;
int led = 0;

//Motor runs from 75 - 128

void setup() {
  Serial.begin(9600);  
  pinMode (CS, OUTPUT);
  SPI.begin();
  
}

void loop() {
  Serial.println("Enter LED brightness (0 - 128)");  

  String ledString = "0";
  
  while (Serial.available()==0) {    
  }

  ledString = Serial.readString();  //Reading the Input string from Serial port.
  led = ledString.toInt();
  
  if (led < 129) {
    digitalPotWrite(led);
    delay(50);
  }
  
  Serial.println("Set to " + ledString);
  
}

int digitalPotWrite(int value) {
  digitalWrite(CS, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CS, HIGH);
}
