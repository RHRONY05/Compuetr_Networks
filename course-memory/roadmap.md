# CSE-311 Computer Networks: 6-Week Roadmap

## Overview

- **Duration:** 6 weeks (Oct 5 – Nov 15, 2026)
- **Pace:** 8–10 hours/week, ~5–6 study days per week
- **Order:** Kurose top-down (Intro → App → Transport → Network → Link → Security)
- **Video Spine:** Kurose & Ross official lectures
- **Labs:** Kurose Wireshark labs (standalone PDFs with step-by-step instructions)
- **Exam:** Mid-November 2026

## Daily Study Routine (1.5–2 hours)

```
 5 min │ Recall: write 3 things from yesterday, no notes
35 min │ Watch Kurose video lecture section (take notes)
30 min │ Hands-on: Wireshark lab, terminal tool, or build
15 min │ Come to AI: ask doubts, request developer angle
10 min │ Review: update tracker, "create note about this"
 5 min │ Preview: skim tomorrow's topic title
```

---

## Week 1: Internet Foundations + Application Layer (Oct 5–11, ~10 hrs)

**Kurose:** Chapter 1 (Internet & protocols) + Chapter 2 (Application Layer)
**Lectures:** https://gaia.cs.umass.edu/kurose_ross/videos/1 and https://gaia.cs.umass.edu/kurose_ross/videos/2

**Syllabus topics covered:**
- Definition of internet
- Client-server and peer-to-peer models
- Network access and physical media (overview)
- ISPs and internet backbones
- Packet-switched and circuit-switched networks
- Protocol hierarchies and service models
- Principles of application layer protocols
- Web and HTTP
- DNS
- Electronic mail, SMTP, POP3, IMAP
- File Transfer Protocol

### Day 1 (Oct 5, Sun)
- **Watch:** Kurose Ch1 sections 1.1–1.3 (Internet, network edge, network core)
- **Hands-on:** Run `ipconfig`, identify default gateway, run `tracert google.com` and annotate hops
- **Outcome:** Explain packet switching vs circuit switching; draw the path from laptop to server

### Day 2 (Oct 6, Mon)
- **Watch:** Kurose Ch1 sections 1.4–1.6 (delay/throughput, protocol layers, security intro)
- **Hands-on:** Draw the 5-layer model and label one of your HTTP requests through each layer
- **Outcome:** Calculate propagation + transmission delay for a simple example

### Day 3 (Oct 7, Tue)
- **Watch:** Kurose Ch2 sections 2.1–2.2 (App layer principles, HTTP)
- **Hands-on:** Install Wireshark → **Wireshark Getting Started lab** → **HTTP lab**
- **Lab PDFs:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v9.0.pdf and https://www-net.cs.umass.edu/wireshark-labs/Wireshark_HTTP_v9.0.pdf
- **Outcome:** Capture and read HTTP GET/response in Wireshark

### Day 4 (Oct 8, Wed)
- **Watch:** Kurose Ch2 sections 2.3–2.4 (Email: SMTP/POP3/IMAP, DNS)
- **Hands-on:** **Wireshark DNS lab** + `nslookup` with different record types
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_DNS_v9.pdf
- **Outcome:** Capture DNS queries in Wireshark; identify A, AAAA, CNAME records

### Day 5 (Oct 9, Thu)
- **Watch:** Kurose Ch2 sections 2.5–2.7 (P2P, video streaming/CDNs, socket programming intro)
- **Hands-on:** Read Cloudflare's CDN page (15 min). Run `curl -v https://httpbin.org/get` and annotate every output line
- **Outcome:** Explain how CDNs work and why P2P scales differently than client-server

### Day 6 (Oct 10, Fri)
- **Review day:** Come to AI for notes on Ch1 + Ch2 topics, take quiz
- **Hands-on:** Create notes for all topics covered this week
- **Mini-project:** Annotate `curl -v https://httpbin.org/get` output: identify DNS, TCP, TLS, HTTP layers

