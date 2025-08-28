import os
from dotenv import load_dotenv
from mistyPy.Robot import Robot
from mistyPy.Events import Events
import google.generativeai as genai

# --- Load .env ---
load_dotenv()
MISTY_IP = os.getenv("MISTY_IP")
API_KEY = os.getenv("GEMINI_API_KEY")

if not MISTY_IP:
    raise ValueError("❌ MISTY_IP not found in .env")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# --- Connect to Misty ---
misty = Robot(MISTY_IP)

# --- Setup Gemini ---
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Event Callbacks ---

# Triggered when Misty hears "Hey Misty"
def on_wake(data):
    print("✅ Heard wake word: Hey Misty")
    misty.speak("Yes, I am listening.")

    # Register voice event only when needed
    misty.register_event("voice", Events.VoiceRecord, on_voice, keep_alive=False)

    # Start recording until 10s silence
    misty.capture_speech(maxSpeechLength=20, silenceTimeout=10)

# Triggered when Misty finishes listening
def on_voice(data):
    msg = data["message"]
    transcript = msg.get("speechRecognitionResult", "")
    print("🎤 Transcript:", transcript)

    if not transcript:
        misty.speak("Sorry, I didn't hear anything.")
        return

    # --- Send transcript to Gemini ---
    try:
        response = model.generate_content(transcript)
        answer = response.text
    except Exception as e:
        answer = "I had trouble answering that."
        print("❌ Gemini error:", e)

    print("🤖 Gemini replied:", answer)
    misty.speak(answer)

# --- Start wake-word recognition ---
misty.start_key_phrase_recognition()

# Register wake event (persistent)
misty.register_event("wake", Events.KeyPhraseRecognized, on_wake, keep_alive=True)

print("🚀 Say 'Hey Misty' to wake her up!")
misty.keep_alive()
