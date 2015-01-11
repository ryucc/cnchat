class Client:
    def __init__(self,sock,addr):
        self.Sock = sock
        self.Addr = addr
        self.Username = ""

class Client_list:
    LIST = []
    def __init__(self):
        self.LIST = [] 
    def add_client(self,sock,addr):
        self.LIST.append(Client(sock,addr))

#handles
    def login(self,sock,username):
        for i in range(0,len(self.LIST)):
            if self.LIST[i].Sock == sock:
                self.LIST[i].Username = username
                return 0
        return -1

    def logoff(self,sock):
        for i in range(0,len(self.LIST)):
            if self.LIST[i].Sock == sock:
                self.LIST[i].close()
                self.LIST.pop(i)
                return 0
        return -1
#Query methods
    def find_client_by_sock(self,sock):
        for item in self.LIST:
            if item.Sock == sock:
                return item
        return -1

    def find_client_by_username(self,username):
        for item in self.LIST:
            if item.Username == username:
                return item
        return -1


###############revision line##################

#error methods
    def broken_socket(self,sock):
        client = find_client_by_sock(sock)
        client.Sock.close()
        if client.username == "":
            LIST.remove(client)

#remove methods
    def remove_client_by_sock(self,sock):
        for item in LIST:
            if item.Sock == sock:
                LIST.remove(item)
                return 0
        return -1

    def remove_client_by_username(self,username):
        for item in LIST:
            if item.Username == username:
                LIST.remove(item)
                return 0
        return -1
#misc methods
    def send_to_user(self,username, msg):
        client = self.find_client_by_username(username)
        client.Sock.send(msg)
        return 0


