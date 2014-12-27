#!/usr/bin/python
import socket
import sys
from protocol import *
from getpass import *

host = socket.gethostname()
port =7122
server=socket.socket()
server.connect((host,port))
print "Connection successful. Welcome to CNChat!"

username=raw_input('Enter username, or "new" to register:')

while username == "new":
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
    server.send(head+body)
    #wait for server
    code=server.read(4);
    while code != 1:
        raw_input("Invalid username, please enter a new one:")
        head = make_header(REGISTER, CLIENT)
        body = client_make_register_body(username,password,email)
        server.send(head+body)
        code=server.read(4);
    print "Registeration success!"
    username=raw_input('Enter username, or "new" to register:')
password = getpass("Enter password:");
head = make_header(LOGIN,CLIENT)
body = client_make_login_body(username,password)

