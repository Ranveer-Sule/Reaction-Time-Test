from machine import Pin,PWM
from Buzzer import Buzzer
import time
import random

red_led = Pin(13, Pin.OUT)
green_led = Pin(12, Pin.OUT)
button = Pin(17, Pin.IN, Pin.PULL_DOWN)
buzzer = Buzzer(16)

while True:
    random_int = random.randint(1, 4)
    random_length = random.random() * random_int + 1
    start_time = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < random_length * 1000:
        red_led.value(1)
        green_led.value(0)
        if time.ticks_diff(time.ticks_ms(), start_time) < random_length * 1000 and button.value() == 1:
            print('Do not press the button before Green LED turns on')
            buzzer.loser_sound()
        
    red_led.value(0)
    green_led.value(1)
    
    button_press_time = time.ticks_ms()
    while button.value() == 0:
        pass  
    reaction_time = time.ticks_diff(time.ticks_ms(), button_press_time)
    
    green_led.value(0)
    
    if reaction_time < 200:
        buzzer.winner_sound()
    else:
        buzzer.loser_sound()
    
    print(f"Reaction Time: {reaction_time} ms")
    time.sleep(2)
