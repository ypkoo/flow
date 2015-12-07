__author__ = 'koo'

# states
COVER = 0
MENU = 1
LEARNING = 2
SOLVING = 3
GRADED = 4
REVIEW = 5
PROGRESS = 6
BUFFER = 7

class StateManager:
    def __init__(self):
        self._state = COVER
        self._title = None
        self.cur_page = -1
        self.page_count = 0
        self.new_pages = []

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        if new_state != self._state:
            self._state = new_state
            changed = True
        else:
            changed = False
        if changed:
            print 'state changed:', new_state
        return changed

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    def get_current_page(self, new_page):
        if new_page != self.cur_page:
            pass
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
