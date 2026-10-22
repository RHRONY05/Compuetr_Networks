# Act 2: Local or Remote? (The Boundary, The Door, and The Bootstrap)

> **Act 2 Master Lesson (Sessions 2.0, 2.1, 2.2) · Step 4 of the journey** · [Back to the map](../notes/00-foundations/02-request-lifecycle.md)

> **Time:** about 3–3.5 hours for the complete act (reading ~45 min, videos ~25 min, labs & build ~60 min)
> **By the end you can:**
> 1. Perform the bitwise AND calculation that your OS kernel runs on every packet to decide **On-link** (local) vs. **Off-link** (remote).
> 2. Read and explain every column of your OS routing table (`route print -4`) and identify the **Default Route (`0.0.0.0/0`)**.
> 3. Trace and explain the 4-way **DHCP DORA handshake** that gives your machine its entire network identity before it even has an IP address.
> 4. Run and modify the **Milestone A3** bitwise decision engine and subnet calculator on your own machine.

---

## 🗺️ Where We Are in the Story

```text
   1. WRITE THE MESSAGE        HTTP text → bytes (Act 1.1)
   2. FIND THE ADDRESS (DNS)   api.example.com → 203.0.113.10 (Act 1.2–1.3)
   3. OPEN A CONNECTION        ports + handshake: "are you there?" (Act 4)
 ► 4. LOCAL OR REMOTE?         my IP + mask vs target IP → who is next? ← TODAY (ACT 2)
   5. NEXT PHYSICAL HOP        MAC address of that "next" (Act 3)
   6. CROSS THE PLANET         routers forward hop by hop (Act 5)
   7. MAKE IT PRIVATE          TLS handshake (Act 6)
   8. SEND, REPLY, UNWRAP      HTTP message goes out; reply comes back
```

**Last time** (Act 1), your application wrote an HTTP request, asked DNS for the destination IP, and received a 32-bit number (such as `140.82.112.4` for GitHub, or `203.0.113.10` in our course anchor).

**Today**, in Act 2, your operating system is ready to put that packet onto the wire. But it cannot simply fling bits into the air. It must solve three tightly coupled questions:
1. **The Boundary:** Is that destination IP inside my local room or somewhere out in the world? *(Session 2.0: The Subnet Mask)*
2. **The Exit Door:** If it is outside in the world, who is my way out? *(Session 2.1: The Default Gateway & The Routing Table)*
3. **The Bootstrap:** Where did my laptop get its own IP, its subnet mask, and its gateway in the first place? *(Session 2.2: DHCP)*

**We stop** at the exact moment the OS knows: *"This packet is remote. I must hand it to my Default Gateway (`192.168.0.1`)."* But a physical Wi-Fi card or Ethernet cable cannot transmit directly to an IP address—it requires a physical 48-bit hardware address (MAC). That cliffhanger leads into Act 3 (MAC & ARP).

> **How to read this lesson.** Boxes marked 🔵 **Later** flag concepts you will meet in upcoming acts (like MAC addresses, ARP, and NAT). They exist to keep today's mental model clean without cluttering you with future mechanics. Read them, note the act, and stay in Step 4.

---

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **Subnet Mask** | A 32-bit filter of consecutive 1s followed by 0s that tells the computer which bits of an IP represent the network and which represent the host. |
| **On-link (Local)** | Located on the same local physical network; reachable directly without passing through a router. |
| **Off-link (Remote)** | Located on a different network; unreachable directly, must be handed to a gateway. |
| **Default Gateway** | The local device (usually your home Wi-Fi router) that acts as the exit door for any packet headed outside your subnet. |
| **Routing Table** | An in-memory decision table inside your OS kernel that maps destination IP ranges to next hops and network interfaces. |
| **Default Route (`0.0.0.0/0`)** | The fallback rule in the routing table: "If no specific local route matches this destination IP, send it to the Default Gateway." |
| **Hop** | One leg of a packet's journey between routers. Your gateway is always Hop 1. |
| **DHCP** | Dynamic Host Configuration Protocol: the automatic system that leases an IP, subnet mask, default gateway, and DNS server to your computer when it joins a network. |
| **DORA** | The 4-step DHCP exchange: **D**iscover, **O**ffer, **R**equest, **A**cknowledge. |
| **Lease Time** | The agreed countdown period during which an IP address is rented to your machine by the DHCP server. |
| **Broadcast Address (`255.255.255.255`)** | The special address meaning "deliver this packet to every single machine on this local network." |

---

