class User_Class:
    def __init__(self,name):
        self.Name = name
        self.Status = "offline" #register & not online

class Client_class:
    def __init__(self,sock,addr):
        self.Sock = sock
        self.Addr = addr
        self.Username = ""

class Group_class:
    def __init__(self,name):
        self.Name = name
        self.Members = []
    def join(self,user):
        if user in self.Members:
            return -1
        else:
            self.Members.append(user)
            return 0
    def leave(self,user):
        if user in self.Members:
            self.Members.remove(user)
            return 0
        else:
            return -1
