# The Request Lifecycle: Master Map of the Course

> **Role of this note:** This is the **anchor**. Every other chapter in the handbook is a zoom-in on one step of the journey below. When you feel lost anywhere in the course, come back here, find your step, and read the "You Are Here" map.
> **Prerequisites:** [Chapter 01: Internet Basics](01-internet-basics.md)
> **Key Goal:** Be able to tell, from memory and in your own words, everything that happens between `fetch()` and the JSON arriving, and know which later chapter explains each step in depth.

> **A note on jargon:** terms like DNS, TCP, ARP, NAT and TLS appear here as **signposts**, each with a one-line gloss. Don't memorize them. Every one gets its own proper introduction at the start of its chapter, and the [Glossary](../GLOSSARY.md) lists where.

---

## 1. The Story in One Breath

We follow one running example through the whole course:

```javascript
const res = await fetch("https://api.example.com/profile");   // your laptop: 192.168.0.104
const data = await res.json();
```

Here is the entire journey as a single story. Read it once, straight through. The rest of the note slows it down.

> Your code says: *get `/profile` from `api.example.com`.* First, the browser **writes that wish down as an HTTP message**: plain text, turned into bytes, because bytes are the only thing a network can carry. But the message has no address on it, and networks speak in numbers, not names. So the computer asks **DNS** to look up `api.example.com`, and gets back `203.0.113.10`.
>
> Now it knows both ends: its own address (`192.168.0.104`) and the server's. Before it can send the message, the two machines must agree to talk. Your OS **opens a connection** (TCP) to port 443 on that server: a quick *"are you there?" – "yes" – "good"*.
>
> To send even that first *"are you there?"*, the OS must decide **how the packet leaves the house**. Is `203.0.113.10` on my own network, or outside it? It's outside, so the packet goes to the **default gateway**, your router. But a Wi-Fi card can't deliver to an IP address, only to a physical hardware address. So the OS asks the room *"who is 192.168.0.1?"*, the router answers with its hardware (MAC) address, and the frame finally leaves.
>
> From there, routers pass the packet hop by hop across the world, each looking only at the destination IP, until it reaches the server. The server answers the same way. With the connection open, both sides set up **encryption** (TLS) so nobody in between can read what comes next.
>
> **Only now does the HTTP message you wrote in the very first step actually travel out**, wrapped in all those layers. The server's reply comes back, gets unwrapped layer by layer, and your `await` resolves.

One detail differs from the way most people picture it: **the HTTP message is created first but sent last.** It waits while DNS, the connection and encryption are set up. That is the thread to hold on to.

---

## 2. The Journey Map

```text
  YOUR CODE
  ┌────────────────────────────────────────────────────────────────────┐
  │ 1. WRITE THE MESSAGE    HTTP text → bytes   (created now, sent last)│
  │ 2. FIND THE ADDRESS     api.example.com → 203.0.113.10   (DNS)      │
  └────────────────────────────────────────────────────────────────────┘
  YOUR OPERATING SYSTEM  (steps 3–5 happen for EVERY packet, from the very first)
  ┌────────────────────────────────────────────────────────────────────┐
  │ 3. OPEN A CONNECTION    ports + handshake: "are you there?" (TCP)   │
  │ 4. LOCAL OR REMOTE?     my IP + mask vs target IP → who is next?    │
  │ 5. NEXT PHYSICAL HOP    MAC address of that "next" (ARP) → frame    │
  └────────────────────────────────────────────────────────────────────┘
  THE WORLD
  ┌────────────────────────────────────────────────────────────────────┐
  │ 6. CROSS THE PLANET     routers forward hop by hop (+ NAT, ICMP)    │
  └────────────────────────────────────────────────────────────────────┘
  THE CONVERSATION  (rides on the connection from step 3)
  ┌────────────────────────────────────────────────────────────────────┐
  │ 7. MAKE IT PRIVATE      TLS handshake, then encrypted bytes         │
  │ 8. SEND, REPLY, UNWRAP  HTTP message goes out; reply comes back     │
  └────────────────────────────────────────────────────────────────────┘
```

