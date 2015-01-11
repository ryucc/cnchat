class Parse:
    def __init__(raw_string):
        Type = ""
        User = ""
        Username = ""
        Group = ""
        Message = ""

        space = raw_string.find(' ')
        Type = raw_string[0:space]

        if Type == "login":
            newline = raw_string.find('\n')
            Username = raw_string[space+1:newline]

        elif Type == "register":
            newline = raw_string.find('\n')
            Username = raw_string[space+1:newline]

        elif Type == "tell_group":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\n')
            Group = raw_string[space+1:second_space]
            Message = raw_string[second_space+1,newline]

        elif Type == "tell_user":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\n')
            User = raw_string[space+1:second_space]
            Message = raw_string[second_space+1,newline]

        elif Type == "knock":
            newline = raw_string.find('\n')
            User = raw_string[space+1:newline]

        elif Type == "file":
            second_space = raw_string.find(' ',space+1)
            newline = raw_string.find('\n')
            User = raw_string[space+1:second_space]
            Message = raw_string[second_space+1,newline]
        elif Type == "enter_group":
            newline = raw_string.find('\n')
            Group = raw_string[space+1:newline]
        elif Type == "leave_group":
            newline = raw_string.find('\n')
            Group = raw_string[space+1:newline]

