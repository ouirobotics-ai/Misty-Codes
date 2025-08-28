import pygame
import sys
import time
import os
from dotenv import load_dotenv
from mistyPy.Robot import Robot


# Hey shregna

# --- Setup ---
load_dotenv()
misty_ip = os.getenv("MISTY_IP", "127.0.0.1")
misty = Robot(misty_ip)

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected!")
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller detected: {joystick.get_name()}")

def clamp_axis(value, deadzone=0.1):  # smaller deadzone for testing
    if abs(value) < deadzone:
        return 0.0
    return float(round(value, 2))

while True:
    pygame.event.pump()

    # Raw axes
    raw_axes = [round(joystick.get_axis(i), 3) for i in range(joystick.get_numaxes())]
    print(f"Raw axes: {raw_axes}")

    # --- Left Stick (drive) ---
    lx = clamp_axis(joystick.get_axis(0))
    ly = -clamp_axis(joystick.get_axis(1))

    if lx == 0.0 and ly == 0.0:
        misty.drive(0, 0)
    else:
        misty.drive(ly * 50, lx * 50)
        print(f"Driving: linear={ly}, angular={lx}")

    # --- Right Stick (head control) ---
    rx = clamp_axis(joystick.get_axis(3))
    ry = -clamp_axis(joystick.get_axis(4))

    if rx != 0.0 or ry != 0.0:
        yaw = int(rx * 40)
        pitch = int(ry * 40)
        misty.move_head(pitch, yaw, 0, 50)
        print(f"Head: yaw={yaw}, pitch={pitch}")

    time.sleep(0.1)
