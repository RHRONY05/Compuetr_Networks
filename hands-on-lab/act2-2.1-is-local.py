# Act 2 · Session 2.1 (The Default Gateway) · Build: is_local() decision & subnet calculator
# Lesson: lessons/act2-local-or-remote.md · Notes: notes/02-network-layer/02-subnet-masks.md, 03-default-gateway.md, 04-dhcp.md

#
# Run from the course folder:
#   python hands-on-lab/act2-2.1-is-local.py
#   python hands-on-lab/act2-2.1-is-local.py 192.168.0.102/24 192.168.0.1
#   python hands-on-lab/act2-2.1-is-local.py 192.168.0.102/24 203.0.113.10
#   python hands-on-lab/act2-2.1-is-local.py 192.168.0.102 255.255.255.0 140.82.112.4
#
# Everything is built with pure integer bitwise operations (&, |, ~, ^, <<, >>),
# matching how the OS kernel routing table logic works under the hood.

import sys


def ip_to_int(ip_str):
    """'192.168.0.102' -> 3232235622 (32-bit unsigned integer)."""
    parts = ip_str.strip().split(".")
    if len(parts) != 4:
        raise ValueError(f"Invalid IP address: {ip_str!r} (must have 4 octets)")
    val = 0
    for p in parts:
        n = int(p)
        if not (0 <= n <= 255):
            raise ValueError(f"Octet {n} out of range (0-255)")
        val = (val << 8) | n
    return val


def int_to_ip(val):
    """3232235622 -> '192.168.0.102'."""
    val = val & 0xFFFFFFFF
    return f"{(val >> 24) & 0xFF}.{(val >> 16) & 0xFF}.{(val >> 8) & 0xFF}.{val & 0xFF}"


def int_to_bin_str(val):
    """Format 32-bit integer as 4 octets of 8 bits each."""
    val = val & 0xFFFFFFFF
    raw = format(val, "032b")
    return f"{raw[0:8]}.{raw[8:16]}.{raw[16:24]}.{raw[24:32]}"


