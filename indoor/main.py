from machine import
from hcsr04 import HCSR04
from init import initialization
from local import localDetection, webtodevice

initialization()

while True:
    localDetection()
    webtodevice()
    
