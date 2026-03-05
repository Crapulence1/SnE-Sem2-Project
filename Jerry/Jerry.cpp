#include "Arduino.h"
#include "Jerry.h"

Jerry:Jerry(
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
) {
  _pinOne = pinOne;
  _pinTwo = pinTwo;
  _pinThree = pinThree;
  _pinFour = pinFour;
  _pinFive = pinFive;
  _pinSix = pinSix;
  _pinSeven = pinSeven;
  _pinEight = pinEight;

  _PWMOne = PWMOne;
  _PWMTwo = PWMTwo;
  _PWMThree = PWMThree;
  _PWMFour = PWMFour;
}

void Jerry::frontLeft(boolean direction) {
  if(direction == true) {
    digitalWrite()
  }
}