> **Why the course study order differs a little from this timeline.** The steps run top to bottom in time. But in the course (the *Acts*), we study "where does this go?" (Acts 2–3: addressing, subnets, gateway, ARP) before "how do we make delivery reliable?" (Act 4: TCP). Reason: you need to know what a packet is and where it travels before studying how to make that travel reliable. The "You Are Here" map below tells you which act covers which step.

### The "You Are Here" Map

| Step | The question it answers | Zoom-in chapter | Act | Status |
|---|---|---|---|---|
| 0 | What is the Internet? | [01 Internet Basics](01-internet-basics.md) | 0 | ✅ |
| 1 | What exactly are we sending? | [HTTP Basics](../04-application-layer/02-http-basics.md) | 1 | ✅ |
| 2 | Where is `api.example.com`, and what is the number we get back? | [DNS Resolution](../04-application-layer/01-dns-resolution.md), then [IP & CIDR](../02-network-layer/01-ip-and-cidr.md) | 1 | ✅ |
| 3 | How do two programs agree to talk, reliably? | Ports, UDP, TCP | 4 | ⏳ |
| 4 | Is that address in my room or outside it? | [Subnet Masks](../02-network-layer/02-subnet-masks.md), [Default Gateway](../02-network-layer/03-default-gateway.md), [DHCP](../02-network-layer/04-dhcp.md) | 2 | ✅ |
| 5 | Which physical card gets the frame next? | MAC & ARP | 3 | ⏳ |
| 6 | How do routers carry it across the planet? | IP packet, routing, ICMP, NAT | 5 | ⏳ |
| 7 | Why can't anyone read or alter it? | TLS | 6 | ⏳ |
| 8 | Why does HTTP work this way, and why did it change? | HTTP/1.1 → 2 → 3, QUIC; capstone trace | 7, 9 | ⏳ |
| ★ | What else sits on the path in real systems? | DHCP, proxies, load balancers, CDN, VPN, firewalls | 8 | ⏳ |

The full study order and sources are in [roadmap.md](../../course-memory/roadmap.md).

---

## 3. Why So Many Envelopes?

Why not stamp one destination on the data and send it? Because three different parties need three different answers, and each answer only makes sense in its own scope:

| Who needs to know | The question | The answer is a... |
|---|---|---|
| The **server's OS** | Which program gets this data: Node, Nginx, Postgres? | **Port** |
| **Routers across the planet** | Which machine in the world is this for? | **IP address** |
| **The wire or air right next to you** | Which network card should pick this up right now? | **MAC address** |

No single header can serve all three. The fix is **encapsulation**: each layer wraps the one above it in its own envelope.

---

## 4. The Mental Model: Nesting Dolls

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ ETHERNET FRAME      one hop only      Src MAC: my NIC     Dst MAC: my router │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ IP PACKET         whole journey     Src IP: 192.168.0.104                │ │
│ │                                     Dst IP: 203.0.113.10                 │ │
│ │ ┌──────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ TCP SEGMENT     program-to-program   Src Port: 54321 (ephemeral)     │ │ │
│ │ │                                      Dst Port: 443    Seq #: ...     │ │ │
│ │ │ ┌──────────────────────────────────────────────────────────────────┐ │ │ │
│ │ │ │ TLS-encrypted HTTP:  GET /profile ...                            │ │ │ │
│ │ │ └──────────────────────────────────────────────────────────────────┘ │ │ │
│ │ └──────────────────────────────────────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

Wrapping on the way out is **encapsulation**; unwrapping on the way in is **decapsulation**. Notice the Destination IP is the faraway server, but the Destination MAC is the *router next to you*. Step 4 explains why.

---

## 5. The Eight Steps, Slowly

Each step follows the same rhythm: **the situation** (what we are stuck on), **what happens**, **what we now have**, and what that **leads to**.

