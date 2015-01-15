#!/usr/bin/python
import socket
import sys
import os
from getpass import *

def client_start(server):
    while 1:
        print "login or register(login/register)?"
        sys.stdout.write("> ")
        sys.stdout.flush()
        cmd_input = sys.stdin.readline()
        cmd_list = cmd_input.split(' ')
        if len(cmd_list) != 1:
            print "Wrong input"
            continue;
        cmd = cmd_list[0]
        if cmd == "login\n":
            name = loginorregister(server, cmd)
            break;
        elif cmd == "register\n":
            name = loginorregister(server, cmd)
            continue
        else:
            print "No such command"
    return name

def loginorregister(server, cmd):
    while 1:
        sys.stdout.write("Enter username: ")
        sys.stdout.flush()
        name_input = sys.stdin.readline()
        name_list = name_input.split(' ')
        password = getpass("Enter password: ")
        if len(name_list) != 1:
            print "Invalid username!"
            continue 
        if cmd == "register":
            msg = "register " + name_list[0]+ ' '+ password + '\n'
        else:
            msg = "login " + name_list[0] + ' '+password+'\n'
        server.send(msg)
        #wait for server
        server.setblocking(1)
        code = server.recv(1024)
        print code
        if code == "registerok\n":
            print "Registeration success!"
            return name_list[0]
            break;
        elif code == "loginok\n":
            print "Login success"
            return name_list[0]
            break;
        else:
            print "Invalid username!"

def client_welcome(name):
    os.system("clear")
    sys.stdout.write("Welcome to CNChat " + name)
    sys.stdout.flush()


