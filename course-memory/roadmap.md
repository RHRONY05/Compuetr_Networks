# Computer Networks: Story-Based Roadmap

> **Goal:** Build a strong, durable foundation in computer networks as a **software developer** who wants to become a software engineer. Not exam-centric. Depth where it helps you reason about real systems (APIs, debugging, performance, security, cloud); brevity where it doesn't.
> **Method:** One story (the life of an HTTP request), nine acts. Every topic is a zoom-in on one step of [the lifecycle map](../notes/00-foundations/02-request-lifecycle.md).
> **Pace:** 2–3 hours per session, about one session a day. There is **no end date**; the unit of progress is a completed act. Estimated total: ~33 sessions.

---

## How This Plan Works

### Sources (best tool per topic, not one playlist)

| Tag | Source | Strength | Used for |
|---|---|---|---|
| **C##** | Chai aur Computer Network (49 videos) | Developer angle, Wireshark demos, HTTP/2/3, TLS, NAT | App/transport/TLS/IP anatomy topics |
| **K#.#** | Kurose & Ross lectures (Ch1–6; no videos found for Ch7–8) | Clean top-down structure, deeper principles, animations | Foundations, transport principles, routing, link layer |
| **AI** | Explanation by your AI tutor | Fills gaps with no video, adapts to you | Missing topics, security/crypto, infrastructure |

Full catalogs: [video_index.md](video_index.md). You never watch a full lecture blind: AI fetches the transcript and gives a pre-flight briefing first, and you watch only the parts worth seeing.

### Vocabulary: introduced just in time

There is no up-front glossary. Every lesson starts with a **🔑 Keywords** block that introduces the words it needs, in plain language, right before they are used. Those words accumulate in [notes/GLOSSARY.md](../notes/GLOSSARY.md). Act 0 is deliberately small: [Internet Basics](../notes/00-foundations/01-internet-basics.md) (what the Internet and Web are) and the lifecycle anchor.

### Depth tags used everywhere

* 🟢 **Core now:** the mental model and mechanics you need today.
* 🟡 **Nuance:** what videos simplify vs. how production actually works.
* 🔵 **Deferred:** buzzwords to recognize and park; revisit only when a real need appears.
* ⭐ **Build:** a hands-on or project step.

### The Session Loop (every session, every act)

```text
  5 min │ RECALL    Write 3 things from last time, no notes.
  5 min │ ANCHOR    Open the lifecycle note. Find today's step. Say it out loud.
 40 min │ LEARN     AI pre-flight briefing → targeted video sections / reading.
 45 min │ HANDS-ON  Run it on your own machine (terminal, Wireshark, DevTools).
 30 min │ BUILD     The act's project milestone (small, real code).
 15 min │ ASK       Doubts; ask "how does this fail in production?"
 15 min │ NOTE      "Create note about this." Update the anchor's Revisit Log.
```

Sessions shorter than 3 hours trim BUILD or NOTE, never RECALL, ANCHOR or HANDS-ON.

### The Project Thread: "Build the Stack"

One small codebase grows across the course. By the end, you've built the thing the lifecycle describes.

| Milestone | Act | What you build |
|---|---|---|
| A1 | 1 | Send a raw HTTP request by typing the text yourself over a socket |
| A2 | 1 | *(stretch)* Hand-build a DNS query as bytes over UDP and parse the reply |
| A3 | 2 | `is_local(my_ip, mask, target)` and a CIDR calculator using bit operations |
| A4 | 3 | Read your ARP table; *(stretch)* send an ARP request with `scapy` |
| A5 | 4 | TCP echo server and client → then a tiny HTTP/1.1 server serving `/profile` JSON |
| A6 | 5 | *(stretch)* A mini `traceroute` using TTL |
| A7 | 6 | Wrap your server in TLS with a self-signed certificate |
| A8 | 7 | Compare HTTP/1.1 and HTTP/2 on the same page; enable HTTP/2 on Nginx |
| A9 | 8 | Docker Compose: Nginx reverse proxy + 2 backends + TLS |
| ★ | 9 | Trace one request through all of it, in Wireshark, layer by layer |

