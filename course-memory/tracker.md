# CSE-311 Computer Networks Progress Tracker

Last updated: 2026-10-04

## Current Position

- **Week:** 1
- **Day:** 1
- **Phase:** Internet Foundations + Application Layer
- **Next action:** Watch Kurose Ch1 sections 1.1–1.3, then run `ipconfig` and `tracert google.com`

---

## Week 1: Internet Foundations + Application Layer (Oct 5–11)

**Kurose Chapters:** 1 + 2 | **Status:** Not Started

### Day 1 (Oct 5) — Ch1: 1.1–1.3
- [ ] Watched lecture (Internet, network edge, network core)
- [ ] Hands-on (`ipconfig`, `tracert google.com`)
- [ ] Notes created
- [ ] Quiz/check done

### Day 2 (Oct 6) — Ch1: 1.4–1.6
- [ ] Watched lecture (delay, throughput, protocol layers, security intro)
- [ ] Hands-on (draw 5-layer model with real request)
- [ ] Notes created
- [ ] Quiz/check done

### Day 3 (Oct 7) — Ch2: 2.1–2.2
- [ ] Watched lecture (App layer principles, HTTP)
- [ ] Wireshark: Getting Started lab
- [ ] Wireshark: HTTP lab
- [ ] Notes created

### Day 4 (Oct 8) — Ch2: 2.3–2.4
- [ ] Watched lecture (Email, DNS)
- [ ] Wireshark: DNS lab
- [ ] Notes created
- [ ] Quiz/check done

### Day 5 (Oct 9) — Ch2: 2.5–2.7
- [ ] Watched lecture (P2P, CDNs, socket programming intro)
- [ ] Hands-on (`curl -v` annotation)
- [ ] Notes created

### Day 6 (Oct 10) — Review
- [ ] Created notes for all Ch1 + Ch2 topics
- [ ] Took quiz with AI
- [ ] Mini-project: annotated `curl -v https://httpbin.org/get`

---

## Week 2: Transport Layer (Oct 12–18)

**Kurose Chapter:** 3 | **Status:** Not Started

### Day 7 (Oct 12) — Ch3: 3.1–3.3
- [ ] Watched lecture (Transport services, mux/demux, UDP)
- [ ] Wireshark: UDP lab
- [ ] Notes created

### Day 8 (Oct 13) — Ch3: 3.4
- [ ] Watched lecture (Reliable data transfer — rdt 1.0, 2.0, 3.0)
- [ ] Hands-on (drew rdt state machines)
- [ ] Notes created

### Day 9 (Oct 14) — Ch3: 3.5 (part 1)
- [ ] Watched lecture (TCP segment structure, seq/ack, RTT)
- [ ] Wireshark: TCP lab
- [ ] Notes created

### Day 10 (Oct 15) — Ch3: 3.5 (part 2)
- [ ] Watched lecture (TCP connection management, 3-way handshake)
- [ ] Hands-on (`netstat -ano`, TCP states)
- [ ] Notes created

### Day 11 (Oct 16) — Ch3: 3.6–3.7
- [ ] Watched lecture (flow control, congestion control)
- [ ] Discussed with AI (developer angle)
- [ ] Notes created

### Day 12 (Oct 17) — Review
- [ ] Created notes for all transport topics
- [ ] Took quiz with AI
- [ ] Mini-project: TCP echo server

---

## Week 3: Network Layer (Oct 19–25)

**Kurose Chapters:** 4 + 5 | **Status:** Not Started

### Day 13 (Oct 19) — Ch4: 4.1–4.2
- [ ] Watched lecture (Network layer overview, router internals)
- [ ] Notes created

### Day 14 (Oct 20) — Ch4: 4.3
- [ ] Watched lecture (IPv4, subnetting, CIDR, NAT)
- [ ] Wireshark: IP lab
- [ ] Wireshark: NAT lab
- [ ] Subnetting practice (192.168.1.0/24 into 4 subnets)
- [ ] Notes created

### Day 15 (Oct 21) — Ch4: 4.3–4.4
- [ ] Watched lecture (DHCP, IPv6, SDN)
- [ ] Wireshark: DHCP lab
- [ ] Hands-on (`ipconfig /all`, identify DHCP fields)
- [ ] Notes created

