class Event():
    def __init__(self, name: str) -> None:
        self.name = name

EVENT_MUSIC_STOP = Event("EVENT_MUSIC_STOP")
EVENT_MUSIC_START = Event("EVENT_MUSIC_START")
EVENT_BELL_STOP = Event("EVENT_BELL_STOP")
