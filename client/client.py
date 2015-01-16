#!/usr/bin/python
import select
import socket
import sys
import os
import curses
import time
from getpass import *
from subprocess import *
from login import * # Login and register process
from clientkernel import * # Client kernal function


# define status code
SNOR = 2000
SPER = 2001
SGRP = 2002

def command_line(str):
    if status == SPER:
        sys.stdout.write("[31m" + str + "[0m"  + "> ")
    elif status == SGRP:
        sys.stdout.write("[32m" + str + "[0m"  + "> ")
    else:
        sys.stdout.write("> ")
    sys.stdout.flush()
    # win.addstr(str)
    # win.refresh()
    # win.getstr()

# clear window
os.system('clear')

# init stdscr
# stdscr = curses.initscr()
WIN1HEIGHT = 15
WIN1WIDTH = 60
WIN2HEIGHT = 15
WIN2WIDTH = 60
WINX = 0
WINY = 15

# win1 = curses.newwin(WIN1HEIGHT, WIN1HEIGHT, 0, 0)
# win2 = curses.newwin(WIN2HEIGHT, WIN2HEIGHT, WINY, WINX)

# Connect to server and login
# host = "linux8.csie.ntu.edu.tw"

# host = socket.gethostname() # localhost
if len(sys.argv) < 3:
    host = "linux2.csie.ntu.edu.tw"
    port = 9049
else:
    print "host = "+sys.argv[1]
    host = sys.argv[1]
    port = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(5)
try:
    server.connect((host, port))
except:
    print "Unable to connect CNChat sever"
    sys.exit()
print "Connect to CNChat server"

# Client register or login
username = client_start(server)
client_welcome(username)

# Init
rc = 0 # return code
cmdbase = ['python', 'clientsh.py'] # command prefix
stimeout = 0.5 # Select timeout
person = "" # set person name ""
group = "" # set group name ""
# status:
#  SNOR: normal mode
#  SPER: personal message mode
#  SGRP: group message mode
status = SNOR

command_line("")

while True:
    # Set selecting socket to be stdin and server
    sock_list = [sys.stdin, server]
    # sock_list = [sys.stdin]
    # Select readable socket with timeout = stimeout
    ready_to_read, ready_to_write, ready_to_error = select.select(sock_list, [], [])

    for sock in ready_to_read:
        if sock == server:
            cmd_input = server.recv(4096)
            if len(cmd_input) == 0:
                print "\nServer disconnected\n"
                sys.exit()
            cmdlist = cmd_input.split(' ')
            cmdlist = cmdbase + cmdlist
            rc, msg = command_server_normal(cmdlist)
            
            if rc == RC_MSG:
                sys.stdout.write('\n' + msg)
                sys.stdout.flush()
            
            elif rc == RC_ERR:
                sys.stdout.write('\n' + "Error: " + msg)
                sys.stdout.flush()
            
            elif rc == RC_FILE:
                # file message
                print msg
                filemsg = msg.split(" ")
                fileservername = filemsg[0]
                fileip = filemsg[1]
                fileport = filemsg[2]
                filename = filemsg[3]
                filename = "receive.txt"

                # open socket
                print "Connect to server..."
                fileserver = socket.socket()
                fileserver.settimeout(2)
                fileserver.connect((fileip, int(fileport)))
                filesocklist = [fileserver]
                print "Before select..."
                ready_to_read, ready_to_write, ready_to_error = select.select(filesocklist, [], [], 1)
                while len(ready_to_read) == 0:
                    ready_to_read, ready_to_write, ready_to_error = select.select(filesocklist, [], [], 1)
                
                print "Open file..."
                # open file
                fp = open(filename, "w")
                buf = fileserver.recv(4096)
                while buf:
                    fp.write(buf)
                    fp.flush()
                    try:
                        buf = fileserver.recv(4096)
                    except:
                        break
                        pass
                        
                fp.close() 

        else:
            # Command handle
            cmd_input = sys.stdin.readline()
            cmdlist = cmd_input.split(' ')
            cmdlist = cmdbase + cmdlist
            if status == SPER: # personal mode
                rc, msg = command_user_message(MSG_PER, person, cmdlist)
            elif status == SGRP: # group message mode
                rc, msg = command_user_message(MSG_GRP, group, cmdlist)
            else: # normal mode
                rc, msg = command_user_normal(cmdlist)

            # return code:
            #  RC_MSG:    normal command with msg for server, ex: knock [username]
            #  RC_NMSG:   normal command without msg for server, ex: clear
            #  RC_LOGOUT: logout
            #  RC_ERR:    error with error msg
            #  RC_NOR:    change to normal mode
            #  RC_PER:    change to personal message mode
            #  RC_GRP:    change to group message mode
            if rc == RC_MSG:
                server.send(msg)
            
            elif rc == RC_ERR:
                sys.stdout.write("[34mError: [0m" + msg)
            
            elif rc == RC_LOGOUT:
                os.system('clear')
                logoutfile = open("./logout.txt", "r")
                sys.stdout.write(logoutfile.read())
                sys.stdout.flush()
                logoutfile.close()
                msg = "logout \n"
                server.send(msg)
                sys.exit(0) 
            
            elif rc == RC_NOR:
                if status == SGRP:
                    msg = "leave_group " + group + '\n'
                    server.send(msg)
                status = SNOR
            
            elif rc == RC_PER:
                status = SPER
                person = msg
            
            elif rc == RC_GRP:
                status = SGRP
                group = msg
                server.send("enter_group " + group + '\n')

            elif rc == RC_FILE:

                # file message
                print msg
                filemsg = msg.split(" ")
                fileclient = filemsg[0]
                fileport = filemsg[1]
                filename = filemsg[2]
                filename = filename[0:len(filename)-1]
                server.send("file " + fileclient + " " + fileport + " " + filename)
                
                print "Start send file: " + filename
                # file server
                fileserver = socket.socket()
                fileserver.bind((socket.gethostname(), int(fileport)))
                fileserver.listen(1)
                fileclient, clientaddr = fileserver.accept()
                
                print "Open file..."
                # open file
                fp = open(filename, "r")
                buf = fp.read(4096)
                while buf:
                    fileclient.send(buf)
                    buf = fp.read(4096)
                fileclient.send(buf)
                fp.close()

                print "Finish sending file"

            elif rc == RC_HELP:
                print msg
               

        # next command line message
        if status == SNOR:
            command_line("")
        elif status == SPER:
            command_line(person + " ")
        elif status == SGRP:
            command_line(group + " ")


