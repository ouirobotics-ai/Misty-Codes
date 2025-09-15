import os
from dotenv import load_dotenv
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

# Load .env file
load_dotenv()
MISTY_IP = os.getenv("MISTY_IP")

# Connect to Misty
misty = Robot(MISTY_IP)

# --- Start "asleep" ---
misty.display_image("e_SleepingZZZ.jpg", 1)
misty.play_audio("e_Sleepy.wav", 50)
misty.move_head(60, 0, 0, 80)
misty.move_arms(85, 85, 80, 80)
misty.change_led(0, 0, 255)

# Track awake state
is_awake = False

# Track last seen faces for cooldown
last_seen = {}
COOLDOWN = 10  # seconds before greeting same face again


# --- Wake-up on key phrase ---
def Key_Phrase_Recognized(data):
    global is_awake
    if not is_awake:
        is_awake = True
        print("Wake word detected:", data)

        # Wake-up animation
        misty.display_image("e_Surprise.jpg", 1)
        misty.play_audio("s_PhraseHello.wav", 50)
        time.sleep(2)
        misty.speak("Good morning")
        misty.move_head(0, 0, 0, 80)
        misty.move_arms(-85, -85, 80, 80)
        misty.change_led(0, 255, 0)

        # Start face recognition after waking up
        misty.start_face_recognition()


# --- Face recognition ---
def on_face(data):
    if not is_awake:
        return  # ignore until Misty wakes up

    global last_seen
    label = data["message"].get("label", "unknown person")
    now = time.time()

    if label not in last_seen or now - last_seen[label] > COOLDOWN:
        last_seen[label] = now

        if label == "unknown person":
            misty.display_image("e_Surprise.jpg")
            misty.transition_led(255, 0, 0, 0, 0, 255, "Blink", 200)
            misty.speak("Hey stranger, let's start a conversation!", 1, voice="English 12 (India)")
        else:
            misty.display_image("e_Joy2.jpg")
            misty.change_led(0, 255, 0)
            misty.speak(f"Hey {label}, let's start a conversation!", 1, voice="English 12 (India)")

            # Friendly wave
            misty.move_arms(80, -80, 50, 50)
            time.sleep(0.8)
            misty.move_arms(0, 0, 50, 50)


# --- Event registrations ---
misty.start_key_phrase_recognition()

misty.register_event(
    event_name="wake_event",
    event_type=Events.KeyPhraseRecognized,
    callback_function=Key_Phrase_Recognized,
    keep_alive=True
)

misty.register_event(
    event_name="face_event",
    event_type=Events.FaceRecognition,
    callback_function=on_face,
    keep_alive=True
)

misty.keep_alive()
