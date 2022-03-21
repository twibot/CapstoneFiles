from machine import Pin
import picosleep
import utime

led = Pin(25, Pin.OUT)
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
signal_out = Pin(4, Pin.OUT)

dis = [0, 0, 0, 0, 0]
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
   print("The distance from object is ",distance,"cm")
   return distance
   
while True:
   led.toggle()
   utime.sleep(3)
#    for x in range(5):
#        dis[x] = ultra()
#        utime.sleep(1)
#        print(dis)
#        utime.sleep(1)
   print("Test1")
   utime.sleep(1)
   picosleep.seconds(10)
   utime.sleep(3)
   print("Test2")
   
