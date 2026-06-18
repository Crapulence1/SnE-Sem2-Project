import RPi.GPIO as GPIO
import time
import socket
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from datetime import datetime
import libcamera

# --- NETWORK CONFIGURATION ---
HOST = "jerry.local"  # Local hostname or Pi IP address
PORT = 9999  # Port used for UDP controller commands
REMOTE_IP = "172.20.10.7"  # Your PC's IP address (where VLC is running)

# Setup UDP Server for receiving controller inputs
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

# --- MOTOR & SERVO GPIO PIN DEFINITIONS ---
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
SERVO = 19

# --- PICAMERA2 LIVE VLC STREAM CONFIGURATION ---
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (1280, 720)}, transform=libcamera.Transform(vflip=1))  # 720p HD stream
picam2.configure(config)

# Setup H264 Encoder for the live network stream
stream_encoder = H264Encoder(bitrate=5000000)  # 5 Mbps bandwidth allocation

# Wrap the stream in an MPEG-TS container and broadcast via UDP to the PC on port 5000
vlc_stream_output = FfmpegOutput(f"-f mpegts udp://{REMOTE_IP}:5000?pkt_size=1316")

# Start camera and begin continuous streaming to VLC immediately
picam2.start()
picam2.start_recording(stream_encoder, vlc_stream_output)
print(f"Live stream broadcasting to VLC at udp://{REMOTE_IP}:5000")

# --- DEFAULT CONTROL STATES ---
left_trigger = -1.0
right_trigger = -1.0
left_stick_x = 0.0
right_stick_x = 0.0
dpad = (0, 0)

current_input = ""
previous_dpad = (0, 0)

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
for pin in [NSLEEP1, NSLEEP2, AN11, AN12, BN11, BN12, AN21, AN22, BN21, BN22, SERVO]:
    GPIO.setup(pin, GPIO.OUT)
    if pin != NSLEEP1 and pin != NSLEEP2 and pin != SERVO:
        GPIO.output(pin, GPIO.LOW)

p1 = GPIO.PWM(NSLEEP1, 200)
p2 = GPIO.PWM(NSLEEP2, 200)
p1.start(0)
p2.start(0)

servo1 = GPIO.PWM(SERVO, 50)
servo1.start(7)  # Starts at 90 degrees
time.sleep(0.35)
servo1.ChangeDutyCycle(0)

servo_angle = 90
last_servo_angle = 90
forward = True
backward = False


# --- MOTOR CONTROL HELPER FUNCTIONS ---
def set_left_speed(speed):
    p1.ChangeDutyCycle(speed)


def set_right_speed(speed):
    p2.ChangeDutyCycle(speed)


def set_speed(speed):
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)


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


def straight(direction):
    if direction == forward:
        left_wheels(forward)
        right_wheels(forward)
    else:
        left_wheels(backward)
        right_wheels(backward)


def stop_motors():
    set_speed(0)
    for pin in [AN11, AN12, BN11, BN12, AN21, AN22, BN21, BN22]:
        GPIO.output(pin, GPIO.LOW)


def read_message(msg):
    split_message = msg.split(" ")
    print(split_message)
    global current_input;
    current_input = split_message[0]

    if current_input == "dpad":
        global dpad;
        dpad = tuple([int(direction) for direction in split_message[1:]])
    elif split_message[0] == "left_stick":
        global left_stick_x;
        left_stick_x = float(split_message[1])
    elif split_message[0] == "right_stick":
        global right_stick_x;
        right_stick_x = float(split_message[1])
    elif split_message[0] == "left_trigger":
        global left_trigger;
        left_trigger = float(split_message[1])
    elif split_message[0] == "right_trigger":
        global right_trigger;
        right_trigger = float(split_message[1])
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
    # Omni-movement via D-Pad
    if current_input == "dpad":
        global previous_dpad
        if dpad != previous_dpad:
            stop_motors()
            set_speed(75)
            previous_dpad = dpad
        match dpad:
            case (0, 0):
                stop_motors()
            case (0, 1):
                straight(forward)
            case (0, -1):
                straight(backward)
            case (1, 0):
                front_left(forward)
                back_right(forward)
                front_right(backward)
                back_left(backward)
            case (-1, 0):
                front_left(backward)
                back_right(backward)
                front_right(forward)
                back_left(forward)
            case (-1, -1):
                front_left(backward)
                back_right(backward)
            case (-1, 1):
                front_right(forward)
                back_left(forward)
            case (1, 1):
                front_left(forward)
                back_right(forward)
            case (1, -1):
                front_right(backward)
                back_left(backward)

    # Driving / Steering motor control
    elif current_input in ["left_trigger", "right_trigger", "left_stick"]:
        left_val = (left_trigger + 1) / 2
        right_val = (right_trigger + 1) / 2
        diff = right_val - left_val

        if abs(diff) < 0.05:  # Stationary turning in-place
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
        else:  # Moving forward/backward with turning adjustments
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
        global servo_angle, last_servo_angle
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


# --- MAIN CONTROL RECEIVE LOOP ---
try:
    while True:
        message, address = server.recvfrom(1024)
        server.sendto("Message Received".encode("utf-8"), address)
        message = message.decode("utf-8")
        read_message(message)
        move_motors()
        if not message:
            break
finally:
    server.close()
    picam2.stop_recording()
    print("end")