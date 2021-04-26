# SecurityCamera
This is a collection of some python programs for implementing a security camera. Each program is made for a specific use case.
## Programs
The following programs already exist. Each has a different purpose.
- camera_window.py

A simple program that continuously shows the camera frames in a window
- motion_detection_autostart.py

A program that detects motion by comparing the image with the previous one and stores each image including date and time rendered in the image in a file. It also writes a log file with all events.
## Material
I have used a Raspberry Pi Zero W for building my cameras. As I wanted to record videos also in darkness, I have ordered camera modules that support night vision. Some of them also are equipped with IR LEDs that emit infrared light into the room. Good keayword for searching such products are "makerhawk ir". There are versions with different properties:
- fisheye

These cameras have a wider angle of the view field. This  is helpful for monitoring the complete room.
- automatic switch

Some of these cameras automatically switch to daylight vision. This creates better pictures in a daylight scene. Others will produce "red" images in daylight.