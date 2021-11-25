import threading
import glob
from pybricks.hubs import EV3Brick
from event_publisher import EventPublisher
from event_listener import EventListener
from event import Event, EVENT_BELL_STOP, EVENT_MUSIC_STOP, EVENT_MUSIC_START


MUSIC_DIR = "../../wav/bg/*.wav"
SOUND_DIR = "../../wav/sound/"

class MusicPlayer(EventPublisher):
    def __init__(self, hub: EV3Brick) -> None:
        self._hub = hub
        self._event_listeners = []

    def _play_music(self):
        while True:
            for file in sorted(glob.iglob(MUSIC_DIR)):
                self._hub.speaker.play_file(SOUND_DIR+"bell.wav")
                self.fireEvent(EVENT_BELL_STOP)
                self.fireEvent(EVENT_MUSIC_START)
                self._hub.speaker.play_file(file)
                self.fireEvent(EVENT_MUSIC_STOP)

    def start(self):
        x = threading.Thread(target=self._play_music)
        x.start()

    def addEventListener(self, listener: EventListener):
        self._event_listeners.append(listener)

    def fireEvent(self, event: Event):
        for l in self._event_listeners:
            l.notify(event)
