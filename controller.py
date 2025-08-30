import pygame
import sys
import time
import os
import subprocess
from mistyPy.Events import Events
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
    """Clamp joystick axis with deadzone filtering."""
    return 0.0 if abs(value) < deadzone else float(round(value, 2))

# --- Face recognition callback ---
last_seen = {}
COOLDOWN = 5   # seconds

def on_face(data):
    global last_seen
    label = data["message"].get("label", "unknown person")
    now = time.time()

    if label not in last_seen or now - last_seen[label] > COOLDOWN:
        last_seen[label] = now
        if label == "unknown person":
            misty.display_image("e_Surprise.jpg")
            misty.transition_led(255, 0, 0, 0, 0, 255, "Blink", 200)
            misty.speak("I see someone new.", 1, voice="English 12 (India)")
        else:
            misty.display_image("e_Joy2.jpg")
            misty.change_led(0, 255, 0)
            misty.speak(f"Hi {label}!", 1, voice="English 12 (India)")
            misty.move_arms(80, -80, 50, 50)
            time.sleep(0.8)
            misty.move_arms(0, 0, 50, 50)
    else:
        print(f"Skipping {label}, still on cooldown.")

# Track previous joystick positions and last commanded angles
prev_lx, prev_ly = 0.0, 0.0
prev_rx, prev_ry = 0.0, 0.0
last_commanded_yaw = 0
last_commanded_pitch = 0

# Keep track of recognition state
face_recognition_active = False

while True:
    pygame.event.pump()

    # --- R3 Button (9) → Stop All Movement ---
    if joystick.get_button(9):
        # Stop drive movement
        misty.stop()
        # Send a command to stop the head at its last commanded position
        misty.move_head(last_commanded_pitch, 0, last_commanded_yaw, velocity=0)
        print("R3 pressed, stopping all movement.")
        # Ensure we don't accidentally send a new command after
        prev_lx, prev_ly = 0.0, 0.0
        prev_rx, prev_ry = 0.0, 0.0
    
    # --- Otherwise, continue with normal control logic ---
    else:
        # Get left stick values for drive movement
        lx = clamp_axis(joystick.get_axis(0))
        ly = clamp_axis(joystick.get_axis(1))
        # Get right stick values for pitch and yaw
        rx = clamp_axis(joystick.get_axis(2))
        ry = clamp_axis(joystick.get_axis(3))
        
        # --- Drive Movement with Left Stick ---
        if (abs(lx - prev_lx) > 0.1 or abs(ly - prev_ly) > 0.1) and (lx != 0.0 or ly != 0.0):
            # Map stick positions to drive velocities
            target_linear = int(-ly * 100)
            target_angular = int(-lx * 100)

            # Send the drive command
            misty.drive(target_linear, target_angular)
            print(f"[Drive control] linear={target_linear}, angular={target_angular}")

            # Update previous joystick position
            prev_lx = lx
            prev_ly = ly
        
        # --- Head Movement with Right Stick ---
        if abs(rx - prev_rx) > 0.1 or abs(ry - prev_ry) > 0.1:
            
            # Map stick positions to target head angles
            target_yaw = int(rx * 81)           # left/right yaw
            target_pitch = int(ry * 40)         # up/down pitch

            # Clamp to Misty’s ranges
            target_yaw = max(-81, min(81, target_yaw))
            target_pitch = max(-40, min(25, target_pitch))

            # Send the command to move to the exact position
            misty.move_head(int(target_pitch), 0, int(target_yaw), velocity=50)
            print(f"[Head control] pitch={int(target_pitch)}, yaw={int(target_yaw)}")

            # Update previous joystick position and last commanded angles
            prev_rx = rx
            prev_ry = ry
            last_commanded_yaw = target_yaw
            last_commanded_pitch = target_pitch


    # --- A button (0) → start face recognition ---
    if joystick.get_button(0) and not face_recognition_active:
        print("A pressed → Start face recognition")
        misty.speak("Starting face recognition.", 1)
        misty.register_event(
            event_name="face_recognition_event",
            event_type=Events.FaceRecognition,
            callback_function=on_face,
            keep_alive=True
        )
        face_recognition_active = True
        # Small wave just to confirm
        misty.move_arms(90, 70, 0, 0)
        time.sleep(0.5)
        misty.move_arms(90, 90, 0, 0)

    # --- B button (1) → stop face recognition + reset pose ---
    if joystick.get_button(1) and face_recognition_active:
        print("B pressed → Stop face recognition & reset body")
        misty.speak("Stopping face recognition.", 1)
        misty.unregister_all_events()
        misty.stop_face_recognition()
        misty.change_led(0, 0, 0)
        misty.move_head(0, 0, 0, velocity=30)
        misty.move_arms(90, 90, 0, 0)
        face_recognition_active = False

    # --- START button (7) → exit program ---
    if joystick.get_button(7):
        print("START pressed → Exiting program.")
        misty.speak("Shutting down controller program.", 1)
        if face_recognition_active:
            misty.unregister_all_events()
            misty.stop_face_recognition()
        time.sleep(0.5)
        sys.exit(0)

    time.sleep(0.01)