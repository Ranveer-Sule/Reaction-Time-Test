import machine
import utime

notes = {
    "C5": 523,
    "E5": 659,
    "G5": 784,
    "C6": 1047,
}
class Buzzer:
    def __init__(self, pin):
        self.buzzer = machine.PWM(machine.Pin(pin))

    def play_note(self, note, duration):
        if note in notes:
            self.buzzer.freq(notes[note])
            self.buzzer.duty_u16(30000)
            utime.sleep(duration)
            self.buzzer.duty_u16(0)
            utime.sleep(0.05)
        
    def winner_sound(self):
        self.play_note("C5", 0.2)
        self.play_note("E5", 0.2)
        self.play_note("G5", 0.2)
        self.play_note("C6", 0.2)
    
