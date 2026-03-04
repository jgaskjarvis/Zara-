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

# Safe Import for Android
try:
    from android.permissions import request_permissions, Permission
    from android import AndroidService
except ImportError:
    AndroidService = None

# --- MASTER CONFIG ---
API_KEY = "AIzaSyCRqE6NrySBhTPbYAKM3TPJ9qlaDSJNH3E" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ZaraAutoMaster(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # Permissions trigger timing fix
        if AndroidService:
            Clock.schedule_once(lambda dt: request_permissions([
                Permission.RECORD_AUDIO, 
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ]), 1)
        
        layout = MDBoxLayout(orientation='vertical', padding=20)
        self.status = MDLabel(text="ZARA: STARTING...", halign="center", font_style="H4")
        self.output = MDLabel(text="Initializing systems, Mr. Ram", halign="center", font_style="H6")
        
        layout.add_widget(self.status)
        layout.add_widget(self.output)
        
        # App ko load hone ke liye 3 second ka delay dijiye
        Clock.schedule_once(self.start_systems, 3)
        return layout

    def start_systems(self, dt):
        # UI update
        self.status.text = "ZARA: ONLINE"
        self.output.text = "Listening for your voice..."
        
        # Background threads start karein
        threading.Thread(target=self.listener, daemon=True).start()
        Clock.schedule_interval(self.ram_cleaner, 300)
        
        # Service start logic
        if AndroidService:
            try:
                self.service = AndroidService('ZaraService', 'running')
                self.service.start('ZARA Background Active')
            except: pass

    def ram_cleaner(self, dt):
        gc.collect()

    def listener(self):
        rec = sr.Recognizer()
        # Microphone access with safety
        try:
            with sr.Microphone() as source:
                while True:
                    try:
                        audio = rec.listen(source, timeout=None)
                        cmd = rec.recognize_google(audio, language="en-IN").lower()
                        if "zara" in cmd or "jarvis" in cmd:
                            Clock.schedule_once(lambda dt: self.run_cmd(cmd))
                    except: continue
        except Exception as e:
            # Error ko screen par dikhayega taaki pata chale mic working hai ya nahi
            Clock.schedule_once(lambda dt: setattr(self.output, 'text', f"Mic Error: {str(e)}"))

    def run_cmd(self, query):
        if "instagram" in query:
            os.system("am start -n com.instagram.android/com.instagram.main.Activity")
        elif "zubeen" in query:
            webbrowser.open("https://www.youtube.com/results?search_query=zubeen+garg+songs")
        else:
            try:
                res = model.generate_content(query)
                self.reply(res.text)
            except:
                self.reply("Sorry sir, I am having trouble connecting to Gemini.")

    def reply(self, text):
        Clock.schedule_once(lambda dt: setattr(self.output, 'text', text))
        self.speak(text)

    def speak(self, text):
        def p():
            try:
                tts = gTTS(text=text, lang='en')
                # Mobile path compatibility
                tts.save("s.mp3")
                snd = SoundLoader.load("s.mp3")
                if snd: 
                    snd.play()
            except Exception as e:
                print(f"TTS Error: {e}")
        threading.Thread(target=p).start()

if __name__ == "__main__":
    ZaraAutoMaster().run()
