#!/usr/bin/python
import socket
import sys
from protocol import *
from getpass import *
from subprocess import *

print "Welcome to CNChat"
host = socket.gethostname()
port = 7122
rc = 0
cmdbase = ['python', 'clientsh.py']

while rc != 255:
    cmd_input = raw_input('JAC> ')
    cmd = cmd_input.split(' ')
    cmd = cmdbase + cmd
    # Run sbuprocess command
    child = Popen(cmd)
    data = child.communicate()[0]
    print data
    rc = child.returncode

'''
if username == "new":
    username = raw_input("Enter username:")
    password = getpass("Enter password:");
    p2 = getpass("Renter password:");
    if password != p2:
        print "Password mismatch, please try again"
        password = getpass("Enter password:");
        p2 = getpass("Renter password:")
    email = raw_input("Enter email:")

    head = make_header(REGISTER, CLIENT)
    body = client_make_register_body(username,password,email)
    conn.send(head+body)
    #wait for server
'''

