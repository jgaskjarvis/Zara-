import os
import threading
import gc
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import webbrowser

# Safe Import for Android Service
try:
    from android import AndroidService
    from android.permissions import request_permissions, Permission
except ImportError:
    AndroidService = None

# --- MASTER CONFIG ---
# Maine aapki API key yahan jod di hai.
API_KEY = "AIzaSyCRqE6NrySBhTPbYAKM3TPJ9qlaDSJNH3E" 
genai.configure(api_key=API_KEY) # API key ko configure kiya gaya.
model = genai.GenerativeModel('gemini-pro')

class ZaraAutoMaster(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # Request Permissions for Mic and Internet
        if AndroidService:
            request_permissions([Permission.RECORD_AUDIO, Permission.INTERNET])
            # Service start karne ka logic yahan hai.
            self.service = AndroidService('ZaraService', 'running')
            self.service.start('service started')
        
        layout = MDBoxLayout(orientation='vertical', padding=20)
        self.status = MDLabel(text="ZARA: ACTIVE", halign="center", font_style="H4")
        self.output = MDLabel(text="Waiting for command, Mr. Ram", halign="center", font_style="H6")
        
        layout.add_widget(self.status)
        layout.add_widget(self.output)
        
        # RAM cleaner har 5 minute mein chalta hai.
        Clock.schedule_interval(self.ram_cleaner, 300)
        # Listener ko alag thread mein start kiya gaya hai.
        threading.Thread(target=self.listener, daemon=True).start()
        return layout

    def ram_cleaner(self, dt):
        gc.collect() # Garbage collection RAM clean karne ke liye.

    def listener(self):
        rec = sr.Recognizer()
        # Microphone se command sunne ka logic.
        with sr.Microphone() as source:
            while True:
                try:
                    audio = rec.listen(source, timeout=5)
                    cmd = rec.recognize_google(audio, language="en-IN").lower()
                    # Agar "zara" ya "jarvis" bola jaye toh command execute hogi.
                    if "zara" in cmd or "jarvis" in cmd:
                        Clock.schedule_once(lambda dt: self.execute_auto_logic(cmd))
                except: continue

    def execute_auto_logic(self, query):
        # Instagram open karne ke liye command.
        if "instagram" in query:
            os.system("am start -n com.instagram.android/com.instagram.main.Activity")
        # YouTube par Zubeen Garg ke gaane search karne ke liye command.
        elif "zubeen" in query:
            webbrowser.open("https://www.youtube.com/results?search_query=zubeen+garg+songs")
        # Baaki queries Gemini AI se process hongi.
        else:
            res = model.generate_content(query)
            self.show_and_speak(res.text)

    def show_and_speak(self, text):
        # UI update aur speak function call.
        Clock.schedule_once(lambda dt: setattr(self.output, 'text', text))
        self.speak(text)

    def speak(self, text):
        def v():
            try:
                # Text-to-speech convert karke play karne ka logic.
                tts = gTTS(text=text, lang='en')
                tts.save("s.mp3")
                snd = SoundLoader.load("s.mp3")
                if snd: snd.play()
            except: pass
        threading.Thread(target=v).start()

if __name__ == "__main__":
    ZaraAutoMaster().run()
