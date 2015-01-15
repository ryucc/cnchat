class Parse:
    Type = ""
    Username = ""
    Group = ""
    Message = ""
    def __init__(self,raw_string):
        space = raw_string.find(' ')
        self.Type = raw_string[0:space]

        if self.Type == "login":
            newline = raw_string.find('\n')
            self.Username = raw_string[space+1:newline-1]

        elif self.Type == "register":
            newline = raw_string.find('\n')
            self.Username = raw_string[space+1:newline-1]

        elif self.Type == "tell_group":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\n')
            self.Group = raw_string[space+1:second_space]
            self.Message = raw_string[second_space+1:newline]

        elif self.Type == "tell_user":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Message = raw_string[second_space+1:newline]

        elif self.Type == "knock":
            newline = raw_string.find('\n')
            self.Username = raw_string[space+1:newline-1]

        elif self.Type == "file":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\n')
            self.Username = raw_string[space+1:second_space]
            self.Message = raw_string[second_space+1:newline]

        elif self.Type == "create_group":
            newline = raw_string.find('\n')
            self.Group = raw_string[space+1:newline-1]
            
        elif self.Type == "enter_group":
            newline = raw_string.find('\n')
            self.Group = raw_string[space+1:newline-1]

        elif self.Type == "leave_group":
            newline = raw_string.find('\n')
            self.Group = raw_string[space+1:newline-1]

