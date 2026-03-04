[app]
title = ZARA Auto Master
package.name = zara_auto_ram
package.domain = org.ram.zara
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 1.0

# In requirements ko dhyan se copy karein (sqlite3 safety ke liye add kiya hai)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, google-generativeai, pyjnius, openssl, sqlite3

# Zaroori permissions
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Naye Android requirements ke hisaab se
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# --- YAHI WO LINE HAI JO LICENSE WALI ERROR KO KHATAM KAREGI --- 👇
android.accept_sdk_license = True
android.allow_backup = True

# Background service registration
services = ZaraService:service.py

[buildozer]
log_level = 2
warn_on_root = 1