### Tools used (the AI will guide installs and usage)

Terminal (`curl`, `ipconfig`, `route print`, `arp`, `tracert`, `nslookup`, `netstat`), **Wireshark**, browser **DevTools → Network**, Python (`socket`, `ssl`, optionally `scapy`), `openssl`, **Docker**, and optionally **Cisco Packet Tracer** to visualize switches, subnets and routing in a simulated network. The AI can also build small interactive visualizer pages (subnet calculator, TCP handshake stepper, routing-algorithm stepper) when a picture would help.

---

## Act 0: The Trigger ✅ *(done)*

**Story step:** The `fetch()` call, the Internet as packets.
**Done:** C1, C2 · notes [01 Internet Basics](../notes/00-foundations/01-internet-basics.md), [02 Request Lifecycle](../notes/00-foundations/02-request-lifecycle.md) (rewritten as the anchor)
**Premise only:** the Internet moves data as independent packets (this is why every packet carries addresses). The deep treatment of packet vs. circuit switching waits for Act 5.1, where routers appear.
**Optional reinforcement (🔵):** K1.1–K1.2 (what the Internet is, the edge).

---

## Act 1: Name → Address (steps 1, 2) · ~3 sessions

*Question: What exactly do I send, how do I find where to send it, and what is the number I get back?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **1.1 HTTP, the text protocol** | C29, C31 · K2.2 part 1 (optional) · 🟢 request line, headers, body, status codes, methods · 🟡 `Host` header, keep-alive · 🔵 HTTP evolution (waits for Act 7) | `curl -v`, DevTools Network tab · ⭐ **A1** raw HTTP over a socket |
| **1.2 DNS, the phone book** | C26, C27, C28 · K2.4 · 🟢 resolver → root → TLD → authoritative, caching, record types (A, AAAA, CNAME, MX, TXT, NS) · 🟡 TTL, why DNS uses UDP · 🔵 DNSSEC, DoH | `nslookup`, `nslookup -type=MX`, `ipconfig /displaydns`; Wireshark DNS capture · ⭐ **A2** (stretch) |
| **1.3 The number DNS gave us** ✅ *learned, note to adapt* | C3, C4 · 🟢 what an IP address is, octets and binary, network part vs. host part, CIDR (`/24`), private vs. public | `ipconfig` (your own IP and prefix) · note [IP & CIDR](../notes/02-network-layer/01-ip-and-cidr.md) *(rework to follow DNS: add Keywords block and zoom banner, open with "DNS just handed us 203.0.113.10")* |

**Notes:** `04-application-layer/` HTTP basics (new) · rewrite DNS note into handbook format.

---

## Act 2: Local or Remote? (step 4) · ~3 sessions

*Question: Is that IP in my room or outside it? Who is my way out?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **2.0 The subnet mask** ✅ *learned, note to adapt* | C5 · bitwise AND, how the OS decides local vs. remote | `ipconfig` done · note [Subnet Masks & Switches](../notes/02-network-layer/02-subnet-masks-and-switches.md) *(rework: Keywords block, zoom banner, open from "we have a destination IP; is it ours?")* |
| **2.1 The Gateway** | C6, C7 · 🟢 default gateway, the routing table, `0.0.0.0/0` · 🟡 the gateway is also a router + NAT box at home · 🔵 static routes | `route print`, `ipconfig`, `tracert 8.8.8.8` (hop 1 = gateway) · ⭐ **A3** `is_local()` + CIDR calculator |
| **2.2 Who gave me these numbers? (DHCP)** | AI + K4.3 (DHCP section) · 🟢 DORA: Discover, Offer, Request, Acknowledge; IP, mask, gateway, DNS from one lease | `ipconfig /all` (lease fields); Wireshark DHCP (`ipconfig /release` then `/renew`) |

**Notes:** `02-network-layer/` Default Gateway (new), DHCP (new).

