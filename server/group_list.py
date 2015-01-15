class Group:
    Name = ""
    Members = []
    def __init__(self,name):
        Name = name
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

'''
class Group_list:
    LIST = []
    def new_group(self,gname):
        for group in self.LIST:
            if group.Name == gname:
                return -1
        ng = Group(gname)
        LIST.append(ng)
        
    def get_member_list(gname):
        for group in self.LIST:
            if group.Name == gname:
                return group.Members

    # remove and add by reference
    def add_user_to_group(user,gname):
        for i in range(0,len(self.LIST)):
            if LIST[i].Name == gname:
                LIST[i].join(user)
                break

    def remove_user_from_group(user,gname):
        for i in range(0,len(self.LIST)):
            if LIST[i].Name == gname:
                LIST[i].leave(user)
                break
'''