## 🔵 Parking Lot: Words You'll Hear, and Where They Live

| You'll hear... | What it is (one line) | Studied in |
|---|---|---|
| MAC address, ARP | How your card physically addresses the gateway on the local radio/wire | Act 3 (Next session) |
| Switch vs. Router | Switches move frames within a local room; routers move packets between different networks | Act 3 & Act 5 |
| NAT (Network Address Translation) | How your router swaps your private IP (`192.168.0.102`) for a single public IP to talk to the Internet | Act 5.4 |
| WAN vs. LAN | Wide Area Network (Internet side) vs. Local Area Network (room side) of a router | Act 5 |
| BGP, OSPF, Routing algorithms | How global Internet routers figure out multi-hop paths between countries | Act 5.3 |
| APIPA (`169.254.x.x`) | The self-assigned fallback IP your OS picks when no DHCP server answers | Session 2.2 / Troubleshooting |

---

## Part 1: The Local Boundary — Subnet Masks & The Decision Engine

### The Problem
Imagine you are sitting in an office with 20 colleagues.
- If you want to say something to Fahim at the next desk, you speak out loud. You don't call an international courier to deliver a note across the room.
- But if you want to send a letter to a server in Tokyo, you cannot shout across the desk. You must drop the letter into an outbound mailbox.

Before your computer touches its Wi-Fi antenna or Ethernet cable, it must answer:
**Is the destination IP in my room, or outside in the world?**

### The Mechanism: Bitwise AND
Your computer does not use string comparisons or heuristics. It performs a single, lightning-fast bitwise arithmetic operation:

```text
                      [ Destination IP to reach ]
                                   │
                                   ▼
             Does (Target IP & Subnet Mask) == My Network ID?
                                   │
                  ┌────────────────┴────────────────┐
                  │ YES                             │ NO
                  ▼                                 ▼
           [ ON-LINK (Local) ]             [ OFF-LINK (Remote) ]
        Target is in my room.            Target is outside in the world.
        Send directly to target.         Send to DEFAULT GATEWAY.
```

### Worked Example: Real Data from Your Laptop
From your machine's live Wi-Fi configuration:
- **My IP:** `192.168.0.102`
- **Subnet Mask:** `255.255.255.0` (`/24`)
- **My Network ID:** `192.168.0.0`

Recall from binary: `255` is eight 1s (`11111111`). `0` is eight 0s (`00000000`).
When you do a bitwise `AND` with `1`, the bit stays unchanged.
When you do a bitwise `AND` with `0`, the bit becomes `0`.

#### Scenario A: You send data to a local printer / roommate (`192.168.0.50`)
```text
Target IP:    192.168.0.50   AND 255.255.255.0  =  192.168.0.0
My Network:   192.168.0.102  AND 255.255.255.0  =  192.168.0.0
```
**Result:** `192.168.0.0 == 192.168.0.0`. **MATCH!**
This target is **On-link**. The packet stays inside your local Wi-Fi room. The router's Internet gateway is never bothered.

#### Scenario B: You call GitHub's API (`140.82.112.4`)
```text
Target IP:    140.82.112.4   AND 255.255.255.0  =  140.82.112.0
My Network:   192.168.0.102  AND 255.255.255.0  =  192.168.0.0
```
**Result:** `140.82.112.0 != 192.168.0.0`. **NO MATCH!**
This target is **Off-link**. Your laptop cannot reach `140.82.112.4` directly over Wi-Fi. It must hand the packet to an exit door.

### 💡 Developer Connection: Database Latency & Subnet Co-location
Why does this distinction matter to a backend developer?
- If your **Node.js API server** and your **PostgreSQL database** are in the **same subnet** (e.g. inside the same AWS VPC subnet `10.0.1.0/24`), packets pass directly between them at wire speed (`<0.5 ms` latency, zero router hops).
- If your database is placed in a **different subnet or outside network**, every SQL query must travel through a gateway and router hops, adding latency, NAT overhead, and firewall inspection.
Understanding subnets is the key to designing low-latency cloud infrastructure.

---

## Part 2: The Exit Door — The Default Gateway & The Routing Table

### The Problem: The Island Dilemma
Your laptop's Wi-Fi radio waves only reach about 15 meters. Your laptop has no physical wires running to Google, GitHub, or Cloudflare.

If your operating system didn't have a designated gateway, the moment you typed `fetch("https://github.com")`, your OS would say:
> *"I have an IP packet addressed to `140.82.112.4`. I checked my local Wi-Fi room, and nobody here has that IP. I don't know any exit door. Packet dropped: Network is unreachable."*

