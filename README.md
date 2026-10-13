# Computer Networks: A Developer's Self-Study Workspace

Learning computer networks from a **software developer's** perspective, by following one story: the life of an HTTP request. An AI tutor writes each lesson; you read, run the labs, and build.

---

## 📖 For You (the learner): read and run these

| Where | What it is | When to open it |
|---|---|---|
| [`playground.md`](playground.md) | **Today's lesson**, live. Open in Markdown Preview (`Ctrl+K V`) | During a session |
| [`notes/`](notes/README.md) | **The handbook**: one chapter per topic, in reading order. Start at [the Request Lifecycle](notes/00-foundations/02-request-lifecycle.md), the map of the whole course | To review or revise |
| [`notes/GLOSSARY.md`](notes/GLOSSARY.md) | Every term → one line → the chapter that introduces it | When a word is unfamiliar |
| [`lessons/`](lessons/) | **Archive of finished lessons**, with the full labs (and earlier versions in collapsed blocks) | To redo a lab or re-read a full lesson |
| [`hands-on-lab/`](hands-on-lab/) | **Scripts you run** for labs and the "Build the Stack" project, named `act<N>-<session>-<name>` | When a lesson says "run..." |
| [`course-memory/roadmap.md`](course-memory/roadmap.md) | The plan: 9 acts, what's covered where | To see the big picture |
| [`course-memory/tracker.md`](course-memory/tracker.md) | Where you are and what's done | At the start of a session |

## 📚 Reading Order (the handbook, start to finish)

Read top to bottom. Each chapter zooms into one step of the journey. ✅ written · 🔧 written, being reworked into the new format · ⏳ not written yet

**Act 0: The Trigger**
1. ✅ [Internet Basics](notes/00-foundations/01-internet-basics.md)
2. ✅ [The Request Lifecycle: Master Map](notes/00-foundations/02-request-lifecycle.md) *(the anchor: come back here whenever you feel lost)*

**Act 1: Name → Address** *(steps 1–2)*

3. ✅ [HTTP Basics](notes/04-application-layer/02-http-basics.md) · full lesson: [lessons/act1-1.1-http.md](lessons/act1-1.1-http.md)
4. 🔧 [DNS Resolution](notes/04-application-layer/01-dns-resolution.md)
5. 🔧 [IP Addressing & CIDR](notes/02-network-layer/01-ip-and-cidr.md)

**Act 2: Local or Remote?** *(step 4)*

6. 🔧 [Subnet Masks & Switches](notes/02-network-layer/02-subnet-masks-and-switches.md)
7. ⏳ Default Gateway
8. ⏳ DHCP

**Act 3: The Next Physical Hop** *(step 5)*

9. ⏳ MAC Addresses & ARP
10. ⏳ Ethernet & Switches

**Act 4: The Reliable Pipe** *(step 3)*

11. ⏳ Ports & UDP
12. ⏳ TCP Handshake & Teardown
13. ⏳ Sequence Numbers & TCP Segments
14. ⏳ MTU, MSS & Why TCP Is Built This Way
15. ⏳ Flow & Congestion Control
16. ⏳ Sockets: Building a Server

**Act 5: Across the Planet** *(step 6)*

17. ⏳ The IP Packet, Packet Switching & Latency
18. ⏳ Routing Basics & ICMP
19. ⏳ How Routers Learn Routes
20. ⏳ NAT

**Act 6: Make It Private** *(step 7)*

21. ⏳ Crypto Toolbox
22. ⏳ TLS & Certificates
23. ⏳ The TLS Handshake

**Act 7: The Conversation Evolves** *(step 8)*

24. ⏳ HTTP/1.1 Limits
25. ⏳ HTTP/2
26. ⏳ QUIC & HTTP/3

**Act 8: What Sits on the Path**

27. ⏳ Proxies & Reverse Proxies
28. ⏳ Load Balancers & CDNs
29. ⏳ Firewalls, VPNs & SSH
30. ⏳ WebSockets & Real-Time; Email
31. ⏳ Error Detection, Multiple Access & Wi-Fi

**Act 9: Close the Circle**

32. ⏳ Capstone: End-to-End Trace & the Layer Models

**Epilogue (optional):** ⏳ Other Roads: protocols beyond HTTP

---

## 🤖 For the AI tutor: instructions and memory (you rarely need these)

| Where | What it is |
|---|---|
| [`.agents/AGENTS.md`](.agents/AGENTS.md) | Tutor rules: story spine, **Lesson Writing Standard**, self-review checklist, note rules |
| [`.agents/skills/start-session/`](.agents/skills/start-session/SKILL.md) | What the tutor does when you say "start session" |
| [`.agents/examples/`](.agents/examples/) | The reference lesson every new lesson must match |
| [`course-memory/`](course-memory/) | Video index, resources, syllabus, and `learning_blueprint.md` (how this learning method evolved) |
| [`scripts/`](scripts/) | `get_transcript.py`: fetches full video transcripts for the tutor |

---

## How a Session Works

1. Say **"start session"** to the tutor. It reads the tracker and writes today's lesson into `playground.md`.
2. Read the lesson, run the labs, and run the `hands-on-lab/` script for the session.
3. Ask questions. If a lesson is unclear, ask for a rewrite: the old version is kept in a collapsed block.
4. Say **"create note"** for the handbook chapter, then **"done for today"**. The tutor archives the lesson to `lessons/` and updates the tracker.
