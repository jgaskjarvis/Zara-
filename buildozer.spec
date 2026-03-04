[app]
title = ZARA Auto Master
package.name = zara_auto_ram
package.domain = org.ram.zara
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 1.0

requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, certifi, urllib3, chardet, idna, google-generativeai, pyjnius, openssl, sqlite3

android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Ye line SDK License ko apne aap accept karegi (Aidl error fix)
android.accept_sdk_license = True
android.allow_backup = True

services = ZaraService:service.py

[buildozer]
log_level = 2
warn_on_root = 1
