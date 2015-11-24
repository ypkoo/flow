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
        self.state = START
        self.title = ""

    def set_book_title(self, title_):
        self.title = title_

    def set_state(self, state_):
        self.state = state_

    def get_state(self):
        return self.state


state = StateManager()