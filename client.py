import socket
import pygame

pygame.init()
pygame.joystick.init()

# Verify controller connectivity
if pygame.joystick.get_count() == 0:
    print("No controller connected.")
    quit()

joystick = pygame.joystick.Joystick(0)
#joystick.init()

# --- NETWORK CONFIGURATION ---
HOST = "172.20.10.4"  # Raspberry Pi IP Address (or "jerry.local")
PORT = 9999           # Target UDP Port on the Pi

current_input = ""
value = ""
message = ""

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.05)
client.sendto("Hello".encode("utf-8"), (HOST, PORT))

clock = pygame.time.Clock()
running = True

print("Controller interface online. Relay active...")

# --- MAIN CONTROLLER LOOP ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Left Stick x-axis
            if event.axis == 0:
                current_input = "left_stick"
                value = round(event.value, 2) if abs(event.value) > 0.05 else 0

            # Right Stick x-axis
            elif event.axis == 2:
                current_input = "right_stick"
                value = round(event.value, 2) if abs(event.value) > 0.05 else 0

            # Left Trigger
            elif event.axis == 4:
                current_input = "left_trigger"
                value = -1.0 if event.value <= -0.9 else event.value

            # Right trigger
            elif event.axis == 5:
                current_input = "right_trigger"
                value = -1.0 if event.value <= -0.9 else event.value

        elif event.type == pygame.JOYBUTTONUP:
            # Button 0 ends the program
            if event.button == 0:
                running = False
                current_input = "end"
                value = ""

        elif event.type == pygame.JOYHATMOTION:
            # Dpad Movement
            current_input = "dpad"
            x, y = event.value
            value = f"{x} {y}"

        # Construct and send command package to the Pi
        message = f"{current_input} {value}"
        client.sendto(message.encode("utf-8"), (HOST, PORT))

    # Listen for acknowledgment from the Pi without freezing the UI
    try:
        ack = client.recv(1024).decode('utf-8')
        print(f"Sent: {message} | Reply: {ack}")
    except socket.timeout:
        pass

    clock.tick(60)

# Clean up connections on exit
client.close()
print("Client shutdown complete.")