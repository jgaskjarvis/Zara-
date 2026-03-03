[app]
# (str) Title of your application
title = ZARA Auto Master

# (str) Package name
package.name = zara_auto_ram

# (str) Package domain (needed for android packaging)
package.domain = org.ram.zara

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,mp3

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Yahan maine aapki sari libraries add kar di hain
requirements = python3, kivy==2.3.0, kivymd==1.2.0, google-generativeai, speech_recognition, gTTS, certifi, chardet, idna, urllib3, requests, PyAudio, pydbus

# (str) Custom source folders for services
services = ZaraService:service.py

# (list) Permissions
# Zara ko mic, internet aur background mein chalne ki permission chahiye
android.permissions = INTERNET, RECORD_AUDIO, FOREGROUND_SERVICE, WAKE_LOCK, MODIFY_AUDIO_SETTINGS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) indicates if the application should be fullscreen or not
fullscreen = 0

# (list) List of Java .jar files to add to the libs dir
# android.add_jars = foo.jar,bar.jar,path/to/baz.jar

# (list) List of Java files to add to the android/src folder
# android.add_src = src/MyActivity.java

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library to project
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
