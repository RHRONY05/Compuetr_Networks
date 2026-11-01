# DHCP: Who Gave Me These Numbers?

> **Zooming into:** Step 4 of the [Request Lifecycle](../00-foundations/02-request-lifecycle.md) · Act 2
> **Prerequisites:** [The Default Gateway & The Routing Table](03-default-gateway.md)
> **Key Goal:** Explain how an unconfigured computer bootstraps its entire network identity using DHCP and the 4-way DORA broadcast handshake, and how IP leases, renewals, and MAC bindings work under the hood.
> **Lesson:** [lessons/act2-local-or-remote.md](../../lessons/act2-local-or-remote.md) · **Recall:** [RECALL.md#act-2--step-4-local-or-remote](RECALL.md#act-2--step-4-local-or-remote)

---

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **DHCP** | Dynamic Host Configuration Protocol: the automatic service that leases IP configurations to connecting devices. |
| **DORA** | The 4-step handshake: **D**iscover, **O**ffer, **R**equest, **A**cknowledge. |
| **Broadcast Address (`255.255.255.255`)** | The special destination address meaning "deliver this packet to every machine on this physical local network." |
| **Lease Time** | The agreed duration for which an assigned IP address is rented to your machine. |
| **T1 / T2 Timers** | The renewal checkpoints: T1 (50% of lease, quiet unicast request) and T2 (87.5% of lease, room-wide broadcast). |
| **APIPA (`169.254.x.x`)** | Automatic Private IP Addressing: the fallback IP an OS assigns itself when no DHCP server answers. |
| **MAC Binding / Static Reservation** | A router configuration mapping a specific physical MAC address to a permanent, fixed IP. |

---

## 1. The Story So Far

In the previous chapters, we saw that to send an HTTP request, your operating system relies on four coupled parameters:
1. **Your IPv4 Address:** `192.168.0.102` (who you are)
2. **Your Subnet Mask:** `255.255.255.0` (your local boundary)
3. **Your Default Gateway:** `192.168.0.1` (your exit door to the world)
4. **Your DNS Resolver:** `192.168.0.1` (your domain name phonebook)

You did not type these numbers into a configuration file by hand. The second you opened your laptop and connected to Wi-Fi, these numbers appeared automatically.

Who assigned them? How did your computer ask for them before it even had an IP address?
That bootstrap system is **DHCP (Dynamic Host Configuration Protocol)**.

---

## 2. The Real-World Problem: The Chicken-and-Egg Paradox

Imagine the dilemma of a newly booted laptop connecting to a network:
- To communicate over an IP network, **you must have an IP address**.
- But if you have no IP address, **how can you ask for an IP address?**
- You do not know your own address, and you do not know the IP address of any server on the network.

If the network only allowed direct, private whispers (unicast between known IP addresses), no new computer could ever join!

---

## 3. The Mental Model: The Job Fair Megaphone

Imagine walking into a large convention center without a name badge. You don't know who the organizer is or where the check-in desk sits.
- You cannot walk up to someone and whisper their name, because you don't know anyone's name.
- So you pick up a **megaphone** in the middle of the hall and shout:
  *"Hello! I am wearing a red jacket (MAC address). Does anyone have a name badge for me?"*

Everyone in the hall hears your shout. The event organizer hears it, steps forward, and hands you a badge with your name and directions to the exit doors.

In computer networking, that megaphone shout is a **Broadcast packet** sent to:
`Destination IP: 255.255.255.255`.

---

## 4. Deep Dive & Mechanics

### 4.1 The 4-Way DORA Handshake
DHCP configures your machine in four clean steps, remembered by the acronym **DORA**:

```text
  YOUR LAPTOP                                          HOME WI-FI ROUTER
  (No IP assigned yet)                                 (DHCP Server: 192.168.0.1)
       │                                                          │
       │  ① DISCOVER (Broadcast: 255.255.255.255)                 │
       ├─────────────────────────────────────────────────────────►│
       │  Src: 0.0.0.0:68  Dst: 255.255.255.255:67                │
       │  "Hello! I am MAC 94-BB-43-74-E0-DD. Anyone have an IP?" │
       │                                                          │
       │  ② OFFER (Unicast or Broadcast)                          │
       │◄─────────────────────────────────────────────────────────┤
       │  Src: 192.168.0.1:67  Dst: 255.255.255.255:68            │
       │  "I offer you 192.168.0.102, mask 255.255.255.0,         │
       │   gateway 192.168.0.1, DNS 192.168.0.1, lease 3 hours."  │
       │                                                          │
       │  ③ REQUEST (Broadcast: 255.255.255.255)                  │
       ├─────────────────────────────────────────────────────────►│
       │  Src: 0.0.0.0:68  Dst: 255.255.255.255:67                │
       │  "I formally accept 192.168.0.102 from server            │
       │   192.168.0.1."                                          │
       │                                                          │
       │  ④ ACKNOWLEDGE (ACK)                                     │
       │◄─────────────────────────────────────────────────────────┤
       │  Src: 192.168.0.1:67  Dst: 255.255.255.255:68            │
       │  "Confirmed! 192.168.0.102 is officially yours.          │
       │   Your 3-hour lease countdown starts now."               │
       ▼                                                          ▼
```

#### Why is Step 3 (Request) also broadcast?
If multiple DHCP servers exist on the network (e.g. in a large office), several servers might send an **Offer**.
By broadcasting its **Request** explicitly naming `Server Identifier: 192.168.0.1`, your laptop politely informs all other DHCP servers:
*"Thank you for your offers, but I chose server 192.168.0.1; you may release your reserved IPs back into your pools."*

---

### 4.2 Why DHCP Uses UDP (Not TCP)
A beginner often asks: *"Isn't getting an IP important? Why doesn't DHCP use TCP for reliability?"*

**TCP requires a 3-way handshake between two already-assigned IP addresses.**
A machine with no IP address cannot establish a TCP connection! DHCP therefore runs over **UDP** (client port `68`, server port `67`), utilizing broad-stroke network broadcasts.

---

### 4.3 Leases, Not Ownership
You do **not own** your IP address. You **rent** it on a **lease**.
Look at the real data captured from your laptop:
- `Lease Obtained: Thursday, October 22, 2026 1:01:15 PM`
- `Lease Expires:  Thursday, October 22, 2026 4:01:25 PM`
Your lease duration is exactly **3 hours** (10,800 seconds).

#### Why are IPs leased instead of permanent?
If IP addresses were assigned permanently, public Wi-Fi networks (cafes, airports, universities) would exhaust their IP pools on the first day. Devices that leave the building would permanently hoard IPs. Leases ensure that inactive devices automatically forfeit unused addresses back to the pool.

---

### 4.4 How Lease Renewal Works (The Two Timers)
Your laptop does not wait until the last second to scramble for a new IP. It runs two quiet renewal timers:

```text
 0%                      50% (T1)                87.5% (T2)             100%
 ├─── Lease Granted ─────┼─── T1 Renewal ────────┼─── T2 Rebinding ─────┼── Expired
 │                       │                       │                      │
 Lease starts            Laptop quietly sends    Router down?           IP released.
 (1:01 PM)               unicast DHCP Request    Laptop panics and      Wi-Fi drops.
                         directly to router.     broadcasts to room.
```

1. **T1 Timer (50% of lease = 1.5 hours):** At halfway through the lease, Windows quietly sends a direct unicast DHCP Request to `192.168.0.1`: *"Hey, I'm still here, can I extend my lease?"* The router replies with an ACK, and the timer resets to 3 hours. You never notice this.
2. **T2 Timer (87.5% of lease = ~2.6 hours):** If your router was restarting or didn't answer at T1, the laptop broadcasts to the room: *"Can ANY DHCP server extend my lease?"*
3. **Expiration (100%):** If no server answers, the laptop releases the IP, and network connectivity terminates.

---

### 4.5 Why Does Your Laptop Get the Same IP After Days?
You might notice that even after turning your laptop off for two days, you reconnect to your home Wi-Fi and receive `192.168.0.102` again. Why?

1. **The Router's MAC Binding Table:**
   Your home router maintains an internal table in memory:
   ```text
   MAC Address: 94-BB-43-74-E0-DD  <───>  Last Known IP: 192.168.0.102
   ```
   When your laptop reconnects, the router checks its table: *"This is Rhrony's laptop. Is `.102` currently free? Yes. Reassign `.102` to him."*
2. **Client Memory (Option 50):**
   Windows remembers its last assigned IP. In its DHCP Discover message, it explicitly requests: *"I was using `192.168.0.102` previously, can I keep it?"*

#### When will you get a different IP?
If 30 guests visit your house while your laptop is off and the router exhausts its pool, the router reallocates `.102` to a guest. When you turn on your laptop, the router sends a `DHCP NAK` (Not Acknowledged): *"Sorry, `.102` is in use. Here is `.115` instead."*

#### What if you disconnect and reconnect within the 3-hour lease?
Your lease is still **active** in the router's table! Your laptop skips the full Discover/Offer dance, sends a rapid Request confirming `.102`, the router sends an instant ACK, and you are online in milliseconds.

---

### 4.6 What Happens When DHCP Fails? (APIPA)
If you connect to a broken switch or an unconfigured router where no DHCP server is running:
- Your computer sends Discover broadcasts.
- Nobody answers.
- Rather than giving up entirely, Windows self-assigns a fallback address called **APIPA** (Automatic Private IP Addressing) in the range:
  `169.254.0.1` to `169.254.255.254` (prefix `/16`).

Whenever you see your network card has an IP starting with **`169.254.x.x`** and Windows reports *"No Internet, Secured"*, you know with 100% certainty: **DHCP failed; no server answered the DORA handshake!**

---

## 5. Hands-On & Developer Lab

### Inspecting Your Live DHCP Lease
Run in PowerShell:
```powershell
ipconfig /all
```
Real output from your Wi-Fi card:
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
Notice that **`DHCP Server: 192.168.0.1`** is the exact same IP address as your **Default Gateway** and your **DNS Server**. Your home router handles all three responsibilities.

---

## 6. Pitfalls & Production Reality

* **Static IP vs. DHCP Reservation:** In server environments, developers often need an EC2 instance or Raspberry Pi to keep a permanent IP. Instead of hard-coding a static IP on the machine (which risks IP collisions if another device takes it), best practice is creating a **DHCP Reservation** in the router: binding the server's MAC address to a fixed IP. The server still uses DHCP, but always receives the exact same IP.
* **Rogue DHCP Servers:** If someone accidentally plugs an unconfigured home Wi-Fi router into an office Ethernet wall port, that rogue router may start answering DORA Discovers faster than the corporate DHCP server, handing out wrong gateways (`192.168.1.1`) and breaking Internet access for the entire floor!
* **Cloud DHCP:** In AWS VPC, Google Cloud VPC, and Docker networks, a virtual DHCP server automatically runs at the VPC router address (typically `.1` or `.2`), dynamically provisioning IPs to new containers and VM instances.

---

## 🧠 The Moral of the Story (One-Look Mindmap)

> **The Core Question:**
> *A computer boots with NO IP address. How does it bootstrap its entire network identity without an address to communicate?*

```text
                        THE 30-SECOND MENTAL WALKTHROUGH

 1. THE CHICKEN & EGG: You need an IP to send packets, but need to send packets to get an IP.
                       Solution: UDP Broadcast to `255.255.255.255` ("everyone on link").
                                           │
                                           ▼
 2. THE DORA DANCE:    • Discover:    Client shouts "I need an IP! My MAC is 94-BB-43-..."
                       • Offer:       Router offers IP 192.168.0.108 + mask + gateway + DNS.
                       • Request:     Client broadcasts "I accept router 192.168.0.1's offer!"
                       • Acknowledge: Router confirms lease and starts the timer.
                                           │
                                           ▼
 3. LEASE RENEWAL:     • At 50% time (T1): Quiet direct unicast request to the router.
                       • At 87.5% time (T2): Desperate room-wide broadcast if T1 failed.
                                           │
                                           ▼
 4. THE FAILSAFE:      If zero DHCP servers answer, the OS self-assigns an APIPA
                       address (`169.254.x.x/16`) allowing local link comms only.
                                           │
                                           ▼
 5. THE CLIFFHANGER:   Step 4 is complete! The kernel selected exit door `192.168.0.1`.
                       How does our Wi-Fi card reach `192.168.0.1` physically through the air?
```

---

## 7. Close the Loop

* **Revisit Log line:**
  `2026-10-22 | DHCP & Network Bootstrapping | Step 4's four parameters (IP, mask, gateway, DNS) are leased at boot via DHCP's 4-way DORA broadcast handshake (ports 67/68 UDP). Leases renew quietly at 50% time (T1), and failover to APIPA (169.254/16) if unanswered.`
* **The cliffhanger:**
  Step 4 is complete! We have our IP, we used our subnet mask to determine GitHub is Off-link, and our routing table selected our Default Gateway (`192.168.0.1`) as the exit door.
  *But your Wi-Fi card cannot transmit to an IP address.* Wi-Fi and Ethernet hardware cards only understand 48-bit physical **MAC addresses**.
  How does your laptop discover the physical MAC address of `192.168.0.1` so it can actually transmit the radio frame?
  → **Act 3 · Step 5: The Next Physical Hop (MAC & ARP).**
