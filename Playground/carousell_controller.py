import time
import threading
import glob

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor

SOUND_DIR = "../../wav/sound/"
BG_MUSIC_DIR = "../../wav/bg/*.wav"

DEFAULT_SPEED = 360 # deg/s
STOPPING_PERIOD = 30


class CarousellController:
    def __init__(self, hub: EV3Brick, motor_port) -> None:
        self._hub = hub
        self._motor = Motor(motor_port)
    
    def _run_loop(self):
        while True:
            for file in sorted(glob.iglob(BG_MUSIC_DIR)):
                self._hub.speaker.play_file(SOUND_DIR+"bell.wav")
                self._motor.run(DEFAULT_SPEED)
                self._hub.speaker.play_file(file)
                self._motor.stop()
                time.sleep(STOPPING_PERIOD)
    
    def start(self):
        x = threading.Thread(target=self._run_loop)
        x.start()
