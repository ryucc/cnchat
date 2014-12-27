import struct
import time
REGISTER=0
LOGIN=1
KNOCK=2
MESSAGE=3
FILE=4
RESPONSE_FILE=5

def make_header (action,datalen):
    t = time.time()
    head=struct.pack('dii',action,datalen)
    return head

def open_header (head):
    return struct.unpack('dii',head)


    
