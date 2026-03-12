import pygame

pygame.init()
pygame.joystick.init()

# Check if a controller is connected
if pygame.joystick.get_count() == 0:
    print("No controller connected.")
    quit()

# Get the first joystick
joystick = pygame.joystick.Joystick(0)

print("Controller detected:", joystick.get_name())

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")

        if event.type == pygame.JOYBUTTONUP:
            print(f"Button {event.button} released")

        if event.type == pygame.JOYAXISMOTION:
            print(f"Axis {event.axis} value {event.value:.2f}")

        if event.type == pygame.JOYHATMOTION:
            print(f"D-pad {event.value}")

        if event.type == pygame.QUIT:
            running = False
