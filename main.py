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

try:
    from android.permissions import request_permissions, Permission
    from android import AndroidService
except ImportError:
    AndroidService = None

# API Configuration
API_KEY = "AIzaSyCRqE6NrySBhTPbYAKM3TPJ9qlaDSJNH3E" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ZaraAutoMaster(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        if AndroidService:
            request_permissions([Permission.RECORD_AUDIO, Permission.INTERNET])
            # Service registration name 'ZaraService' jo spec file se match karega
            try:
                self.service = AndroidService('ZaraService', 'running')
                self.service.start('ZARA is running in background')
            except Exception as e:
                print(f"Service Error: {e}")
        
        layout = MDBoxLayout(orientation='vertical', padding=20)
        self.status = MDLabel(text="ZARA: ONLINE", halign="center", font_style="H4")
        self.output = MDLabel(text="Listening for Mr. Ram...", halign="center", font_style="H6")
        
        layout.add_widget(self.status)
        layout.add_widget(self.output)
        
        Clock.schedule_once(self.start_jarvis, 1)
        return layout

    def start_jarvis(self, dt):
        threading.Thread(target=self.listener, daemon=True).start()

    def listener(self):
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                try:
                    audio = rec.listen(source)
                    cmd = rec.recognize_google(audio, language="en-IN").lower()
                    if "zara" in cmd or "jarvis" in cmd:
                        Clock.schedule_once(lambda dt: self.run_cmd(cmd))
                except: continue

    def run_cmd(self, query):
        if "instagram" in query:
            os.system("am start -n com.instagram.android/com.instagram.main.Activity")
        elif "zubeen" in query:
            webbrowser.open("https://www.youtube.com/results?search_query=zubeen+garg+songs")
        else:
            res = model.generate_content(query)
            self.reply(res.text)

    def reply(self, text):
        Clock.schedule_once(lambda dt: setattr(self.output, 'text', text))
        self.speak(text)

    def speak(self, text):
        def p():
            try:
                tts = gTTS(text=text, lang='en')
                tts.save("s.mp3")
                snd = SoundLoader.load("s.mp3")
                if snd: snd.play()
            except: pass
        threading.Thread(target=p).start()

if __name__ == "__main__":
    ZaraAutoMaster().run()
