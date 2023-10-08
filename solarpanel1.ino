#include <Servo.h>

Servo myservo;  
int ldr1Pin = A0; 
int ldr2Pin = A1; 
int threshold = 50; 
bool rotatedRight = false;
int mq8_pin = A2;

void setup() {
  myservo.attach(9);  
  Serial.begin(9600);
}
void loop() {
  int ldr1Value = analogRead(ldr1Pin);
  int ldr2Value = analogRead(ldr2Pin); 
  int mq8 = analogRead(mq8_pin);
  Serial.print("mq8: ");
  Serial.println(mq8);
  // Rotate servo based on LDR readings
  if (ldr1Value > ldr2Value + threshold && !rotatedRight) {
    myservo.write(120);
    delay(500);
    myservo.write(90);
    rotatedRight = true;
  } else if (ldr2Value > ldr1Value + threshold && rotatedRight) {
    myservo.write(60);
    delay(500);
    myservo.write(90);  
    rotatedRight = false;
    
  } else {
    myservo.write(90);
  }

  delay(1000);
}
