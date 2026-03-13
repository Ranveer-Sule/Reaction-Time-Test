import machine
import random
import time
from Buzzer import Buzzer

class Game:
    def __init__(self, red_led_pin, green_led_pin, button_pin, buzzer_pin, servo_pin):
        self.red_led = machine.Pin(red_led_pin, machine.Pin.OUT)
        self.green_led = machine.Pin(green_led_pin, machine.Pin.OUT)
        self.button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.buzzer = Buzzer(buzzer_pin)
        self.servo = machine.PWM(machine.Pin(servo_pin))
        self.servo.freq(50)
        
        # game state
        self.reaction_time = 0
        self.score = 0
    
    def generate_random_delay(self): # Generate a random delay between 1 and 5 seconds
        random_int = random.randint(1, 4)
        return random.random() * random_int + 1
    
    def red_led_phase(self, duration): # Run the red LED phase and check for early button presses
        self.red_led.value(1)
        self.green_led.value(0)
        
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < duration * 1000:
            if self.button.value() == 1:
                print('Do not press the button before Green LED turns on')
                return True  
        
        return False
    
    def set_servo(self): 
        duty = int(1638 + (6554/24) * self.score)
        self.servo.duty_u16(duty)

    def green_led_phase(self): # Run the green LED phase and measure reaction time
        self.red_led.value(0)
        self.green_led.value(1)
        
        button_press_time = time.ticks_ms()
        while self.button.value() == 0:
            pass 
        
        self.reaction_time = time.ticks_diff(time.ticks_ms(), button_press_time)
        self.green_led.value(0)
        
        return self.reaction_time
    
    def run_round(self, score):
        delay = self.generate_random_delay()
        
        # Red LED phase with early press detection
        early_press = self.red_led_phase(delay)
        if early_press:
            self.buzzer.loser_sound()
            score = 0
            self.score = score
            self.set_servo()
            return False, score
        
        # Green LED phase - measure reaction time
        self.green_led_phase()
        
        # Determine win/loss based on reaction time
        # faster than 3 seconds or improved over previous score
        if self.reaction_time < 3000 and (self.score == 0 or self.reaction_time < 3000 / self.score):
            self.buzzer.winner_sound()
            score += 1
            self.score = score
            # move servo proportional to score (20° per point, capped at 180°)
            self.set_servo()
            return True, score
        else:
            self.buzzer.loser_sound()
            score = 0
            self.score = score
            self.set_servo()
            return False, score
    
    def display_result(self):
        print(f"Reaction Time: {self.reaction_time} ms")