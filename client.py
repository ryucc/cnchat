import socket
import sys

s = socket.socket()
host = socket.gethostname()
port = 7122

s.connect((host, port))
print s.recv(1024)
try:
    line = str(raw_input("cnfinal>"))
except (EOFError):
    s.close()
    exit();
while 1:
    if line:
        s.send(line);
        print 'client:'+s.recv(1024)
    try:
        line = str(raw_input("cnfinal>"))
    except (EOFError):
        break; 
s.close()
exit();