---

## Act 3: The Next Physical Hop (step 5) · ~2 sessions

*Question: A gateway has an IP. How does my Wi-Fi card reach it physically?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **3.1 MAC and ARP** | C8, C9, C10 · K6.1 · 🟢 MAC vs IP (scope), ARP request/reply/cache, why the frame carries the gateway MAC · 🟡 ARP spoofing as a security idea · 🔵 RARP | `getmac`, `arp -a`, `arp -d` then ping gateway; Wireshark ARP · ⭐ **A4** |
| **3.2 Switch, hub, Ethernet** | AI (Kurose 6.4 has no video) · 🟢 Ethernet frame fields, switch MAC table, hub vs switch vs router · 🟡 broadcast domains, VLANs in cloud (VPC subnets) · 🔵 STP, token ring | Packet Tracer: 3 PCs + a switch, watch the MAC table fill |

**Notes:** `01-data-link/` MAC & ARP, Ethernet & Switches.

---

## Act 4: The Reliable Pipe (step 3) · ~6 sessions

*Question: Which program gets this, and what if packets are lost, reordered, or too many?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **4.1 Ports and UDP** | C14, C15, C16 · K3.1, K3.2, K3.3 · 🟢 ports, sockets, mux/demux, UDP header, when UDP wins (DNS, games, streaming) | `netstat -ano` (find your dev server's port); Wireshark UDP · **Protocol landscape exercise:** place DNS, SSH, SMTP, WebRTC/RTP, NTP, Postgres, game traffic: TCP or UDP? which port? why? |
| **4.2 TCP: the connection** | C17, C18, C19 · K3.5-1 · 🟢 3-way handshake, 4-way teardown, why connections have states · 🟡 TIME_WAIT, port exhaustion | `netstat -ano` states; Wireshark SYN/SYN-ACK/ACK |
| **4.3 TCP: bytes and numbers** | C20, C21 · 🟢 sequence/ack numbers, segment anatomy, retransmission | Wireshark TCP follow-stream; read real seq/ack |
| **4.4 Why TCP is built this way** | K3.4-1, K3.4-2 · C22 · 🟢 stop-and-wait → pipelining → sliding window (the "invent TCP" story), MTU/MSS/PMTUD · 🔵 Go-Back-N vs Selective Repeat internals | `ping -f -l 1472 8.8.8.8` to find your MTU |
| **4.5 Flow and congestion control** | C23, C24 · K3.5-2, K3.6, K3.7 · 🟢 receive window, slow start, congestion avoidance, why a new connection is slow · 🔵 CUBIC/BBR details | Wireshark TCP window graph or DevTools throttling |
| **4.6 Sockets: build it** | C25 · K2.7 · 🟢 `bind/listen/accept/connect` | ⭐ **A5** echo server → HTTP/1.1 server serving `/profile` |

**Notes:** `03-transport-layer/` Ports & UDP, TCP Handshake & Teardown, Sequence Numbers, MTU/MSS, Flow & Congestion Control, Sockets.

---

## Act 5: Across the Planet (step 6) · ~4 sessions

*Question: How do routers carry this across oceans, and how does the reply find me?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **5.1 The IP packet and the network core** | C48, C49 · K1.3 · K4.3 · K1.4 · 🟢 packet switching vs. circuit switching (store-and-forward, statistical multiplexing; a TCP connection is **not** a circuit), IPv4 header (TTL, protocol, fragmentation), delay/latency/throughput · 🔵 FDM/TDM details, IPv6 detail | Wireshark: read an IPv4 header; `ping -n`, observe TTL |
| **5.2 Routing and ICMP** | C12, C13 · K4.1, K4.2 (light), K5.1, K5.6 · 🟢 forwarding vs routing, longest-prefix match, how `ping`/`traceroute` work via ICMP/TTL | `tracert` to 3 sites, annotate hops · ⭐ **A6** (stretch) |
| **5.3 How routers learn routes** | K5.2 (link state), K5.2-2 (distance vector), K5.3 OSPF, K5.4 BGP · 🟢 concept of each, why the Internet uses hierarchy (inside an ISP vs between ISPs) · 🟡 BGP leaks/outages as real incidents · 🔵 algorithm math | Packet Tracer: static route then RIP/OSPF between two routers |
| **5.4 NAT** | C47 · K4.3 · 🟢 private↔public, port mapping table, why servers behind NAT are unreachable · 🟡 port forwarding, CGNAT | Compare `ipconfig` IP vs "what is my IP" site |

**Notes:** `02-network-layer/` IP Packet & TTL, Routing Basics, ICMP, NAT.

---

## Act 6: Make It Private (step 7) · ~4 sessions

*Question: How can two strangers agree on a secret on a public wire?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **6.1 Crypto toolbox** | AI + K1.6 · 🟢 symmetric vs asymmetric, hashing, MACs, digital signatures · 🔵 DES/IDEA internals | `certutil -hashfile` and change one byte (avalanche effect) |
| **6.2 TLS overview and certificates** | C41, C43 · 🟢 what TLS guarantees (confidentiality, integrity, identity), certificate chains, CAs | Browser padlock → inspect the chain; `openssl s_client -connect` |
| **6.3 The handshake** | C45 (TLS 1.2), C46 (TLS 1.3), C44 (Diffie-Hellman) · 🟢 key exchange idea, forward secrecy · 🟡 1.3 is 1 round trip · 🔵 RSA math (C42) | Wireshark TLS handshake; `curl -v` annotated |
| **6.4 TLS in your server** | AI · 🟢 `ssl` module, cert files, SNI | ⭐ **A7** TLS around your A5 server |

**Notes:** `05-security/` Crypto Toolbox, TLS & Certificates, TLS Handshake.

---

## Act 7: The Conversation Evolves (step 8) · ~3 sessions

*Question: Why was HTTP rewritten twice?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **7.1 HTTP/1.1 limits** | C30, C32, C33 · K2.2 part 2 (caching, conditional GET) · 🟢 persistent connections, head-of-line blocking, why browsers open 6 connections | DevTools waterfall on a many-asset page |
| **7.2 HTTP/2** | C34, C35, C36, C37, C38 · 🟢 streams, multiplexing, binary frames, HPACK idea · 🟡 TCP-level HOL blocking remains · 🔵 frame byte layouts | DevTools protocol column = `h2`; `curl --http2 -v` |
| **7.3 QUIC and HTTP/3** | C39, C40, K3.8 · 🟢 why UDP again, per-stream loss recovery, 0-RTT · 🔵 QUIC packet internals | `curl --http3` (if supported); DevTools `h3` · ⭐ **A8** |

**Notes:** `04-application-layer/` HTTP/1.1 Limits, HTTP/2, QUIC & HTTP/3.

---

## Act 8: What Sits on the Path in Real Systems · ~5 sessions

*Question: Between your code and a production server, what else is there?*

| Session | Learn | Hands-on / Build |
|---|---|---|
| **8.1 Proxies and reverse proxies** | AI · 🟢 forward vs reverse, `X-Forwarded-For`, TLS termination | Nginx in Docker; inspect added headers |
| **8.2 Load balancers and CDNs** | K2.6, K4.5 · AI · 🟢 L4 vs L7, health checks, edge caching, `cache-control` | `curl -I` on a CDN-backed site (`cf-cache-status`) |
| **8.3 Firewalls, VPNs, SSH** | AI · 🟢 stateful firewall, ACLs, tunnels, how SSH authenticates · 🔵 IDS internals | `ssh -v`; Windows firewall rule |
| **8.4 Real-time and email** | AI · K2.3 · 🟢 WebSockets and SSE vs polling; SMTP/IMAP at a glance | DevTools → WS frames on a live chat site |
| **8.5 LAN and wireless depth** | K6.2, K6.3 · AI · 🟢 error detection idea (CRC), why shared media needs rules (CSMA), Wi-Fi vs Ethernet · 🔵 Bluetooth, 5G, legacy tech (see appendix) | Wireshark 802.11 *(only if hardware allows)* |

**Project ⭐ A9:** Docker Compose with Nginx reverse proxy, 2 backends, TLS.
**Notes:** `05-security/` Firewalls & VPNs; `04-application-layer/` Proxies, Load Balancers & CDN, WebSockets; `01-data-link/` Error Detection & Multiple Access.

---

## Act 9: Close the Circle · ~2 sessions

*Question: Can you now explain every step, from memory, and prove it with a capture?*

* **File the story into the layer models:** C11 (OSI vs TCP/IP), K1.5 (layering, encapsulation). You have lived every layer by now, so the models stop being abstract and become a filing cabinet for what you already know.
* Wireshark capture of one request to your A9 stack. Annotate every layer.
* Re-write the lifecycle story **in your own words**, one paragraph per step, then compare with the anchor note.
* Fill the Revisit Log. Close all ⏳ in the "You Are Here" map.
* Ask the AI for a "break it" challenge: it describes a failure (timeout, 502, slow TLS, cert error) and you diagnose which step failed.

---

## Epilogue: Other Roads (curiosity, after the journey)

*Question: HTTP was one language on the shared road. What do the others look like?*

Every protocol below uses the same IP, routing and link layers you learned. Only the top layer (what the messages mean) and the TCP-or-UDP choice differ. For each one, ask: **what language does it speak, TCP or UDP, which port, and why?** One short note or AI explanation each, picked in any order, whenever curiosity strikes.

| Road | Rides on | Why it isn't HTTP |
|---|---|---|
| Voice and video calls (WebRTC, RTP/SRTP) | UDP | Late audio is useless, so drop it instead of resending |
| Online games | UDP (custom binary) | Dozens of position updates per second; freshness beats completeness |
| SSH | TCP 22 | Interactive remote shell and tunnels *(basics in Act 8.3)* |
| Email (SMTP, IMAP, POP3) | TCP 25/587, 993, 995 | Store-and-forward mail between servers *(basics in Act 8.4)* |
| Database wire protocols (Postgres, MySQL, Redis RESP) | TCP | Compact binary messages on long-lived connections |
| Message streaming (Kafka, AMQP) | TCP | High-throughput event pipes between servers |
| NTP (clock sync) | UDP 123 | Tiny, frequent, and stale replies are worthless |
| BitTorrent (P2P) | TCP/UDP | Many peers share pieces; no central server |
| gRPC | HTTP/2 | Still HTTP underneath, a nice twist after Act 7 |
| DHCP, ICMP, BGP, OSPF | UDP / IP / TCP | The Internet's own plumbing *(covered in Acts 2 and 5)* |

---

## Appendix: Syllabus Coverage Map (for completeness, not driving)

The course syllabus is [syllabus.md](syllabus.md). Where each module lives in this plan:

| Syllabus module | Covered in |
|---|---|
| 1. Introduction (Internet, models, switching) | Act 0, Act 5.1, Act 8 |
| 2. Link layer (error detection, multiple access, ARP, Ethernet, switches, Wi-Fi) | Acts 3, 8.5 |
| 3. Network layer (IP, subnetting, ICMP, DHCP, NAT, routing) | Acts 2, 5 |
| 4. Transport layer | Act 4 |
| 5. Application layer (HTTP, DNS, email, sockets) | Acts 1, 4.6, 7, 8.4 |
| 6. Security (crypto, TLS, firewalls, SSH) | Acts 6, 8.3 |
| Legacy items (ATM, Frame Relay, Token Ring, FDDI, HDLC, PPP, MPLS, Mobile IP, Blockchain, IDEA) | Not in the main path. Brief AI notes on request. |
| By-hand numericals (subnetting, VLSM, CRC, Hamming, ALOHA, Dijkstra, Bellman-Ford) | Practiced inside their acts as understanding tools. A dedicated drill block can be added later if you want one. |
