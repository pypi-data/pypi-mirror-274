from engi1020.arduino.api import *
from time import sleep

def aToc(a):         
  m = 255/2   
  if -1 <= a <= 1:
   return (m*(a + 1))
  elif a < -1:
   return (0.0)       
  else:
   return 255

pressure_getTemp()
pressure_getPressure()
pressure_getAltitude()

digital_read(6)
digital_write(4, True)
analog_read(6)

for i in range(10):
    #buzzer_note(5, analog_read(0)+200, 1)
    #temp_humid_getTemp(3)
    #analog_read(6)
    #sleep(1)
    three_axis_getAccelX()
    #sleep(1)
    three_axis_getAccelY()
    #sleep(1)
    three_axis_getAccelZ()
    pressure_getTemp()
    pressure_getPressure()
    pressure_getAltitude()


while True:
  r = int(aToc(three_axis_getAccelX()))
  g = int(aToc(three_axis_getAccelY()))
  b = int(aToc(three_axis_getAccelZ()))
  rgb_lcd_print(f"r:{r},g:{g},b:{b}")
  rgb_lcd_colour(r, g, b)
  sleep(0.5) 