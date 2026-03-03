volatile int currentSpeed = 0;
int frequency = 60;

void setup()
{
  Serial.begin(9600);

  //direction pins
  //back left
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  //front left
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  //back right
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  //front right
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  //PWM pins
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
}

void loop()
{
  setSpeed(255);

  frontRight(true);
  delay(500);
  frontLeft(true);
  delay(500);
  backLeft(true);
  delay(500);
  backRight(true);
  delay(500);


  forward();
  delay(500);
  backward();
  delay(500);
  turnRight();
  delay(500);
  turnLeft();
  delay(500);
  rightOmni();
  delay(500);
  leftOmni();
  delay(500);
  setSpeed(0);
  delay(2000);
}

void setSpeed(int speed) {
  analogWrite(3, speed);
  analogWrite(5, speed);
  analogWrite(10, speed);
  analogWrite(11, speed);
}


//Controlling the robots movemment
void forward() {
  frontRight(true);
  frontLeft(true);
  backRight(true);
  backLeft(true);
}

void backward() {
  frontRight(false);
  frontLeft(false);
  backRight(false);
  backLeft(false);
}

void turnRight() {
  frontRight(false);
  backRight(false);
  frontLeft(true);
  backLeft(true);
}

void turnLeft() {
  frontRight(true);
  backRight(true);
  frontLeft(false);
  backLeft(false);
}

void rightOmni() {
  frontLeft(true);
  backRight(true);
  frontRight(false);
  backLeft(false);
}

void leftOmni() {
  frontLeft(false);
  backRight(false);
  frontRight(true);
  backLeft(true);
}


//Forward and backward control of each individual wheel
void frontRight(boolean forward) {
  if(forward) {
    digitalWrite(12, LOW);
    digitalWrite(13, HIGH);
  } else {
    digitalWrite(12, HIGH);
    digitalWrite(13, LOW);
  }
}

void backRight(boolean forward) {
  if(forward) {
    digitalWrite(8, LOW);
    digitalWrite(9, HIGH);
  } else {
    digitalWrite(8, HIGH);
    digitalWrite(9, LOW);
  }
}

void frontLeft(boolean forward) {
  if(forward) {
    digitalWrite(6, LOW);
    digitalWrite(7, HIGH);
  } else {
    digitalWrite(6, HIGH);
    digitalWrite(7, LOW);
  }
}

void backLeft(boolean forward) {
  if(forward) {
    digitalWrite(2, LOW);
    digitalWrite(4, HIGH);
  } else {
    digitalWrite(2, HIGH);
    digitalWrite(4, LOW);
  }
}        