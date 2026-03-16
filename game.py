import machine
import random
import time
from Buzzer import Buzzer


class Game:
    MAX_REACTION_MS = 3000
    DUTY_MIN = 1638
    DUTY_MAX = 8192 # variables needed for servo control

    def __init__(self, red_led_pin, green_led_pin, button_pin, buzzer_pin, servo_pin): # initialize hardware components
        self.red_led = machine.Pin(red_led_pin, machine.Pin.OUT)
        self.green_led = machine.Pin(green_led_pin, machine.Pin.OUT)
        self.button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.buzzer = Buzzer(buzzer_pin)
        self.servo = machine.PWM(machine.Pin(servo_pin))
        self.servo.freq(50)
        self.reaction_time = 0
        self.score = 0
        self.set_servo_duty(self.DUTY_MIN)

    def generate_random_delay(self):
        # Generate a random delay between 1 and 5 seconds
        random_int = random.randint(1, 4)
        return random.random() * random_int + 1

    def set_servo_duty(self, duty):
        duty = max(self.DUTY_MIN, min(self.DUTY_MAX, int(duty)))
        self.servo.duty_u16(duty)

    def set_servo_from_elapsed(self, elapsed_ms):
        elapsed_ms = max(0, min(self.MAX_REACTION_MS, elapsed_ms))
        ratio = elapsed_ms / self.MAX_REACTION_MS
        duty = self.DUTY_MIN + ratio * (self.DUTY_MAX - self.DUTY_MIN)
        self.servo.duty_u16(int(duty))

    def red_led_phase(self, duration):
        self.red_led.value(1)
        self.green_led.value(0)

        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < duration * 1000:
            if self.button.value() == 1:
                self.red_led.value(0)
                print("Do not press the button before Green LED turns on")
                return True
        self.red_led.value(0)
        return False

    def pre_game(self):
        while self.button.value() == 0:
            time.sleep_ms(10)
        time.sleep_ms(50)
        while self.button.value() == 1:
            self.buzzer.start_sound()
            time.sleep_ms(10)
        return True

    def green_led_phase(self):
        self.red_led.value(0)
        self.green_led.value(1)
        start_time = time.ticks_ms()

        while self.button.value() == 0:
            elapsed = time.ticks_diff(time.ticks_ms(), start_time)
            self.set_servo_from_elapsed(elapsed)
            if elapsed >= self.MAX_REACTION_MS:
                self.reaction_time = elapsed
                self.green_led.value(0)
                return self.reaction_time
            time.sleep_ms(20)

        self.reaction_time = time.ticks_diff(time.ticks_ms(), start_time)
        self.green_led.value(0)
        return self.reaction_time

    def run_round(self, score):
        delay = self.generate_random_delay()

        early_press = self.red_led_phase(delay)
        if early_press:
            self.buzzer.loser_sound()
            score = 0
            self.score = score
            self.set_servo_duty(self.DUTY_MIN)
            return False, score
        self.green_led_phase()

        if self.reaction_time < self.MAX_REACTION_MS:
            self.buzzer.winner_sound()
            score += 1
            self.score = score
            return True, score
        else:
            self.buzzer.loser_sound()
            score = 0
            self.score = score
            self.set_servo_duty(self.DUTY_MIN)
            return False, score

    def display_result(self):
        print(f"Reaction Time: {self.reaction_time} ms")
        print(f"Score: {self.score}")