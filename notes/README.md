# Computer Networks: A Developer's Handbook

A story-based handbook for **software developers**. Every chapter is a zoom-in on one step of the life of an HTTP request. Read in the order below (the order of the study plan), not by folder.

**Look up a word:** [Glossary](GLOSSARY.md). Each term is introduced at the top of the lesson that needs it.

**Test yourself:** [Recall](RECALL.md): think-through questions for every chapter.

**Start here:** [The Request Lifecycle: Master Map](00-foundations/02-request-lifecycle.md). It holds the "You Are Here" map and the Revisit Log. Study plan: [roadmap](../course-memory/roadmap.md). Progress: [tracker](../course-memory/tracker.md).

Legend: ✅ written · 🔧 exists but needs rewrite · ⏳ not written yet

---

## Act 0: The Trigger
* ✅ [Internet Basics & Network Models](00-foundations/01-internet-basics.md)
* ✅ [Request Lifecycle: Master Map](00-foundations/02-request-lifecycle.md) *(anchor)*

## Act 1: Name → Address *(steps 1, 2)*
* ✅ [HTTP Basics](04-application-layer/02-http-basics.md)
* ✅ [DNS Resolution](04-application-layer/01-dns-resolution.md)
* 🔧 [IP Addressing & CIDR](02-network-layer/01-ip-and-cidr.md) *(learned; adapt to follow DNS: "what is the number we got?")*

## Act 2: Local or Remote? *(step 4)*
* 🔧 [Subnet Masks & Switches](02-network-layer/02-subnet-masks-and-switches.md) *(learned; adapt to open from the decision step)*
* ⏳ Default Gateway
* ⏳ DHCP

## Act 3: The Next Physical Hop *(step 5)*
* ⏳ MAC Addresses & ARP
* ⏳ Ethernet & Switches

## Act 4: The Reliable Pipe *(step 3)*
* ⏳ Ports & UDP
* ⏳ TCP Handshake & Teardown
* ⏳ Sequence Numbers & TCP Segments
* ⏳ MTU, MSS & Why TCP Is Built This Way
* ⏳ Flow & Congestion Control
* ⏳ Sockets: Building a Server

## Act 5: Across the Planet *(step 6)*
* ⏳ The IP Packet, TTL & Latency
* ⏳ Routing Basics & ICMP
* ⏳ How Routers Learn Routes (Link State, Distance Vector, OSPF, BGP)
* ⏳ NAT

## Act 6: Make It Private *(step 7)*
* ⏳ Crypto Toolbox
* ⏳ TLS & Certificates
* ⏳ The TLS Handshake (1.2 vs 1.3)

## Act 7: The Conversation Evolves *(step 8)*
* ⏳ HTTP/1.1 Limits
* ⏳ HTTP/2
* ⏳ QUIC & HTTP/3

## Act 8: What Sits on the Path
* ⏳ Proxies & Reverse Proxies
* ⏳ Load Balancers & CDNs
* ⏳ Firewalls, VPNs & SSH
* ⏳ WebSockets & Real-Time; Email
* ⏳ Error Detection, Multiple Access & Wi-Fi

## Act 9: Close the Circle
* ⏳ Capstone: End-to-End Trace

## Epilogue: Other Roads *(optional, for curiosity)*
* ⏳ Beyond HTTP: other protocols on the same road (WebRTC, SSH, email, database protocols, NTP, BitTorrent, gRPC)

---

## Style Guidelines
Every chapter follows [NOTE_TEMPLATE.md](NOTE_TEMPLATE.md), a full tutorial written after the session from the lesson and its questions:
1. A **zoom-in banner** pointing to its lifecycle step.
2. Start from a real-world problem; **no prior assumptions**.
3. ASCII diagrams for packets and flows.
4. **Developer-grounded**: hands-on commands and how it fails in production.
5. **No LaTeX**; plain Unicode and code blocks so any Markdown viewer renders it.
6. Close with a Revisit Log line added to the anchor note; recall questions go in [RECALL.md](RECALL.md).
