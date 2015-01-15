import tarfile
import socket
import time
import os

def send_files(file_list,host,port):
    t= int(time.time())
    fname = str(t)+".tar.gz"
    tar = tarfile.open(fname,'w:gz')
    for fff in file_list:
        tar.add(fff)
    tar.close()
    tf = open(fname,'r')
    s = socket.socket()
    s.connect((host, port))
    buff = tf.read(4096)
    while buff:
        s.send(buff)
    tf.close()
    os.remove(fname)

def recieve_files(port):
    t= int(time.time())
    fname = str(t)+".tar.gz"
    fff=open(fname,'w')
    s=socket.socket()
    host = socket.gethostname()
    s.bind((host,port));
    print host
    s.listen(2)
    c,addr = s.accept()
    st = c.recv(4096)
    while st:
        fff.write(st)
        st = c.recv(4096)
    fff.close()
    tar = tarfile.open(fname)
    tar.extractall()
    tar.close()
    os.remove(fname);


