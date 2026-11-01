# The Default Gateway & The Kernel Routing Table

> **Zooming into:** Step 4 of the [Request Lifecycle](../00-foundations/02-request-lifecycle.md) · Act 2
> **Prerequisites:** [Subnet Masks & The Decision Step](02-subnet-masks.md)
> **Key Goal:** Explain how an operating system kernel uses its in-memory routing table to select an exit door for off-link packets, why `0.0.0.0/0` matches the entire Internet, and how packets physically depart through the hardware interface.
> **Lesson:** [lessons/act2-local-or-remote.md](../../lessons/act2-local-or-remote.md) · **Script:** [hands-on-lab/act2-2.1-is-local.py](../../hands-on-lab/act2-2.1-is-local.py) · **Recall:** [RECALL.md#act-2--step-4-local-or-remote](RECALL.md#act-2--step-4-local-or-remote)

---

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **Default Gateway** | The local device (usually your home Wi-Fi router) that serves as the exit door for packets leaving your subnet. |
| **Routing Table** | An in-memory decision table inside the OS kernel mapping destination address ranges to next hops and network interfaces. |
| **Default Route (`0.0.0.0/0`)** | The universal fallback rule: "If no specific local route matches, forward to the Default Gateway." |
| **Longest Prefix Match (LPM)** | The kernel routing rule: when multiple routing table rows match an IP, the row with the most specific (longest) netmask wins. |
| **Hop** | One leg of a packet's journey between routers. Your Default Gateway is always **Hop 1**. |
| **NIC (Network Interface Card)** | The physical or virtual hardware card (e.g. MediaTek Wi-Fi chip) that translates digital bits into electromagnetic airwaves or wire voltages. |

---

## 1. The Story So Far

In the [previous chapter](02-subnet-masks.md), our operating system ran the bitwise AND decision on our outbound packet:
```text
Target IP (GitHub): 140.82.112.4  AND 255.255.255.0 = 140.82.112.0
My Network ID:      192.168.0.102 AND 255.255.255.0 = 192.168.0.0
```
The network IDs do not match (`140.82.112.0 != 192.168.0.0`). The destination is **Off-link**.

Your laptop cannot reach GitHub directly over Wi-Fi. It has no physical cables running to Virginia or Tokyo. To get that packet to GitHub, the operating system must answer:
```text
"Who is my exit door, and how does my kernel decide where to hand this packet?"
```
That exit door is the **Default Gateway**.

---

## 2. The Real-World Problem: The Island Dilemma

Your computer is an island surrounded by 15 meters of Wi-Fi airwaves. Without an exit door, your computer is trapped:
- If your operating system did not have a configured gateway, calling `fetch("https://github.com")` would fail immediately with:
  `Network is unreachable` or `No route to host`.
- The computer knows who it wants to reach (`140.82.112.4`), but it has no physical path to reach it.

Every device that connects to any network—your laptop, your phone, an EC2 virtual machine in AWS, or a container in Docker—must have an exit door designated for traffic heading outside.

---

## 3. The Mental Model: The All-In-One Living Room Box

People often point to the plastic box with antennas in their living room and call it "the Wi-Fi" or "the router".
In networking reality, that box houses **five completely distinct network roles in a single physical chassis**:

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                    THE ALL-IN-ONE HOME NETWORK BOX                     │
 │                                                                        │
 │  1. Wi-Fi Access Point (AP)  ── Antennas translating radio waves to bits│
 │  2. Network Switch           ── Layer 2 hardware bridging local LAN    │
 │  3. Router Engine & NAT      ── Layer 3 gateway connecting LAN to WAN  │
 │  4. DHCP Server              ── Automatically leases IPs & config      │
 │  5. DNS Forwarder            ── Relays domain lookups to upstream DNS  │
 └────────────────────────────────────────────────────────────────────────┘
```

The IP address printed on the physical sticker on the bottom of your router (e.g., `192.168.0.1` or `192.168.1.1` along with `admin/admin`):
- **IS your Default Gateway** (the exit door for remote packets).
- **IS your DHCP Server** (the machine that leased your IP at boot).
- **IS your local DNS Resolver** (which your browser queries).
- **IS the Web Server** you visit in Chrome (`http://192.168.0.1`) to manage your Wi-Fi settings.

The router has **two faces**:
1. **The LAN interface (`192.168.0.1`):** Sits inside your room on your local subnet. Your laptop can reach it directly over Wi-Fi.
2. **The WAN interface (Public IP):** Connects to your ISP's fiber-optic cable running out into the city.

Because the router sits on *both* networks simultaneously, it acts as the bridge.

---

## 4. Deep Dive & Mechanics

### 4.1 The Kernel Routing Table: How the OS Evaluates Outbound Packets
A common beginner misconception is that the routing table keeps a history of recently visited websites. **It does not.** (Domain names are cached by DNS; recent MACs are cached by ARP).

The **Routing Table** is an in-memory kernel lookup table containing **rules about network interfaces and destination subnets**.

Here is the real routing table from your laptop (from `route print -4`):

```text
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.0.1    192.168.0.102     45  ◄ Row 1: Default Route
      192.168.0.0    255.255.255.0         On-link     192.168.0.102    301  ◄ Row 2: Local Wi-Fi
    192.168.0.102  255.255.255.255         On-link     192.168.0.102    301  ◄ Row 3: My Own IP
     172.19.160.0    255.255.240.0         On-link      172.19.160.1   5256  ◄ Row 4: WSL Adapter
===========================================================================
```

### 4.2 How the Kernel Evaluates Each Row
The kernel does **not** make up a subnet mask for an IP on the fly. **It uses the netmask specified in each row of the table!**

For any destination IP `X`, the kernel tests:
```text
Does (X & row.Netmask) == row.Network_Destination?
```

Let's test an outbound packet to **GitHub (`140.82.112.4`)**:
1. **Row 3:** `140.82.112.4 & 255.255.255.255` = `140.82.112.4` != `192.168.0.102` ❌
2. **Row 4:** `140.82.112.4 & 255.255.240.0` != `172.19.160.0` ❌
3. **Row 2:** `140.82.112.4 & 255.255.255.0` = `140.82.112.0` != `192.168.0.0` ❌
4. **Row 1:** `140.82.112.4 & 0.0.0.0` = `0.0.0.0` == `0.0.0.0` ✅ **MATCH!**

---

### 4.3 Why `0.0.0.0/0` Matches the Entire Internet
Recall what bitwise AND does:
Any 32-bit number `AND 0.0.0.0` equals `0.0.0.0`.
Because the netmask requires **0 matching bits**, **every single IPv4 address on Earth matches `0.0.0.0/0`!**
It is the universal wildcard, the catch-all. And Row 1 specifies:
`Gateway: 192.168.0.1`!

---

### 4.4 Longest Prefix Match (LPM): What If Multiple Rows Match?
What happens if you ping your roommate at `192.168.0.50`?
- Row 2 (`/24`) matches: `192.168.0.50 & 255.255.255.0 == 192.168.0.0` ✅
- Row 1 (`/0`) **also matches**: `192.168.0.50 & 0.0.0.0 == 0.0.0.0` ✅

Which rule wins?
**Longest Prefix Match (LPM): The rule with the longest prefix (most 1-bits in the netmask) ALWAYS wins.**
- Row 2 has **24 bits** (`/24`).
- Row 1 has **0 bits** (`/0`).
- Since `24 > 0`, **Row 2 wins!** The packet stays On-link and is never sent to the gateway.

---

### 4.5 🟡 The Big Reality Check: Destination IP Does NOT Change!
When your laptop hands the packet to the Default Gateway (`192.168.0.1`), **it does NOT rewrite the destination IP address**.
- `Source IP:` `192.168.0.102`
- `Destination IP:` `140.82.112.4` (GitHub)

The destination IP remains `140.82.112.4` across the entire journey. If your laptop changed the destination IP to `192.168.0.1`, the router would think the packet was meant for the router itself and discard it!
You hand the packet to the router saying: *"Deliver this packet to GitHub. I cannot reach GitHub directly, but you know the way."*

---

### 4.6 Does Every Bit Pass Through Physical Hardware?
When your browser makes an HTTP request, it feels like data moves software-to-software. In reality, **every single byte must traverse physical hardware**:

```text
 Browser (User-space code)
    │ System call: socket.send()
    ▼
 OS Kernel (TCP chops into segments; IP wraps in packet)
    ▼
 Device Driver (MediaTek Wi-Fi driver)
    │ PCIe bus transfer
    ▼
 Physical Network Interface Card (MediaTek MT7921 NIC)
    │ Oscillates radio transmitter at 2.4 / 5 GHz
    ▼
 The Air (Electromagnetic radio waves) ──► Wi-Fi Router
```

*(The only exception is `localhost` / `127.0.0.1`, where the kernel short-circuits the packet inside RAM and never touches the physical NIC).*

---

## 5. Hands-On & Developer Lab

### Lab A: Inspecting the Active Routes
Run in PowerShell:
```powershell
route print -4
```
Locate the first row under `Active Routes`:
```text
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.0.1    192.168.0.102     45
```
Notice:
- `Interface: 192.168.0.102` (your physical Wi-Fi card).
- `Metric: 45` (the routing priority). If you plug in an Ethernet cable with metric 25, the kernel automatically routes Internet traffic over the faster Ethernet interface.

---

### Lab B: Proving the Gateway is Hop 1
Run `tracert` without DNS lookups:
```powershell
tracert -d -h 3 8.8.8.8
```
Real output from your machine:
```text
Tracing route to 8.8.8.8 over a maximum of 3 hops

  1    <1 ms    <1 ms    <1 ms  192.168.0.1 
  2     2 ms     1 ms     1 ms  10.115.0.1 
  3     6 ms     4 ms    10 ms  172.23.6.121 
```
- **Hop 1 is `192.168.0.1` in `<1 ms`:** It is your Default Gateway sitting right across the room over Wi-Fi.
- **Hop 2 (`10.115.0.1`):** Your ISP's neighborhood aggregation router miles away across optical fiber.

---

## 6. Pitfalls & Production Reality

* **Multiple Default Gateways:** If you are connected to Wi-Fi and Ethernet simultaneously, your OS table lists two `0.0.0.0/0` entries. The OS uses the route with the lower **Metric**.
* **VPN Route Takeover:** When you connect to a corporate VPN (or WireGuard/Tailscale), the VPN software adds a new `0.0.0.0/0` route pointing to the virtual VPN adapter with a very low metric (e.g. `10`), hijacking all default traffic into the encrypted tunnel!
* **Cloud VPC Gateways:** In AWS or Google Cloud, every VPC subnet automatically receives a default gateway at `.1` (e.g., `10.0.1.1`). If you delete the `0.0.0.0/0 -> Internet Gateway` route from your AWS Route Table, your EC2 instance instantly loses all Internet access.

---

## 🧠 The Moral of the Story (One-Look Mindmap)

> **The Core Question:**
> *Target `203.0.113.10` is off-link. How does the kernel routing table select `192.168.0.1`, and why does Dst IP stay unchanged?*

```text
                        THE 30-SECOND MENTAL WALKTHROUGH

 1. THE ROUTING TABLE: An in-memory decision table consulted for EVERY outgoing packet.
                                           │
                                           ▼
 2. THE CATCH-ALL:    Row `Destination: 0.0.0.0, Netmask: 0.0.0.0` matches EVERY IPv4
                      address on Earth because zero matching bits are required.
                      Next Hop = Default Gateway (`192.168.0.1`).
                                           │
                                           ▼
 3. LONGEST PREFIX:   Longest Prefix Match (LPM) rule: If a specific local `/24` route
                      matches, it always beats the general `/0` default route (24 > 0).
                                           │
                                           ▼
 4. THE GOLDEN RULE:  The packet leaves with:
                      • Source IP:      192.168.0.108  (You)
                      • Destination IP: 203.0.113.10   (Google/Server - NEVER rewritten to gateway!)
                      The gateway's IP is ONLY used to find who receives the local frame.
                                           │
                                           ▼
 5. THE CLIFFHANGER:  We have our IP, mask, and gateway. Who gave our computer these numbers
                      at boot, and how did we ask without having an address?
```

---

## 7. Close the Loop

* **Revisit Log line:**
  `2026-10-22 | Default Gateway & Routing Table | Step 4 uses the kernel routing table and Longest Prefix Match (LPM). If no specific local subnet matches, the default route (0.0.0.0/0) forwards the packet to the Default Gateway (192.168.0.1). The destination IP remains the remote server.`
* **Bridge forward:** We now know our packet must be handed to `192.168.0.1`. But how did our laptop learn its own IP, mask, gateway, and DNS in the first place?
  → [Chapter 04: DHCP & Who Gave Me These Numbers?](04-dhcp.md).
