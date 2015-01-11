#!/usr/bin/python
import sys, socket, select, client_list, parse_message, group_list

HOST = socket.gethostname()
SOCKET_LIST = []
CLIENT_LIST = client_list.Client_list()
GROUP_LIST = group_list.Group_list()
RECV_BUFFER = 4096 
PORT = 9009

def init_server(HOST,PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    print "Chat server started on port " + str(PORT)
    return s

def chat_server():

    #initiate server
    server_socket = init_server(HOST,PORT)
    SOCKET_LIST.append(server_socket)
 
 
    while 1:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                sockfd.send("Welcome To CNChat!\n")
                CLIENT_LIST.add_client(sockfd,addr)
             
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:

                        Message = Parse(data)

                        if Message.Type == "login":
                            CLIENT_LIST.login(sock,Message.Username)
                            sock.send("Login Successful\n");

                        elif Message.Type == "register":
                            if CLIENT_LIST.register(Message.Username) == 0:
                                sock.send("Register OK\n");
                            else:
                                sock.send("Username exists!\n");

                        elif Message.Type == "quit":
                            client = CLIENT_LIST.find_client_by_sock(sock)
                            client.logout()
                            sock.send("Good bye!")

                        elif Message.Type == "tell_group":
                            #find sender by sock query
                            name = CLIENT_LIST.find_client_by_sock(sock).Username

                        elif Message.Type == "tell_user":
                            #find recipient by username
                            recipient = CLIENT_LIST.find_client_by_username(Message.User)
                            #find sender by sock query
                            name = CLIENT_LIST.find_client_by_sock(sock).Username
                            #send message protocol
                            try:
                                recipient.Sock.write("msg_person "+name+" "+Message.Message)
                            except:
                                sock.close()
                                SOCKET_LIST.remove(sock)
                                client = CLIENT_LIST.find_client_by_sock(sock)
                                client.logout()
                                client.Status = "Broken"

                        elif Message.Type == "knock":
                            knocked = CLIENT_LIST.find_client_by_username(Message.User)
                            if knocked == -1:
                                sock.write("notexist\n")
                            elif knocked.Status == "Online":
                                sock.write("online\n")
                            elif knocked.Status == "Offline":
                                sock.write("offline\n")
                            elif knocked.Status == "Broken":
                                sock.write("offline\n")
                            else:
                                sock.write("offline\n")

                        elif Message.Type == "file":
                            #file
                            sock.write("open 10003")
                        else:
                            sock.write("bad message\n")
                except:
                        CLIENT_LIST.broken_socket(sock)
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

    server_socket.close()


#start server
if __name__ == "__main__":

    sys.exit(chat_server())
