#ifndef Jerry
#define Jerry

#include "Arduino.h"

class Jerry
{
  public:
    Jerry(
      pinOne,
      pinTwo,
      pinThree,
      pinFour,
      pinFive,
      pinSix,
      pinSeven,
      pinEight,

      PWMOne,
      PWMTwo,
      PWMThree,
      PWMFour,
    );

    void frontLeft(boolean direction);
    void frontRight(boolean direction);
    void backLeft(boolean direction);
    void backRight(boolean direction);

    void frontLeftSpeed(int speed);
    void frontRightSpeed(int speed);
    void backLeftSpeed(int speed);
    void backRightSpeed(int speed);
    void setSpeed(int speed);

    void forward();
    void backward();
    void left();
    void right();
    void omniLeft();
    void omniRight();
  private:
    int _pinOne;
    int _pinTwo;
    int _pinThree;
    int _pinFour;
    int _pinFive;
    int _pinSix;
    int _pinSeven;
    int _pinEight;

    int _PWMOne;
    int _PWMTwo;
    int _PWMThree;
    int _PWMFour;
}

#endif