import os
from dotenv import load_dotenv
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time

load_dotenv()
MISTY_IP = os.getenv("MISTY_IP")
misty = Robot(MISTY_IP)

is_awake = False

# --- Wake up ---
def on_keyphrase(data):
    global is_awake
    if not is_awake:
        is_awake = True
        misty.display_image("e_Surprise.jpg", 1)
        misty.play_audio("s_PhraseHello.wav", 50)
        time.sleep(1)
        misty.speak("Good morning! I'm awake and ready to chat. Ask me something.")
        misty.start_listening()   # start listening after wake-up

# --- Handle speech input ---
def on_transcription(data):
    text = data["message"]["text"].lower()
    print("Heard:", text)

    # Simple Q&A logic
    if "your name" in text or "who are you" in text:
        misty.speak("My name is Misty. I am your friendly robot assistant.")
    elif "how are you" in text:
        misty.speak("I am doing great, thank you for asking!")
    elif "dance" in text:
        misty.speak("Sure, watch me dance!")
        misty.move_arms(80, -80, 50, 50)
        misty.move_head(20, 0, 0, 70)
        time.sleep(1)
        misty.move_arms(-80, 80, 50, 50)
        misty.move_head(-20, 0, 0, 70)
    else:
        misty.speak("I'm not sure about that yet, but I'm learning every day.")

    # Keep listening for more
    time.sleep(1)
    misty.start_listening()

# --- Register events ---
misty.start_key_phrase_recognition()

misty.register_event(
    event_name="wake_event",
    event_type=Events.KeyPhraseRecognized,
    callback_function=on_keyphrase,
    keep_alive=True
)

misty.register_event(
    event_name="speech_event",
    event_type=Events.Transcription,
    callback_function=on_transcription,
    keep_alive=True
)

misty.keep_alive()