### Step 1: Write the Message
**Situation.** `fetch()` has been called. Nothing has touched the network.
**What happens.** The browser builds an **HTTP message**: a method, a path, headers, maybe a body. A message is just structured text, and text is converted to **bytes** (numbers), because bytes are all a network carries.
```http
GET /profile HTTP/1.1
Host: api.example.com
Authorization: Bearer xyz123
```
**We now have:** a message, as bytes, ready to send, with no address on it yet.
**Leads to:** *To whom do we send it?* Only a name, `api.example.com`, is known.
**Zoom →** HTTP basics (Act 1)

### Step 2: Find the Address (DNS)
**Situation.** Routers only understand numeric IP addresses, not names.
**What happens.** The OS asks a **DNS resolver**: *"what is the IP of `api.example.com`?"* The answer, `203.0.113.10`, is remembered for a while (cached).
**We now have:** both ends of the conversation: **source** `192.168.0.104` (our own address, given to us by the router when we joined Wi-Fi) and **destination** `203.0.113.10`.
**Leads to:** *We know who, but the two machines haven't agreed to talk yet.*
**Zoom →** [DNS Resolution](../04-application-layer/01-dns-resolution.md) (Act 1)

### Step 3: Open a Connection (Ports, TCP)
**Situation.** An address says *which machine*. The server runs many programs: Node, Nginx, a database. And the network can lose or reorder packets.
**What happens.** The OS opens a **TCP connection** to **port 443** (the standard HTTPS port) on `203.0.113.10`. It does this with a three-step exchange (`SYN`: "are you there?", `SYN-ACK`: "yes, are you?", `ACK`: "yes"). It also picks a temporary **ephemeral source port** (say 54321) so replies can find this exact connection. From here on, TCP numbers every chunk of data so lost or out-of-order pieces can be fixed.
**We now have:** a plan to send a first packet ("SYN") from `192.168.0.104:54321` to `203.0.113.10:443`.
**Leads to:** *To send that packet, the OS must decide how it physically leaves the house.*
**Zoom →** Ports, UDP, TCP (Act 4)

### Step 4: Local or Remote? (The Decision)
**Situation.** The OS has a packet for `203.0.113.10`. Is that machine on my own network, or somewhere else?
**What happens.** It compares the **network part** of both addresses, using the **subnet mask** (a bitwise AND):

```text
My IP:        192.168.0.104   AND 255.255.255.0 = 192.168.0.0
Target IP:    203.0.113.10    AND 255.255.255.0 = 203.0.113.0   ← different network

Same network  → ON-LINK:  deliver directly to the target machine
Different     → OFF-LINK: hand it to the DEFAULT GATEWAY (192.168.0.1)
```

The target is remote, so the *next hop* is the **default gateway** (your router), not the server. The OS stores this rule in its **routing table**; the last line, `0.0.0.0/0 → gateway`, means "anything I don't recognize goes to the gateway."
**We now have:** the next hop is `192.168.0.1`, the router.
**Leads to:** *A network card can't deliver to an IP address. It needs a hardware address.*
**Zoom →** [IP & CIDR](../02-network-layer/01-ip-and-cidr.md), [Subnet Masks](../02-network-layer/02-subnet-masks-and-switches.md), Default Gateway (Act 2)

### Step 5: The Next Physical Hop (MAC and ARP)
**Situation.** The Wi-Fi card transmits frames to **MAC addresses** (hardware IDs burned into network cards), not IPs.
**What happens.** The OS broadcasts an **ARP** question to the local network: *"Who has 192.168.0.1? Tell me your MAC."* The router replies. The OS builds the frame: `Dst MAC = router`, while `Dst IP` stays the faraway server. The answer is cached for next time.
**We now have:** a complete, sendable frame. The first packet leaves your laptop.
**Leads to:** *The router now has to get it the rest of the way.*
**Why not the server's MAC?** A MAC address only means something on one local link, so your laptop could neither learn nor use the server's.
**Zoom →** MAC & ARP (Act 3)

