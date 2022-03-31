from machine import Pin
from machine import UART
import picosleep
import utime


led = Pin(25, Pin.OUT)
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
xbee_out = Pin(4, Pin.OUT, Pin.PULL_DOWN)
xbee_in = Pin(5, Pin.OUT, Pin.PULL_DOWN)

dis = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
parking_dist = 110
uart1 = machine.UART(0, baudrate = 9600, tx=Pin(0) , rx=Pin(1) )


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
       sum = sum + dis[x]
   avg = sum / 10
   print(avg)
   utime.sleep(6)
   if avg < parking_dist:
      uart1.write('Oc')
   else:
      uart1.write('Av')
       
   led.off()
   utime.sleep(2)

   
#    picosleep.seconds(60)
   utime.sleep(3)
  