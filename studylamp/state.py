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
        self._state = STUDY
        self._title = None
        cur_page = -1
        page_count = 0
        new_pages = []

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

    def get_current_page(self, new_page):
        if new_page != self.cur_page:
            self.new_pages.append(new_page)
            self.page_count = self.page_count + 1

        if self.page_count == 3: 
            # recognize 3 consecutive new pages. If all 3 pages are same, change current page.
            if self.new_pages[0] == self.new_pages[1] and self.new_pages[1] == self.new_pages[2]:
                self.cur_page = new_page

            self.new_pages[0] = self.new_pages[1]
            self.new_pages[1] = self.new_pages[2]
            self.new_pages.pop()
            self.page_count = self.page_count - 1

        return self.cur_page


state = StateManager()