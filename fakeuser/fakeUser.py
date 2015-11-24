__author__ = 'koo'

from msgManager import *
from udpSocket import *
import time

# Start from main menu.
# at 3 sec, user clicks Study button.

TIME_INTERVAL = 1.0

events = {}

def add_event(tick, event, x, y):
    if event == 'STUDY':
        events[tick] = make_msg(x, y, 0, 0)
    elif event == 'CHECK':
        events[tick] = make_msg(0, 0, x, y)

    print('event %s add at %d seconds.' % (event, tick))

def send_msg(s, tick):
    try:
        msg = events[tick]
    except:
        msg = make_random_msg()

    s.sendto(msg, SERVER_ADDR)
    print('sent msg: %s' % msg)


if __name__ == "__main__":
    s = init_socket()

    add_event(3, 'STUDY', STUDY_X, STUDY_Y)
    add_event(4, 'STUDY', STUDY_X, STUDY_Y)
    add_event(5, 'STUDY', STUDY_X, STUDY_Y)

    add_event(10, 'CHECK', CHECK1_X, CHECK1_Y)
    add_event(15, 'CHECK', CHECK2_X, CHECK2_Y)
    add_event(20, 'CHECK', CHECK3_X, CHECK3_Y)

    tick = 0
    start_time=time.time()

    while True:
        send_msg(s, tick)
        tick = tick + 1
        time.sleep(TIME_INTERVAL - ((time.time() - start_time) % TIME_INTERVAL))

