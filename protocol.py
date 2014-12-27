import struct
import time

# actions
REGISTER = 0
LOGIN = 1
KNOCK = 2
MESSAGE = 3
FILE = 4
RESPONSE_FILE = 5

# who
SERVER = 0
CLIENT = 1

# other
FAIL = 0
SUCCESS = 1

# REGISTER
REPETITVE_USERNAME = 689
INVALID_USERNAME = 609

# KNOCK
NO_SUCH_USER = 7122
USER_ONLINE = 7123

def make_header(action, who) :
    t = time.time()
    head = struct.pack('dii', t, action, who)
    return head

def open_header(head) :
    return struct.unpack('di', head)

def client_make_register_body(username, password, email) :
    ulen = len(username)
    plen = len(password)
    elen = len(email)
    return struct.pack('isisis', ulen, username, plen, password, elen, email)

def client_make_login_body(username, password) :
    ulen = len(username)
    plen = len(password)
    return struct.pack('isisis', ulen, username, plen, password)

def client_make_knock_body(search_user) :
    sulen = len(search_user)
    return struct.pack('is', sulen, search_user)

def client_make_message_body(recipient, message) :
    ulen = len(recipient)
    mlen = len(message)
    return struct.pack('isis', ulen, recipient, mlen, message)

def server_make_resgister_body(result) :
    return struct.pack('i', result)
    
def server_make_login_body(result) :
    return struct.pack('i', result)

def server_make_knock_body(result) :
    return struct.pack('i', result)

def server_make_response_message_body(result) :  # SUCCESS/ NO_SUCH_USER/ FAIL
    return struct.pack('i', result)

def server_make_message_body(from_who,message) :
    ulen = len(from_who)
    mlen = len(message)
    return struct.pack('isis', ulen, from_who, mlen, message)
