#!/ usr/bin/env python
import sys
from getpass import *
from protocol import *

def hello_command(name, print_counter=False, repeat=10):
    for i in range(repeat):
        if print_counter:
            print i+1
        print "Hello, %s" % name

def register_command():
    username =  raw_input("Enter username: ")
    password = getpass("Enter password: ")
    p2 = getpass("Reenter password: ")
    if password != p2:
        print "Password mismatch, please try again"
        username =  raw_input("Enter username: ")
        password = getpass("Enter password: ")
    email = raw_input("Enter email: ")
    head = make_header(REGISTER, CLIENT)
    body = client_make_register_body(username, password, email)
    return head + body

def quit_command():
    sys.exit(-1)

if __name__ == '__main__':
    import scriptine
    scriptine.run()




