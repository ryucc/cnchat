# chat_server.py
 
import sys, socket, select, traceback
from parse_message import *
from user_client_class import *

HOST = '' 
SOCKET_LIST = []
USER_LIST = []
CLIENT_LIST = []
GROUP_LIST = []
RECV_BUFFER = 4096 
server_socket = None

def init_server(HOST,PORT):
    # load Accounts
    fd = open("accounts","r")
    line = fd.readline()
    username = line[0:len(line)-1]
    while username:
        USER_LIST.append(User_Class(username))
        line = fd.readline()
        username = line[0:len(line)-1]
    fd.close()
    # load filter
        #TODO
    # start socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print "Chat server started on port " + str(PORT)
    return sock

def chat_server(port):
    
    global server_socket
    server_socket = init_server(HOST,port)
    SOCKET_LIST.append(server_socket)

    while 1:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                sockfd.send("Welcome To CNCHAT!\n")
                CLIENT_LIST.append(Client_class(sockfd,addr))
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
                            # register and login
                            # CLIENT_LIST.login(sock,Message.Username)

                        elif Message.Type == "login":
                            flag = 0
                            for i in range(0,len(USER_LIST)):
                                # ignore duplicate login
                                if USER_LIST[i].Name == Message.Username:
                                    USER_LIST[i].Status = "online"
                                    sock.send("loginok\n")
                                    for client in CLIENT_LIST:
                                        if client.Sock == sock:
                                            client.Username = Message.Username
                                    flag = 1
                                    break
                            if flag == 0: # Can't find user
                                    sock.send("loginnotok\n")

                        elif Message.Type == "logout":
                            sock.send("goodbye\n")
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    CLIENT_LIST.remove(client)
                            for i in range(0,len(USER_LIST)):
                                if USER_LIST[i].Name == Message.Username:
                                    USER_LIST[i].Status = "offline"
                                    break
                            sock.close()
                            SOCKET_LIST.remove(sock)
                        elif Message.Type == "tell_user":
                            flag = 0
                            reciver = 0
                            sender = 0
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    sender = client
                                    flag = flag + 1
                                if client.Username == Message.Username:
                                    reciver = client
                                    flag = flag + 2
                            if flag == 3:
                                # duplicate login bug
                                reciver.Sock.send("msg "+sender.Username+" "+Message.Message+"\n")
                            else:
                                sock.send("msgnotok "+Message.Username+" "+Message.Message+"\n")
                        elif Message.Type == "tell_group":
                            sender = 0
                            flag = 0
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    sender = client
                                    flag = 1
                            if flag == 0:
                                # not logged in
                                sock.send("msgnotok "+Message.Group+" "+Message.Message+"\n")
                            for group in GROUP_LIST:
                                if group.Name == Message.Group:
                                    for client in CLIENT_LIST:
                                        if client.Username in group.Members:
                                            client.Sock.send("msg "+ sender.Username+" "+Message.Message+"\n")
                        elif Message.Type == "create_group":
                            flag = 0
                            for i in range(0,len(GROUP_LIST)):
                                if GROUP_LIST[i].Name == Message.Group:
                                    flag = 1
                                    #sock.send("groupexists\n")
                                    break
                            if flag == 0:
                                #sock.send("groupcreated\n")
                                group = Group_class(Message.Group)
                                GROUP_LIST.append(group)
                                # register and join
                                for client in CLIENT_LIST:
                                    if client.Sock == sock:
                                        group.Members.append(client.Username)
                        elif Message.Type == "enter_group":
                            flag = 0
                            client = None 
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    break
                            for group in GROUP_LIST:
                                if group.Name == Message.Group:
                                    flag = 1
                                    group.join(client.Username)
                                    #sock.send("groupexists\n")
                                    break
                            if flag == 0:
                                sock.send("groupcreated\n")
                                group = Group_class(Message.Group)
                                group.Members.append(client.Username)
                                GROUP_LIST.append(group)
                        elif Message.Type == "my_group":
                            list_of_groups = ""
                            client = None 
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    break
                            for group in GROUP_LIST:
                                if client.Username in group.Members:
                                    list_of_groups = list_of_groups + group.Name + " "
                            sock.send(list_of_groups+"\n")
                        elif Message.Type == "leave_group":
                            flag = 0
                            client = None 
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    break
                            for group in GROUP_LIST:
                                if group.Name == Message.Group:
                                    flag = 1
                                    flag1 = 0
                                    for user in group.Members:
                                        if user == client.Username:
                                            group.Members.remove(user)
                                            if len(group.Members) == 0:
                                                #remove empty group
                                                GROUP_LIST.remove(group)
                                            flag1 = 1
                                            #sock.send("leavesuccess\n")
                                            break
                                    #if flag1 == 0:
                                        #undefined protocol
                                        #sock.send("notingroup\n")
                            #if flag == 0:
                                #undefined protocol
                                #sock.send("nosuchgroup\n")
                        elif Message.Type == "knock":
                            flag = 0
                            for user in USER_LIST:
                                if user.Name == Message.Username:
                                    if user.Status == "online":
                                        sock.send("online "+Message.Username+"\n")
                                    else:
                                        sock.send("offline "+Message.Username+"\n")
                                    flag = 1
                                    break
                            if flag == 0:
                                sock.send("notexist "+Message.Username+"\n")

                        elif Message.Type == "whoami":
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    print client.Username
                                    sock.send(client.Username+"\r\n")

                except Exception,err:
                    print traceback.format_exc()
                    #broken socket
                    print "broken"
                    for client in CLIENT_LIST:
                        if client.Sock == sock:
                            CLIENT_LIST.remove(client)
                    for i in range(0,len(USER_LIST)):
                        if USER_LIST[i].Name == Message.Username:
                            USER_LIST[i].Status = "broken"
                            break
                    sock.close()
                    SOCKET_LIST.remove(sock)
                    continue
    server_socket.close()

    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    else:
        PORT = 9009
    try:
        sys.exit(chat_server(PORT))
    except KeyboardInterrupt:
        fd = open("accounts","w")
        for user in USER_LIST:
            fd.write(user.Name+"\n")
        fd.close()
        for client in CLIENT_LIST:
            client.Sock.close()
        server_socket.close()



