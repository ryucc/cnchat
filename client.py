#!/usr/bin/python
import socket
import sys
from protocol import *
from getpass import *

print "Welcome to CNChat"
host = socket.gethostname()
port =7122
username=raw_input('Enter username, or "new" to register:')
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



