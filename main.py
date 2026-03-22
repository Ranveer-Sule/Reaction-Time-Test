from Game import Game
import time

# Initialize the game with hardware pin numbers
game = Game(red_led_pin=13, green_led_pin=12, button_pin=17, buzzer_pin=16, servo_pin=3)

# Main game loop
score = 0
game.pre_game() # Wait for the player to press the button to start the game
while True:
    _, score = game.run_round(score)
    time.sleep(2)
