import speech_recognition as sr

def listen():
    print("\nChoose input mode:")
    print("1. Voice (speak)")
    print("2. Text (type)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤  Listening... (Speak now)")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        try:
            text = recognizer.recognize_google(audio, language="en-IN")
            print(f"You (voice): {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏱️ No voice detected, switching to text mode.")
            return input("You (text): ")
        except Exception as e:
            print("Didn't catch that, please type manually.")
            return input("You (text): ")
    else:
        return input("You (text): ")
