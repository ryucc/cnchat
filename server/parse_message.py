class Parse:
    # overflow bug
    Type = ""
    Username = ""
    Group = ""
    Message = ""
    Password = ""
    Port = 0
    Filename = ""
    def __init__(self,raw_string):
        space = raw_string.find(' ')
        self.Type = raw_string[0:space]

        if self.Type == "login":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Password = raw_string[second_space+1:newline]

        elif self.Type == "register":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Password = raw_string[second_space+1:newline]

        elif self.Type == "msg_group":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Group = raw_string[space+1:second_space]
            self.Message = raw_string[second_space+1:newline]

        elif self.Type == "msg_person":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Message = raw_string[second_space+1:newline]

        elif self.Type == "knock":
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Username = raw_string[space+1:newline]
        elif self.Type == "create_group":
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Group = raw_string[space+1:newline]
            
        elif self.Type == "enter_group":
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Group = raw_string[space+1:newline]

        elif self.Type == "leave_group":
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Group = raw_string[space+1:newline]
        elif self.Type == "file":
            second_space = raw_string.find(' ',space+1)
            third_space = raw_string.find(' ',second_space+1)
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Port = raw_string[second_space+1:third_space]
            self.Filename = raw_string[third_space+1:newline]
        
        elif self.Type == "broadcast":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\r\n')
            if newline == -1:
                newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Message = raw_string[second_space+1:newline]


