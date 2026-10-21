# Computer Networks Progress Tracker

Last updated: 2026-10-21 (Act 1 completed; Wireshark wrap-up lab + quiz pending) · Plan: [roadmap.md](roadmap.md) (story-based, 9 acts, no end date)

## Current Position

- **Act 1: Completed** (student approved 2026-10-21), with one open item: the **Wireshark DNS practice lab + Act 1 quiz** (below).
- **Next session:** Act 1 wrap-up lab, then **Act 2 · Session 2.0: The subnet mask**.
- **Wrap-up lab plan:** Wireshark on `*Wi-Fi`, filter `dns`, one experiment at a time. Experiment 3: `curl.exe -s -o NUL http://bn.wikipedia.org` twice (1st run shows DNS rows, 2nd shows none: the OS cache). Experiment 4: `python hands-on-lab/act1-1.2-dns-query.py github.com A --walk` (3 questions to 3 servers). Then the 1.2 recall, then an Act 1 quiz mixing HTTP, DNS and IP/CIDR (`notes/RECALL.md`).
- **How to run Wireshark with this student (important):** they had never used it. Give **one experiment at a time**: *"1. In PowerShell run X. 2. In Wireshark look at Y. 3. Reply with Z."* Say what each window does first (PowerShell asks, Wireshark only records). The student gets bored and leaves the lesson when given a block of instructions. Laptop IP `192.168.0.102/24`, resolver/router `192.168.0.1`.
- **Tutor's shell can't read the DNS cache** (`ipconfig /displaydns`, `/flushdns` need elevation there). Don't pre-test a name the student will use for a cache experiment: it pollutes their cache.
- **Open question to settle later:** Cloudflare `1.1.1.1` returned TTL 77 and 161 for a record whose owners say 60. Lesson and note say "TTL is a request, not a guarantee"; the exact rule is unconfirmed.
- **Waiting in its slot:** subnet mask (video 5, watched) → Session 2.0. Default Gateway videos 6 & 7 → Session 2.1.

> Status values: `Not Started` · `In Progress` · `Completed`. Mark an **act** Completed only with the student's explicit approval.
> Session checkboxes: `[x]` done, `[ ]` pending. Each session = Learn · Hands-on · Build/Note · Recall check.

---

## Act 0: The Trigger — Completed ✅

### Session 0.1: Series intro & the request journey
- [x] C1, C2 · [x] Notes (`01-internet-basics`, `02-request-lifecycle`, both rebuilt in the new format) · [x] `ping` latency lab · [x] Anchor read

> The old "Day 2" (IP, CIDR, subnet masks) has been **moved into its story slots**: 1.3 and 2.0 below. It is no longer part of Act 0.

---

## Act 1: Name → Address (steps 1, 2) — Completed ✅ *(Wireshark wrap-up lab + quiz pending)*

### Session 1.1: HTTP, the text protocol
- [x] Lesson read (`lessons/act1-1.1-http.md`) · [ ] Videos C29, C31 *(optional now; watch any time)*
- [x] Hands-on: `curl -v`, cookie experiment, DevTools
- [x] ⭐ A1: raw HTTP request over a socket (`hands-on-lab/act1-1.1-raw-http.py`)
- [x] Note: `02-http-basics.md` · [x] Revisit Log · [ ] Recall check *(warm-up of 1.2)*

### Session 1.2: DNS, the phone book
- [x] Pre-flight briefing · [x] Lesson archived (`lessons/act1-1.2-dns.md`) · [ ] Videos C26, C27 (first ~28 min), C28, K2.4 *(optional, any time)*
- [ ] Hands-on: [x] `nslookup`, record types, `displaydns`, `curl -v` · [ ] Wireshark DNS (experiments 1 and 2 done; 3 and 4 → Act 1 wrap-up lab)
- [ ] ⭐ A2 *(stretch)*: hand-built DNS query (`hands-on-lab/act1-1.2-dns-query.py`, tested; student has not yet run it with `--walk`)
- [x] Note: rewrite `04-application-layer/01-dns-resolution.md` into handbook format (2026-10-18) · [x] Revisit Log · [ ] Recall check