Every computer that wants to talk to the Internet needs an exit door: the **Default Gateway**.

### What Actually Is the Default Gateway?
In home and office networks, the **Default Gateway is your Wi-Fi router**.

Look at the router box in your room. That box has **two different sides**:
1. **The LAN side (Local Area Network):** Faces inward toward you. It has an IP address on your subnet—`192.168.0.1`. Your laptop can reach this address directly over local Wi-Fi.
2. **The WAN side (Wide Area Network):** Faces outward toward your ISP (Internet Service Provider) via fiber-optic cable or coaxial cable.

```text
 ┌─────────────────┐
 │ Your Laptop     │
 │ 192.168.0.102   │
 └────────┬────────┘
          │ (Local Wi-Fi link)
          ▼
 ┌──────────────────────────────────────────────────────────────┐
 │                    HOME WI-FI ROUTER                         │
 │                                                              │
 │   LAN Interface: 192.168.0.1  <── [ THIS IS YOUR GATEWAY ]   │
 │   WAN Interface: 103.x.x.x (or ISP fiber link)               │
 └──────────────────────────────┬───────────────────────────────┘
                                │ (Fiber / Cable to ISP)
                                ▼
                       THE GLOBAL INTERNET
```

Because the router's LAN address (`192.168.0.1`) sits **on your own subnet**, your laptop can talk to it directly. You hand your remote packet to the router, and the router pushes it out its WAN port toward the world.

### The Decision Engine: The OS Kernel Routing Table
Your operating system doesn't guess. It maintains a kernel table called the **Routing Table**. Whenever a packet is created, the kernel scans this table from most specific prefix to least specific prefix.

Here is the real table from your machine (from `route print -4`):

```text
===========================================================================
IPv4 Route Table
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.0.1    192.168.0.102     45  ◄ [DEFAULT ROUTE]
      192.168.0.0    255.255.255.0         On-link     192.168.0.102    301  ◄ [LOCAL SUBNET]
    192.168.0.102  255.255.255.255         On-link     192.168.0.102    301  ◄ [MY OWN IP]
     172.19.160.0    255.255.240.0         On-link      172.19.160.1   5256  ◄ [WSL VIRTUAL NET]
===========================================================================
```

### The Universal Catch-all: `0.0.0.0/0`
Look at Row 1:
- `Network Destination: 0.0.0.0`
- `Netmask: 0.0.0.0`

Any 32-bit number `AND 0.0.0.0` equals `0.0.0.0`.
That means **EVERY IP ADDRESS ON THE INTERNET matches `0.0.0.0/0`!**
It is the ultimate fallback rule. The rule says:
*"If no specific local rule claimed this packet, hand it to Gateway `192.168.0.1` via Wi-Fi interface `192.168.0.102`."*

> 🟡 **Crucial Reality Check:** When your laptop hands this packet to the Default Gateway, **it does NOT rewrite the destination IP**. The IP packet still says `Dst IP: 140.82.112.4` (GitHub). You are saying to the router: *"Here is a packet for GitHub. I cannot deliver it to GitHub directly, but you know the way outside."*

---

## Part 3: The Bootstrap — DHCP & Who Gave Me These Numbers?

### The Chicken-and-Egg Paradox
We just saw that your laptop needs four critical parameters to function:
1. Its own **IPv4 Address** (`192.168.0.102`)
2. Its **Subnet Mask** (`255.255.255.0`)
3. Its **Default Gateway** (`192.168.0.1`)
4. Its **DNS Resolver** (`192.168.0.1`)

*Think about the dilemma:*
When you turn on your laptop or walk into a coffee shop and connect to Wi-Fi, your laptop has **no IP address**.
To communicate over IP, you need an IP address. But how can you ask for an IP address over the network if you don't have an IP address yet?

This bootstrap problem is solved by **DHCP (Dynamic Host Configuration Protocol)**.

### The Mechanism: Broadcast Shouting
If you don't know who you are, and you don't know who the router is, you cannot whisper directly (unicast).
You must **stand in the middle of the room and shout at the top of your lungs (broadcast)**.

In IPv4, the universal room shout is sent to:
`Destination IP: 255.255.255.255`
Every device connected to that Wi-Fi network picks up and examines a broadcast packet.

### The 4-Way DORA Handshake
DHCP configures your machine in four clean steps, remembered by the acronym **DORA**:

```text
  YOUR LAPTOP                                          HOME WI-FI ROUTER
  (No IP yet)                                          (DHCP Server: 192.168.0.1)
       │                                                          │
       │  ① DISCOVER (Broadcast: 255.255.255.255)                 │
       ├─────────────────────────────────────────────────────────►│
       │  "Hello! I am MAC 94-BB-43-74-E0-DD. Anyone have an IP?" │
       │                                                          │
       │  ② OFFER (Broadcast or Unicast)                          │
       │◄─────────────────────────────────────────────────────────┤
       │  "I can lease you 192.168.0.102, mask 255.255.255.0,     │
       │   gateway 192.168.0.1, DNS 192.168.0.1 for 3 hours."     │
       │                                                          │
       │  ③ REQUEST (Broadcast: 255.255.255.255)                  │
       ├─────────────────────────────────────────────────────────►│
       │  "Thank you! I formally accept 192.168.0.102 from        │
       │   server 192.168.0.1."                                   │
       │                                                          │
       │  ④ ACKNOWLEDGE (ACK)                                     │
       │◄─────────────────────────────────────────────────────────┤
       │  "Confirmed! 192.168.0.102 is officially yours.          │
       │   Your 3-hour countdown begins now."                     │
       ▼                                                          ▼
```

#### Why is Step 3 (Request) also broadcast?
If there were two DHCP servers on the network, both might send an Offer. By broadcasting its Request naming Server `192.168.0.1`, the client politely informs any other DHCP server: *"Thank you for your offer, but I chose server 192.168.0.1; you may release your reserved IP back into your pool."*

### Leases, Not Ownership
You do **not own** your IP address. You **rent** it on a **lease**.
Look at the real data captured from your machine today:
- `Lease Obtained: Thursday, October 22, 2026 1:01:15 PM`
- `Lease Expires:  Thursday, October 22, 2026 4:01:25 PM`
Your lease duration is exactly **3 hours** (10,800 seconds).

#### Why are IPs leased instead of permanent?
If IP addresses were assigned permanently, a coffee shop or university would run out of addresses on day one. Guests who leave would permanently hoard IP addresses. Leases guarantee that inactive or departed devices automatically forfeit their IP back into the available pool.

#### How Lease Renewal Works (The Two Timers)
Your laptop does not wait until 4:01 PM to scramble for a new IP. It runs two quiet renewal timers:
1. **T1 (Renewal at 50% = 1.5 hours):** At halfway through the lease, your laptop quietly sends a unicast DHCP Request directly to `192.168.0.1`: *"Hey, I'm still here, can I renew?"* The router replies with an ACK, and the timer resets to 3 hours. You never notice this.
2. **T2 (Rebinding at 87.5% = ~2.6 hours):** If your router crashed or didn't answer at T1, your laptop panics and broadcasts to the entire room: *"Can ANY DHCP server extend my lease?"*
3. **Expiration:** If the timer reaches 100% with no answer, the OS immediately releases the IP, and your Wi-Fi disconnects.

### What Happens When DHCP Fails? (APIPA)
If you connect to a broken Wi-Fi router or an Ethernet switch where no DHCP server is running:
Your OS waits a few seconds, gets no DORA response, and gives up.
To prevent complete failure, the OS self-assigns an **APIPA** (Automatic Private IP Addressing) address in the range:
`169.254.0.1` to `169.254.255.254` (prefix `/16`).
Whenever you see your laptop has an IP starting with **`169.254.x.x`**, you immediately know: **DHCP failed; no router answered my DORA shout!**

---

## 🔬 Labs: On Your Real Machine

Let's inspect all three components live on your system.

### Lab A: The Complete Network Identity (`ipconfig /all`)
Run this in PowerShell:
```powershell
ipconfig /all
```

Look at the `Wireless LAN adapter Wi-Fi` section (captured live 2026-10-22):
```text
Wireless LAN adapter Wi-Fi:

   Physical Address. . . . . . . . . : 94-BB-43-74-E0-DD
   DHCP Enabled. . . . . . . . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 192.168.0.102(Preferred) 
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Lease Obtained. . . . . . . . . . : Thursday, October 22, 2026 1:01:15 PM
   Lease Expires . . . . . . . . . . : Thursday, October 22, 2026 4:01:25 PM
   Default Gateway . . . . . . . . . : 192.168.0.1
   DHCP Server . . . . . . . . . . . : 192.168.0.1
   DNS Servers . . . . . . . . . . . : 192.168.0.1
```
Notice how **one single DHCP server (`192.168.0.1`)** handed your laptop everything in one lease:
- Your IP (`192.168.0.102`)
- Your boundary (`255.255.255.0`)
- Your exit door (`192.168.0.1`)
- Your phonebook resolver (`192.168.0.1`)

