#!/usr/bin/python
import socket,struct

HOST = socket.gethostname()                
PORT = 50002                         
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(6)
conn, addr = s.accept()

while 1:
    aaa=conn.recv(8+4+4)
    print struct.unpack('dii',aaa)
    aaa=conn.recv(4)
    ulen=struct.unpack('i',aaa)
    aaa=conn.recv(ulen[0])
    print aaa
    username=struct.unpack('s',aaa)
    print ulen[0]
    print username
    aaa=conn.recv(4)
    plen=struct.unpack('i',aaa)
    password=conn.recv(plen[0])
    print password
    aaa=conn.recv(4)
    mlen=struct.unpack('i',aaa)
    mail=conn.recv(mlen[0])
    print mail
    conn.send(struct.pack('i',1));
