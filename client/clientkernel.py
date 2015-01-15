from getpass import *
import os

# define return code
RC_MSG = 1000
RC_NMSG = 1001
RC_ERR = 1002
RC_LOGOUT = 1003
RC_NOR = 1004
RC_PER = 1005
RC_GRP = 1006
RC_FILE = 1007

# define message types
MSG_PER = 2000
MSG_GRP = 2001

def hello_command(name):
    msg = "hello " + name
    return msg

def knock_command(search_name):
    msg = "knock "+ search_name + '\n'
    return msg

# Command: file
#   input: file file1 file2 ...
#   msg: file file1 file2 ... filen\n
#   
#   unsolved issue: space in the end of argument list
def file_command(*argvar):
    cmdlist = argvar[0]
    argnum = len(cmdlist)
    msg = ""
    for i in xrange(0, argnum-1):
        msg += cmdlist[i] + ' '
    msg += cmdlist[argnum-1]
    msg += '\n'
    return msg

def clear_command():
    os.system('clear')
    msg = "Clear\n"
    return msg

def ls_command():
    os.system('ls')
    msg = "List\n"
    return msg

def cat_command(filename):
    os.system("cat " + filename)
    msg = "Cat\n"
    return msg

def logout_command():
    msg = "logout\n"
    return msg

def startmsg_command(username):
    msg = username
    return msg

def sendmsg_command(msgtype, name, *argvar):
    cmdlist = argvar[0]
    argnum = len(cmdlist)
    if msgtype == MSG_PER:
        msg = "msg_person " + name + ' '
    elif msgtype == MSG_GRP:
        msg = "msg_group " + name + ' '
    for i in xrange(0, argnum-1):
        msg += cmdlist[i] + ' '
    msg += cmdlist[argnum-1]
    msg += '\n';
    return msg

def startgroup_command(groupname):
    msg = groupname
    return msg

# Client kernal function handler for normal mode
# return: (rc, msg)
#   rc:  return code, 1: OK, 2: OK & don't confirm server, 0: error, -1: quit
#   msg: message
def command_user_normal(*argvar):
    # argument initialization
    if len(argvar) < 1:
        return (0,"Argument list error")

    cmdlist = argvar[0]
    cmd = cmdlist[2]
    argnum = len(cmdlist)-2

    # command handle
    if cmd == "hello":
        if argnum != 2:
            msg = "The number of aruments for hello command should be 2\n"
            return (RC_ERR, msg)
        msg = hello_command(cmdlist[3])
    
    elif cmd == "knock":
        if argnum != 2:
            msg = "The number of aruments for knock command should be 2\n"
            return (RC_ERR, msg)
        msg = knock_command(cmdlist[3])
    
    elif cmd == "clear\n":
        msg = clear_command()
        return (RC_NMSG, msg)
    
    elif cmd == "logout\n":
        msg = logout_command()
        return (RC_LOGOUT, msg)
    
    elif cmd == "quit\n":
        msg = "Do you mean logout?\n"
        return (RC_ERR, msg)
    
    elif cmd == "msg":
        if argnum != 2:
            msg = "The number of aruments for msg command should be 2\n"
            return (RC_ERR, msg)
        msg = startmsg_command(cmdlist[3][0:len(cmdlist[3])-1]) # throw away \n
        return (RC_PER, msg)
    
    elif cmd == "group":
        if argnum != 2:
            msg = "The number of aruments for group command should be 2\n"
            return (RC_ERR, msg)
        msg = startgroup_command(cmdlist[3][0:len(cmdlist[3])-1]) # throw away \n
        return (RC_GRP, msg)
   
    # file user port filename
    elif cmd == "file":
        if argnum != 4:
            msg = "The number of aruments for file command should be 4\n"
            return (RC_ERR, msg)
        msg = cmdlist[3] + " " + cmdlist[4] + " " + cmdlist[5];
        return (RC_FILE, msg)
    
    elif cmd == "ls\n":
        msg = ls_command()
        return (RC_NMSG, msg)
    
    elif cmd == "cat":
        if argnum != 2:
            msg = "The number of aruments for cat command should be 2\n"
            return (RC_ERR, msg)
        msg = cat_command(cmdlist[3])
        return (RC_NMSG, msg)

    else:
        msg = "No such command!\n"
        return (RC_ERR, msg)
    
    # Correct command 
    return (RC_MSG, msg)


# Client kernal function handler for personal message mode
# return: (rc, msg)
#   rc:  return code, 1: OK, 2: OK & don't confirm server, 0: error, -1: quit
#   msg: message
def command_user_message(msgtype, name, *argvar):
    # argument initialization
    if len(argvar) < 1:
        return (0,"Argument list error")

    cmdlist = argvar[0]
    cmd = cmdlist[2]
    argnum = len(cmdlist)-2

    # command handle
    if cmd == "quit\n":
        msg = ""
        return (RC_NOR, msg)
    
    elif cmd == "send":
        msg = sendmsg_command(msgtype, name, cmdlist[3:len(cmdlist)])
    
    elif cmd == "clear\n":
        msg = clear_command()
        return (RC_NMSG, msg)
    
    elif cmd == "file":
        if argnum < 2:
            msg = "The number of aruments for file command should be larger than 2\n"
            return (RC_ERR, msg)
        msg = file_command(cmdlist[2:len(cmdlist)])
    
    else:
        msg = "No such command\n"
        return (RC_ERR, msg)

    return (RC_MSG, msg)

# Client kernal function handler for server mode
# return: (rc, msg)
#   rc:  return code, 1: OK, 2: OK & don't confirm server, 0: error, -1: quit
#   msg: message
def command_server_normal(*argvar):
    # argument initialization
    if len(argvar) < 1:
        return (0,"Argument list error")

    cmdlist = argvar[0]
    cmd = cmdlist[2]
    argnum = len(cmdlist)-2

    # command handle
    if cmd == "loginok\n":
        msg = "loginok\n"
        return (RC_NOR, msg)

    elif cmd == "loginnotok":
        msg = "loginnotok\n"
        return (RC_ERR, msg)

    elif cmd == "msgnotok":
        name = cmdlist[3]
        msg = "message to " + name + ": "
        for i in xrange(4,len(cmdlist)-1):
            msg += cmdlist[i]
        msg += cmdlist[len(cmdlist)-1]
        return (RC_ERR, msg)

    elif cmd == "msg":
        name = cmdlist[3]
        msg = "[31m" + name + " [0m" + ">"
        for i in xrange(4,len(cmdlist)-1):
            msg += ' ' + cmdlist[i]
        msg += " " + cmdlist[len(cmdlist)-1]
    
    elif cmd == "notexist":
        name = cmdlist[3]
        msg = "user not exist: " + name
        return (RC_ERR, msg)
    
    elif cmd == "online":
        name = cmdlist[3]
        msg = "user online: " + name
    
    elif cmd == "offline":
        name = cmdlist[3]
        msg = "user offline: " + name
        return (RC_ERR, msg)
    
    elif cmd == "file":
        msg = cmdlist[3] + " " + cmdlist[4] + " " + cmdlist[5] + " " + cmdlist[6]
        return (RC_FILE, msg)

    else:
        msg = "Server: " + cmd
        return (RC_MSG, msg)

    return (RC_MSG, msg)

