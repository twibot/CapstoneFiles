from machine import Pin
from machine import UART
import picosleep
import utime


led = Pin(25, Pin.OUT)
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
signal_out = Pin(4, Pin.OUT)
xbee_out = Pin(5, Pin.OUT)

dis = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
parking_dist = 110
uart = machine.UART(0, baudrate = 9600)


def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   return distance
   
while True:
   led.on()
   utime.sleep(2)
   sum = 0
   for x in range(10):
       dis[x] = ultra()
       utime.sleep(2)
       print(dis)
       sum = sum + dis[x]
   avg = sum / 10

   if avg < parking_dist:
       print("Send Signal")
       
   led.off()
   utime.sleep(15)

   
   picosleep.seconds(180)
   utime.sleep(3)
  