---

### Lab B: Inspecting the Active Routes (`route print -4`)
Run:
```powershell
route print -4
```

Look at the active routes:
```text
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.0.1    192.168.0.102     45
      192.168.0.0    255.255.255.0         On-link     192.168.0.102    301
```
- `192.168.0.0/24` is marked **On-link**: delivered directly out interface `192.168.0.102`.
- `0.0.0.0/0` points to **Gateway `192.168.0.1`**: the catch-all for every other IP in existence.

---

### Lab C: Verifying the First Hop with `tracert`
Run:
```powershell
tracert -d -h 3 8.8.8.8
```

Real output captured on your machine:
```text
Tracing route to 8.8.8.8 over a maximum of 3 hops

  1    <1 ms    <1 ms    <1 ms  192.168.0.1 
  2     2 ms     1 ms     1 ms  10.115.0.1 
  3     6 ms     4 ms    10 ms  172.23.6.121 

Trace complete.
```
- **Hop 1 is `192.168.0.1` in `<1 ms`:** It's your Default Gateway sitting right across the room over Wi-Fi.
- **Hop 2 & Hop 3 (`10.115.0.1`):** Your ISP's internal routing infrastructure outside your building.

---

## 🛠️ Build: Project Milestone A3 — `is_local()` & Subnet Calculator

We built the core decision engine that models how the OS handles Step 4:
**Script:** [hands-on-lab/act2-2.1-is-local.py](../hands-on-lab/act2-2.1-is-local.py).


### Run it
Run the script with no arguments:
```powershell
python hands-on-lab/act2-2.1-is-local.py
```

### What the tool demonstrates:
1. **Integer Bit Operations:** Uses pure `&`, `|`, `~`, `<<` bitwise operators to convert IPs and masks into 32-bit integers.
2. **Subnet Calculation:** Calculates Network ID, Broadcast ID, and usable host count.
3. **Decision Step:** Compares `(My IP & Mask)` against `(Target IP & Mask)` and outputs whether the packet stays **On-link** or goes to the **Default Gateway**.

### Experiments to run:
1. **Check local router:**
   ```powershell
   python hands-on-lab/act2-2.1-is-local.py 192.168.0.102/24 192.168.0.1
   ```
   *(MATCH -> ON-LINK: deliver directly without a gateway).*
2. **Check remote server (Google DNS):**
   ```powershell
   python hands-on-lab/act2-2.1-is-local.py 192.168.0.102/24 8.8.8.8
   ```
   *(NO MATCH -> OFF-LINK: hand to Default Gateway `192.168.0.1`).*
3. **Check WSL adapter:**
   ```powershell
   python hands-on-lab/act2-2.1-is-local.py 172.19.160.1/20 172.19.165.42
   ```
   *(MATCH -> ON-LINK on the virtual hypervisor adapter).*

---

## 📺 Watch Guide (about 25 min total)

Read the lesson first. The videos bring the network diagrams and packet exchanges to life:

| Video | Watch? | Notes |
|---|---|---|
| **C5** Subnet Masks Deep Dive (10:56) | ✅ All | Matches Part 1. Shows bitwise AND on the whiteboard and the database co-location example. |
| **C6** Understanding Default Gateway (04:06) | ✅ All | Matches Part 2. The 4-minute overview of why remote packets must go to "brother router". |
| **C7** How Default Gateways Facilitate Network Communication (09:11) | ✅ All | Two networks (A and B) connected by a router with two interfaces. Great visual reinforcement of Part 2. |
| **K4.3** Kurose Lecture (DHCP section) | 🟡 Optional | Academic breakdown of the DORA message format and UDP ports 67/68. |

---

## ⚠️ Common Confusions

1. **"The default gateway changes the packet's destination IP to itself."**
   *Never!* The destination IP remains `140.82.112.4` (GitHub) from start to finish. Only the local physical delivery envelope targets the gateway.
2. **"If my router loses Internet connection, my home network stops working."**
   *False!* Your router is also a local switch. Local devices (`192.168.0.102` to `192.168.0.105`) communicate directly on-link. Local printing, media streaming (Plex/Chromecast), and file sharing continue working with the Internet cable unplugged!
