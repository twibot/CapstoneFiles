from machine import Pin, UART, RTC
from time import sleep
import ubinascii


uart1 = UART(1, baudrate=9600, tx=26, rx=27)
LED = Pin(2, Pin.OUT)
rtc = RTC()
#year, month, day, weekday, hours, minutes, seconds, subseconds
rtc.init((2022,3,12,1,30,0,0,0))

while True:
    
    
    
    timestamp = rtc.datetime()
    print(timestamp)
    print('This should be transmitting timestamp')
    sleep(5)
    response = ubinascii.unhexlify('7265736572766564')
    print('this is outside loop')
    #if there is any messages are coming in read it. If message is reserved, turn LED Blue
    timestamp = str(timestamp)
    timestamp1 = ubinascii.hexlify(timestamp)
    
    sleep(1)
    message = uart1.read()
    print(message)
    print(response)
    if  message == response:
        LED.value(0)
        sleep(1)
        LED.value(1)
        sleep(1)
        LED.value(0)
        print('message read successful')
        uart1.write(timestamp1)
       
    else:
        print('no read')

    
            
        
    
   
   


