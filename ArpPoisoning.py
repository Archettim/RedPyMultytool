import os
import sys
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,send, sniff, sndrcv, srp, wrpcap)

def get_target_mac(ip):
    packet=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has",pdst=ip)
    resp,_=srp(packet,timeout=2,retry=10,verbose=False)
    for _, r in resp:
        return(r[Ether].src)

class ArpPoison:
    def __init__(self) -> None:
        pass

if __name__=="__main__":
    print(get_target_mac(input("ip:")))