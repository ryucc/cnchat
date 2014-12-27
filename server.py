import socket

s=socket.socket()
host = socket.gethostname()
port = 7122;
s.bind((host,port));
print host

s.listen(6)
while 1:
    c,addr = s.accept()
    print 'Got connection form', addr;
    c.send('Welcome')
    st = c.recv(1024)
    while st:
        print 'server:'+st
        c.send(st)
        st = c.recv(1024)
c.close()
