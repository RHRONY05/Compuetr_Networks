# Act 3 · Session 3.1 (MAC and ARP) · Build: ARP & MAC Explorer (A4)
# Lesson: playground.md (will archive to lessons/act3-3.1-mac-and-arp.md)
# Notes: notes/01-data-link/01-mac-and-arp.md
#
# Run from workspace root:
#   python hands-on-lab/act3-3.1-arp-explorer.py
#   python hands-on-lab/act3-3.1-arp-explorer.py 192.168.0.1
#   python hands-on-lab/act3-3.1-arp-explorer.py 94-BB-43-74-E0-DD
#
# Explores your real hardware NICs, parses the kernel ARP cache,
# decodes OUI manufacturers, and explains the L2 -> L3 mapping.

import sys
import subprocess
import re
import platform

# Sample of well-known OUIs (first 3 bytes of MAC) for instant offline lookup
KNOWN_OUIS = {
    "94-BB-43": "MediaTek Inc.",
    "CC-28-AA": "Realtek Semiconductor Corp.",
    "00-15-5D": "Microsoft Corporation (Hyper-V / WSL)",
    "3C-84-6A": "Shenzhen Mercury / TP-Link Technologies",
    "B0-BE-76": "TP-Link Corporation",
    "F4-F2-6D": "TP-Link Corporation",
    "00-0C-29": "VMware, Inc.",
    "08-00-27": "PCS Systemtechnik (Oracle VirtualBox)",
    "AC-DE-48": "Private / Randomized MAC",
    "DC-A6-32": "Raspberry Pi Trading Ltd",
    "E4-5F-01": "Raspberry Pi Trading Ltd",
    "F0-18-98": "Apple, Inc.",
    "3C-06-30": "Apple, Inc.",
    "00-1A-11": "Google, Inc.",
    "F4-03-43": "Intel Corporate",
    "00-50-56": "VMware, Inc.",
}


def normalize_mac(mac_str):
    """Normalizes MAC to uppercase hyphenated format XX-XX-XX-XX-XX-XX."""
    cleaned = re.sub(r"[^0-9a-fA-F]", "", mac_str).upper()
    if len(cleaned) != 12:
        return None
    return "-".join(cleaned[i:i+2] for i in range(0, 12, 2))


def lookup_oui(mac_normalized):
    """Extracts first 3 bytes (OUI) and returns vendor name."""
    if not mac_normalized or len(mac_normalized) < 8:
        return "Unknown"
    oui = mac_normalized[:8]
    return KNOWN_OUIS.get(oui, "Unknown / Unlisted Manufacturer")


def get_local_interfaces():
    """Runs getmac /v /fo csv or ipconfig to find local physical network cards."""
    interfaces = []
    try:
        res = subprocess.run(["getmac", "/v", "/fo", "csv"], capture_output=True, text=True, check=True)
        lines = res.stdout.strip().splitlines()
        if len(lines) > 1:
            header = [h.strip('"') for h in lines[0].split('","')]
            for line in lines[1:]:
                cols = [c.strip('"') for c in line.split('","')]
                if len(cols) >= 3:
                    conn_name = cols[0]
                    adapter = cols[1]
                    phys_addr = cols[2]
                    transport = cols[3] if len(cols) > 3 else ""
                    if phys_addr and phys_addr != "N/A":
                        norm = normalize_mac(phys_addr)
                        vendor = lookup_oui(norm)
                        interfaces.append({
                            "name": conn_name,
                            "adapter": adapter,
                            "mac": norm,
                            "vendor": vendor,
                            "connected": "Media disconnected" not in transport
                        })
    except Exception as e:
        # Fallback if getmac fails
        pass
    return interfaces


def parse_arp_table():
    """Parses system ARP table using 'arp -a'."""
    entries = []
    try:
        res = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        current_interface = "Unknown"
        for line in res.stdout.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("Interface:"):
                # Interface: 192.168.0.102 --- 0x4
                parts = line_str.split()
                if len(parts) >= 2:
                    current_interface = parts[1]
                continue
            # Match: IP, MAC, Type
            match = re.match(r"^(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)\s+(\w+)", line_str)
            if match:
                ip, raw_mac, entry_type = match.groups()
                norm_mac = normalize_mac(raw_mac)
                vendor = lookup_oui(norm_mac) if norm_mac != "FF-FF-FF-FF-FF-FF" else "BROADCAST (All Nodes)"
                entries.append({
                    "interface": current_interface,
                    "ip": ip,
                    "mac": norm_mac or raw_mac,
                    "type": entry_type,
                    "vendor": vendor
                })
    except Exception as e:
        print(f"Error reading ARP table: {e}")
    return entries


def main():
    print("=" * 70)
    print("  Act 3 · Session 3.1: Hardware MAC & ARP Explorer (Milestone A4)")
    print("  Mapping IP Addresses (Layer 3) -> Physical MAC Cards (Layer 2)")
    print("=" * 70)

    # 1. Inspect Local Hardware Interfaces
    print("\n[+] Step 1: Your Local Network Hardware Interfaces (NICs)")
    local_nics = get_local_interfaces()
    if local_nics:
        for nic in local_nics:
            status = "ACTIVE" if nic["connected"] else "DISCONNECTED"
            print(f"  • {nic['name']:<18} [{status}]")
            print(f"    Adapter: {nic['adapter']}")
            print(f"    MAC:     {nic['mac']}  -> OUI Vendor: {nic['vendor']}")
    else:
        print("  (Could not read interfaces via getmac)")

    # 2. Parse Kernel ARP Table
    print("\n[+] Step 2: Kernel ARP Cache (Resolved Neighbors on Link)")
    arp_entries = parse_arp_table()
    
    # Group by interface
    interfaces = {}
    for entry in arp_entries:
        interfaces.setdefault(entry["interface"], []).append(entry)

    for iface, rows in interfaces.items():
        print(f"\n  Interface: {iface}")
        print(f"  {'IP Address':<18} {'Physical (MAC)':<20} {'Type':<10} {'Device / Vendor'}")
        print("  " + "-" * 66)
        for r in rows:
            print(f"  {r['ip']:<18} {r['mac']:<20} {r['type']:<10} {r['vendor']}")

    # 3. Query / Diagnosis Mode
    target = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if target:
        print(f"\n[+] Lookup Query for: {target}")
        # Check if target is an IP in ARP table
        found_ip = [e for e in arp_entries if e["ip"] == target]
        if found_ip:
            for item in found_ip:
                print(f"  Found in ARP Cache on interface {item['interface']}:")
                print(f"    IP Address:  {item['ip']}")
                print(f"    MAC Address: {item['mac']}")
                print(f"    Vendor:      {item['vendor']}")
                print(f"    Cache Type:  {item['type']}")
                print(f"  Conclusion: Frame sent to {target} will be stamped with Dst MAC {item['mac']}")
        else:
            norm_q = normalize_mac(target)
            if norm_q:
                vendor = lookup_oui(norm_q)
                print(f"  MAC Address: {norm_q}")
                print(f"  OUI (First 3 bytes): {norm_q[:8]}")
                print(f"  Manufacturer:        {vendor}")
            else:
                print(f"  IP {target} is NOT currently in the ARP cache.")
                print(f"  If you send a packet to {target}, your OS kernel will first emit an")
                print(f"  ARP Request broadcast: 'Who has {target}? Tell my IP.'")

    print("\n" + "=" * 70)
    print("  Key Takeaway: The IP packet never changes across the Internet.")
    print("  The MAC address changes at EVERY hop to name the next physical wire/antenna.")
    print("=" * 70)


if __name__ == "__main__":
    main()
