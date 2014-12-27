#!/ usr/bin/env python
import sys
from getpass import *
from protocol import *

def hello_command(name, print_counter=False, repeat=5):
    for i in range(repeat):
        if print_counter:
            print i+1
        sys.stderr.write("Hello, %s" % name)

def quit_command():
    sys.exit(-1)

if __name__ == '__main__':
    import scriptine
    scriptine.run()