---

## Week 2: Transport Layer (Oct 12–18, ~8 hrs)

**Kurose:** Chapter 3 (Transport Layer)
**Lectures:** https://gaia.cs.umass.edu/kurose_ross/videos/3

**Syllabus topics covered:**
- Transport layer services
- Multiplexing and demultiplexing
- Connectionless and connection-oriented transport
- UDP
- Principles of reliable data transfer
- TCP
- Connection management
- Timer management
- Principles of congestion control
- Congestion and flow controls with TCP

### Day 7 (Oct 12, Sun)
- **Watch:** Kurose Ch3 sections 3.1–3.3 (Transport services, mux/demux, UDP)
- **Hands-on:** **Wireshark UDP lab**
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_UDP_v9.pdf
- **Outcome:** Explain multiplexing using port numbers; compare UDP header to TCP header

### Day 8 (Oct 13, Mon)
- **Watch:** Kurose Ch3 section 3.4 (Reliable data transfer principles — rdt 1.0, 2.0, 3.0)
- **Hands-on:** Draw the rdt state machines from memory. Use Kurose's interactive animations
- **Animations:** https://gaia.cs.umass.edu/kurose_ross/animations.php
- **Outcome:** Explain stop-and-wait, pipelining, and why Go-Back-N and Selective Repeat exist

### Day 9 (Oct 14, Tue)
- **Watch:** Kurose Ch3 section 3.5 (TCP segment structure, seq/ack numbers, RTT estimation)
- **Hands-on:** **Wireshark TCP lab** — identify SYN, SYN-ACK, ACK in a real capture
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_TCP_v9.pdf
- **Outcome:** Read sequence and acknowledgment numbers from a Wireshark capture

### Day 10 (Oct 15, Wed)
- **Watch:** Kurose Ch3 section 3.5 continued (TCP connection management: 3-way handshake, teardown)
- **Hands-on:** Use `netstat -ano` to see TCP connections in different states (ESTABLISHED, TIME_WAIT, etc.)
- **Outcome:** Draw the TCP state diagram; explain why TIME_WAIT exists

### Day 11 (Oct 16, Thu)
- **Watch:** Kurose Ch3 sections 3.6–3.7 (Flow control, congestion control, TCP Reno/CUBIC)
- **Hands-on:** Ask AI: "Explain TCP congestion control like I'm debugging a slow API response"
- **Outcome:** Explain slow start, congestion avoidance, fast retransmit, fast recovery

### Day 12 (Oct 17, Fri)
- **Review day:** Notes, quiz, catch-up
- **Mini-project:** Write a TCP echo server in Python or Node.js using raw sockets. Connect with `telnet`

---

## Week 3: Network Layer (Oct 19–25, ~10 hrs)

**Kurose:** Chapter 4 (Data Plane) + Chapter 5 (Control Plane)
**Lectures:** https://gaia.cs.umass.edu/kurose_ross/videos/4 and https://gaia.cs.umass.edu/kurose_ross/videos/5

**Syllabus topics covered:**
- Network layer services
- Internet Protocol, IPv4, IPv6
- IP addressing, Subnetting, VLSM
- ICMP
- DHCP and NAT
- Fragmentation and reassembly
- Router architecture
- Routing principles
- Distance vector routing
- Link state routing
- Hierarchical routing
- Multicast routing
- Congestion control (network layer)
- Mobile IP
- Internetworking
- WAN technologies and protocols
- Introduction to 5G and next generation networks

