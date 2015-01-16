# chat_server.py
 
import sys, socket, select, traceback
from parse_message import *
from user_client_class import *
from my_filter import *

HOST = '' 
SOCKET_LIST = []
USER_LIST = []
CLIENT_LIST = []
GROUP_LIST = []
RECV_BUFFER = 4096 
server_socket = None
F = my_filter("wordlist.txt")

def init_server(HOST,PORT):
    # load Accounts
    fd = open("accounts","r")
    line = fd.readline()
    username = line[0:len(line)-1]
    while username:
        line = fd.readline()
        password = line[0:len(line)-1]
        USER_LIST.append(User_Class(username,password))
        line = fd.readline()
        username = line[0:len(line)-1]
    fd.close()
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
                #sockfd.send("Welcome To CNCHAT!\n")
                CLIENT_LIST.append(Client_class(sockfd,addr))
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    print data
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
                                USER_LIST.append(User_Class(Message.Username,Message.Password))
                            # register and login
                            # CLIENT_LIST.login(sock,Message.Username)

                        elif Message.Type == "login":
                            flag = 0
                            for i in range(0,len(USER_LIST)):
                                # ignore duplicate login
                                if USER_LIST[i].Name == Message.Username and USER_LIST[i].Password == Message.Password:
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
                            name = ""
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    name = client.Username
                                    CLIENT_LIST.remove(client)
                            for i in range(0,len(USER_LIST)):
                                if USER_LIST[i].Name == name:
                                    USER_LIST[i].Status = "offline"
                                    break
                            for group in GROUP_LIST:
                                if name in group.Members:
                                    group.Members.remove(group)
                            sock.close()
                            SOCKET_LIST.remove(sock)
                        elif Message.Type == "msg_person":
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
                                Message.Message = F.filt(Message.Message)
                                reciver.Sock.send("msg "+sender.Username+" "+Message.Message+"\n")
                            else:
                                sock.send("msgnotok "+Message.Username+" "+Message.Message+"\n")
                        elif Message.Type == "see_all":
                            print "online users:"
                            for client in CLIENT_LIST:
                                print client.Username
                            for group in GROUP_LIST:
                                print "Group "+group.Name+":"
                                for client in CLIENT_LIST:
                                    if client.Username in group.Members:
                                        print client.Username

                        elif Message.Type == "msg_group":
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
                                            Message.Message = F.filt(Message.Message)
                                            client.Sock.send("msg "+ sender.Username+" "+Message.Message+"\n")
                                            print "To "+client.Username+ ":"
                                            print "msg "+ sender.Username+" "+Message.Message+"\n"
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
                            print "enter_group"
                            flag = 0
                            client = None 
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    break
                            print client.Username
                            for group in GROUP_LIST:
                                print "Is he in "+group.Name+"?"
                                if group.Name == Message.Group:
                                    flag = 1
                                    print "yes, found group enter group"
                                    group.Members.append(client.Username)
                                    #sock.send("groupexists\n")
                                    break
                                else:
                                    print "no"
                            if flag == 0:
                                #sock.send("groupcreated\n")
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
                        elif Message.Type == "file":
                            reciver = None
                            flag = 0
                            for client in CLIENT_LIST:
                                if client.Username == Message.Username:
                                    reciver = client
                                    flag = 1
                                    break
                            if flag == 1:
                                for client in CLIENT_LIST:
                                    if client.Sock == sock:
                                        IP = client.Addr[0]
                                        reciver.Sock.send("file "+client.Username+" "+str(IP)+" "+Message.Port+" "+Message.Filename+"\n")
                            #undefined
                            #else:
                            #    sock.send("notonline\n");
                        
                        
                        elif Message.Type == "alluser":
                            flag = 1
                            msg = "alluser"
                            for user in USER_LIST:
                                msg += " " + user.Name
                            msg += "\n"
                            sock.send(msg)

                        elif Message.Type == "allonline":
                            flsg = 1
                            msg = "allonline"
                            for user in USER_LIST:
                                if user.Status == "online":
                                    msg += " " + user.Name
                            msg += "\n"
                            sock.send(msg)

                        elif Message.Type == "whoami":
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    print client.Username
                                    sock.send(client.Username+"\r\n")
                    
                        elif Message.Type == "broadcast":
                            flag = 0
                            sender = 0
                            for client in CLIENT_LIST:
                                if client.Sock == sock:
                                    sender = client
                                    flag = flag + 1
                            
                            Message.Message = F.filt(Message.Message)
                            for client in CLIENT_LIST:
                                print "bcast: " + client.Username + " " + Message.Message
                                client.Sock.send("broadcast "+sender.Username+" "+Message.Message+"\n")
                    
                    else:
                        print "broken"
                        name = ""
                        for client in CLIENT_LIST:
                            if client.Sock == sock:
                                name = client.Username
                                CLIENT_LIST.remove(client)
                        for i in range(0,len(USER_LIST)):
                            if USER_LIST[i].Name == name:
                                USER_LIST[i].Status = "broken"
                                break
                        for group in GROUP_LIST:
                            if name in group.Members:
                                group.Members.remove(name)
                        sock.close()
                        SOCKET_LIST.remove(sock)
                        continue


                except Exception,err:
                    print traceback.format_exc()
                    #broken socket
                    print "broken"
                    name = ""
                    for client in CLIENT_LIST:
                        if client.Sock == sock:
                            name = client.Username
                            CLIENT_LIST.remove(client)
                    for i in range(0,len(USER_LIST)):
                        if USER_LIST[i].Name == name:
                            USER_LIST[i].Status = "broken"
                            break
                    for group in GROUP_LIST:
                        if name in group.Members:
                            group.Members.remove(name)
                    sock.close()
                    SOCKET_LIST.remove(sock)
                    continue
    server_socket.close()

    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    else:
        PORT = 9049
    try:
        sys.exit(chat_server(PORT))
    except KeyboardInterrupt:
        fd = open("accounts","w")
        for user in USER_LIST:
            fd.write(user.Name+"\n")
            fd.write(user.Password+"\n")
        fd.close()
        for client in CLIENT_LIST:
            client.Sock.close()
        server_socket.close()



