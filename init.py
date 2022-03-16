from machine import Pin, UART, Timer, RTC
#Ultrasonic Library is used to initialize pins 
from hcsr04 import HCSR04
#Time library is used to introduce delays
from time import sleep



def initialization():

    #initalizes RGB LED as GPIO.OUT
    #Green.pin(32), Blue.pin(33), Red.Pin(25)
    ledGreen = Pin(32,Pin.OUT)
    ledBlue = Pin(33, Pin.OUT)
    ledRed = Pin(25, Pin.OUT)

    #Sets up Ultrasonic sensors US1, US2, Function in HCSR04 Library
    #Trigger pins 13, 23, Echo pins 14, 22, Timeout for signal received 10000 us
    US1 = HCSR04(trigger_pin=13, echo_pin=14, echo_timeout_us=10000)
    US2 = HCSR04(trigger_pin=23, echo_pin=22, echo_timeout_us=10000)

    #Sets up UART Protocol to variable uart1, Baudrate = 9600, Transmitter Pin (26), Receiver Pin (27)
    uart1 = UART(1, baudrate=9600, tx=26, rx=27)
    
    rtc = RTC()
    rtc.init((2022,3,2,1,30,0))

    #Green Led indicator is on to display parking spot is available
    ledGreen.value(1)