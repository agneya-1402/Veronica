#include <Servo.h>

Servo servoX;  // Horizontal eye movement
Servo servoY;  // Vertical eye movement

void setup() {
  servoX.attach(9);  // Attach servo to pin 9 
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    
    if (commaIndex != -1) {
      int x = data.substring(0, commaIndex).toInt();
      int y = data.substring(commaIndex + 1).toInt();
      
      servoX.write(x);
      servoY.write(y);
    }
  }
}
