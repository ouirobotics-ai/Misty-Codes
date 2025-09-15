from vosk import Model, KaldiRecognizer
import wave
import json

# Path to your saved audio file from Misty
AUDIO_FILE = "voice_test.wav"

# Load Vosk model (make sure you downloaded + unzipped it)
MODEL_PATH = r"C:\Users\HP\Desktop\Misty-Codes\vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Open audio file
wf = wave.open(AUDIO_FILE, "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    raise ValueError("❌ Audio file must be WAV mono PCM 16bit 16kHz")

# Process audio in chunks
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print("Partial:", result["text"])

# Final result
final = json.loads(recognizer.FinalResult())
print("✅ Final transcription:", final["text"])
