import threading

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor


DEFAULT_SPEED = 240 # deg/s


class RollerController:
    def __init__(self, hub: EV3Brick, motor_port) -> None:
        self._hub = hub
        self._motor = Motor(motor_port)

    def _run_loop(self):
        self._motor.run(DEFAULT_SPEED)
    
    def start(self):
        x = threading.Thread(target=self._run_loop)
        x.start()
