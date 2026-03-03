[app]
title = ZARA Auto Master
package.name = zara_auto_ram
package.domain = org.ram.zara
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 1.0

# Sabhi zaroori libraries yahan hain
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, google-generativeai, pyjnius

# Permissions for AI and Voice
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, MODIFY_AUDIO_SETTINGS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
fullscreen = 0

# Ye line zaroori hai debugging ke liye
android.logcat_filters = *:S python:D
