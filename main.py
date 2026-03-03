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
from android import AndroidService  # Background service ke liye

# --- MASTER CONFIG ---
API_KEY = "AIzaSyCRqE6NrySBhTPbYAKM3TPJ9qlaDSJNH3E" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ZaraAutoMaster(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # Start Background Service
        self.service = AndroidService('ZaraService', 'running')
        self.service.start('service started')
        
        layout = MDBoxLayout(orientation='vertical', padding=20)
        self.status = MDLabel(text="ZARA: SERVICE ACTIVE", halign="center", font_style="H4", theme_text_color="Custom", text_color=(0, 1, 1, 1))
        self.output = MDLabel(text="I am watching in the background, Mr. Ram.", halign="center", font_style="H6")
        
        layout.add_widget(self.status)
        layout.add_widget(self.output)
        
        Clock.schedule_interval(self.ram_cleaner, 300)
        threading.Thread(target=self.listener, daemon=True).start()
        return layout

    def ram_cleaner(self, dt):
        gc.collect()

    def listener(self):
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source, duration=1)
            while True:
                try:
                    audio = rec.listen(source)
                    cmd = rec.recognize_google(audio, language="en-IN").lower()
                    if "zara" in cmd or "jarvis" in cmd:
                        Clock.schedule_once(lambda dt: self.execute_auto_logic(cmd))
                except: continue

    def execute_auto_logic(self, query):
        if any(x in query for x in ["message", "reply", "bhej", "potai"]):
            threading.Thread(target=self.ai_auto_drafter, args=(query,)).start()
        elif "instagram" in query:
            os.system("am start -n com.instagram.android/com.instagram.main.Activity")
        elif "zubeen" in query:
            webbrowser.open("https://www.youtube.com/results?search_query=zubeen+garg+songs")
        else:
            threading.Thread(target=self.normal_ai, args=(query,)).start()

    def ai_auto_drafter(self, user_cmd):
        try:
            prompt = f"Ram is busy. He said '{user_cmd}'. Write a short professional message in 1 line."
            res = model.generate_content(prompt)
            final_msg = res.text
            Clock.schedule_once(lambda dt: self.show_and_speak(f"Drafted: {final_msg}"))
            os.system("am start -n com.instagram.android/com.instagram.direct.HomeActivity")
        except:
            self.show_and_speak("AI error.")

    def normal_ai(self, query):
        res = model.generate_content(query)
        self.show_and_speak(res.text)

    def show_and_speak(self, text):
        Clock.schedule_once(lambda dt: setattr(self.output, 'text', text))
        self.speak(text)

    def speak(self, text):
        def v():
            try:
                tts = gTTS(text=text, lang='en')
                tts.save("s.mp3")
                snd = SoundLoader.load("s.mp3")
                if snd: snd.play()
            except: pass
        threading.Thread(target=v).start()

if __name__ == "__main__":
    ZaraAutoMaster().run()
