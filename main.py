from machine import Pin, UART, RTC
from hcsr04 import HCSR04
from functions import *



initialization()

while True:
    localDetection()
    webtodevice()
    