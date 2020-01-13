/*
        Arduino Brushless Motor Control
     by Dejan, https://howtomechatronics.com
*/
#include <Servo.h>
#define HM_MIN_PULSE_WIDTH_CW 1517 // microseconds
#define HM_MAX_PULSE_WIDTH_CW 1555 // microseconds

#define HM_MIN_PULSE_WIDTH_CCW 1402 // microseconds
#define HM_MAX_PULSE_WIDTH_CCW 1363 // microseconds

#define HM_MAX_CCW_SPEED 1363 // microseconds
#define HM_MIN_CCW_SPEED 1402 // microseconds

#define HM_MAX_CW_SPEED 1555 // microseconds
#define HM_MIN_CW_SPEED 1517 // microseconds


/*
clockwise @ 93
counter clockwise @ 70
*/
Servo ESC;     // create servo object to control the ESC
int potValue;  // value from the analog pin
void setup() {
  Serial.begin(115200);
  // Attach the ESC on pin 9
  //ESC.attach(9,1000,2000); // (pin, min pulse width, max pulse width in microseconds) 
  ESC.attach(9,1300,1600); // (pin, min pulse width, max pulse width in microseconds) 
//MAX CCW @ 83
// STOP (87-93) [1421-1498]
//MAX CW @ 100
  
  //ESC.attach(9);
    ESC.write(93);    // Send the signal to the ESC
  delay(1000);
  ESC.write(102);
  
}
void loop() {
  
  //potValue = analogRead(A0);   // reads the value of the potentiometer (value between 0 and 1023)
  //potValue = map(potValue, 0, 1023, 0, 180);   // scale it to use it with the servo library (value between 0 and 180)
  //ESC.write(87);    // Send the signal to the ESC
  //delay(10000);
  ESC.write(101);
  
  Serial.println(potValue);
}
