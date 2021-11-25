import time
import threading

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor


DEFAULT_SPEED = 90 # deg/s
DISTANCE_THRESHOLD = 10
RUNNING_PERIOD = 10 # seconds
STOPPING_PERIOD = 10 # seconds
STARTING_PERIOD = 1 # second

STATE_INIT = 0
STATE_STARTING = 1
STATE_RUNNING = 2
STATE_STOPPED = 3


class FerrisController:
    def __init__(self, hub: EV3Brick, motor_port, distance_port) -> None:
        self._hub = hub
        self._motor = Motor(motor_port)
        self._distance_sensor = InfraredSensor(distance_port)
        self._timeout_end_ts = None
        self._starting_end_ts = None
        self._stopping_end_ts = None
        self._motor_running = False
        self._state = STATE_INIT

    def _is_running(self):
        return self._timeout_end_ts is not None \
            and time.time() < self._timeout_end_ts

    def _set_running_timeout(self):
        print("_set_running_timeout")
        self._timeout_end_ts = time.time() + RUNNING_PERIOD

    def _is_starting(self):
        return self._starting_end_ts is not None \
            and time.time() < self._starting_end_ts

    def _set_starting_timeout(self):
        print("_set_starting_timeout")
        self._starting_end_ts = time.time() + STARTING_PERIOD

    def _is_stopping(self):
        return self._stopping_end_ts is not None \
            and time.time() < self._stopping_end_ts

    def _set_stopping_timeout(self):
        print("_set_stopping_timeout")
        self._stopping_end_ts = time.time() + STOPPING_PERIOD

    def _set_state(self, to_state: int):

        if to_state == STATE_STARTING:
            self._start_motor()
            self._set_starting_timeout()
        
        if to_state == STATE_RUNNING:
            self._set_running_timeout()
        
        if to_state == STATE_STOPPED:
            self._stop_motor()
            self._set_stopping_timeout()

        self._state = to_state

    def _start_loop(self):
        self._set_state(STATE_STARTING)

        while True:
            dis = self._distance_sensor.distance()
            
            if self._state == STATE_STARTING:
                if not self._is_starting():
                    self._set_state(STATE_RUNNING)
            elif self._state == STATE_RUNNING:
                if dis <= DISTANCE_THRESHOLD:
                    if not self._is_running():
                        self._set_state(STATE_STOPPED)
            elif self._state == STATE_STOPPED:
                if not self._is_stopping():
                    self._set_state(STATE_STARTING)

            time.sleep(0.1)
    
    def _start_motor(self):
        print("_start_motor")
        self._motor.run(DEFAULT_SPEED)
        self._motor_running = True
    
    def _stop_motor(self):
        print("_stop_motor")
        self._motor.stop()
        self._motor_running = False

    def start(self):
        x = threading.Thread(target=self._start_loop)
        x.start()

    