### Day 13 (Oct 19, Sun)
- **Watch:** Kurose Ch4 sections 4.1–4.2 (Network layer overview, what's inside a router)
- **Hands-on:** Conceptual — draw the data plane vs control plane distinction
- **Outcome:** Explain forwarding vs routing; describe input/output port processing

### Day 14 (Oct 20, Mon)
- **Watch:** Kurose Ch4 section 4.3 (IPv4, addressing, subnetting, CIDR, NAT)
- **Hands-on:** **Wireshark IP lab** + **NAT lab**. Practice: subnet 192.168.1.0/24 into 4 subnets by hand
- **Lab PDFs:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_IP_v9.pdf and https://www-net.cs.umass.edu/wireshark-labs/Wireshark_NAT_v9.pdf
- **Outcome:** Calculate network address, broadcast, host range for any /prefix

### Day 15 (Oct 21, Tue)
- **Watch:** Kurose Ch4 sections 4.3 continued (DHCP, IPv6) + 4.4 (Generalized forwarding, SDN)
- **Hands-on:** **Wireshark DHCP lab**. Run `ipconfig /all` and identify every DHCP-assigned field
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_DHCP_v9.pdf
- **Outcome:** Explain DORA (Discover, Offer, Request, Acknowledge); describe IPv6 motivation

### Day 16 (Oct 22, Wed)
- **Watch:** Kurose Ch5 sections 5.1–5.2 (Routing algorithms: link state, distance vector)
- **Hands-on:** Work through Dijkstra's algorithm and Bellman-Ford on a 6-node graph by hand
- **Outcome:** Trace both algorithms step-by-step; explain count-to-infinity problem

### Day 17 (Oct 23, Thu)
- **Watch:** Kurose Ch5 sections 5.3–5.4 (Intra-AS: OSPF, Inter-AS: BGP)
- **Hands-on:** Run `tracert` to 3 different sites, identify where AS boundaries likely are
- **Outcome:** Explain why the internet uses hierarchical routing; distinguish OSPF from BGP

### Day 18 (Oct 24, Fri)
- **Watch:** Kurose Ch5 sections 5.5–5.7 (SDN control plane, ICMP, network management/SNMP)
- **Hands-on:** **Wireshark ICMP lab** (using ping and traceroute captures)
- **Outcome:** Explain ICMP message types; how traceroute uses TTL

### Day 19 (Oct 25, Sat)
- **Review day:** Notes, quiz. **15-min daily subnetting drills start here (continue through exam)**
- **Mini-project:** VLSM exercise: allocate IPs for a company with 3 departments needing 30, 60, and 120 hosts

---

## Week 4: Link Layer + Wireless (Oct 26–Nov 1, ~10 hrs)

**Kurose:** Chapter 6 (Link Layer) + Chapter 7 (Wireless)
**Lectures:** https://gaia.cs.umass.edu/kurose_ross/videos/6 and https://gaia.cs.umass.edu/kurose_ross/videos/7

**Syllabus topics covered:**
- Physical and data link layer services
- Error detection and correction techniques
- Flow control
- Multiple access protocols (CSMA, CSMA/CD, ALOHA, Slotted ALOHA)
- Network topology
- Token Ring and FDDI
- Hub, Bridge and switch, STP
- LAN protocols and IEEE 802.*
- PPP, HDLC
- ARP and RARP
- Ethernet, Fast Ethernet, Gigabit Ethernet
- ATM and Frame Relay
- Wi-Fi and WLAN architecture
- Bluetooth
- MPLS
- Virtualization

### Day 20 (Oct 26, Sun)
- **Watch:** Kurose Ch6 sections 6.1–6.2 (Link layer intro, error detection: parity, CRC, checksums)
- **Hands-on:** Work through a CRC calculation by hand with a small example
- **Outcome:** Explain parity check, internet checksum, and CRC; when each is used

### Day 21 (Oct 27, Mon)
- **Watch:** Kurose Ch6 section 6.3 (Multiple access: channel partitioning, random access, taking turns)
- **Hands-on:** Use Kurose's interactive ALOHA/CSMA animations
- **Outcome:** Compare pure ALOHA, slotted ALOHA, CSMA, CSMA/CD; explain why Ethernet uses CSMA/CD

### Day 22 (Oct 28, Tue)
- **Watch:** Kurose Ch6 section 6.4 (Switched LANs: MAC addresses, ARP, Ethernet, switches, VLANs)
- **Hands-on:** **Wireshark Ethernet and ARP lab**
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_Ethernet_ARP_v9.pdf
- **Outcome:** Capture ARP request/reply; explain why ARP is needed alongside IP

### Day 23 (Oct 29, Wed)
- **Watch:** Kurose Ch6 sections 6.5–6.7 (Link virtualization: MPLS, data center networking)
- **Hands-on:** Ask AI about: PPP, HDLC, ATM, Frame Relay, STP, Token Ring, FDDI (syllabus items Kurose covers briefly)
- **Outcome:** Brief notes on each; understand STP's purpose in preventing loops

### Day 24 (Oct 30, Thu)
- **Watch:** Kurose Ch7 sections 7.1–7.3 (Wireless links, WiFi 802.11, cellular architecture)
- **Hands-on:** **Wireshark 802.11 WiFi lab**
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_802.11_v9.pdf
- **Outcome:** Explain hidden terminal problem; compare WiFi (CSMA/CA) to Ethernet (CSMA/CD)

### Day 25 (Oct 31, Fri)
- **Watch:** Kurose Ch7 continued (mobility, cellular, Bluetooth, 5G overview)
- **Hands-on:** Notes + quiz. Gap-fill for syllabus topics Kurose covers lightly
- **Outcome:** Brief notes on Bluetooth, 5G, mobility management

### Day 26 (Nov 1, Sat)
- **Review day + Mini-project:** Create a Docker bridge network. Run 2 containers, ping between them, inspect MAC addresses with `docker network inspect`

---

## Week 5: Security + Socket Programming (Nov 2–8, ~8 hrs)

**Kurose:** Chapter 8 (Security — note: official videos may be incomplete, supplement with AI)
**Lectures:** https://gaia.cs.umass.edu/kurose_ross/lectures.php (Ch8 link when available)

**Syllabus topics covered:**
- Socket programming with TCP and UDP
- SNMP
- Security issues in computer networks
- Principles of cryptography
- Symmetric key cryptography, DES, IDEA
- Public key encryption, RSA
- MD5
- SSH
- Message integrity and digital signatures
- End-point authentication
- Diffie-Hellman key exchange algorithm
- Access-control list
- Gateway
- Firewalls
- Intrusion detection systems
- Blockchain

### Day 27 (Nov 2, Sun)
- **Watch:** Kurose Ch8 sections 8.1–8.3 (Security principles, symmetric crypto, public key crypto)
- **Hands-on:** Hash a file: `certutil -hashfile yourfile.txt MD5`, change 1 byte, re-hash. See avalanche effect
- **Outcome:** Distinguish symmetric vs asymmetric encryption; explain DES, AES, RSA at a high level

### Day 28 (Nov 3, Mon)
- **Watch:** Kurose Ch8 sections 8.4–8.5 (Message integrity, digital signatures, key distribution)
- **Hands-on:** Inspect an HTTPS certificate in browser (click padlock → certificate → details)
- **Outcome:** Explain hash functions, MACs, digital signatures, and certificate chains

### Day 29 (Nov 4, Tue)
- **Watch:** Kurose Ch8 sections 8.6–8.8 (TLS, IPsec, firewalls, IDS)
- **Hands-on:** **Wireshark TLS lab** + `curl -v https://google.com` — annotate the TLS handshake steps
- **Lab PDF:** https://www-net.cs.umass.edu/wireshark-labs/Wireshark_TLS_v9.pdf
- **Outcome:** Trace a TLS 1.3 handshake; explain why HTTPS needs both asymmetric and symmetric crypto

### Day 30 (Nov 5, Wed)
- **Study with AI:** SSH internals, Diffie-Hellman key exchange, ACLs, gateways, IDEA, MD5 details, Blockchain basics
- **Hands-on:** If SSH available: run `ssh -v` and read the handshake output
- **Outcome:** Exam-ready notes on all Module 6 topics

### Day 31 (Nov 6, Thu)
- **Watch:** Kurose Ch2.7 revisited (Socket programming)
- **Hands-on:** Build a TCP chat server + client in Python or Node.js
- **Outcome:** Working client-server program; understand bind, listen, accept, connect

### Day 32 (Nov 7, Fri)
- **Build:** UDP echo server. Compare the code to the TCP version
- **Hands-on:** Capture your own TCP/UDP program's traffic in Wireshark
- **Outcome:** See your own SYN-ACK handshake and data packets

---

## Week 6: Review, Integration, and Exam Prep (Nov 9–15, ~8 hrs)

**No new lectures.** Pure consolidation, practice, and the capstone project.

### Day 33 (Nov 9, Sun)
- **End-to-end trace:** Open Wireshark, visit a website, annotate every packet layer by layer
- **Write:** A complete narrative of "what happens when I type a URL and press Enter"

### Day 34 (Nov 10, Mon)
- **Review:** Module 1 + Module 5 (Introduction + Application Layer)
- **Do:** Kurose knowledge checks for Ch1 + Ch2 at https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/
- **Quiz with AI** on HTTP, DNS, SMTP, FTP, socket programming

### Day 35 (Nov 11, Tue)
- **Review:** Module 4 + Module 3 (Transport + Network Layer)
- **Drills:** Subnetting speed drills, routing algorithm practice, TCP state diagram from memory
- **Quiz with AI** on TCP, UDP, IP, DHCP, NAT, routing algorithms

### Day 36 (Nov 12, Wed)
- **Review:** Module 2 + Module 6 (Link Layer + Security)
- **Create:** Protocol comparison tables, security concept maps
- **Quiz with AI** on ARP, Ethernet, CSMA, TLS, RSA, firewalls

### Day 37 (Nov 13, Thu) — CAPSTONE
- **Build:** Docker Compose project: 2 backend containers + Nginx reverse proxy + self-signed HTTPS
- **Trace:** Use `curl -v` and Wireshark to trace one request end-to-end through the system
- **Document:** Which layer handles what in your Docker setup

### Day 38 (Nov 14, Fri)
- **Mock exam:** Ask AI for a 30-question timed mixed-topic exam
- **Fix:** Weak spots identified in mock exam

### Day 39 (Nov 15, Sat) — BUFFER
- **Final review:** Focus on weak areas only
- **Create:** One-page personal revision cheat sheet

---

## Wireshark Lab Quick Reference

All labs are standalone PDFs with step-by-step instructions. Download trace files: https://www-net.cs.umass.edu/wireshark-labs/wireshark-traces-9e.zip

| Lab | When | PDF Link |
|---|---|---|
| Getting Started | Week 1, Day 3 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v9.0.pdf |
| HTTP | Week 1, Day 3 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_HTTP_v9.0.pdf |
| DNS | Week 1, Day 4 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_DNS_v9.pdf |
| UDP | Week 2, Day 7 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_UDP_v9.pdf |
| TCP | Week 2, Day 9 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_TCP_v9.pdf |
| IP | Week 3, Day 14 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_IP_v9.pdf |
| NAT | Week 3, Day 14 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_NAT_v9.pdf |
| DHCP | Week 3, Day 15 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_DHCP_v9.pdf |
| ICMP | Week 3, Day 18 | (v8.0 available) |
| Ethernet & ARP | Week 4, Day 22 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_Ethernet_ARP_v9.pdf |
| 802.11 WiFi | Week 4, Day 24 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_802.11_v9.pdf |
| TLS | Week 5, Day 29 | https://www-net.cs.umass.edu/wireshark-labs/Wireshark_TLS_v9.pdf |