### Step 6: Cross the Planet
**Situation.** The packet is in the router, and the server is on the other side of the world.
**What happens.** The router strips the Ethernet frame, reads only the **Destination IP**, consults its own routing table, and builds a **new** frame for *its* next hop. This repeats at every router. The IP packet stays (almost) unchanged; frames are destroyed and rebuilt at every hop. Your home router also does **NAT**: it swaps your private source address for its public one and remembers the swap, so replies find their way back. **ICMP** carries error messages and powers `ping` and `traceroute`.
**We now have:** the SYN arrives at the server. The server answers (SYN-ACK) over the same machinery in reverse, we send the final ACK, and **the connection is open**.
**Leads to:** *The connection works, but anyone along the path could read what we send.*
**Zoom →** IP packet, routing, ICMP, NAT (Act 5)

### Step 7: Make It Private (TLS)
**Situation.** The connection exists, but every router along the path can see the bytes.
**What happens.** For `https://`, client and server run a **TLS handshake** over the open connection: the server proves who it is with a certificate, both sides agree on a shared secret, and everything afterwards is encrypted. Routers see only IPs and ports, not your `Authorization` header.
**We now have:** a private, authenticated channel.
**Leads to:** *At last, the message from step 1 can go out.*
**Zoom →** TLS (Act 6)

### Step 8: Send, Reply, Unwrap
**Situation.** The channel is ready.
**What happens.** The HTTP message from step 1 is encrypted, wrapped in TCP, IP and Ethernet, and sent (steps 3–6 happen again for every packet). The server's reply returns and is peeled apart in reverse:

```text
NIC receives frame → strip Ethernet (is this my MAC?)
 → strip IP (is this my IP? protocol = TCP)
 → TCP (which connection? Dst Port 54321 → this socket; check numbers, reorder, ACK)
 → TLS decrypts
 → HTTP bytes handed to the browser → the pending fetch() promise resolves
```

The **port number** is how the OS knows which of your many open programs and tabs a reply belongs to.
**We now have:** your `await` returns. The circle is closed.
**Zoom →** HTTP/1.1 → HTTP/2 → HTTP/3, QUIC (Act 7); the capstone trace (Act 9)

---

## 6. Developer Diagnostics: Error → Step

| What you see | Which step failed |
|---|---|
| `ERR_NAME_NOT_RESOLVED`, `ENOTFOUND` | Step 2: DNS found no address |
| `ECONNREFUSED` | Step 3: the packet arrived, but nothing listens on that port |
| `ETIMEDOUT`, request hangs | Steps 4–6: packet dropped (wrong gateway, firewall, routing failure) |
| `ERR_CERT_*`, `UNABLE_TO_VERIFY_LEAF_SIGNATURE` | Step 7: TLS identity or trust check failed |
| `502 Bad Gateway`, `504` | Step 8 territory: a proxy reached you, but not the app behind it |
| `CORS error` | The round trip fully **succeeded**. The browser blocked the response in step 8 |

---

## 7. Hands-On: A Lab That Unlocks as You Learn

Nothing to run yet. Each tool below is taught, with its output explained, in the act where its step is introduced. Treat this table as the course's lab roadmap, and come back to it as you go.

| Tool | What it lets you watch | Step | Unlocked in |
|---|---|---|---|
| `ping` | Latency | 0 | Act 0 *(you already used it)* |
| `curl -v` | The request text and response headers; later DNS, TCP and TLS lines | 1 | Act 1 *(and it grows through Act 6)* |
| `nslookup` | A DNS answer | 2 | Act 1 |
| `ipconfig`, `route print` | Your IP, mask, gateway; the routing table | 4 | Act 2 |
| `arp -a` | Cached IP → MAC pairs | 5 | Act 3 |
| `netstat -ano` | Open ports and connections | 3 | Act 4 |
| `tracert` | The routers along the path | 6 | Act 5 |
| Browser padlock, `openssl s_client` | The TLS certificate | 7 | Act 6 |
| DevTools Network tab | HTTP/1.1 vs HTTP/2 vs HTTP/3 | 8 | Act 7 |
| Wireshark | Every layer, in a real capture | all | from Act 1, and the Act 9 capstone |

When the capstone arrives (Act 9), you will run all of these against one request and match each line of output to a step in this note.

---

## 8. Common Traps

