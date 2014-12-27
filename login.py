#!/usr/bin/python
import socket
import sys
from protocol import *
from getpass import *

def register(server):
    username = raw_input("Enter username:")
    password = getpass("Enter password:");
    p2 = getpass("Renter password:");
    while password != p2:
        print "Password mismatch, please try again"
        password = getpass("Enter password:");
        p2 = getpass("Renter password:")
    email = raw_input("Enter email:")

    head = make_header(REGISTER, CLIENT)
    body = client_make_register_body(username,password,email)
    server.send(head+body)
    #wait for server
    code=server.recv(4)
    code = struct.unpack('i',code)
    while code != 1:
        raw_input("Invalid username, please enter a new one:")
        head = make_header(REGISTER, CLIENT)
        body = client_make_register_body(username,password,email)
        server.send(head+body)
        code=server.recv(4);
    print "Registeration success!"

def login(server):
    code = 0;
    while code!=1:
        username=raw_input('Enter username, or "new" to register:')
        while username == "new":
            register(server);
            username=raw_input('Enter username, or "new" to register:')
        password = getpass("Enter password:");
        head = make_header(LOGIN,CLIENT)
        body = client_make_login_body(username,password)
        code=server.recv(4);
        if code == 204:
            print "Wrong password, please try again."
        elif code == 205:
            print "Invalid username, please try again."

