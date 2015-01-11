# chat_server.py
 
import sys, socket, select
from parse_message, group_list, user_list, client_list import *

HOST = '' 
SOCKET_LIST = []
USER_LIST = []
CLIENT_LIST = Client_list()
RECV_BUFFER = 4096 
PORT = 9009

def init_server(HOST,PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print "Chat server started on port " + str(PORT)
    return sock

def chat_server():
    
    server_socket = init_server(HOST,PORT)
    SOCKET_LIST.append(server_socket)

    while 1:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                sockfd.send("Welcome To CNCHAT!\n")
             
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        Message = Parse(data)
                        if Message.Type == "register":
                            flag = 0
                            for i in range(0,len(USER_LIST)):
                                if USER_LIST[i].Name == Message.Username:
                                    flag = 1
                                    sock.send("registernotok\n")
                                    break
                            if flag == 0:
                                sock.send("registerok\n")
                                USER_LIST.append(User_Class(Message.Username))

                        elif Message.Type == "login":
                            flag = 0
                            for i in range(0,len(USER_LIST)):
                                if USER_LIST[i].Name == Message.Username:
                                    USER_LIST[i].Status = "online"
                                    sock.send("loginok\n")
                                    CLIENT_LIST.login(sock,Message.Username)
                                    flag = 1
                                    break
                            if flag == 0:
                                    sock.send("loginnotok\n")


                        elif Message.Type == "logout":
                            username = CLIENT_LIST.find_client_by_sock(sock).Username
                            for i in range(0,len(USER_LIST)):
                                if USER_LIST[i].Name == Message.Username:
                                    USER_LIST[i].Status = "offline"
                                    break
                            CLIENT_LIST.logout(sock)
                                    




                except:
                    continue

    server_socket.close()
    
if __name__ == "__main__":

    sys.exit(chat_server())


         
