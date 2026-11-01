# IP Addresses and CIDR: The Number DNS Gave Us

> **Zooming into:** Step 2 of the [lifecycle](../00-foundations/02-request-lifecycle.md) (the answer DNS returns) · Act 1
> **Prerequisites:** [DNS Resolution](../04-application-layer/01-dns-resolution.md) (where the number came from)
> **Key Goal:** Read any IPv4 address as four 8-bit parts and as one 32-bit number; split an address with a `/X` prefix into network part and host part and size the network; tell private, public and loopback addresses apart at a glance; recognize IPv6.
> **Lesson:** [lessons/act1-1.3-ip-address.md](../../lessons/act1-1.3-ip-address.md) · **Script:** [hands-on-lab/act1-1.3-ip-explorer.py](../../hands-on-lab/act1-1.3-ip-explorer.py) · **Recall:** [Think it through](../RECALL.md#act-1--step-2-ip-addresses-and-cidr)

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **Bit** | A single 0 or 1. Eight bits make a **byte** |
| **IPv4 address** | A 32-bit number naming one machine's connection to a network, written like `20.205.243.166` |
| **Octet** | One of the four parts of an IPv4 address: 8 bits, so 0 to 255 |
| **Dotted quad** | The usual way to write IPv4: four octets in decimal with dots between them |
| **Host** | Any device that holds an IP address: your laptop, phone, a server, the router itself |
| **Network** | A group of hosts that can reach each other directly, like everything on your home Wi-Fi |
| **LAN** (local area network) | A network in one place: your home, an office floor |
| **Network part / host part** | The left bits of an address say *which network*; the right bits say *which host in it* |
| **Prefix** (`/X`) | How many bits from the left are the network part: `/24` = the first 24 bits |
| **CIDR** (Classless Inter-Domain Routing) | Writing an address or a block as `address/X`, with the line allowed at *any* bit |
| **Network address** | The first address of a block (host bits all 0). It names the network, not a device |
| **Private address** | From three blocks reserved for inside networks (`10.x`, `172.16–31.x`, `192.168.x`). Reused in millions of homes; not reachable from the Internet |
| **Public address** | Unique on the whole Internet; anyone can send to it |
| **Loopback** (`127.0.0.1`, `localhost`) | An address that means "this same machine" |
| **IPv6** | The newer 128-bit address format, written in hex with colons |

---

## 1. The Story So Far

In [DNS Resolution](../04-application-layer/01-dns-resolution.md), the OS asked a resolver for `github.com` and got back **`20.205.243.166`**. For `example.com` it got two numbers like that (`172.66.147.243`, `104.20.23.154`) plus two much longer ones (`2606:4700:10::6814:179a`).

Step 2 of the journey is done: we know where to send the message. But we've been treating that number as an opaque label. Before Act 2 can answer the next question ("is this machine in my room, or outside?"), we need to see what the number is made of: why four parts, why none is ever above 255, and how one number can say both *which network* and *which machine*.

## 2. The Real-World Problem

Why not give every machine a serial number: device #1, device #2, ..., device #4,000,000,000?

Picture a router in Dhaka holding a packet for "device #3,892,104,112". Which cable should it use? A serial number says nothing about *where* the device is. Every router on the planet would need a table of **every device on Earth**, updated every time a phone joins a café's Wi-Fi. Impossible.

So the address itself has to carry location: a part that names a network, which far-away routers can steer by, and a part that names one machine inside it, which only matters once the packet gets there.

## 3. The Mental Model: Phone Numbers

`+880 2 ...`: `880` is Bangladesh, `2` is Dhaka, the rest is one subscriber. An exchange in London doesn't know your number. It knows "`+880` → send toward Bangladesh", and Bangladesh's exchanges handle the rest.

**An IP address works the same way: its left part says which network, its right part says which machine in that network.** Here's the real thing for GitHub's number, asked on 2026-10-19 from the public registry that records who owns which addresses:

```text
20.205.243.166  is inside the block  20.192.0.0 – 20.255.255.255
owner: Microsoft Corporation          (GitHub belongs to Microsoft)
```

A router far away doesn't need to know `20.205.243.166`. It needs one line: "anything from `20.192` to `20.255` → toward Microsoft." The rest of this chapter is how a number carries those two parts.

## 4. Deep Dive & Mechanics

### 4.1 Read the Number: Four Octets

`20.205.243.166` is four numbers with dots between them. This way of writing it is the **dotted quad**, and each of the four numbers is an **octet**.

No part is ever above 255 because each part is **8 bits**, and 8 bits can only count from `00000000` (0) to `11111111` (255). That's where the name comes from: *octet* = a group of eight. GitHub's number, part by part (from the build script):

```text
Octets  :  20 = 00010100   205 = 11001101   243 = 11110011   166 = 10100110
32 bits : 00010100 11001101 11110011 10100110
```

So `192.168.1.256` is not an address: 256 doesn't fit in 8 bits. Interviewers love this one.

<details>
<summary><b>How to turn an octet into bits by hand (the 128-64-32 ruler)</b></summary>

The 8 positions are worth, from left to right:

```text
128  64  32  16   8   4   2   1
```

To write **205**: go left to right; if the value fits in what's left, write 1 and subtract, else write 0.

```text
205 ≥ 128 → 1, left 77
 77 ≥  64 → 1, left 13
 13 ≥  32? no → 0
 13 ≥  16? no → 0
 13 ≥   8 → 1, left 5
  5 ≥   4 → 1, left 1
  1 ≥   2? no → 0
  1 ≥   1 → 1, left 0
205 = 11001101
```

All eight on: 128+64+32+16+8+4+2+1 = **255**, the maximum. The [Subnet Masks](02-subnet-masks-and-switches.md) chapter uses this ruler for real.

</details>

### 4.2 It's Really One Number

The dots are for humans. The computer stores an IPv4 address as **one 32-bit number** (4 octets × 8 bits = 32 bits = 4 bytes). The dotted quad is just a readable way to write it, the same way `0xFF` and `255` are the same number.

Proof, on the student's laptop (2026-10-19). The router is `192.168.0.1`; as one 32-bit number that's `3232235521`. Ask `ping` to reach that *number*:

```text
PS> ping -n 2 3232235521

Pinging 192.168.0.1 with 32 bytes of data:          ← ping turned the number back into a dotted quad
Reply from 192.168.0.1: bytes=32 time=1ms TTL=64
Reply from 192.168.0.1: bytes=32 time=3ms TTL=64
```

And GitHub by number: `ping -n 1 349041574` → `Pinging 20.205.243.166 ... time=66ms`.

**How many addresses exist?** 32 bits give 2^32 = **4,294,967,296**, about 4.3 billion. That sounds like a lot until you count phones, laptops, servers, TVs and cameras for 8 billion people. This shortage explains private addresses (4.6) and IPv6 (4.7).

**Developer connection.** Databases often store IPv4 as an unsigned 32-bit integer (MySQL has `INET_ATON()` / `INET_NTOA()` to convert); PostgreSQL has a dedicated `inet` type. Sorting, range checks ("is this IP in our office block?") and rate limiters all work on the number, not on the text.

### 4.3 Network Part and Host Part, on Your Own Wi-Fi

From `ipconfig` on the student's laptop:

```text
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.0.102
```

The router is `192.168.0.1`; a phone on the same Wi-Fi gets something like `192.168.0.10x`. They share the first three octets, `192.168.0`. Only the last differs.

- `192.168.0` = the **network part**: "the network in Rony's home".
- `102` = the **host part**: "this laptop, inside that network".

All the devices joined to one router form a **network** (a **LAN**, local area network), and each device in it is a **host**. Hosts on the same LAN can reach each other directly, even with the Internet cable unplugged.

Where exactly is the line between the parts? The address alone doesn't say. That's what the **prefix** `/X` is for: *the first X bits are the network part*. Windows reports the Wi-Fi as **`192.168.0.102/24`**:

```text
/24: the first 24 bits name the NETWORK, the last 8 name the HOST
  network bits | host bits : 110000001010100000000000 | 01100110
                              192      168      0        102
```

24 bits = exactly 3 octets, so the line falls on a dot: `192.168.0` network, `.102` host.

**How big is the network?** 8 host bits → 2^8 = **256 addresses**, `192.168.0.0` to `192.168.0.255`. The two ends are found by filling the host bits with all 0s and all 1s:

```text
  host bits all 0  -> 192.168.0.0      (the network's own name: the network address)
  host bits all 1  -> 192.168.0.255    (the last address in the block)
```

Both ends are reserved: `.0` *names* the network (that's what `192.168.0.0/24` means), and `.255` is a special "everyone on this network" address (🔵 Sessions 2.2, 3.1). That leaves **254** addresses for real devices: `.1` (the router) through `.254`.

> 🟡 **Reality check:** video C4 says a `/24` can hold 256 hosts. It holds 256 *addresses*; only **254** can go to devices. In AWS, a `/24` subnet gives you **251**, because AWS also reserves `.1`, `.2` and `.3` for its own router, DNS and future use.

### 4.4 When the Line Doesn't Fall on a Dot (CIDR)

The laptop has a second adapter: the virtual network Windows made for **WSL** (Linux inside Windows).

```text
172.19.160.1    20   vEthernet (WSL (Hyper-V firewall))
```

`/20`. Twenty is not a multiple of 8, so the line falls **inside the third octet**. You can't read it off the dots any more; you have to look at the bits:

```text
172.19.160.1
  10101100 00010011 1010|0000 00000001
  └──── 20 network bits ───┘└─ 12 host bits ─┘

  host bits all 0  -> 172.19.160.0     (the network's name)
  host bits all 1  -> 172.19.175.255   (the last address)
  addresses: 2^12 = 4,096
```

The third octet runs from 160 to 175: its left 4 bits (`1010`) are locked, its right 4 are free (`0000` to `1111` = 0 to 15, so 160 to 175).

**This freedom is the "C" in CIDR: Classless.** Writing `address/X` with the line at *any* bit is **CIDR notation**, and it's what you type in cloud consoles, firewall rules and Docker configs.

#### Who gave WSL that address?

*(Question from the session: "the IP WSL gets, is it assigned by Windows?")*

**Yes. Your router has nothing to do with it.** When WSL 2 starts, Windows builds a small **virtual network** that lives entirely inside your laptop:

1. Windows picks a free private block (here `172.19.160.0/20`).
2. Windows keeps `.1` for its own side, the `vEthernet (WSL)` adapter. `Get-NetIPAddress` lists it with `PrefixOrigin: Manual`, meaning Windows set it itself; no router handed it out.
3. The Linux side gets another address from the same block. Inside Ubuntu (run 2026-10-21):

```text
$ ip -4 addr show eth0; ip route
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    inet 172.19.165.5/20 brd 172.19.175.255 scope global eth0      ← Ubuntu's address: same /20 block
default via 172.19.160.1 dev eth0 proto kernel                     ← "to leave, go through Windows"
172.19.160.0/20 dev eth0 proto kernel scope link src 172.19.165.5 ← "the whole /20 is my local network"
```

Notice `brd 172.19.175.255`: Linux computed the same last address as the script above. And both machines share the network part, so `172.19.160.1` (Windows) and `172.19.165.5` (Ubuntu) are hosts on one tiny network, exactly like your laptop and router on Wi-Fi.

That gives three networks on one laptop: the Wi-Fi LAN (`192.168.0.0/24`, numbered by your router), the WSL network (`172.19.160.0/20`, numbered by Windows), and loopback (`127.0.0.0/8`, inside each machine). Docker Desktop's VM (`docker-desktop` in `wsl -l -v`) runs on the WSL network too.

**Developer consequence:** Windows can pick a different free block after a reboot, so WSL's address changes. Don't hard-code `172.19.x.x` in configs. That's why WSL forwards `localhost` between Windows and Linux for you.

> 🔵 **Later:** "`default via 172.19.160.1`" means Windows is Ubuntu's **default gateway** (Session 2.1). How Ubuntu's private `172.19.x` traffic reaches the Internet through your Wi-Fi is **NAT** (Session 5.4). DHCP, the usual way a device *receives* an address, is Session 2.2.

> 🟡 **Reality check (history):** before 1993, the line could only fall on a dot. Addresses came in fixed **classes**: Class A (`/8`, 16.7 million addresses), Class B (`/16`, 65,536), Class C (`/24`, 256). A company needing 300 addresses got a Class B and wasted 65,000. CIDR ended that. You'll still hear "Class C network" for a `/24`: it's an old name, not a rule.

### 4.5 The Prefixes You'll Actually Meet

| Prefix | Host bits | Addresses | Where you see it |
|---|---|---|---|
| `/32` | 0 | 1 | One exact address: "allow only my office IP `203.0.113.7/32`" |
| `/24` | 8 | 256 | Home Wi-Fi, one AWS subnet (`10.0.1.0/24`) |
| `/20` | 12 | 4,096 | The WSL network; default AWS subnets |
| `/16` | 16 | 65,536 | An AWS VPC (`10.0.0.0/16`), Docker's default bridge (`172.17.0.0/16`) |
| `/8` | 24 | 16,777,216 | `10.0.0.0/8`, `127.0.0.0/8` |
| `/0` | 32 | all 4.3 billion | `0.0.0.0/0` = **any address at all** |

**Rule of thumb:** a bigger number after the slash = a *smaller* network. Each step of 1 halves or doubles the size. The formula is always **addresses = 2^(32 − X)**.

> 🟡 **The `0.0.0.0/0` blunder:** a cloud firewall rule "allow port 5432 from `0.0.0.0/0`" means *let the entire Internet knock on your database*. Scanners can sweep all 4.3 billion IPv4 addresses in under an hour, so an exposed database gets found and attacked fast. Use `/32` for your own IP instead.

### 4.6 Private, Public, and "Myself"

**The problem.** 4.3 billion addresses aren't enough for every device on Earth, and most devices (your phone, your smart TV) never need to be *reachable* from the Internet; they only reach out.

**The fix:** three blocks were set aside as **private**. Anyone may use them inside their own network, and millions of homes use the very same numbers at once:

| Private block | Range | Size | Where you see it |
|---|---|---|---|
| `10.0.0.0/8` | `10.0.0.0` – `10.255.255.255` | 16.7 million | Companies, AWS/GCP VPCs |
| `172.16.0.0/12` | `172.16.0.0` – `172.31.255.255` | 1 million | Docker, **the WSL network** (`172.19.160.1`) |
| `192.168.0.0/16` | `192.168.0.0` – `192.168.255.255` | 65,536 | Home routers, **the laptop** (`192.168.0.102`) |

A private address only means something *inside its own network*. A neighbour's laptop may also be `192.168.0.102`; there's no clash, because neither address ever appears on the open Internet. Internet routers don't carry traffic for private addresses at all. Everything else (apart from a few special blocks) is **public**: unique worldwide, like GitHub's `20.205.243.166`.

> 🟡 **The `172` trap:** DNS gave `example.com` the address `172.66.147.243`. Private? **No.** The private block is only `172.16` to `172.31`; `172.66` is a public Cloudflare address. The build script:
> ```text
> 172.19.160.1    → private  [inside 172.16.0.0/12]
> 172.66.147.243  → public
> ```

**And "myself": loopback.** `127.0.0.1` (the name `localhost`) means *this same machine*. When you run `npm run dev` and open `http://localhost:3000`, the request never leaves your laptop. The whole block `127.0.0.0/8` is reserved for this; Windows lists it as `127.0.0.1/8`.

> 🔵 **Later (Session 5.4, NAT):** if the laptop is `192.168.0.102` and that number is meaningless on the Internet, how did GitHub's reply find it? The router swaps in its own public address on the way out and remembers the swap. For now: *private inside, one public address outside*.

> 🔵 **Later (Session 2.2):** `169.254.x.x` addresses appear on adapters that aren't connected. A device gives itself one when nobody hands it an address.

### 4.7 The Other Format: IPv6 (Recognize It)

DNS also gave `example.com` `2606:4700:10::6814:179a` (its `AAAA` record). That's **IPv6**, built because 4.3 billion wasn't enough.

```text
IPv4:  20.205.243.166              32 bits, 4 decimal parts, dots
IPv6:  2606:4700:10::6814:179a     128 bits, 8 hex parts of 16 bits, colons
                    ↑ "::" = a run of all-zero parts, written once to save space
```

128 bits is 2^128 addresses, enough to give every device a public address with no sharing. The same idea holds: left part = network, right part = host (`/64` is the usual size of one network).

On the student's laptop, `ipconfig` shows only `fe80::...` on Wi-Fi: a local-only IPv6 address (🔵 Session 5.1), not a public one. So this network reaches the Internet over **IPv4**, which is why the course uses IPv4 in its examples.

## 5. Hands-On & Developer Lab

All output below is from the student's laptop (2026-10-19, WSL part 2026-10-21). Full click-by-click steps: [the lesson](../../lessons/act1-1.3-ip-address.md).

| Tool | What it shows | What to look for |
|---|---|---|
| `ipconfig` | Each adapter's IPv4 (and IPv6) address | Wi-Fi `192.168.0.102` shares `192.168.0` with the router `192.168.0.1`; disconnected adapters show `Media disconnected` |
| `Get-NetIPAddress -AddressFamily IPv4 \| Select-Object IPAddress, PrefixLength, InterfaceAlias` | The same addresses with their `/X` | `/24` on Wi-Fi, `/20` on WSL, `/8` on loopback; none of them public |
| `ping <number>` (e.g. `ping 3232235521`) | That an address is one 32-bit number | The `Pinging ...` line converts it back to a dotted quad |
| `wsl -e sh -c "ip -4 addr show eth0; ip route"` | WSL's own address and its way out | The same `/20` as the Windows side; `default via 172.19.160.1` |

```text
PS> Get-NetIPAddress -AddressFamily IPv4 | Select-Object IPAddress, PrefixLength, InterfaceAlias

IPAddress       PrefixLength InterfaceAlias
---------       ------------ --------------
172.19.160.1              20 vEthernet (WSL (Hyper-V firewall))   ← /20: line inside octet 3
169.254.163.53            16 Ethernet                             ← 🔵 self-assigned, Session 2.2
169.254.23.122            16 Local Area Connection* 10            ← 🔵 same
169.254.110.171           16 Local Area Connection* 8             ← 🔵 same
192.168.0.102             24 Wi-Fi                                ← /24: 192.168.0 | 102
127.0.0.1                  8 Loopback Pseudo-Interface 1          ← localhost
```

In `ipconfig`, the `Subnet Mask` line (`255.255.255.0`) is the same `/24` written as an address, and `Default Gateway` is the router; both belong to Act 2.

### Build: look inside any address

[hands-on-lab/act1-1.3-ip-explorer.py](../../hands-on-lab/act1-1.3-ip-explorer.py) does everything above with plain text and bits, no networking library:
- `to_bits` splits on dots, rejects any part outside 0–255, and writes each part as 8 bits (4.1).
- `int(bits, 2)` reads the 32 bits as one number (4.2).
- With `/X`, it cuts the bits after X characters (network | host) and fills the host bits with all 0s and all 1s for the first and last address (4.3, 4.4).
- `kind` compares only the first X bits with each private/special block (4.6). Act 2 does the same comparison the way the OS does it, with a mask.
- Given a name, it asks DNS first, so the chapter sits right after the DNS chapter.

```powershell
python hands-on-lab/act1-1.3-ip-explorer.py                     # the examples from this chapter
python hands-on-lab/act1-1.3-ip-explorer.py 172.19.160.1/20     # any address, with or without /X
python hands-on-lab/act1-1.3-ip-explorer.py github.com          # a name: DNS first
```

Try `192.168.1.256` (refused: "8 bits stop at 255"), `10.0.0.5/8` (private, 16,777,216 addresses), and the same address as `/16` and `/32` (65,536 and 1).

### Developer impact

- **Cloud:** a VPC is a private block (`10.0.0.0/16`) cut into smaller `/24` or `/20` subnets. Overlapping blocks between two VPCs break peering, so choose them deliberately.
- **Firewalls / security groups:** `/32` = one address, `0.0.0.0/0` = everyone.
- **Docker / WSL:** containers and WSL get private `172.x` addresses from a virtual network on your machine; they change, so use names or `localhost` forwarding.
- **Validation and storage:** 4 parts, each 0–255; store as a 32-bit integer or a database `inet` type.

## 6. Pitfalls & Production Reality

* **"The dots are part of the address."** They're only for humans. The address is one 32-bit number (`ping 3232235521` works).
* **"`/24` means 24 addresses."** It means 24 bits are the *network* part. The addresses come from the *other* 8 bits: 2^8 = 256.
* **"A `/24` holds 256 devices."** 256 addresses, 254 devices (251 in AWS).
* **"Every address starting with 172 is private."** Only `172.16` to `172.31`. `172.66.147.243` is public.
* **"`192.168.0.102` is my address on the Internet."** It's the address *inside the home*. The Internet sees the router's public address (🔵 Session 5.4).
* **"A bigger `/X` is a bigger network."** The opposite: more network bits, fewer host bits, fewer addresses.
* **Hard-coding a WSL or Docker IP.** They're handed out by a virtual network on your machine and change after restarts.

🔵 **Later:** subnet mask and the local-or-remote decision (Session 2.0), default gateway (2.1), DHCP and `169.254.x.x` (2.2), broadcast and MAC addresses (Act 3), routers forwarding by prefix (Act 5), NAT (5.4), IPv6 details (5.1).

## 🧠 The Moral of the Story (One-Look Mindmap)

> **The Core Question:**
> *DNS gave us `203.0.113.10`. Why isn't an IP address just a random serial number, and how does it encode location?*

```text
                        THE 30-SECOND MENTAL WALKTHROUGH

 1. THE HIERARCHY:    Like a country code and phone number (`+880 2 ...`), an IP address
                      is split into two halves: Network Part (left) and Host Part (right).
                                           │
                                           ▼
 2. 32 BITS:          An IPv4 address is one 32-bit integer, written as four 8-bit octets
                      (0–255) separated by dots purely for human readability.
                                           │
                                           ▼
 3. CIDR PREFIX (/X): The `/X` specifies how many bits from the left belong to the Network:
                      • `/24`: 24 network bits, 8 host bits (2^8 = 256 addresses).
                      • Larger `/X` = MORE network bits, FEWER host addresses!
                                           │
                                           ▼
 4. SPECIAL BLOCKS:   • Loopback: `127.0.0.1` (stays inside your own RAM; skips physical NIC).
                      • Private:  `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` (reused in homes/VPCs).
                      • Public:   Globally unique numbers routed across the open Internet.
                                           │
                                           ▼
 5. THE CLIFFHANGER:  You hold `192.168.0.108/24` and destination `203.0.113.10`.
                      How does your OS mathematically decide if the target is in your room?
```

---

## 7. Close the Loop

* **Revisit Log line** (added to the anchor): `2026-10-21 | IP & CIDR | The number DNS returns in step 2 is one 32-bit value written as four octets. Its left X bits (/X) name a network, the rest name a host in it, so routers can work with whole networks. 10.x, 172.16–31.x and 192.168.x are private: reused in every home, never seen on the Internet.`
* **Bridge forward:** you hold `192.168.0.102/24` (you) and `20.205.243.166` (GitHub). Your router `192.168.0.1` is in your network; GitHub clearly isn't. But the OS can't "see" that the way you just did. It needs a rule it can run in a nanosecond for every packet: *is this destination in my network, or do I hand it to someone else?* The `255.255.255.0` line in `ipconfig` is that rule → [Subnet Masks](02-subnet-masks-and-switches.md) (Act 2, Session 2.0).
