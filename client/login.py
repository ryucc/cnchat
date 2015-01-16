#!/usr/bin/python
import socket
import sys
import os
from getpass import *

def client_start(server):
    while 1:
        print "login or register([34mlogin[0m/[34mregister[0m)?"
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
            print "[31mNo such command[0m"
    return name

def loginorregister(server, cmd):
    while 1:
        sys.stdout.write("Enter username: ")
        sys.stdout.flush()
        name_input = sys.stdin.readline()
        name_list = name_input.split(' ')
        password = getpass("Enter password: ")

        username = name_list[0]
        username = username[0:len(username)-1]

        if len(name_list) != 1:
            print "[31mInvalid username![0m"
            continue 
        if cmd == "register\n":
            msg = "register " + username + ' '+ password + '\n'
        else:
            msg = "login " + username + ' '+password+'\n'
        server.send(msg)
        #wait for server
        server.setblocking(1)
        code = server.recv(1024)
        if code == "registerok\n":
            print "Registeration success!"
            return name_list[0]
            break;
        elif code == "loginok\n":
            print "Login success"
            return name_list[0]
            break;
        else:
            print "[31mInvalid username![0m"

        sys.stdout.write("Try again?([30m[0my/[3mn[0m): ")
        sys.stdout.flush()
        again_input = sys.stdin.readline()
        if again_input != "y\n":
            os.system('clear')
            logoutfile = open("./logout.txt", "r")
            sys.stdout.write(logoutfile.read())
            sys.stdout.flush()
            logoutfile.close()
            sys.exit(0) 

def client_welcome(name):
    os.system("clear")
    sys.stdout.write("Welcome to CNChat " + name)
    sys.stdout.flush()