### Session 1.3: The number DNS gave us (IP address & CIDR) — Completed 2026-10-21
- [x] Watched C3, C4 *(earlier)* · [x] `ipconfig`: IP and prefix *(earlier)*
- [x] Lesson (`lessons/act1-1.3-ip-address.md`) · [x] Labs: `ipconfig`, `Get-NetIPAddress`, `ping <number>` · [x] Build: `act1-1.3-ip-explorer.py`
- [x] Note rewritten: `02-network-layer/01-ip-and-cidr.md` (incl. the student's WSL question) · [x] RECALL section · [x] Glossary
- [x] Revisit Log · [ ] Recall check *(in the Act 1 quiz)*

### Act 1 wrap-up (pending)
- [ ] Wireshark DNS practice: Experiments 3 (cache) and 4 (`--walk`)
- [ ] Act 1 quiz (HTTP, DNS, IP/CIDR)

---

## Act 2: Local or Remote? (step 4) — Not Started

### Session 2.0: The subnet mask — *video already watched*
- [x] Watched C5 *(earlier)*
- [ ] Re-read with the story: we have a destination IP, is it ours?
- [ ] Adapt note `02-network-layer/02-subnet-masks-and-switches.md` (Keywords block, zoom banner, open from the decision step)
- [ ] Revisit Log · [ ] Recall check

### Session 2.1: The Default Gateway
- [ ] C6, C7 · [ ] `route print`, `tracert 8.8.8.8` · [ ] ⭐ A3 `is_local()` + CIDR calculator
- [ ] Note: Default Gateway · [ ] Revisit Log · [ ] Recall check

### Session 2.2: DHCP, who gave me these numbers?
- [ ] AI + K4.3 · [ ] `ipconfig /all`, Wireshark DHCP
- [ ] Note: DHCP · [ ] Revisit Log · [ ] Recall check

---

## Act 3: The Next Physical Hop (step 5) — Not Started

### Session 3.1: MAC and ARP
- [ ] C8, C9, C10, K6.1 · [ ] `getmac`, `arp -a`, Wireshark ARP · [ ] ⭐ A4
- [ ] Note: MAC & ARP · [ ] Revisit Log · [ ] Recall check

### Session 3.2: Switch, hub, Ethernet
- [ ] AI explanation · [ ] Packet Tracer: switch MAC table
- [ ] Note: Ethernet & Switches · [ ] Revisit Log · [ ] Recall check

---

## Act 4: The Reliable Pipe (step 3) — Not Started

- [ ] **4.1** Ports & UDP (C14–16, K3.1–3.3) · protocol landscape exercise
- [ ] **4.2** TCP connection: handshake, teardown, states (C17–19, K3.5-1)
- [ ] **4.3** TCP bytes & numbers (C20, C21)
- [ ] **4.4** Why TCP is built this way; MTU/MSS (K3.4, C22)
- [ ] **4.5** Flow & congestion control (C23, C24, K3.5-2, K3.6, K3.7)
- [ ] **4.6** Sockets: build it (C25, K2.7) · ⭐ A5 echo server → HTTP server

---

## Act 5: Across the Planet (step 6) — Not Started

- [ ] **5.1** The IP packet, packet vs. circuit switching & latency (C48, C49, K1.3, K4.3, K1.4)
- [ ] **5.2** Routing & ICMP (C12, C13, K4.1, K4.2, K5.1, K5.6) · ⭐ A6 *(stretch)*
- [ ] **5.3** How routers learn routes: link state, DV, OSPF, BGP (K5.2–K5.4)
- [ ] **5.4** NAT (C47, K4.3)

---

## Act 6: Make It Private (step 7) — Not Started

- [ ] **6.1** Crypto toolbox (AI, K1.6)
- [ ] **6.2** TLS overview & certificates (C41, C43)
- [ ] **6.3** The handshake: TLS 1.2 vs 1.3, Diffie-Hellman (C45, C46, C44)
- [ ] **6.4** TLS in your server · ⭐ A7

---

## Act 7: The Conversation Evolves (step 8) — Not Started

- [ ] **7.1** HTTP/1.1 limits (C30, C32, C33)
- [ ] **7.2** HTTP/2 (C34–C38)
- [ ] **7.3** QUIC & HTTP/3 (C39, C40, K3.8) · ⭐ A8

---

## Act 8: What Sits on the Path — Not Started

- [ ] **8.1** Proxies & reverse proxies
- [ ] **8.2** Load balancers & CDNs (K2.6, K4.5)
- [ ] **8.3** Firewalls, VPNs, SSH
- [ ] **8.4** Real-time (WebSockets) & email (K2.3)
- [ ] **8.5** LAN & wireless depth: CRC, CSMA, Wi-Fi (K6.2, K6.3)
- [ ] ⭐ A9: Docker Compose, Nginx reverse proxy, 2 backends, TLS

---

## Act 9: Close the Circle — Not Started

- [ ] Wireshark end-to-end trace of the A9 stack, annotated
- [ ] Lifecycle story rewritten in own words, then compared with the anchor
- [ ] Revisit Log filled; "You Are Here" map fully ✅
- [ ] "Break it" diagnosis challenge
- [ ] File the story into the layer models (C11 OSI vs TCP/IP, K1.5)

---

## Epilogue: Other Roads — Optional, for curiosity

Pick any, in any order, after the journey (see roadmap): WebRTC/RTP, game UDP, SSH, email, database wire protocols, Kafka/AMQP, NTP, BitTorrent, gRPC. Ask of each: what language, TCP or UDP, which port, why?

---

## Progress Summary

| Act | Status | Sessions |
|---|---|---|
| 0 The Trigger | Completed | 1 / 1 |
| 1 Name → Address | Completed | 3 / 3 *(Wireshark wrap-up lab + quiz pending)* |
| 2 Local or Remote? | Not Started | 0 / 3 *(2.0 video already watched, note to adapt)* |
| 3 Next Physical Hop | Not Started | 0 / 2 |
| 4 The Reliable Pipe | Not Started | 0 / 6 |
| 5 Across the Planet | Not Started | 0 / 4 |
| 6 Make It Private | Not Started | 0 / 4 |
| 7 Conversation Evolves | Not Started | 0 / 3 |
| 8 What Sits on the Path | Not Started | 0 / 5 |
| 9 Close the Circle | Not Started | 0 / 2 |
| **Total** | | **4 / 33** |
