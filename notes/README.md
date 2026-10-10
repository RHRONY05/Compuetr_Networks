# Computer Networks: A Developer's Handbook

Welcome to the **Computer Networks Tutorial Handbook**. This repository is structured as a comprehensive, sequential learning series designed for **software developers, DevOps engineers, and students preparing for the CUET Computer Networks exam**.

Instead of isolated lecture summaries, each document here is written as a **self-contained tutorial chapter** that connects to the previous and next topics, building an unbroken mental model from raw silicon bits up to cloud architectures.

---

## 📖 How to Read This Handbook

If you are new to Computer Networks, **read the chapters sequentially from Part 0 through Part 6**. Each chapter builds upon the terminology and mechanics introduced in the preceding one.

---

## 🗺️ Table of Contents

### Part 0: Foundations & The Request Journey
* 📄 **Chapter 01:** [Internet Basics & Network Models](00-foundations/01-internet-basics.md) — What the Internet actually is, Client-Server vs. P2P, and Packet Switching.
* 📄 **Chapter 02:** [Request Lifecycle & Encapsulation](00-foundations/02-request-lifecycle.md) — What really happens when you make a `fetch()` call: The Russian nesting dolls of Frames, Packets, Segments, and Signals.

### Part 1: The Network Layer (Global Addressing & Subnets)
* 📄 **Chapter 03:** [IP Addressing, CIDR & Global Architecture](02-network-layer/01-ip-and-cidr.md) — Dotted quad notation, 32-bit math, CIDR prefix slicing, Private vs. Public IPs, and the Global Postal Analogy.
* 📄 **Chapter 04:** [Subnet Masks and Switches](02-network-layer/02-subnet-masks-and-switches.md) — How devices decide local vs. remote via Bitwise AND, why subnet masks must be uniform, and demystifying the living room "Wi-Fi Box" (AP vs. Switch vs. Router).
* 📄 **Chapter 05:** `Default Gateways & Outer Network Access` *(Coming up in Day 3)* — The bridge between your living room and the ISP.
* 📄 **Chapter 06:** `Routing Decisions & ICMP (Ping)` *(Coming up in Day 5)* — How routers navigate packets across global internet hops.

### Part 2: The Data Link Layer (Local Hop-to-Hop)
* 📄 **Chapter 07:** `MAC Addresses, NICs & ARP` *(Coming up in Day 4)* — Physical hardware addressing and resolving IPs to local network cards.

### Part 3: The Transport Layer (Process-to-Process Reliability)
* 📄 **Chapter 08:** `Ports, Sockets & UDP` *(Week 2)* — Reaching specific application processes (Node.js vs. Python) and lightweight datagrams.
* 📄 **Chapter 09:** `TCP Handshake & Sequence Numbers` *(Week 2)* — Creating reliable pipes and reassembling out-of-order data chunks.
* 📄 **Chapter 10:** `TCP States & Connection Teardown` *(Week 2)* — ESTABLISHED, TIME_WAIT, CLOSE_WAIT, and the 4-way FIN handshake.
* 📄 **Chapter 11:** `Flow Control, MTU/MSS & Congestion` *(Week 2)* — Sliding window mechanics and avoiding network collapse.

### Part 4: The Application Layer (Web & Cloud Protocols)
* 📄 **Chapter 12:** [DNS Resolution Architecture](04-application-layer/01-dns-resolution.md) — How human-friendly domain names turn into IP addresses via distributed recursive resolvers and authoritative servers.
* 📄 **Chapter 13:** `HTTP Evolution (HTTP/1.1 to HTTP/3 QUIC)` *(Week 3)* — Pipelining, binary framing, multiplexing, and UDP-based QUIC.
* 📄 **Chapter 14:** `WebSockets & Real-Time Communication` *(Week 3)* — Persistent bi-directional sockets vs. HTTP polling.

### Part 5: Security & Cryptography
* 📄 **Chapter 15:** `TLS Handshake, Certificates & HTTPS` *(Week 3)* — Symmetric vs. Asymmetric encryption, RSA/Diffie-Hellman math, and certificate chains.

### Part 6: Cloud Networking & Exam Cram
* 📄 **Chapter 16:** `NAT (Network Address Translation)` *(Week 4)* — Port Address Translation (PAT) and how multiple devices share a single public IP.
* 📄 **Chapter 17:** `Reverse Proxies, Load Balancers & CDNs` *(Week 4)* — Nginx routing headers, L4 vs. L7 load balancing, and Cloudflare edge caching.
* 📄 **Chapter 18:** `CUET Exam Numerical Speed Drills` *(Week 5)* — Step-by-step formulas for CRC polynomial division, Hamming codes, Subnetting math, and ALOHA throughput.

---

## 🛠️ Contribution & Style Guidelines
Every chapter in this series follows the strict standard in [`NOTE_TEMPLATE.md`](NOTE_TEMPLATE.md):
1. **Zero prior assumptions** — start with an intuitive real-world scenario.
2. **ASCII diagrams** — visually map every packet and data flow.
3. **Developer-grounded** — explain how concepts directly impact API latency, cloud deployment, and debugging logs.
4. **No raw LaTeX markup** — formatted for universal markdown rendering.
