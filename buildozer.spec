[app]
title = PharmacyApp
package.name = pharmacyapp
package.domain = org.example

source.dir = .
source.include_exts = py,json,png,jpg

requirements = python3,kivy,kivymd,opencv-python,pyzbar

orientation = portrait

[buildozer]
log_level = 2

[android]
permissions = CAMERA