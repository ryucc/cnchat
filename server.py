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
    conn.send(struct.pack('i',1))
