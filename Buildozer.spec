[app]
# (str) Title of your application
title = ZARA Auto Master

# (str) Package name
package.name = zara_auto_ram

# (str) Package domain
package.domain = org.ram.zara

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,mp3

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Note: PyAudio aur pydbus ko hata diya gaya hai kyunki wo Android par support nahi hote.
# openssl ko HTTPS/API calls ke liye add kiya gaya hai.
requirements = python3, kivy==2.3.0, kivymd==1.2.0, google-generativeai, requests, certifi, chardet, idna, urllib3, openssl, plyer

# (str) Custom source folders for services
services = zara:service.py

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, MODIFY_AUDIO_SETTINGS, READ_EXTERNAL_STORAGE

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
