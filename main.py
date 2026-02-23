import os
import threading
import base64
import certifi
from gtts import gTTS
import google.generativeai as genai
import speech_recognition as sr
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from jnius import autoclass
from android.permissions import request_permissions, Permission

# SSL Fix
os.environ['SSL_CERT_FILE'] = certifi.where()

# API Key
ENCRYPTED_KEY = "QUl6YVN5Q1gyY05XeEowUHNmajhqV2FrTEh5dExrbXpJeEJHMHdB"
genai.configure(api_key=base64.b64decode(ENCRYPTED_KEY).decode("utf-8"))
model = genai.GenerativeModel('gemini-pro')

class ZaraAI(MDApp):
    def build(self):
        request_permissions([Permission.RECORD_AUDIO, Permission.INTERNET, Permission.FOREGROUND_SERVICE])
        
        # --- Background Service Start Karne Ka Logic ---
        from android import python_service
        python_service.start_service("ZaraService", "service.py", "")
        
        self.theme_cls.theme_style = "Dark"
        screen = MDScreen()
        self.status = MDLabel(text="ZARA: ACTIVE", halign="center", font_style="H4")
        screen.add_widget(self.status)
        return screen

    def speak(self, text):
        tts = gTTS(text=text, lang='hi')
        tts.save("res.mp3")
        sound = SoundLoader.load("res.mp3")
        if sound: sound.play()

    def handle_tasks(self, query):
        if "whatsapp" in query:
            self.open_app("com.whatsapp")
            self.speak("Opening WhatsApp")
        # ... baaki apps yahan jodein ...

    def open_app(self, package):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        pm = PythonActivity.mActivity.getPackageManager()
        intent = pm.getLaunchIntentForPackage(package)
        if intent: PythonActivity.mActivity.startActivity(intent)

if __name__ == "__main__":
    ZaraAI().run()