from machine import Pin,PWM
from Buzzer import Buzzer

green_led = Pin(13, Pin.OUT)
red_led = Pin(12, Pin.OUT)
button = Pin(17, Pin.IN, Pin.PULL_DOWN)
buzzer = Buzzer(16)

while True:
    if button.value() == 1:
        green_led.value(1)
        red_led.value(1)
        buzzer.winner_sound()
    else:
        green_led.value(0)
        red_led.value(0)
        buzzer.buzzer.duty_u16(0)