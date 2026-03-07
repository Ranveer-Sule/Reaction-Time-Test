from machine import Pin

led1 = Pin(13, Pin.OUT)
led2 = Pin(12, Pin.OUT)
button = Pin(17, Pin.IN)

while True:
  while button.value() == 1:
    led1.value(1)
    led2.value(1)
  else:
    led1.value(0)
    led2.value(0)