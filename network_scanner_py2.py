#It will print all ip and mac adresses of same network
#!usr/bin/env python

import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="target",help="Target To scan the Network")
    # parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    if not options.target:
        parser.error("[-] Plese specify target, use --help for more info.")
    return options
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
# this line will return 2 lists, answered and unanswered.Timeout will specify time to request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    clients_list = []

    for element in answered_list:
        client_dict = {"ip":element[1].psrc,"MAC":element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
        print("IP\t\t\tMAC address\n-------------------------")
        for client in results_list:
            print(client["ip"]+"\t\t" + client["MAC"])

# use ifcongig to get to know MAC address of your PC network card
options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
