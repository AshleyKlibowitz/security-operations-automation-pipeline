from scapy.all import IP, TCP, wrpcap

packets = []
# normal SYN
packets.append(IP(src="10.0.0.1", dst="10.0.0.2")/TCP(sport=1234, dport=80, flags="S"))
# TCP Reset (R)
packets.append(IP(src="192.0.2.1", dst="198.51.100.2")/TCP(sport=3456, dport=80, flags="R"))
# TCP Reset-Ack (RA)
packets.append(IP(src="203.0.113.5", dst="198.51.100.2")/TCP(sport=4567, dport=443, flags="RA"))

wrpcap('traffic.pcap', packets)
print('Wrote traffic.pcap with', len(packets), 'packets')
