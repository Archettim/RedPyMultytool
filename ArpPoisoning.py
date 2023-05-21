import os
import textual
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,
send, sniff, sndrcv, srp, wrpcap)

class ArpPoison:
    def __init__(self) -> None:
        pass