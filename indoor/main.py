#Library on the ESP32 for PIN, UART and Real Time Clocks
from machine import Pin, UART, RTC
#Hex to Str Library
import ubinascii
#Ultrasonic Library is used to initialize the Ultrasonic sensors
from hcsr04 import HCSR04
#Time library is used to introduce delays
from time import sleep


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
    
#Sets up the real time clock
rtc = RTC()
rtc.init((2022,3,2,1,30,0,0,0))

    
#Variable 'response' is holding a byte called 'ir' (Reserved)
response = ubinascii.unhexlify('6972')

#Turns on Green Led indicator initially to display parking spot is available
ledGreen.value(1)

def localDetection():
    
    #Checks if object is there, returns value and prints it if object is there
    USdistance_1 = US1.distance_cm()
    print('Ultrasonic Sensor 1: ', USdistance_1, ' cm')
    timestamp = rtc.datetime()
    timestamp = str(timestamp)
    timestamp1 = ubinascii.hexlify(timestamp)
    #delay of 1 second.
    sleep(1)
    #Checks if the distance to object is within 10 cm using Ultrasonic Sensor 1
    if USdistance_1 < 10:
        
        print('Sensor_1 has detected object, waiting 5 seconds to check for false positives')
        
        #Waits 5 seconds before going checking for false positives
        sleep(5)
        
        #Gets the distance from the second ultrasonic sensor and the timestamp
        USdistance_1 = US1.distance_cm()
        USdistance_2 = US2.distance_cm()
        print('Ultrasonic Sensor 2: ', USdistance_2, ' cm')
        #If both the ultrasonic sensors detect an object within 10cm than turn LED to RED.
        #If initial detection was false positive, turn LED to Green
        #It also 
        if (USdistance_2 < 10) and (USdistance_1 < 10):
            #Gets the current date time, turns it to string format, changes it to byte format
            #timestamp = rtc.datetime()
            #timestamp = str(timestamp)
            #timestamp1 = ubinascii.hexlify(timestamp)
            
            #Ensures other LED Colors are off and turns on the red LED
            ledGreen.value(0)
            ledBlue.value(0)
            sleep(1)
            ledRed.value(1)
            
            #Sends to xbee chip the message occupied and timestamp
            uart1.write('io')
            #uart1.write(timestamp1)
            print('Vehicle is detected, parking spot occupied')
            
        else:
            #If is a false positive, the red and blue LED is turned off and green is turned on
            ledRed.value(0)
            ledBlue.value(0)
            sleep(1)
            ledGreen.value(1)
            print('False Reading, Parking spot is free')
    
    #If sensor does not detect anything, ensure other LED is off and Green LED is turned back on, sends 'available' to hub
    else:
        ledRed.value(0)
        ledBlue.value(0)
        sleep(1)
        ledGreen.value(1)
        uart1.write('ia')
        #uart1.write(timestamp1)
        print('No Vehicles Detected')

def webtodevice():
    
    #if there is any messages are coming in read it. If message is 'reserved', turn LED Blue
    message = uart1.read()
    if message == response:
        ledGreen.value(0)
        sleep(1)
        ledBlue.value(1)
        print('Someone Reserved the spot Online!')
            
        #Timer counter of 1 second with an interval up to 20 seconds for testing
        #if both the sensors was able to detect an object, break out of the loop (Used as timer system)
        for x in range(20):
            sleep(1)
            USdistance_1 = US1.distance_cm()
            if (USdistance_1 < 10):
                sleep(5)
                USdistance_2 = US2.distance_cm()
                USdistance_1 = US1.distance_cm()
                if (USdistance_2 < 10) and (USdistance_1 < 10):
                    break

while True:
    localDetection()
    webtodevice()
    print('currently in 15 second sleep timer')
    sleep(15)

    
