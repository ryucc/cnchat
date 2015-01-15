#!/usr/bin/python
import select
import socket
import sys
import os
import curses
import time
from getpass import *
from subprocess import *
#from protocol import * # Define CNChat protocols and APIs
from login import * # Login and register process
from clientkernal import * # Client kernal function


# define status code
SNOR = 2000
SPER = 2001
SGRP = 2002

def command_line(str):
    sys.stdout.write("[31m" + str + "[0m"  + "> ")
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
host = "linux1.csie.ntu.edu.tw"
port = 9009
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
                sys.stdout.write("Error: " + msg)
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
           
        # next command line message
        if status == SNOR:
            command_line("")
        elif status == SPER:
            command_line(person + " ")
        elif status == SGRP:
            command_line(group + " ")

