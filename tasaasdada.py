import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)  # your Airdopes Alpha mic index

print("🎤 Say something...")

with mic as source:
    r.adjust_for_ambient_noise(source, duration=1)
    print("Listening now...")
    audio = r.listen(source)

print("Got audio!")

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("❌ Could not understand audio")
except sr.RequestError as e:
    print("⚠️ API error:", e)
