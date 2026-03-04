[app]
# App ka naam aur details
title = ZARA Auto Master
package.name = zara_auto_ram
package.domain = org.ram.zara
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 1.0

# REQUIREMENTS: Maine Gemini AI ke liye zaroori dependencies add kar di hain
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, google-generativeai, pyjnius, openssl, sqlite3, setuptools, hostpython3, charset-normalizer

# PERMISSIONS: Storage permissions add ki hain taaki awaaz save ho sake
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# ANDROID SETTINGS: Aapke Vivo phone ke liye stable version
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# SERVICE: Background mein Jarvis ko chalane ke liye
services = ZaraService:service.py

[buildozer]
log_level = 2
warn_on_root = 1
