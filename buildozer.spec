[app]
title = ZARA Auto Master
package.name = zara_auto_ram
package.domain = org.ram.zara
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 1.0

# In requirements ko dhyan se copy karein
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, google-generativeai, pyjnius, openssl

android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK

# Naye Android requirements ke hisaab se
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Background service registration
services = ZaraService:service.py

[buildozer]
log_level = 2
