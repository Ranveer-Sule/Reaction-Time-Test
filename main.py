from game import Game
import time

# Initialize the game with hardware pin numbers
game = Game(red_led_pin=13, green_led_pin=12, button_pin=17, buzzer_pin=16, servo_pin=18)

# Main game loop
score = 0
while True:
    won, score = game.run_round(score)
    game.display_result()
    time.sleep(2)
