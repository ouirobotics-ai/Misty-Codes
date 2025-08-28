import pygame
import sys
import time
import os
import subprocess
from dotenv import load_dotenv
from mistyPy.Robot import Robot

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

def clamp_axis(value, deadzone=0.15):
    return 0.0 if abs(value) < deadzone else float(round(value, 2))

# Track head angles
head_yaw = 0
head_pitch = 0

# Track subprocess for face detection
face_proc = None

while True:
    pygame.event.pump()

    # --- Right Stick (head control only) ---
    # --- Right Stick (head control only) ---
    rx = clamp_axis(joystick.get_axis(3))
    ry = clamp_axis(joystick.get_axis(4))  # 👈 remove the extra minus sign here

    if rx != 0.0 or ry != 0.0:
        head_yaw = max(-90, min(90, head_yaw + int(rx * 5)))
        head_pitch = max(-40, min(40, head_pitch - int(ry * 5)))  # 👈 subtract so up stick = up head
        misty.move_head(head_pitch, head_yaw, 0, 50)
        print(f"[Head control] yaw={head_yaw}, pitch={head_pitch}")

    # --- Button R1 (index 5 on most controllers) → run face_detection.py ---
    if joystick.get_button(5):  # R1
        if face_proc is None or face_proc.poll() is not None:
            print("▶ Starting face_detection.py")
            face_proc = subprocess.Popen(
                ["python", "face_detection.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            misty.speak("Face detection started.", 1)
            time.sleep(0.5)

    # --- Button START (index 7 on Xbox / PS controllers) → stop face_detection.py ---
    if joystick.get_button(7):  # START button
        if face_proc is not None and face_proc.poll() is None:
            print("⏹ Stopping face_detection.py")
            face_proc.terminate()
            misty.speak("Face detection stopped.", 1)
            face_proc = None
            time.sleep(0.5)

    # --- Exit on A / Cross (button 0) ---
    if joystick.get_button(0):
        print("Exiting controller loop.")
        if face_proc is not None and face_proc.poll() is None:
            face_proc.terminate()
        break

    time.sleep(0.1)
