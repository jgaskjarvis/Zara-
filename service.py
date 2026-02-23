import time
import speech_recognition as sr

def start_listening():
    r = sr.Recognizer()
    r.energy_threshold = 300
    while True:
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, phrase_time_limit=3)
                text = r.recognize_google(audio, language='en-in').lower()
                if "zara" in text:
                    print("Wake word detected!")
                    # Service yahan se main app ko jaga degi
            except:
                continue
        time.sleep(1)

if __name__ == '__main__':
    start_listening()