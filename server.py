import RPi.GPIO as GPIO
import time
import socket

# HOST = "localhost" # Localhost connection
HOST = "jerry.local" # Jerry Connection
PORT = 9999 # Port used for TCP/UDP

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

# Sets up all motor control pins
NSLEEP1 = 12
AN11 = 17
AN12 = 27
BN11 = 22
BN12 = 23
NSLEEP2 = 13
AN21 = 24
AN22 = 25
BN21 = 26
BN22 = 16

# Sets up servo control pin
SERVO = 19

#Default states of all controls
left_trigger = -1.0
right_trigger = -1.0
left_stick_x = 0.0
right_stick_x = 0.0
dpad = (0, 0)

current_input = ""
previous_dpad= (0, 0)

# sets up GPIO pins for motor control and starts PWM
GPIO.setmode(GPIO.BCM) # Mode is BCM so remember for future connections
GPIO.setup(NSLEEP1,GPIO.OUT)
GPIO.setup(NSLEEP2,GPIO.OUT)
GPIO.setup(AN11,GPIO.OUT)
GPIO.setup(AN12,GPIO.OUT)
GPIO.setup(BN11,GPIO.OUT)
GPIO.setup(BN12,GPIO.OUT)
GPIO.setup(AN21,GPIO.OUT)
GPIO.setup(AN22,GPIO.OUT)
GPIO.setup(BN21,GPIO.OUT)
GPIO.setup(BN22,GPIO.OUT)
GPIO.setup(SERVO,GPIO.OUT)
GPIO.output(AN11,GPIO.LOW)
GPIO.output(AN12,GPIO.LOW)
GPIO.output(BN11,GPIO.LOW)
GPIO.output(BN12,GPIO.LOW)
GPIO.output(AN21,GPIO.LOW)
GPIO.output(AN22,GPIO.LOW)
GPIO.output(BN21,GPIO.LOW)
GPIO.output(BN22,GPIO.LOW)
p1=GPIO.PWM(NSLEEP1,200)
p2=GPIO.PWM(NSLEEP2,200)
p1.start(0)
p2.start(0)

# Sets up GPIO pins for Servo control and starts PWM
servo1 = GPIO.PWM(SERVO, 50)
servo1.start(7) # Starts at 90 degrees
time.sleep(0.35) # Time to get to 90 degree position
servo1.ChangeDutyCycle(0) # Turns off servo motor

# Default states for servo motor
servo_angle = 90
last_servo_angle = 90

# Variables to make code easier to read/write
forward = True
backward = False

# Sets speed of left and right wheels, range 0-100
def set_left_speed(speed):
    p1.ChangeDutyCycle(speed)
def set_right_speed(speed):
    p2.ChangeDutyCycle(speed)

# Sets speed of all wheels
def set_speed(speed):
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)

# Individual wheel direction control
def front_right(direction):
    if direction == backward:
        GPIO.output(AN11, GPIO.HIGH)
        GPIO.output(AN12, GPIO.LOW)
    if direction == forward:
        GPIO.output(AN11, GPIO.LOW)
        GPIO.output(AN12, GPIO.HIGH)
def back_right(direction):
    if direction == forward:
        GPIO.output(BN11, GPIO.HIGH)
        GPIO.output(BN12, GPIO.LOW)
    if direction == backward:
        GPIO.output(BN11, GPIO.LOW)
        GPIO.output(BN12, GPIO.HIGH)
def front_left(direction):
    if direction == forward:
        GPIO.output(AN21, GPIO.HIGH)
        GPIO.output(AN22, GPIO.LOW)
    if direction == backward:
        GPIO.output(AN21, GPIO.LOW)
        GPIO.output(AN22, GPIO.HIGH)
def back_left(direction):
    if direction == backward:
        GPIO.output(BN21, GPIO.HIGH)
        GPIO.output(BN22, GPIO.LOW)
    if direction == forward:
        GPIO.output(BN21, GPIO.LOW)
        GPIO.output(BN22, GPIO.HIGH)

# Left/right Wheel direction control
def left_wheels(direction):
    if direction == forward:
        front_left(forward)
        back_left(forward)
    else:
        front_left(backward)
        back_left(backward)
def right_wheels(direction):
    if direction == forward:
        front_right(forward)
        back_right(forward)
    else:
        front_right(backward)
        back_right(backward)

# Forward/Backward movement
def straight(direction):
    if direction == forward:
        left_wheels(forward)
        right_wheels(forward)
    else:
        left_wheels(backward)
        right_wheels(backward)

