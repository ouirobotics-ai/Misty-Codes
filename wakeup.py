import os
from dotenv import load_dotenv
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time
# Load .env file
load_dotenv()

# Get Misty IP from environment
MISTY_IP = os.getenv("MISTY_IP")

# Connect to Misty
misty = Robot(MISTY_IP)


misty.display_image("e_SleepingZZZ.jpg", 1)
misty.play_audio("e_Sleepy.wav", 50)
misty.move_head(60, 0, 0, 80)
misty.move_arms(85, 85, 80, 80)
misty.change_led(0, 0, 255)
misty.start_key_phrase_recognition()

def Key_Phrase_Recognized(data):
    print(data)
    misty.display_image("e_Surprise.jpg", 1)
    misty.play_audio("s_PhraseHello.wav", 50)
    time.sleep(2)
    misty.speak("Good morning")
    misty.move_head(0, 0, 0, 80)
    misty.move_arms(-85, -85, 80, 80)

misty.register_event(event_name='Key_Phrase_Recognized', event_type=Events.KeyPhraseRecognized, callback_function=Key_Phrase_Recognized, keep_alive=True)
misty.keep_alive()