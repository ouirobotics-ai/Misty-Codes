import speech_recognition as sr
from mistyPy.Robot import Robot
import time

MISTY_IP = "10.1.14.125"
DEVICE_INDEX = 9

misty = Robot(MISTY_IP)

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=DEVICE_INDEX)

print("🎤 Listening... Say 'Hey Misty' to wake her up.")

active = False

while True:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"Heard: {text}")

        # Wake word
        if "hey misty" in text and not active:
            print("🔔 Wake word detected!")
            misty.speak("Hi! I'm here!")
            misty.change_led(0, 255, 0)
            active = True

        # Commands
        elif active:
            if any(word in text for word in ["wave", "hello", "hi"]):
                misty.speak("Waving at you!")
                misty.move_arms(70, -70)
                time.sleep(1)
                misty.move_arms(0, 0)

            elif any(word in text for word in ["dance", "move", "party"]):
                misty.speak("Let's dance!")
                misty.drive(50, 50)
                time.sleep(1.5)
                misty.drive(-50, -50)
                time.sleep(1.5)
                misty.stop()

            elif "goodbye" in text or "stop" in text:
                misty.speak("Goodbye!")
                misty.change_led(255, 0, 0)
                break

    except sr.UnknownValueError:
        continue
    except sr.RequestError as e:
        print(f"API error: {e}")
        break