# Stop
def stop_motors():
    set_speed(0)
    GPIO.output(AN11,GPIO.LOW)
    GPIO.output(AN12,GPIO.LOW)
    GPIO.output(BN11,GPIO.LOW)
    GPIO.output(BN12,GPIO.LOW)
    GPIO.output(AN21,GPIO.LOW)
    GPIO.output(AN22,GPIO.LOW)
    GPIO.output(BN21,GPIO.LOW)
    GPIO.output(BN22,GPIO.LOW)

def read_message(msg):
    split_message = msg.split(" ")
    print(split_message)
    global current_input; current_input = split_message[0]
    if current_input == "dpad":
        global dpad; dpad = tuple([int(direction) for direction in split_message[1:]])
    elif split_message[0] == "left_stick":
        global left_stick_x; left_stick_x = float(split_message[1])
    elif split_message[0] == "right_stick":
        global right_stick_x; right_stick_x = float(split_message[1])
    elif split_message[0] == "left_trigger":
        global left_trigger; left_trigger = float(split_message[1])
    elif split_message[0] == "right_trigger":
        global right_trigger; right_trigger = float(split_message[1])
    elif split_message[0] == "end":
        stop_motors()
        servo1.ChangeDutyCycle(7)
        p1.stop()
        p2.stop()
        servo1.stop()
        GPIO.cleanup()
        current_input = ""
        server.close()

def move_motors():
    # Omni-movement
    if current_input == "dpad":
        global previous_dpad
        if dpad != previous_dpad:
            stop_motors()
            set_speed(75)
            previous_dpad = dpad
        match dpad:
            case (0, 0):
                stop_motors()
            case (0, 1):  # Forward
                straight(forward)
            case (0, -1):  # Backward
                straight(backward)
            case (1, 0):  # Right
                front_left(forward)
                back_right(forward)
                front_right(backward)
                back_left(backward)
            case (-1, 0):  # Left
                front_left(backward)
                back_right(backward)
                front_right(forward)
                back_left(forward)
            case (-1, -1):  # Back Left
                front_left(backward)
                back_right(backward)
            case (-1, 1):  # Front Left
                front_right(forward)
                back_left(forward)
            case (1, 1):  # Front Right
                front_left(forward)
                back_right(forward)
            case (1, -1):  # Back Right
                front_right(backward)
                back_left(backward)

    # Driving/Steering motor control
    elif current_input == "left_trigger" or current_input == "right_trigger" or current_input == "left_stick":
        left_val = (left_trigger + 1) / 2
        right_val = (right_trigger + 1) / 2
        diff = right_val - left_val
        if abs(diff) < 0.05:  # If stationary, turn in place
            if left_stick_x != 0:
                set_speed(abs(left_stick_x) * 100)
                if left_stick_x > 0:
                    left_wheels(forward)
                    right_wheels(backward)
                else:
                    left_wheels(backward)
                    right_wheels(forward)
            else:
                stop_motors()

        else:  # If moving, subtract speed from wheels to turn
            speed = abs(diff) * 100
            set_speed(speed)
            if diff < 0:
                if left_stick_x > 0:
                    set_left_speed(max(0, int(speed - (abs(left_stick_x) * 100))))
                elif left_stick_x < 0:
                    set_right_speed(max(0, int(speed - (abs(left_stick_x) * 100))))
                straight(backward)
            else:
                if left_stick_x > 0:
                    set_left_speed(max(0, int(speed - (abs(left_stick_x) * 100))))
                elif left_stick_x < 0:
                    set_right_speed(max(0, int(speed - (abs(left_stick_x) * 100))))
                straight(forward)

    # Servo Control
    elif current_input == "right_stick":
        global servo_angle; global last_servo_angle
        servo_angle = servo_angle + (right_stick_x * 5)
        if servo_angle > 180:
            servo_angle = 180
        elif servo_angle < 0:
            servo_angle = 0
        if last_servo_angle != servo_angle:
            duty = servo_angle / 18 + 2
            servo1.ChangeDutyCycle(duty)
            last_servo_angle = servo_angle
            print("servo angle", servo_angle, "degrees")
        else:
            servo1.ChangeDutyCycle(0)

try:
    while True:
        message, address = server.recvfrom(1024) # Decodes message
        server.sendto("Message Received".encode("utf-8"), address)
        message = message.decode("utf-8")
        read_message(message)
        move_motors()
        if not message: # If connection closed, message not received
            break
finally:
    server.close()
    print("end")

