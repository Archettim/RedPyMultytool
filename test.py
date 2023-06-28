import subprocess
from OpenRevShells import OpenSH
import os

a=OpenSH()
srvP=4242
os.environ["DISPLAY"] =":0.0"
f=subprocess.check_output(["id -un 1000"],shell=True)
r=subprocess.Popen([f"sudo -u {f.decode().strip()} xterm -e python3 RevShListener.py {srvP}"],shell=True)
print(r)