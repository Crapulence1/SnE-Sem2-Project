volatile int currentSpeed = 0;
int frequency = 60;

void setup()
{
  Serial.begin(9600);

  //direction pins
  //back left
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  //back right
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  //
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  //
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  //PWM pins
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);

  //Potentiometer pin
  pinMode(A5, INPUT);
  pinMode(A4, INPUT);
}

void loop()
{
  int difference = analogRead(A5) - analogRead(A4);
  
  int targetSpeed = difference / 4; //range 0-255
  
  if(targetSpeed < 0) {
    forward();
  } else {
    backward();
  }
  
  targetSpeed = abs(targetSpeed);
  
  int accel = 2;  //acceleration speed (constant)
  if(currentSpeed < targetSpeed) {  //accelerate
    currentSpeed += accel;
    if(currentSpeed > targetSpeed) {//prevents overshooting speed
      currentSpeed = targetSpeed;
    }
  } else if(currentSpeed > targetSpeed) { //decelerate
    currentSpeed -= accel;
    if(currentSpeed < targetSpeed) {//prevents undershooting speed
      currentSpeed = targetSpeed;
    }
  }
  
  setSpeed(currentSpeed);
  Serial.println(targetSpeed);
  Serial.println(currentSpeed);
  Serial.println(accel);
  //to be replaced with timer and interrupthandler
  delay(1000 / frequency);
}

void setSpeed(int speed) {
  analogWrite(3, speed);
  analogWrite(5, speed);
  analogWrite(10, speed);
  analogWrite(11, speed);
}

void forward() {
  digitalWrite(2, LOW);
  digitalWrite(4, HIGH);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  digitalWrite(8, LOW);
  digitalWrite(9, HIGH);
  digitalWrite(12, LOW);
  digitalWrite(13, HIGH);
}

void backward() {
  digitalWrite(2, HIGH);
  digitalWrite(4, LOW);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
  digitalWrite(8, HIGH);
  digitalWrite(9, LOW);
  digitalWrite(12, HIGH);
  digitalWrite(13, LOW);
}