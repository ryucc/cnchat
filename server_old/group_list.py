class Group:
    Name = ""
    Members = []
    def join(username):
        if Members.find(username):
            return 0
        else:
            Members.append(username)
            return 0
    def leave(username):
        if Members.find(username):
            Members.remove(username)
            return 0
        else:
            return -1

class Group_list:
    LIST = []
    def new_group(gname):
        if group in LIST:
            if group.Name == gname:
                return -1;
        ng = Group()
        ng.Name = gname
        LIST.append(ng);
        
    def get_member_list(gname):
        for group in LIST:
            if group.Name == gname:
                return group.Members

    def add_user_to_group(user,gname):
        for group in LIST:
            if group.Name == gname:
                group.join(user)
                break

    def remove_user_from_group(user,gname):
        for group in LIST:
            if group.Name == gname:
                group.leave(user)
                break


