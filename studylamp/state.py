__author__ = 'koo'

# states
BOOTING = 0
START = 1
MENU = 2
STUDY = 3
REVIEW = 4
PROGRESS = 5

class StateManager:
    def __init__(self):
        self._state = START
        self._title = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title


state = StateManager()