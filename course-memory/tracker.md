# CSE-311 Computer Networks Progress Tracker

Last updated: 2026-10-10

## Current Position

- **Week:** 1
- **Day:** 3
- **Focus:** Default Gateways & Outer Network Access
- **Next action:** Videos 6 & 7 (Understanding Default Gateway, How Gateways Facilitate Communication)

---

## Week 1: Foundations, IP Addressing & Core Protocols (Oct 10–16)

**Video Spine:** Chai aur Computer Network (Videos 1–13) | **Status:** In Progress

### Day 1 (Oct 10) — Series Intro & The Request Journey
- **Videos:** Video 1 (Intro) + Video 2 (What Really Happens When You Make an HTTP Request?)
- [x] Watched Videos 1 & 2
- [x] Hands-on: Run `curl -v https://httpbin.org/get`, inspect request/response headers
- [x] Notes created (`notes/00-foundations/02-request-lifecycle.md`)
- [x] Quiz/check done

### Day 2 (Oct 11) — IP Addressing, CIDR & Subnet Masks
- **Videos:** Videos 3, 4, 5 (IP Address Structure, Network/Host/CIDR, Subnet Masks Deep Dive)
- [x] Watched Videos 3, 4, 5
- [x] Hands-on: Run `ipconfig`/PowerShell, identify IP address, subnet mask, prefix length
- [x] Notes created (`01-ip-and-cidr.md`, `02-subnet-masks-and-switches.md`)
- [x] Quiz/check done

### Day 3 (Oct 12) — Default Gateways & Outer Network Access
- **Videos:** Videos 6 & 7 (Understanding Default Gateway, How Gateways Facilitate Communication)
- [ ] Watched Videos 6 & 7
- [ ] Hands-on: Identify Default Gateway in `ipconfig`, run `tracert 8.8.8.8` to see first hop
- [ ] Notes created
- [ ] Quiz/check done

### Day 4 (Oct 13) — MAC Addresses & ARP
- **Videos:** Videos 8, 9, 10 (What is a MAC Address, IP vs MAC, How Does ARP Work)
- [ ] Watched Videos 8, 9, 10
- [ ] Hands-on: Run `getmac` and `arp -a` in terminal to see local ARP cache
- [ ] Notes created
- [ ] Quiz/check done

### Day 5 (Oct 14) — OSI vs TCP/IP Models, Routing & ICMP (Ping)
- **Videos:** Videos 11, 12, 13 (OSI vs TCP/IP, How Routing Works, What Happens When You PING Google)
- [ ] Watched Videos 11, 12, 13
- [ ] Hands-on: Run `ping google.com` and `ping 127.0.0.1`, examine TTL and RTT
- [ ] Notes created
- [ ] Quiz/check done

### Day 6 (Oct 15) — Week 1 Review & Wireshark Getting Started
- [ ] Created notes for all Week 1 topics
- [ ] Wireshark: Getting Started lab (capture a ping and curl request)
- [ ] Took active recall quiz with AI tutor

---

## Week 2: Transport Layer & TCP/UDP Deep Dive (Oct 17–23)

**Video Spine:** Chai aur Computer Network (Videos 14–25) | **Status:** Not Started

### Day 7 (Oct 17) — Transport Layer, Ports & Sockets
- **Videos:** Videos 14, 15, 16 (Transport layer services, Port numbers & Sockets, UDP vs TCP)
- [ ] Watched Videos 14, 15, 16
- [ ] Wireshark: UDP lab
- [ ] Notes created

### Day 8 (Oct 18) — TCP 3-Way Handshake & Sequence Numbers
- **Videos:** Videos 17, 18, 19 (TCP Handshake, Sequence & Ack Numbers, Connection Teardown)
- [ ] Watched Videos 17, 18, 19
- [ ] Wireshark: TCP lab (identify SYN, SYN-ACK, ACK packets)
- [ ] Notes created

### Day 9 (Oct 19) — TCP Connection States
- **Videos:** Videos 20, 21, 22 (TCP States: ESTABLISHED, TIME_WAIT, CLOSE_WAIT)
- [ ] Watched Videos 20, 21, 22
- [ ] Hands-on: Run `netstat -ano` in terminal, filter for ESTABLISHED vs TIME_WAIT
- [ ] Notes created

### Day 10 (Oct 20) — TCP Flow Control & Congestion Control
- **Videos:** Videos 23, 24, 25 (Flow control, Sliding Window, Congestion control basics)
- [ ] Watched Videos 23, 24, 25
- [ ] Discussion with AI: How TCP congestion control impacts API latency and web apps
- [ ] Notes created

### Day 11 (Oct 21) — DNS (Domain Name System) Deep Dive
- **Videos:** Videos 26 & 27 (How DNS resolves names, Root/TLD servers, DNS record types)
- [ ] Watched Videos 26 & 27
- [ ] Hands-on: `nslookup google.com` and `nslookup -type=MX google.com`, Wireshark DNS lab
- [ ] Notes created

### Day 12 (Oct 22) — Week 2 Review & Socket Mini-Project
- [ ] Created notes for transport layer
- [ ] Mini-project: Build a simple TCP Echo Server in Node.js or Python
- [ ] Took active recall quiz with AI tutor

---

## Week 3: Application Protocols, WebSockets & Security (Oct 24–30)

**Video Spine:** Chai aur Computer Network (Videos 28–40) | **Status:** Not Started

### Day 13 (Oct 24) — DHCP (Dynamic Host Configuration)
- **Videos:** Videos 28, 29, 30 (DHCP DORA process, IP leasing, Static vs Dynamic)
- [ ] Watched Videos 28, 29, 30
- [ ] Hands-on: `ipconfig /all`, identify DHCP lease, Wireshark DHCP lab
- [ ] Notes created

