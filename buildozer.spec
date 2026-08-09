[app]
title = دوربین و متن فارسی
package.name = persiantts
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = CAMERA,INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# آیکون و اسپلش اختیاری - در صورت داشتن عکس، مسیر آن را اینجا بگذارید
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
