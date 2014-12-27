#!/usr/bin/python
import socket
import protocol     # self-defined module

if __name__ == '__main__' :

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET : IPv4
    # SOCKET_STREAM : TCP
    # print 'server socket created\n'

    host = socket.gethostname()
    port = 7122

    s.bind((host, port))
    # print 'server socket bind completed\n'

    s.listen(6)
    # print 'server is now listening ...\n'
    # server now keeps listening to clients' connection
    client_list = []
    s.setblocking(0)    # no wait
    while True :
        try:
            conn, addr = s.accept()
            client_list.append((conn,addr))
        except socket.timeout as msg :
            print 'no new client'
        for client in client_list :
            try socket

    s.close()
