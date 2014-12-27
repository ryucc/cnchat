#!/usr/bin/python
import socket
import sys
from protocol import *
from getpass import *
from subprocess import *
from login import *

# Connect to server and login
host = 'linux8.csie.ntu.edu.tw'
port = 50002
server=socket.socket()
server.connect((host,port))
login(server)

# Init
rc = 0
cmdbase = ['python', 'clientsh.py']

while rc != 255:
    cmd_input = raw_input('JAC> ')
    cmd = cmd_input.split(' ')
    cmd = cmdbase + cmd
    # Run sbuprocess command
    child = Popen(cmd)
    child.wait()
    data = child.communicate()[1]
    print data
    rc = child.returncode



