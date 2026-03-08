from machine import Pin,PWM

green_led = Pin(13, Pin.OUT)
red_led = Pin(12, Pin.OUT)
button = Pin(17, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(16))

while True:
    if button.value() == 1:
        green_led.value(1)
        red_led.value(1)
        buzzer.freq(1000)
        buzzer.duty_u16(30000)
    else:
        green_led.value(0)
        red_led.value(0)
        buzzer.duty_u16(0)