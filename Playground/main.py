#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor)
from pybricks.parameters import Port, Button

import time
from ferris_controller import FerrisController
from carousell_controller import CarousellController
from roller_controller import RollerController

from music_player import MusicPlayer

ev3 = EV3Brick()
music_player = MusicPlayer(ev3)
carousell_controller = CarousellController(ev3, Port.A)
roller_controller = RollerController(ev3, Port.B)
ferris_controller = FerrisController(ev3, Port.C, Port.S1)

ev3.speaker.set_volume(100)
ev3.speaker.set_speech_options(pitch=50)
ev3.speaker.say("Welcome to the Lego Theme Park")

# music_player.start()
carousell_controller.start()
ferris_controller.start()
roller_controller.start()

while True:
    exit_program = False
    button_pressed = ev3.buttons.pressed()

    for button in button_pressed:
        print(button)
        if button == Button.CENTER:
            exit_program = True
    
    if exit_program:
        break

    time.sleep(1)
