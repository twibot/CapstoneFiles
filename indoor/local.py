from machine import Pin, UART, RTC
#Ultrasonic Library is used to initialize pins 
from hcsr04 import HCSR04
#Time library is used to introduce delays
from time import sleep
  
def localDetection():
    
    #Checks if object is there, returns value and prints it if object is there
    USdistance_1 = US1.distance_cm()
    print('Ultrasonic Sensor 1: ', USdistance_1, ' cm')
    
    #delay of 1 second.
    sleep(1)
    timestamp = rtc.datetime()
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
            ledGreen.value(0)
            ledBlue.value(0)
            sleep(1)
            ledRed.value(1)
            #Sends to xbee chip the message occupied and timestamp
            uart1.write('occupied')
            uart1.write(timestamp)
            print('Vehicle is detected, parking spot occupied')
            
        else:
            ledRed.value(0)
            ledblue.value(0)
            sleep(1)
            ledGreen.value(1)
            uart1.write('available')
            uart1.write(timestamp)
            print('False Reading, Parking spot is free')
        
    else:
        ledRed.value(0)
        ledblue.value(0)
        sleep(1)
        ledGreen.value(1)
        uart1.write('available')
        uart1.write(timestamp)
        print('No Vehicles Detected')

def webtodevice():
    #decodes the byte to string format
    response = uart.any()
    response.decode('UTF-8')
    
    #if there is any messages are coming in read it. If message is reserved, turn LED Blue
    if response != 0:
        message = uart1.read()
        if  message.decode('UTF-8') == 'reserved':
            ledGreen.value(0)
            sleep(1)
            ledBlue.value(1)
            print('Someone Reserved the spot Online!')
            
            #Timer counter of 1 second with an interval up to 20 seconds for testing
            #if both the sensors 
            for x in range(20):
                sleep(1)
                USdistance_1 = US1.distance_cm()
                if (USdistance_1 < 10):
                    sleep(5)
                    USdistance_2 = US2.distance_cm()
                    USdistance_1 = US1.distance_cm()
                    if (USdistance_2 < 10) and (USdistance_1 < 10):
                        break
                    

                
            
