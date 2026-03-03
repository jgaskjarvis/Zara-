[app]
# (str) Title of your application
title = ZARA Auto Master

# (str) Package name
package.name = zara_auto_ram

# (str) Package domain (needed for android packaging)
package.domain = org.ram.zara

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,mp3

# (str) Application versioning
version = 1.0

# (list) Application requirements
# [span_1](start_span)PyAudio aur pydbus hata diye gaye hain kyunki wo Android par support nahi karte[span_1](end_span)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, google-generativeai, speech_recognition, gTTS, certifi, chardet, idna, urllib3, requests

# (str) Custom source folders for services
services = ZaraService:service.py

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, MODIFY_AUDIO_SETTINGS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) indicates if the application should be fullscreen or not
fullscreen = 0

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library to project
android.copy_libs = 1

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
