//////////////////////////////////////////////////////////////////////////////////////////

#include <Arduino.h>

//////////////////////////////////////////////////////////////////////////////////////////

#define PWM_L 9   // PWM L Motor
#define PWM_R 10  // PWM R Motor
#define DIR_L 15  // Dir L Motor
#define DIR_R 16  // Dir R Motor
#define ENC_L 2   // Encoder L Motor
#define ENC_R 3   // Encoder R Motor

//////////////////////////////////////////////////////////////////////////////////////////

enum speeds       { STOP = 0, HALF = 128, FULL = 255 };
enum wheels       { LEFT = 0, RIGHT = 1 };
enum directions   { FORWARD = 0, BACKWARD = 1 };

////////////////////////////////////////////////////////////

// Current DIR pin value for each wheel
volatile int sign_l = 1;
volatile int sign_r = 1;

////////////////////////////////////////////////////////////

// Encoder ticks since start
volatile long ticks_l = 0;
volatile long ticks_r = 0;

//////////////////////////////////////////////////////////////////////////////////////////
const unsigned long STEP_TIME = 5000; // each step lasts 5 seconds
int setSpeed(int step);

void leftEncoderCallback();
void rightEncoderCallback();

//////////////////////////////////////////////////////////////////////////////////////////

void setup() {

  // Init motor PINs
  pinMode(PWM_L, OUTPUT);
  pinMode(PWM_R, OUTPUT);
  pinMode(DIR_L, OUTPUT);
  pinMode(DIR_R, OUTPUT);
  pinMode(ENC_L, INPUT);
  pinMode(ENC_R, INPUT);

  ////////////////////////////////////////////////////////////

  digitalWrite(DIR_L, sign_l);
  digitalWrite(DIR_R, sign_r);

  analogWrite(PWM_L, 0);
  analogWrite(PWM_R, 0);

  ////////////////////////////////////////////////////////////

  Serial.begin(115200);

  ////////////////////////////////////////////////////////////

  attachInterrupt(digitalPinToInterrupt(ENC_L), leftEncoderCallback, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC_R), rightEncoderCallback, CHANGE);

}

//////////////////////////////////////////////////////////////////////////////////////////

void loop() {

  // TODO: Update steps correctly
  int step = millis() / STEP_TIME;
   
  ////////////////////////////////////////////////////////////

  int wheel = step / 6;
  int dir   = (step % 6) / 3;

//   print whee and dir
//Serial.println("wheel int");
//Serial.println(wheel);
//Serial.println("dir");
//Serial.println(dir);
//Serial.println();


  ////////////////////////////////////////////////////////////

  int speed_l = speeds::STOP;
  int speed_r = speeds::STOP;

  //int direction = 1;

  ////////////////////////////////////////////////////////////

  if (wheel == LEFT)    speed_l = setSpeed(step % 3);
  if (wheel == RIGHT)   speed_r = setSpeed(step % 3);


  //if (dir == directions::FORWARD)    direction = 1;
  //if (dir == directions::BACKWARD)   direction = 0;

 if (dir == directions::FORWARD) {
    sign_l = LOW;
    sign_r = HIGH;
 }
 else {
    sign_l = HIGH;
    sign_r = LOW;
 }

digitalWrite(DIR_L, sign_l);
digitalWrite(DIR_R, sign_r);
  ////////////////////////////////////////////////////////////

 // digitalWrite(DIR_L, direction);
  //digitalWrite(DIR_R, direction);

  analogWrite(PWM_L, speed_l);
  analogWrite(PWM_R, speed_r);

//Serial.print("Step: ");
//Serial.println(step);
//Serial.print(" Left PWM: ");
//Serial.println(speed_l);
//Serial.print(" Right PWM: ");
//Serial.println(speed_r);
//Serial.print(" Left DIR: ");
//Serial.println(sign_l);
//Serial.print(" Right DIR: ");
//Serial.println(sign_r);

  ////////////////////////////////////////////////////////////

  // Copy the tick counts with interrupts paused so they can't change mid-read
  noInterrupts();
  long left = ticks_l;
  long right = ticks_r;
  interrupts();

  ////////////////////////////////////////////////////////////

  String encoder_out = "L: " + String(left) + "  R: " + String(right);
  Serial.println(encoder_out);

  ////////////////////////////////////////////////////////////

  delay(100);

//   print "---------------------------------------"
//Serial.println("-------");
}

//////////////////////////////////////////////////////////////////////////////////////////

int setSpeed(int step) {
    // print step
    //Serial.println("Set speed step");
    //Serial.println(step);
//Serial.println("-------");

  if (step == 0) return speeds::STOP;
  if (step == 1) return speeds::HALF;
  if (step == 2) return speeds::FULL;
}

//////////////////////////////////////////////////////////////////////////////////////////

void rightEncoderCallback() {
//   switch (sign_r) {
//     case HIGH:  ticks_r++; break;
//     case LOW:   ticks_r--; break;
//   }
if (sign_r == 1) ticks_r++;
else ticks_r--;

}

//////////////////////////////////////////////////////////////////////////////////////////

void leftEncoderCallback() {
  //switch (sign_l){
   // case HIGH:  ticks_l++; break;
    //case LOW:   ticks_l--; break;
if (sign_l == 0) ticks_l++;
else ticks_l--;

  
}

//////////////////////////////////////////////////////////////////////////////////////////

