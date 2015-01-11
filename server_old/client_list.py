class Client:
    def __init__(self,sock,addr):
        Sock = sock
        Addr = addr
        Username = ""
        Email = ""
        Status = ""

    def logout(self):
        self.Status = "Offline"
        self.Sock.close()
        self.Addr = -1
    def broken(self):
        self.Status = "Broken"
        self.Sock.close()
        self.Addr = -1



class Client_list:
    def __init__(self):
        self.LIST = [] 
    def add_client(self,sock,addr):
        self.LIST.append(Client(sock,addr))

    def login(self,sock,username):
        client = self.find_client_by_sock(sock)
        client.Username = username
        client.Status = "Online"
    def register(self,username):
        if self.find_client_by_username(username) == -1:
            self.LIST.append(-1,-1,username)
            return 0
        else:
            return -1
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


#Query methods

    def find_client_by_sock(self,sock):
        for item in LIST:
            if item.Sock == sock:
                return item
        return -1

    def find_client_by_username(self,username):
        for item in LIST:
            if item.Username == username:
                return item
        return -1
