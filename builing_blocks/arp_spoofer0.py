import scapy.all as scapy
# this is how packet made of
packet = scapy.ARP(op=2, pdst="192.168.0.117",hwdst="60:a4:d0:b9:70:74",psrc="192.168.0.1")
#if we dont specify hwsrc,it will be detected automatically and if we dont specify "op" then it will take 1 value
#op = 1 is request and op=2 is for response
scapy.ls(scapy.ARP)

#packet all information
print(packet.show())
#who sent ip+mac
print(packet.summary())