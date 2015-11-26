__author__ = 'koo'

from msgManager import *
from udpSocket import *
import time

# Start from main menu.
# at 3 sec, user clicks Study button.

TIME_INTERVAL = 1.0

events = {}

def add_event(tick, finger_x, finger_y, check_x, check_y, page):

    events[tick] = make_msg(finger_x, finger_y, check_x, check_y, page)

    print('event added at %d seconds.' % tick)

def send_msg(s, tick):
    try:
        msg = events[tick]
    except:
        msg = make_random_msg()

    s.sendto(msg, SERVER_ADDR)
    print('sent msg: %s' % msg)


if __name__ == "__main__":
    s = init_socket()

    add_event(3, 0, 0, 40, 50, 40)
    add_event(5, 0, 0, 130, 50, 40)
    add_event(7, 0, 0, 200, 300, 40)

    tick = 0
    start_time=time.time()

    while True:
        send_msg(s, tick)
        tick = tick + 1
        time.sleep(TIME_INTERVAL - ((time.time() - start_time) % TIME_INTERVAL))

