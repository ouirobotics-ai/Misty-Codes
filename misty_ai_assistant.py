import os
import time
from dotenv import load_dotenv
from mistyPy.Robot import Robot

# Load Misty IP from .env
load_dotenv()
MISTY_IP = os.getenv("MISTY_IP")
misty = Robot(MISTY_IP)

print("🎤 Recording your voice (5s)...")
misty.start_recording_audio("voice_test.wav")
time.sleep(5)
misty.stop_recording_audio()
print("✅ Saved recording on Misty as voice_test.wav")

# --- Download from Misty to your computer ---
response = misty.get_audio_file("voice_test.wav")

if response and hasattr(response, "content"):
    local_filename = "voice_test.wav"
    with open(local_filename, "wb") as f:
        f.write(response.content)   # <-- use .content here
    print(f"💾 File downloaded to PC as {local_filename}")
else:
    print("❌ Failed to fetch file from Misty")

# Misty plays it back out loud
misty.play_audio("voice_test.wav")
time.sleep(3)

# Misty gives her own spoken response
misty.speak("I heard you! This was recorded using my microphone.")