### Day 14 (Oct 25) — HTTP Evolution (HTTP/1.1 vs HTTP/2 vs HTTP/3)
- **Videos:** Videos 31, 32, 33 (HTTP/1.1 pipelining, HTTP/2 multiplexing, HTTP/3 QUIC)
- [ ] Watched Videos 31, 32, 33
- [ ] Hands-on: Inspect HTTP/2 & HTTP/3 multiplexing in browser DevTools Network tab
- [ ] Notes created

### Day 15 (Oct 26) — WebSockets & Real-Time Communication
- **Videos:** Videos 34, 35, 36 (WebSockets vs HTTP Polling vs SSE)
- [ ] Watched Videos 34, 35, 36
- [ ] Hands-on: Inspect WebSocket frames in Chrome DevTools on a live chat app
- [ ] Notes created

### Day 16 (Oct 27) — HTTPS, SSL/TLS Handshake
- **Videos:** Videos 37, 38, 39 (Symmetric vs Asymmetric encryption, TLS Handshake, Certificates)
- [ ] Watched Videos 37, 38, 39
- [ ] Hands-on: Click padlock in browser to inspect certificate chain, Wireshark TLS lab
- [ ] Notes created

### Day 17 (Oct 28) — Cookies, Sessions, JWTs & CORS
- **Videos:** Video 40 + Developer Security Deep Dive
- [ ] Watched Video 40
- [ ] Hands-on: Inspect CORS preflight `OPTIONS` request in DevTools
- [ ] Notes created

### Day 18 (Oct 29) — Week 3 Review
- [ ] Consolidated notes on Application Layer & Security
- [ ] Took active recall quiz with AI tutor

---

## Week 4: Cloud Networking, Proxies, CDNs & VPNs (Oct 31–Nov 6)

**Video Spine:** Chai aur Computer Network (Videos 41–49) | **Status:** Not Started

### Day 19 (Oct 31) — NAT (Network Address Translation)
- **Videos:** Videos 41, 42, 43 (NAT types, PAT, Private vs Public IPs, Port Forwarding)
- [ ] Watched Videos 41, 42, 43
- [ ] Hands-on: Wireshark NAT lab, map internal IP to router public IP
- [ ] Notes created

### Day 20 (Nov 1) — Proxies & Load Balancers
- **Videos:** Videos 44, 45, 46 (Forward Proxy vs Reverse Proxy, L4 vs L7 Load Balancing)
- [ ] Watched Videos 44, 45, 46
- [ ] Hands-on: Trace Nginx reverse proxy headers (`X-Forwarded-For`, `X-Forwarded-Proto`)
- [ ] Notes created

### Day 21 (Nov 2) — CDNs, Edge Caching & VPNs
- **Videos:** Videos 47, 48, 49 (CDNs, Cloudflare edge caching, VPN tunnels, Series recap)
- [ ] Watched Videos 47, 48, 49
- [ ] Hands-on: Run `curl -I` against Cloudflare-backed site, check `cf-cache-status: HIT`
- [ ] Notes created

### Day 22 (Nov 3) — Full Capstone: End-to-End Packet Trace
- [ ] Trace an end-to-end user journey: URL typed $\rightarrow$ DNS $\rightarrow$ TCP $\rightarrow$ TLS $\rightarrow$ Reverse Proxy $\rightarrow$ App
- [ ] Wrote complete developer architecture summary
- [ ] Took comprehensive full-course quiz with AI tutor

---

## Week 5: CUET Exam Numerical & Syllabus Gap-Fill Cram (Nov 7–13)

**Focus:** Exam Formulas, Numericals & Academic Syllabus Items | **Status:** Not Started

### Day 23 (Nov 7) — Subnetting & VLSM Speed Drills
- [ ] Mastered Classless / CIDR subnetting calculations by hand
- [ ] Solved 5 previous year CUET subnetting numericals

### Day 24 (Nov 8) — Error Detection: CRC & Hamming Code
- [ ] CRC polynomial division by hand
- [ ] Hamming Code error detection and correction

### Day 25 (Nov 9) — Flow Control Formulas & Window Calculations
- [ ] Stop-and-Wait efficiency ($a = T_{prop}/T_{trans}$)
- [ ] Go-Back-N and Selective Repeat window size formulas

### Day 26 (Nov 10) — Routing Algorithms: Dijkstra & Bellman-Ford
- [ ] Solved Dijkstra step-by-step routing table on paper
- [ ] Bellman-Ford distance vector iterations & count-to-infinity

### Day 27 (Nov 11) — Multiple Access Formulas (ALOHA & CSMA)
- [ ] Pure ALOHA ($S = G e^{-2G}$) vs Slotted ALOHA ($S = G e^{-G}$) throughput
- [ ] CSMA/CD minimum frame length calculation ($L \ge 2 \times R \times T_{prop}$)

### Day 28 (Nov 12) — Legacy Syllabus Quick-Fire
- [ ] ATM, Frame Relay, Token Ring, FDDI, HDLC, PPP, STP
- [ ] Classical Ciphers & Cryptography (DES, RSA mathematical steps)

### Day 29 (Nov 13) — Timed Mock Exam
- [ ] 30-question mixed theory & numerical exam with AI tutor
- [ ] Addressed all weak points

---

## Progress Summary

| Module | Status |
|---|---|
| Week 1: Foundations & IP | 2 / 6 days |
| Week 2: Transport & TCP | 0 / 6 days |
| Week 3: Web Protocols & Security | 0 / 6 days |
| Week 4: Proxies, CDNs & Cloud | 0 / 4 days |
| Week 5: CUET Exam Cram & Numericals | 0 / 7 days |
| **Total** | **2 / 29 days** |
