import socket
import pygame

pygame.init()
pygame.joystick.init()

# Check if a controller is connected
if pygame.joystick.get_count() == 0:
    print("No controller connected.")
    quit()

# Get the first Joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# HOST= "localhost" # Localhost Connection
HOST = "172.20.10.6" # Jerry connection
PORT = 9999

current_input = ""
value = ""
message = ""

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.05)
client.sendto("Hello".encode("utf-8"), (HOST, PORT))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.JOYAXISMOTION:

            # Left Stick x-axis
            if event.axis == 0:
                current_input = "left_stick"
                if abs(event.value) > 0.05:
                    value = round(event.value, 2)
                else:
                    value = 0

            # Right Stick x-axis
            elif event.axis == 2:
                current_input = "right_stick"
                if abs(event.value) > 0.05:
                    value = round(event.value, 2)
                else:
                    value = 0

            # Left Trigger, axis 4 on windows pc, axis 2 on raspberry pi
            elif event.axis == 4:
                current_input = "left_trigger"
                if event.value <= -0.9:
                    value = -1.0
                else:
                    value = event.value

            # Right trigger
            elif event.axis == 5:
                current_input = "right_trigger"
                if event.value <= -0.9:
                    value = -1.0
                else:
                    value = event.value

        elif event.type == pygame.JOYBUTTONUP:

            # Ends program
            if event.button == 0:
                running = False
                current_input = "end"

        elif event.type == pygame.JOYHATMOTION:
            # Dpad
            current_input = "dpad"
            dpad = event.value
            x, y = dpad
            value = f"{x} {y}"

        message = f"{current_input} {value}"
        client.sendto(message.encode("utf-8"), (HOST, PORT))

    try:
        print(f"{message}, {client.recv(1024).decode("utf-8")}")
    except socket.timeout:
        print("No response")
    clock.tick(60)
    if current_input == "end":
        client.close()