* **Source Port Myth:** your outgoing source port is *not* 3000 or 80. It is a random ephemeral port (49152–65535) assigned by the OS. Port 3000 is where your dev server *listens*.
* **Frames vs. Packets:** the IP packet travels (almost) unchanged end to end. Ethernet frames are rebuilt at every hop.
* **Dst IP vs. Dst MAC:** IP names the final target; MAC names only the next hop.
* **DNS is not part of the HTTP request.** It happens first, as a separate conversation (usually over UDP).
* **Steps 3–5 are not one-time.** Every packet goes through them, including the very first connection packet.

---

## 9. Active Recall

1. Why does a packet need a Destination IP *and* a Destination Port *and* a Destination MAC?
2. Your IP is `192.168.0.104/24`. You send to `192.168.0.55` and then to `142.250.80.46`. For each, whose MAC goes in the frame?
3. Your code reports `ECONNREFUSED`. Which step of the journey failed, and what does that tell you about the earlier steps?
4. How does a response reach one specific browser tab among dozens?
5. Which is created first and which is sent last: the HTTP message, or the TCP connection? Why?

<details>
<summary><b>Answers</b></summary>

1. Port = which program; IP = which machine in the world; MAC = which card on this local link right now. Each scope has a different owner and lifetime.
2. `.55` is on-link (same /24), so the frame carries `.55`'s MAC (found via ARP). `142.250.80.46` is off-link, so the frame carries the **default gateway's** MAC.
3. Step 3 (the port). The packet reached the server machine, so DNS, the local-or-remote decision, the hardware hop and routing all worked. Nothing is listening on that port (the server program isn't running, or it listens on a different port).
4. The OS matches the response's Dst Port (the ephemeral port) plus the source IP and port to an open socket, and hands the data to the process that owns it.
5. The HTTP message is created first (step 1) but sent last (step 8). It must wait until the address is known (2), the connection is open (3–6) and encryption is ready (7).

</details>

---

## 10. Revisit Log (This Note Grows)

After each chapter, add a few lines here: what that step now means with what you learned. The circle closes by repeated passes.

| Date | Chapter completed | What this step now means |
|---|---|---|
| 2026-10-10 | Internet Basics | The path is packets, not a wire. Each packet is routed independently. |
| 2026-10-11 | IP & CIDR | The Dst IP in step 4 has a network part and a host part; /24 means 24 bits identify the network. |
| 2026-10-11 | Subnet Masks | Step 4's decision is literally IP AND mask compared against my network. |
| 2026-10-13 | HTTP Basics | Step 1's message is text: request line, headers, empty line, body, turned into bytes. Proof of identity rides in every message (Cookie / Authorization) because HTTP remembers nothing. |
| 2026-10-18 | DNS Resolution | Step 2 is a separate, earlier conversation: one small UDP question to my resolver, which answers from cache or walks root → TLD → authoritative, following referrals. Every answer carries a TTL, so "propagation" is just caches expiring. |
| 2026-10-21 | IP & CIDR (reworked) | The number DNS returns in step 2 is one 32-bit value written as four octets. Its left X bits (/X) name a network, the rest name a host in it, so routers can work with whole networks. 10.x, 172.16–31.x and 192.168.x are private: reused in every home, never seen on the Internet. |
| 2026-10-22 | Act 2: Local or Remote? | Step 4 isolates the network ID via bitwise AND (IP & mask). If off-link, the kernel routing table uses 0.0.0.0/0 to select the Default Gateway (192.168.0.1) as the exit door; the destination IP remains the remote server. All 4 parameters (IP, mask, gateway, DNS) were dynamically leased at boot via DHCP's 4-way DORA handshake. |

---

## 11. What's Next?

Now we start the story at its true beginning: **Act 1**. We write the HTTP message (step 1), look up the address with DNS (step 2), and then look closely at the number DNS hands back: what an IP address is and how CIDR splits it into a network part and a host part. That last piece, which you have partly learned already, gets its place here. **Act 2** then uses it to answer step 4: is the address ours or remote, and who is our way out (the subnet mask and the default gateway)?

See [roadmap.md](../../course-memory/roadmap.md) for the full order.
