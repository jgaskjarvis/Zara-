[app]
# (str) Title of your application
title = Zara AI

# (str) Package name
package.name = zaraai

# (str) Package domain (needed for android packaging)
package.domain = org.ram.zara

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp3

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3, kivy==2.3.0, kivymd, pyjnius, gtts, google-generativeai, speechrecognition, requests, urllib3, certifi, chardet, android

# (str) Supported orientation
orientation = portrait

# (list) Permissions (Background listening ke liye zaruri permissions)
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, QUERY_ALL_PACKAGES, FOREGROUND_SERVICE, WAKE_LOCK

# (str) Services (Yahan humne aapka background service file jod diya hai)
services = ZaraService:service.py

# (int) Android API level
android.api = 33
android.minapi = 21
android.ndk = 25b

# (bool) Use private storage for the app
android.private_storage = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

[buildozer]
# (int) Log level (2 = debug info)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1