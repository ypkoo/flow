__author__ = 'koo'

import socket
import sys

HOST = 'localhost'
PORT = 9999
SERVER_ADDR = (HOST, PORT)

def init_socket():
     # Datagram (udp) socket
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # Bind socket to local host and port
    # try:
    #     s.bind(SERVER_ADDR)
    # except socket.error , msg:
    #     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    #     sys.exit()

    return s