3. **"DHCP uses TCP because it needs to be reliable."**
   *False!* DHCP cannot use TCP because TCP requires a 3-way handshake between two known IP addresses. A client with no IP address cannot open a TCP connection! DHCP uses UDP with broadcast (`255.255.255.255`).
4. **"An IP address starting with 169.254 means my internet is working."**
   *Opposite!* `169.254.x.x` is APIPA. It means your computer shouted for a DHCP server and nobody answered.
5. **"Can I have two default gateways?"**
   If both Wi-Fi and Ethernet are connected, your OS routing table has two `0.0.0.0/0` rules. The kernel picks the route with the lower **Metric** (lower cost/higher speed, usually Ethernet).

---

## 🧠 Active Recall

Test your understanding before finishing Act 2. Try answering without peeking:

1. Your computer has IP `10.0.1.20/24` and Default Gateway `10.0.1.1`. You send a ping to `10.0.1.75`. Does this packet go to the default gateway? Why or why not?
2. What does `0.0.0.0` with netmask `0.0.0.0` mean in a routing table, and why is it called the "default route"?
3. Name the four steps of DORA in order, and explain why Step 1 (Discover) must be sent to `255.255.255.255`.
4. When your laptop is halfway through its 3-hour lease (at 1.5 hours), does it broadcast to the whole room again? How does it renew?
5. When your packet for GitHub (`140.82.112.4`) leaves your laptop for your gateway (`192.168.0.1`), what address is written in the packet's `Destination IP` field?
6. You plug an Ethernet cable into an office wall jack, and your laptop gets IP `169.254.45.12`. What went wrong?

<details>
<summary><b>View Answers</b></summary>

1. **No.** `10.0.1.20 AND 255.255.255.0 = 10.0.1.0`. `10.0.1.75 AND 255.255.255.0 = 10.0.1.0`. Both share the identical network ID `10.0.1.0/24`. The target is **On-link**; the OS delivers it directly across the local wire without touching the gateway.
2. `0.0.0.0` with netmask `0.0.0.0` matches zero required bits, meaning **every single IPv4 address on Earth matches it**. It is the catch-all fallback route when no specific local subnet matches.
3. **Discover, Offer, Request, Acknowledge.** Discover must be sent to `255.255.255.255` because the new client has no IP address and does not know the IP address of any DHCP server.
4. **No.** At 50% lease time (T1), it sends a quiet, direct **unicast** DHCP Request to the known DHCP server (`192.168.0.1`). It only broadcasts to the room if the router fails to reply and the timer reaches 87.5% (T2).
5. **`140.82.112.4`**. The destination IP is **never** changed to the gateway's IP. If it were changed, the router would think the packet was for itself and would never forward it to GitHub!
6. **DHCP failed.** No DHCP server answered the Discover shout on that wall jack. The OS fell back to self-assigning an APIPA address.

</details>

---

## 🔄 Close the Loop

**Revisit Log line for the anchor note:**
`2026-10-22 | Act 2: Local or Remote? | Step 4 resolves local vs remote using (IP & mask). If remote, the kernel routing table (0.0.0.0/0) selects the Default Gateway (192.168.0.1). All 4 network parameters (IP, mask, gateway, DNS) were dynamically leased at boot via DHCP's 4-way DORA handshake.`

**The cliffhanger:**
We now know where the packet must go: it must be handed to our Default Gateway at `192.168.0.1`.
*But here is the catch:* your laptop's Wi-Fi card does not transmit to IP addresses. Wi-Fi radios and Ethernet cables only understand physical 48-bit hardware addresses called **MAC addresses**.

How does your laptop discover the physical MAC address of `192.168.0.1` so it can actually transmit the radio frame?
→ **Act 3: The Next Physical Hop (MAC and ARP).**

---

## Previous Versions

<details>
<summary><b>v1 · 2026-10-22 · Session 2.1 standalone</b>. Consolidated into full Act 2 master lesson upon student request.</summary>

# Session 2.1: The Default Gateway (Your Door to the World)

> **Act 2 · Step 4 of the journey** · [Back to the map](notes/00-foundations/02-request-lifecycle.md)
> **Time:** about 2–2.5 hours (reading ~35 min, videos ~15 min, labs & build ~50 min)
> **By the end you can:** explain why your laptop cannot talk to the Internet without a gateway, read your OS routing table (`route print`) to identify `0.0.0.0/0`, predict whether a packet stays on-link or leaves through the gateway using bitwise logic, and verify your gateway as hop 1 with `tracert`.

*(Standalone Session 2.1 draft replaced by the unified Act 2 Master Lesson above).*

</details>
