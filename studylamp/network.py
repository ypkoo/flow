__author__ = 'koo'

import threading
import socket
import sys
from msg_handler import msg_dispatcher

HOST = 'localhost'
SEND_PORT1 = 7469
SEND_PORT2 = 26974
RECV_PORT = 6974
SEND_ADDR1 = (HOST, SEND_PORT1)
SEND_ADDR2 = (HOST, SEND_PORT2)
RECV_ADDR = (HOST, RECV_PORT)


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        try :
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Server socket created'
        except socket.error, msg :
            print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        try:
            self.server_socket.bind(RECV_ADDR)
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def run(self):
        while True:
            msg = self.server_socket.recv(1024) # buffer size is 1024 bytes
            print "received message:", msg
            msg_dispatcher(msg)


class Client(object):
    def __init__(self):
        try :
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Client socket created'
        except socket.error, msg :
            print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def sendto_sunghoi(self, msg):
        self.client_socket.sendto(str(msg), SEND_ADDR1)
        print "send to sunghoi. msg: %s" % msg

    def sendto_saehun(self, msg):
        self.client_socket.sendto(str(msg), SEND_ADDR2)
        # print "send to saehun. msg: %s" % msg

server = Server()
client = Client()
