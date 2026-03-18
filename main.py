from Game import Game
import time

# Initialize the game with hardware pin numbers
game = Game(red_led_pin=13, green_led_pin=12, button_pin=17, buzzer_pin=16, servo_pin=3)

# Main game loop
score = 0
print("Welcome to the Reaction Time Game!")
print("Press the button to start the game.")
game.pre_game()  # Wait for initial button press to start the game
while True:
    won, score = game.run_round(score)
    if won:
        game.display_result()
    else:
        pass
    time.sleep(2)
