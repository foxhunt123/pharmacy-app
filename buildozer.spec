[app]
title = PharmacyApp
package.name = pharmacyapp
package.domain = org.example

version = 1.0

source.dir = .
source.include_exts = py,json,png,jpg

requirements = python3,kivy,kivymd

orientation = portrait

[buildozer]
log_level = 2

[android]
permissions = CAMERA

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version=33.0.2
android.accept_sdk_license = True 
