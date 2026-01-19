import scapy.all as scapy
import argparse
import sys


def parse_args():
    p = argparse.ArgumentParser(description='Forensics: detect TCP Reset (R/RA) in a pcap')
    p.add_argument('-f', '--file', default='traffic.pcap', help='PCAP file to read (default: traffic.pcap)')
    return p.parse_args()


def process_pcap(path):
    try:
        packets = scapy.rdpcap(path)
    except FileNotFoundError:
        print(f"[-] PCAP file not found: {path}")
        return 2
    except Exception as e:
        print(f"[-] Failed to read PCAP: {e}")
        return 3

    found = 0
    for pkt in packets:
        if scapy.TCP in pkt:
            flags = str(pkt[scapy.TCP].flags)
            # Scapy may represent flags as integers; use string check for common forms
            if flags in ('R', 'RA') or 'R' in flags:
                found += 1
                print("[!] Suspicious Activity: TCP Reset detected!")
                if scapy.IP in pkt:
                    src = pkt[scapy.IP].src
                    dst = pkt[scapy.IP].dst
                elif scapy.IPv6 in pkt:
                    src = pkt[scapy.IPv6].src
                    dst = pkt[scapy.IPv6].dst
                else:
                    src = 'N/A'
                    dst = 'N/A'
                print(f"Source: {src} -> Destination: {dst}")

    if found == 0:
        print("[i] No TCP Reset (R/RA) packets found.")
    else:
        print(f"[i] Detected {found} TCP Reset packet(s).")
    return 0


def main():
    args = parse_args()
    return process_pcap(args.file)


if __name__ == '__main__':
    sys.exit(main())
