# Act 1 · Session 1.3 (The number DNS gave us) · Build: look inside an IP address
# Lesson: lessons/act1-1.3-ip-address.md · Note: notes/02-network-layer/01-ip-and-cidr.md
#
# Run from the course folder:
#   python hands-on-lab/act1-1.3-ip-explorer.py                      the examples from the lesson
#   python hands-on-lab/act1-1.3-ip-explorer.py github.com           ask DNS first, then look at the number
#   python hands-on-lab/act1-1.3-ip-explorer.py 192.168.0.102/24     an address with its prefix (/X)
#   python hands-on-lab/act1-1.3-ip-explorer.py 172.19.160.1/20      a prefix that does not end on a dot
#
# No networking library is used for the address itself: we split the text on dots,
# turn each part into 8 bits, and read the 32 bits back as one number.

import socket
import sys

# Blocks that are NOT ordinary public addresses: the three private blocks, then two special ones.
# Written in the same /X form the lesson uses, so you can check them against it.
SPECIAL = [
    ("10.0.0.0/8", "private (home, office, cloud networks)"),
    ("172.16.0.0/12", "private (home, office, cloud networks)"),
    ("192.168.0.0/16", "private (home, office, cloud networks)"),
    ("127.0.0.0/8", "loopback: this machine talking to itself (localhost)"),
    ("169.254.0.0/16", "link-local: self-assigned when nobody handed out an address"),
]

EXAMPLES = ["github.com", "192.168.0.102/24", "172.19.160.1/20", "172.66.147.243", "127.0.0.1/8"]


def to_bits(dotted):
    """'192.168.0.102' -> '11000000101010000000000001100110' (32 characters)."""
    parts = dotted.split(".")
    if len(parts) != 4:
        raise ValueError(f"{dotted!r} needs exactly 4 parts separated by dots")
    bits = ""
    for p in parts:
        n = int(p)
        if not 0 <= n <= 255:
            raise ValueError(f"{p} is not 0-255: one part has only 8 bits, and 8 bits stop at 255")
        bits += format(n, "08b")
    return bits


def to_dotted(bits):
    """32 bit-characters -> dotted quad, 8 bits at a time."""
    return ".".join(str(int(bits[i:i + 8], 2)) for i in range(0, 32, 8))


def kind(bits):
    """Is this address in one of the special blocks? Compare only the first <prefix> bits."""
    for block, label in SPECIAL:
        addr, prefix = block.split("/")
        if bits[:int(prefix)] == to_bits(addr)[:int(prefix)]:
            return f"{label}  [inside {block}]"
    return "public: unique on the whole Internet, reachable from anywhere"


def explain(arg):
    print("=" * 72)
    text, _, prefix = arg.partition("/")
    if not text.replace(".", "").isdigit():                  # a name, not a number: ask DNS (Session 1.2)
        number = socket.gethostbyname(text)
        print(f"{text}  --DNS-->  {number}")
        text = number
    bits = to_bits(text)

    print(f"Address : {text}")
    print("Octets  : " + "   ".join(f"{p:>3} = {format(int(p), '08b')}" for p in text.split(".")))
    print(f"32 bits : {' '.join(bits[i:i + 8] for i in range(0, 32, 8))}")
    print(f"As ONE number: {int(bits, 2):,}   (try: ping {int(bits, 2)})")
    print(f"Kind    : {kind(bits)}")

    if prefix:
        x = int(prefix)
        if not 0 <= x <= 32:
            raise ValueError("the prefix /X counts bits, so it must be 0-32")
        net, host = bits[:x], bits[x:]
        print(f"\n/{x}: the first {x} bits name the NETWORK, the last {32 - x} name the HOST")
        print(f"  network bits | host bits : {net} | {host}")
        first, last = net + "0" * (32 - x), net + "1" * (32 - x)
        print(f"  host bits all 0  -> {to_dotted(first):<15}  (the network's own name)")
        print(f"  host bits all 1  -> {to_dotted(last):<15}  (the last address in the block)")
        print(f"  addresses in this network: 2^{32 - x} = {2 ** (32 - x):,}")


if __name__ == "__main__":
    for a in (sys.argv[1:] or EXAMPLES):
        try:
            explain(a)
        except (ValueError, OSError) as e:
            print(f"{a}: {e}")
