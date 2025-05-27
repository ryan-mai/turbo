#include <Arduino.h>
#include <Servo.h>

Servo myServo;

void servoSpin(int speed);

void setup(){
  Serial.begin(9600);
  myServo.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'P') {
      servoSpin(15);
      Serial.println("1 Revolution Completed...");
    }
  }
}

void servoSpin(int speed){
  for (int pos = 0; pos <= 180; pos ++){
    myServo.write(pos);
    delay(speed);
  }
  for (int pos = 180; pos >= 0; pos --){
    myServo.write(pos);
    delay(speed);
  }
}