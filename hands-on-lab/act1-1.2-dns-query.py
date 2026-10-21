# Act 1 · Session 1.2 (DNS, the phone book) · Part 8: Build A2, a DNS query by hand
# Lesson: lessons/act1-1.2-dns.md
#
# Run from the course folder:
#   python hands-on-lab/act1-1.2-dns-query.py github.com              ask a resolver (1.1.1.1), type A
#   python hands-on-lab/act1-1.2-dns-query.py gmail.com MX            any type: A, AAAA, CNAME, MX, NS, TXT
#   python hands-on-lab/act1-1.2-dns-query.py github.com A --walk     do the resolver's job yourself:
#                                                                     root -> TLD -> authoritative
#
# No DNS library is used. We write the question as bytes, send it, and read the answer's bytes.

import random
import socket
import struct
import sys

TYPES = {"A": 1, "NS": 2, "CNAME": 5, "MX": 15, "TXT": 16, "AAAA": 28}
TYPE_NAMES = {v: k for k, v in TYPES.items()} | {6: "SOA"}
RESOLVER = "1.1.1.1"          # Cloudflare's public resolver
ROOT = "198.41.0.4"           # a.root-servers.net, one of the 13 root names (built into every resolver)


def build_query(name, qtype, recursion):
    """The whole question as bytes: a 12-byte header, then the question."""
    query_id = random.randint(0, 65535)
    flags = 0x0100 if recursion else 0x0000         # one bit: "please do the whole search for me"
    header = struct.pack(">HHHHHH", query_id, flags, 1, 0, 0, 0)   # id, flags, 1 question, 0, 0, 0
    # "github.com" is written as labels: 6 g i t h u b 3 c o m 0
    labels = b"".join(bytes([len(p)]) + p.encode("ascii") for p in name.rstrip(".").split("."))
    question = labels + b"\x00" + struct.pack(">HH", qtype, 1)    # type, class 1 = Internet
    return query_id, header + question


def read_name(data, pos):
    """Read a name. Answers reuse earlier names with a 2-byte pointer to save space."""
    labels, jumped, end = [], False, pos
    while True:
        length = data[pos]
        if length == 0:
            pos += 1
            break
        if length >= 0xC0:                           # pointer: "the rest of the name is at offset X"
            if not jumped:
                end = pos + 2
            pos = ((length & 0x3F) << 8) | data[pos + 1]
            jumped = True
            continue
        labels.append(data[pos + 1:pos + 1 + length].decode("ascii"))
        pos += 1 + length
    return ".".join(labels), (end if jumped else pos)


def read_record(data, pos):
    name, pos = read_name(data, pos)
    rtype, _cls, ttl, rdlen = struct.unpack(">HHIH", data[pos:pos + 10])
    pos += 10
    rdata = data[pos:pos + rdlen]
    if rtype == 1:
        value = socket.inet_ntop(socket.AF_INET, rdata)
    elif rtype == 28:
        value = socket.inet_ntop(socket.AF_INET6, rdata)
    elif rtype in (2, 5):
        value = read_name(data, pos)[0]
    elif rtype == 6:                                 # SOA: the zone's "who is in charge" record
        value = "primary server " + read_name(data, pos)[0]
    elif rtype == 15:
        value = f"preference {struct.unpack('>H', rdata[:2])[0]}, {read_name(data, pos + 2)[0]}"
    elif rtype == 16:
        value = rdata[1:1 + rdata[0]].decode("utf-8", "replace")   # first text piece only
    else:
        value = rdata.hex()
    return {"name": name, "type": TYPE_NAMES.get(rtype, rtype), "ttl": ttl, "value": value}, pos + rdlen


def ask(server, name, qtype, recursion=True):
    query_id, packet = build_query(name, qtype, recursion)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP: one message out, one back (Act 4)
    sock.settimeout(3)
    for attempt in range(1, 4):            # UDP never resends a lost message, so DNS clients do
        sock.sendto(packet, (server, 53))                      # 53 = the DNS port
        try:
            data, _ = sock.recvfrom(4096)
            break
        except TimeoutError:
            print(f"  (no answer from {server} after 3 s, attempt {attempt} of 3)")
    else:
        sys.exit(f"Gave up: {server} never answered.")
    sock.close()

    rid, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", data[:12])
    assert rid == query_id, "answer id does not match our question id"
    pos = 12
    for _ in range(qd):                                        # skip the echoed question
        pos = read_name(data, pos)[1] + 4
    sections = {}
    for section, count in (("answer", an), ("authority", ns), ("additional", ar)):
        sections[section] = []
        for _ in range(count):
            record, pos = read_record(data, pos)
            sections[section].append(record)
    info = {
        "bytes_sent": len(packet), "bytes_back": len(data),
        "authoritative": bool(flags & 0x0400), "truncated": bool(flags & 0x0200),
        "rcode": {0: "NOERROR", 3: "NXDOMAIN (no such name)"}.get(flags & 0xF, flags & 0xF),
    }
    return info, sections


def show(server, info, sections, limit=4):
    print(f"  asked {server}: sent {info['bytes_sent']} bytes, got {info['bytes_back']} bytes back"
          f" | {info['rcode']} | authoritative={info['authoritative']} truncated={info['truncated']}")
    for section, records in sections.items():
        for r in records[:limit]:
            print(f"    {section:<10} {r['name']:<28} {r['type']:<5} TTL={r['ttl']:<6} {r['value']}")
        if len(records) > limit:
            print(f"    {section:<10} ... and {len(records) - limit} more")
    if info["truncated"]:
        print("    (truncated: the full answer did not fit in one UDP message;"
              " a real resolver would ask again over TCP)")


def walk(name, qtype):
    """Do what a recursive resolver does: start at a root server and follow the referrals."""
    server, server_name, step = ROOT, "a.root-servers.net", 1
    while True:
        print(f"\nStep {step}: ask {server_name} ({server}) for {name} {TYPE_NAMES[qtype]}")
        info, s = ask(server, name, qtype, recursion=False)
        show(server, info, s)
        if s["answer"]:
            print(f"\nDone in {step} questions. Answer: {[r['value'] for r in s['answer']]}")
            return
        # A referral: "I don't know, ask these servers". Use one whose address came along (glue).
        glue = {r["name"]: r["value"] for r in s["additional"] if r["type"] == "A"}
        next_ns = [r["value"] for r in s["authority"] if r["type"] == "NS"]
        known = [ns for ns in next_ns if ns in glue]
        if known:
            server_name, server = known[0], glue[known[0]]
        elif next_ns:   # no glue: look up the name server's own address first (a side trip)
            server_name = next_ns[0]
            server = ask(RESOLVER, server_name, 1)[1]["answer"][-1]["value"]
            print(f"  (no glue: looked up {server_name} -> {server} separately)")
        else:
            print("No answer and no referral.")
            return
        step += 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:   # started with no arguments (e.g. the editor's Run button): ask instead
        print("usage: python hands-on-lab/act1-1.2-dns-query.py NAME [TYPE] [--walk]")
        print("examples: github.com | gmail.com MX | github.com A --walk")
        args = input("What should I look up? ").split()
        if not args:
            sys.exit(0)
    target = args[0]
    qtype = TYPES[args[1].upper()] if len(args) > 1 and not args[1].startswith("--") else 1
    if "--walk" in args:
        walk(target, qtype)
    else:
        print(f"Question: {target} {TYPE_NAMES[qtype]}?")
        show(RESOLVER, *ask(RESOLVER, target, qtype), limit=10)