### Day 16 (Oct 22) — Ch5: 5.1–5.2
- [ ] Watched lecture (Routing: link state, distance vector)
- [ ] Hands-on (Dijkstra's + Bellman-Ford on paper)
- [ ] Notes created

### Day 17 (Oct 23) — Ch5: 5.3–5.4
- [ ] Watched lecture (OSPF, BGP)
- [ ] Hands-on (`tracert` to 3 sites, identify AS boundaries)
- [ ] Notes created

### Day 18 (Oct 24) — Ch5: 5.5–5.7
- [ ] Watched lecture (SDN control plane, ICMP, SNMP)
- [ ] Wireshark: ICMP lab
- [ ] Notes created

### Day 19 (Oct 25) — Review
- [ ] Created notes for all network layer topics
- [ ] Took quiz with AI
- [ ] Mini-project: VLSM exercise
- [ ] Started daily subnetting drills

---

## Week 4: Link Layer + Wireless (Oct 26–Nov 1)

**Kurose Chapters:** 6 + 7 | **Status:** Not Started

### Day 20 (Oct 26) — Ch6: 6.1–6.2
- [ ] Watched lecture (Link layer intro, error detection)
- [ ] Hands-on (CRC calculation by hand)
- [ ] Notes created

### Day 21 (Oct 27) — Ch6: 6.3
- [ ] Watched lecture (Multiple access: ALOHA, CSMA, CSMA/CD)
- [ ] Used Kurose interactive animations
- [ ] Notes created

### Day 22 (Oct 28) — Ch6: 6.4
- [ ] Watched lecture (MAC addresses, ARP, Ethernet, switches, VLANs)
- [ ] Wireshark: Ethernet and ARP lab
- [ ] Notes created

### Day 23 (Oct 29) — Ch6: 6.5–6.7
- [ ] Watched lecture (MPLS, data center networking)
- [ ] Studied with AI: PPP, HDLC, ATM, Frame Relay, STP, Token Ring, FDDI
- [ ] Notes created

### Day 24 (Oct 30) — Ch7: 7.1–7.3
- [ ] Watched lecture (Wireless links, WiFi 802.11, cellular)
- [ ] Wireshark: WiFi lab
- [ ] Notes created

### Day 25 (Oct 31) — Ch7 continued
- [ ] Watched lecture (Bluetooth, mobility, 5G)
- [ ] Gap-fill notes for syllabus topics
- [ ] Notes created

### Day 26 (Nov 1) — Review
- [ ] Created notes for all link layer + wireless topics
- [ ] Took quiz with AI
- [ ] Mini-project: Docker bridge network inspection

---

## Week 5: Security + Socket Programming (Nov 2–8)

**Kurose Chapter:** 8 + revisit Ch2.7 | **Status:** Not Started

### Day 27 (Nov 2) — Ch8: 8.1–8.3
- [ ] Studied (Security principles, symmetric/asymmetric crypto)
- [ ] Hands-on (hash a file, see avalanche effect)
- [ ] Notes created

### Day 28 (Nov 3) — Ch8: 8.4–8.5
- [ ] Studied (Message integrity, digital signatures, key distribution)
- [ ] Hands-on (inspect HTTPS certificate in browser)
- [ ] Notes created

### Day 29 (Nov 4) — Ch8: 8.6–8.8
- [ ] Studied (TLS, IPsec, firewalls, IDS)
- [ ] Wireshark: TLS lab
- [ ] Notes created

### Day 30 (Nov 5) — Security gap-fill
- [ ] Studied with AI: SSH, Diffie-Hellman, ACLs, gateways, IDEA, MD5, Blockchain
- [ ] Notes created

### Day 31 (Nov 6) — Socket programming
- [ ] Watched Kurose Ch2.7 revisited
- [ ] Built TCP chat server + client
- [ ] Notes created

### Day 32 (Nov 7) — Review
- [ ] Built UDP echo server
- [ ] Captured own program's traffic in Wireshark
- [ ] Took quiz with AI

---

## Week 6: Review + Exam Prep (Nov 9–15)

**Status:** Not Started

### Day 33 (Nov 9) — End-to-end trace
- [ ] Captured full website visit in Wireshark
- [ ] Wrote complete "what happens when I type a URL" narrative

### Day 34 (Nov 10) — Review Module 1 + 5
- [ ] Kurose knowledge checks Ch1 + Ch2
- [ ] Quiz with AI

### Day 35 (Nov 11) — Review Module 4 + 3
- [ ] Subnetting speed drills
- [ ] Routing algorithm practice
- [ ] TCP state diagram from memory
- [ ] Quiz with AI

### Day 36 (Nov 12) — Review Module 2 + 6
- [ ] Protocol comparison tables
- [ ] Security concept maps
- [ ] Quiz with AI

### Day 37 (Nov 13) — Capstone
- [ ] Built Docker Compose project (Nginx + backends + HTTPS)
- [ ] Traced one request end-to-end

### Day 38 (Nov 14) — Mock exam
- [ ] 30-question timed mock exam with AI
- [ ] Reviewed weak spots

### Day 39 (Nov 15) — Buffer
- [ ] Final weak-area review
- [ ] One-page revision cheat sheet created

---

## Progress Summary

| Week | Days Done | Status |
|---|---|---|
| Week 1: Foundations + App Layer | 0 / 6 | Not Started |
| Week 2: Transport Layer | 0 / 6 | Not Started |
| Week 3: Network Layer | 0 / 7 | Not Started |
| Week 4: Link Layer + Wireless | 0 / 7 | Not Started |
| Week 5: Security + Sockets | 0 / 6 | Not Started |
| Week 6: Review + Exam Prep | 0 / 7 | Not Started |
| **Total** | **0 / 39** | |

## Wireshark Labs Progress

| Lab | Status |
|---|---|
| Getting Started | Not Started |
| HTTP | Not Started |
| DNS | Not Started |
| UDP | Not Started |
| TCP | Not Started |
| IP | Not Started |
| NAT | Not Started |
| DHCP | Not Started |
| ICMP | Not Started |
| Ethernet & ARP | Not Started |
| 802.11 WiFi | Not Started |
| TLS | Not Started |