def prefix_to_mask_int(prefix_len):
    """24 -> 0xFFFFFF00 (255.255.255.0 as 32-bit int)."""
    if not (0 <= prefix_len <= 32):
        raise ValueError(f"Invalid prefix length /{prefix_len}")
    if prefix_len == 0:
        return 0
    return ((0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF)


def mask_str_to_int(mask_str):
    """Accepts either '/24', '24', or '255.255.255.0'."""
    s = mask_str.strip().lstrip("/")
    if s.isdigit():
        return prefix_to_mask_int(int(s))
    return ip_to_int(s)


def count_prefix_bits(mask_int):
    """Count leading 1 bits in mask integer."""
    bin_str = format(mask_int & 0xFFFFFFFF, "032b")
    # Must be contiguous 1s followed by 0s
    ones = bin_str.count("1")
    expected = ("1" * ones) + ("0" * (32 - ones))
    if bin_str != expected:
        raise ValueError("Non-contiguous subnet mask is not supported in standard CIDR")
    return ones


def is_local(my_ip_str, mask_str, target_ip_str):
    """Core decision: does (my_ip & mask) == (target_ip & mask)?"""
    my_ip = ip_to_int(my_ip_str)
    mask = mask_str_to_int(mask_str)
    target = ip_to_int(target_ip_str)

    my_net = my_ip & mask
    target_net = target & mask

    return (my_net == target_net), my_net, target_net, mask


def analyze_decision(my_ip_str, mask_str, target_ip_str, gateway_ip_str="192.168.0.1"):
    same_net, my_net, target_net, mask = is_local(my_ip_str, mask_str, target_ip_str)
    prefix_len = count_prefix_bits(mask)
    my_ip = ip_to_int(my_ip_str)
    target = ip_to_int(target_ip_str)

    print("=" * 72)
    print(f"DECISION STEP: Is {target_ip_str} local or remote to {my_ip_str}/{prefix_len}?")
    print("=" * 72)
    print(f"My IP:       {my_ip_str:<15}  bits: {int_to_bin_str(my_ip)}")
    print(f"Subnet Mask: {int_to_ip(mask):<15}  bits: {int_to_bin_str(mask)} (/{prefix_len})")
    print(f"Target IP:   {target_ip_str:<15}  bits: {int_to_bin_str(target)}")
    print("-" * 72)
    print("BITWISE AND OPERATION ((IP & Mask) = Network ID):")
    print(f"  My IP   & Mask:   {int_to_bin_str(my_net)} -> {int_to_ip(my_net)}")
    print(f"  Target  & Mask:   {int_to_bin_str(target_net)} -> {int_to_ip(target_net)}")
    print("-" * 72)

    if same_net:
        print("RESULT: MATCH! Both have the identical network ID.")
        print(f"  Classification: ON-LINK (Local subnet: {int_to_ip(my_net)}/{prefix_len})")
        print("  Action:         Deliver DIRECTLY on local wire/Wi-Fi.")
        print(f"  Next Hop:       {target_ip_str} directly (OS will ARP for {target_ip_str}'s MAC)")
    else:
        print("RESULT: NO MATCH! Different network IDs.")
        print("  Classification: OFF-LINK (Remote Internet / outside network)")
        print(f"  Action:         Hand packet to DEFAULT GATEWAY.")
        print(f"  Next Hop:       Gateway {gateway_ip_str} (OS will ARP for Gateway's MAC)")
        print(f"                  (The destination IP in the packet remains {target_ip_str})")
    print("=" * 72)
    print()


def show_subnet_details(ip_str, mask_str):
    ip = ip_to_int(ip_str)
    mask = mask_str_to_int(mask_str)
    prefix_len = count_prefix_bits(mask)

    net_int = ip & mask
    bcast_int = net_int | (~mask & 0xFFFFFFFF)
    total_addrs = 2 ** (32 - prefix_len)
    usable_hosts = max(0, total_addrs - 2)

    first_usable = net_int + 1 if usable_hosts > 0 else net_int
    last_usable = bcast_int - 1 if usable_hosts > 0 else bcast_int

    print("+" + "-" * 70 + "+")
    print(f"| SUBNET CALCULATOR: {ip_str}/{prefix_len}".ljust(71) + "|")
    print("+" + "-" * 70 + "+")
    print(f"| Netmask:        {int_to_ip(mask):<18} ({int_to_bin_str(mask)}) |")
    print(f"| Network ID:     {int_to_ip(net_int):<18} (first address, cannot assign)    |")
    print(f"| Broadcast ID:   {int_to_ip(bcast_int):<18} (last address, room shout)        |")
    print(f"| Usable Range:   {int_to_ip(first_usable)} - {int_to_ip(last_usable)}".ljust(71) + "|")
    print(f"| Total / Usable: {total_addrs} addresses / {usable_hosts} usable host machines".ljust(71) + "|")
    print("+" + "-" * 70 + "+")
    print()


def main():
    if len(sys.argv) == 1:
        # Default self-demo using the student's actual network setup
        print("No arguments provided. Running built-in experiments from Session 2.1:\n")
        show_subnet_details("192.168.0.102", "255.255.255.0")

        # Experiment 1: Room device (Local)
        analyze_decision("192.168.0.102", "255.255.255.0", "192.168.0.1", gateway_ip_str="192.168.0.1")

        # Experiment 2: Outside server (Remote / GitHub)
        analyze_decision("192.168.0.102", "255.255.255.0", "140.82.112.4", gateway_ip_str="192.168.0.1")

        # Experiment 3: Google DNS (Remote)
        analyze_decision("192.168.0.102", "255.255.255.0", "8.8.8.8", gateway_ip_str="192.168.0.1")

        # Experiment 4: Non-slash-24 subnet (WSL virtual network)
        analyze_decision("172.19.160.1", "255.255.240.0", "172.19.165.42", gateway_ip_str="172.19.160.1")
        return

    # User-provided arguments
    # Cases:
    # 1. python script.py 192.168.0.102/24 8.8.8.8
    # 2. python script.py 192.168.0.102 255.255.255.0 8.8.8.8
    if len(sys.argv) == 3:
        first_arg = sys.argv[1]
        target_arg = sys.argv[2]
        if "/" in first_arg:
            ip, prefix = first_arg.split("/")
            show_subnet_details(ip, prefix)
            analyze_decision(ip, prefix, target_arg)
        else:
            print("Usage: python act2-2.1-is-local.py <ip/prefix> <target_ip>")
            print("   or: python act2-2.1-is-local.py <ip> <mask> <target_ip>")
    elif len(sys.argv) >= 4:
        ip = sys.argv[1]
        mask = sys.argv[2]
        target = sys.argv[3]
        gw = sys.argv[4] if len(sys.argv) > 4 else "192.168.0.1"
        show_subnet_details(ip, mask)
        analyze_decision(ip, mask, target, gateway_ip_str=gw)
    else:
        print("Usage: python act2-2.1-is-local.py [my_ip/prefix] [target_ip]")


if __name__ == "__main__":
    main()
