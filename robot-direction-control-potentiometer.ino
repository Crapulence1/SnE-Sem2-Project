volatile int currentSpeed = 0;
int frequency = 60;

void setup()
{
  Serial.begin(9600);

  //direction pins
  pinMode(4, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(12, OUTPUT);

  //PWM pins
  pinMode(5, OUTPUT);
  pinMode(9, OUTPUT);

  //Potentiometer pin
  pinMode(A5, INPUT);
}

void loop()
{
  digitalWrite(4, LOW);
  digitalWrite(7, HIGH);
  digitalWrite(8, LOW);
  digitalWrite(12, HIGH);
  
  int difference = analogRead(A5) - analogRead(A4);
  
  int targetSpeed = difference / 4; //range 0-255
  
  if(targetSpeed < 0) {
    digitalWrite(4, LOW);
    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);
    digitalWrite(12, HIGH);
  } else {
    digitalWrite(4, HIGH);
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
    digitalWrite(12, LOW);
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
  
  analogWrite(5, currentSpeed);
  analogWrite(9, currentSpeed);
  Serial.println(targetSpeed);
  Serial.println(currentSpeed);
  Serial.println(accel);
  //to be replaced with timer and interrupthandler
  delay(1000 / frequency);
}