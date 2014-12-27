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
    while True :


    s.close()
