# Session 1.3: The Number DNS Gave Us (IP Address and CIDR)

> **Act 1 · Step 2 of the journey (the answer's second half)** · [Back to the map](../notes/00-foundations/02-request-lifecycle.md)
> **Time:** about 1.5 hours (reading ~35 min, labs and build ~35 min, videos optional ~15 min: you've watched them)
> **By the end you can:** read any IPv4 address as four 8-bit parts and as one 32-bit number; split an address with a `/X` prefix into its network part and host part, and say how many addresses that network holds; tell private, public and loopback addresses apart at a glance (including the `172.x` trap); and recognize an IPv6 address when DNS hands you one.

---

## 🗺️ Where We Are in the Story

```text
   1. WRITE THE MESSAGE        ✅ Session 1.1
 ► 2. FIND THE ADDRESS (DNS)   ✅ Session 1.2 found it · today: what IS it?
   3. OPEN A CONNECTION
   4. LOCAL OR REMOTE?         ← next act uses today's idea
   5. NEXT PHYSICAL HOP
   6. CROSS THE PLANET
   7. MAKE IT PRIVATE
   8. SEND, REPLY, UNWRAP
```

**Last time** (Session 1.2), DNS turned `github.com` into **`20.205.243.166`**, and `example.com` into two of those plus two long ones like `2606:4700:10::6814:179a`.

**Today** we open that number up: why four parts, why never above 255, how one number can say *which network* and *which machine*, and why your own laptop's number (`192.168.0.102`) can't be used from outside your home.

**We stop** with a question: your laptop holds `192.168.0.102/24` and wants to reach `20.205.243.166`. Is that machine in your room or not, and how does the OS *check*? That check is Act 2.

> **How to read this lesson.** Boxes marked 🔵 **Later** are words that belong to a later act: read them, note the act number, move on. 🟡 boxes are **reality checks**: where videos simplify and production differs.

---

## ⏪ Warm-up (2 min)

You just finished the DNS recall, so only one question: DNS gave `github.com` an `A` record and `example.com` both `A` and `AAAA` records. What's the difference between the two record types?

<details>
<summary><b>Answer</b></summary>

`A` holds an IPv4 address (`20.205.243.166`), `AAAA` holds an IPv6 address (`2606:4700:10::6814:179a`). Today explains both formats, mostly the first.

</details>

---

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

## 🔵 Parking Lot: Words You'll Hear, and Where They Live

| You'll hear... | What it is (one line) | Studied in |
|---|---|---|
| **Subnet mask** (`255.255.255.0`) | The prefix written as an address; the OS uses it to compare networks | Session 2.0 (next) |
| **Default gateway** | The router your laptop hands remote packets to | Session 2.1 |
| **DHCP** | How the router hands your laptop its address when you join Wi-Fi | Session 2.2 |
| **`169.254.x.x`** (link-local / APIPA) | The address a device gives itself when no one handed it one | Session 2.2 |
| **Broadcast address** | The last address of a block, meaning "everyone on this network" | Sessions 2.2, 3.1 |
| **MAC address** | The hardware address of a network card | Act 3 |
| **NAT** | How your router lets many private addresses share one public one | Session 5.4 |
| **Routing, routers forwarding by prefix** | How the network part steers packets across the planet | Act 5 |
| **IPv6 details** (`fe80::`, `::` rules, header) | The full IPv6 story | Session 5.1 |
| **Subnet, VPC** | A network carved out of a bigger block (home, office, AWS) | Session 2.0, Act 8 |
| **WAN** | A network spanning a large area (ISPs, the Internet) | Act 5 |
| **Address classes (A, B, C)** | The pre-1993 fixed way of splitting addresses | History only (🟡 box in Part 5) |

---

## Part 1: The Problem, a Number That Says *Where*

DNS gave us `20.205.243.166`. Why not just give every machine a serial number: device #1, device #2, ..., device #4,000,000,000?

Picture a router in Dhaka holding a packet for "device #3,892,104,112". Which cable should it use? A serial number says nothing about where the device is. Every router on the planet would need a table of **every device on Earth**, updated every time a phone joins a café's Wi-Fi. Impossible.

Phone numbers solved this long ago. `+880 2 ...`: `880` is Bangladesh, `2` is Dhaka, the rest is one subscriber. An exchange in London doesn't know your number. It knows "`+880` → send toward Bangladesh", and Bangladesh's exchanges handle the rest.

**An IP address works the same way: its left part says which network, its right part says which machine in that network.** Here's the real thing for the number from last session (asked on 2026-10-19 from the public registry that records who owns which addresses):

```text
20.205.243.166  is inside the block  20.192.0.0 – 20.255.255.255
owner: Microsoft Corporation          (GitHub belongs to Microsoft)
```

So a router far away doesn't need to know `20.205.243.166`. It needs one line: "anything starting `20.192` to `20.255` → toward Microsoft." That's the whole trick, and the rest of today is how a number carries those two parts.

---

## Part 2: Read the Number: Four Octets

`20.205.243.166` is four numbers with dots between them. This way of writing it is the **dotted quad**. Each of the four numbers is an **octet**.

Why does no part ever go above 255? Because each part is **8 bits**, and 8 bits can only count from `00000000` (0) to `11111111` (255). That's also where the name comes from: *octet* = a group of eight.

Here is last session's number, part by part (from today's build script):

```text
Octets  :  20 = 00010100   205 = 11001101   243 = 11110011   166 = 10100110
32 bits : 00010100 11001101 11110011 10100110
```

So `192.168.1.256` is not an address. There is no way to fit 256 into 8 bits. An interview question loves this one.

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

All eight on: 128+64+32+16+8+4+2+1 = **255**, the maximum. You'll use this ruler for real in Session 2.0.

</details>

---

## Part 3: It's Really One Number

The dots are for humans. The computer stores an IPv4 address as **one 32-bit number** (4 octets × 8 bits = 32 bits = 4 bytes). The dotted quad is just a readable way to write it, the same way `0xFF` and `255` are the same number.

You can prove it on your own machine. Your router is `192.168.0.1`. As one 32-bit number, that's `3232235521`. Ask `ping` to reach that *number* (run 2026-10-19):

```text
PS> ping -n 2 3232235521

Pinging 192.168.0.1 with 32 bytes of data:          ← ping turned the number back into a dotted quad
Reply from 192.168.0.1: bytes=32 time=1ms TTL=64
Reply from 192.168.0.1: bytes=32 time=3ms TTL=64
```

And GitHub, by number: `ping -n 1 349041574` → `Pinging 20.205.243.166 ... time=66ms`.

**How many addresses exist?** 32 bits give 2^32 = **4,294,967,296**, about 4.3 billion. That sounds like a lot, until you count phones, laptops, servers, TVs and cameras for 8 billion people. Keep that shortage in mind; it explains Part 6.

**Developer connection.** Databases often store IPv4 as an unsigned 32-bit integer (MySQL even has `INET_ATON()` / `INET_NTOA()` to convert), and PostgreSQL has a dedicated `inet` type. Sorting, range checks ("is this IP in our office block?") and rate limiters all work on the number, not on the text.

---

## Part 4: Network Part and Host Part, on Your Own Wi-Fi

Here is your laptop, from `ipconfig` (Lab A):

```text
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.0.102
```

And the router: `192.168.0.1`. Your phone on the same Wi-Fi probably has something like `192.168.0.10x` too. What do they share? The first three octets, `192.168.0`. What differs? Only the last.

- `192.168.0` = the **network part**: "the network in Rony's home".
- `102` = the **host part**: "this laptop, inside that network".

All the devices joined to one router form a **network** (a **LAN**, local area network), and each device in it is a **host**. Hosts on the same LAN can reach each other directly, even with the Internet cable unplugged.

Where exactly is the line between the two parts? The address alone doesn't say. That's what the **prefix** `/X` is for: *the first X bits are the network part*. Windows shows it in Lab B: your Wi-Fi is **`192.168.0.102/24`**.

```text
/24: the first 24 bits name the NETWORK, the last 8 name the HOST
  network bits | host bits : 110000001010100000000000 | 01100110
                              192      168      0        102
```

24 bits = exactly 3 octets, so the line falls on a dot. Easy to read: `192.168.0` network, `.102` host.

**How big is your network?** 8 host bits → 2^8 = **256 addresses**, `192.168.0.0` to `192.168.0.255`:

```text
  host bits all 0  -> 192.168.0.0      (the network's own name: the network address)
  host bits all 1  -> 192.168.0.255    (the last address in the block)
```

Both ends are reserved: `.0` *names* the network (that's what `192.168.0.0/24` means), and `.255` is a special "everyone on this network" address (🔵 Sessions 2.2, 3.1). That leaves **254** addresses for real devices: `.1` (the router) through `.254`.

> 🟡 **Reality check:** video C4 says a `/24` can hold 256 hosts. It can hold 256 *addresses*; only **254** can go to devices. And in AWS, a `/24` subnet gives you **251**, because AWS also reserves `.1`, `.2` and `.3` for its own router, DNS and future use.

---

## Part 5: When the Line Doesn't Fall on a Dot (CIDR)

Your laptop has a second adapter you may never have noticed: the virtual network Windows made for **WSL** (Linux inside Windows). From Lab B:

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

Notice the third octet runs from 160 to 175: the left 4 bits of it (`1010`) are locked, the right 4 are free (`0000` to `1111` = 0 to 15, so 160 to 175).

**This freedom is the "C" in CIDR: Classless.** Writing `address/X` with the line at *any* bit is called **CIDR notation**, and it's what you'll type in cloud consoles, firewall rules and Docker configs.

> 🟡 **Reality check (history):** before 1993, the line could only fall on a dot. Addresses came in fixed **classes**: Class A (`/8`, 16.7 million addresses), Class B (`/16`, 65,536), Class C (`/24`, 256). A company needing 300 addresses got a Class B and wasted 65,000. CIDR ended that. You'll still hear "Class C network" for a `/24`: it's an old name, not a rule.

**The prefixes you'll actually meet as a developer:**

| Prefix | Host bits | Addresses | Where you see it |
|---|---|---|---|
| `/32` | 0 | 1 | One exact address: "allow only my office IP `203.0.113.7/32`" |
| `/24` | 8 | 256 | Home Wi-Fi, one AWS subnet (`10.0.1.0/24`) |
| `/20` | 12 | 4,096 | Your WSL network; default AWS subnets |
| `/16` | 16 | 65,536 | An AWS VPC (`10.0.0.0/16`), Docker's default bridge (`172.17.0.0/16`) |
| `/8` | 24 | 16,777,216 | `10.0.0.0/8`, `127.0.0.0/8` |
| `/0` | 32 | all 4.3 billion | `0.0.0.0/0` = **any address at all** |

**Rule of thumb:** a bigger number after the slash = a *smaller* network. Each step of 1 halves or doubles the size.

> 🟡 **The `0.0.0.0/0` blunder:** a cloud firewall rule "allow port 5432 from `0.0.0.0/0`" means *allow the entire Internet to knock on your database*. Scanners can sweep all 4.3 billion IPv4 addresses in under an hour, so an exposed database gets found and attacked fast. Use `/32` for your own IP instead.

---

## Part 6: Private, Public, and "Myself"

**The problem.** 4.3 billion addresses (Part 3) aren't enough for every device on Earth. And most devices (your phone, your smart TV) never need to be *reachable* from the Internet; they only reach out.

**The fix:** three blocks were set aside as **private**. Anyone may use them inside their own network, and millions of homes use the very same numbers at once:

| Private block | Range | Size | Where you see it |
|---|---|---|---|
| `10.0.0.0/8` | `10.0.0.0` – `10.255.255.255` | 16.7 million | Companies, AWS/GCP VPCs |
| `172.16.0.0/12` | `172.16.0.0` – `172.31.255.255` | 1 million | Docker, **your WSL** (`172.19.160.1`) |
| `192.168.0.0/16` | `192.168.0.0` – `192.168.255.255` | 65,536 | Home routers, **your laptop** (`192.168.0.102`) |

A private address is only meaningful *inside its own network*. Your neighbour's laptop may also be `192.168.0.102`; there's no clash, because neither address ever appears on the open Internet. Internet routers don't carry traffic for private addresses at all. Everything else (apart from a few special blocks) is **public**: unique worldwide, like GitHub's `20.205.243.166`.

> 🟡 **The `172` trap:** in Session 1.2 Lab E, DNS gave `example.com` the address `172.66.147.243`. Private? **No.** The private block is only `172.16` to `172.31`. `172.66` is a public Cloudflare address. The build script confirms it:
> ```text
> 172.19.160.1    → private  [inside 172.16.0.0/12]
> 172.66.147.243  → public
> ```

**And "myself": loopback.** `127.0.0.1` (the name `localhost`) means *this same machine*. When you run `npm run dev` and open `http://localhost:3000`, the request never leaves your laptop. The whole block `127.0.0.0/8` is reserved for this; your laptop lists it as `127.0.0.1/8` (Lab B).

> 🔵 **Later (Session 5.4, NAT):** if your laptop is `192.168.0.102` and that number is meaningless on the Internet, how did GitHub's reply find you in Session 1.2? Your router swaps in its own public address on the way out and remembers the swap. That's NAT. For now: *private inside, one public address outside*.

> 🔵 **Later (Session 2.2):** Lab B shows a few `169.254.x.x` addresses on adapters that aren't connected. A device gives itself one of those when nobody hands it an address. Skip until DHCP.

---

## Part 7: The Other Format, IPv6 (Just Recognize It)

DNS also gave `example.com` `2606:4700:10::6814:179a` (its `AAAA` record). That's **IPv6**, built because 4.3 billion wasn't enough.

```text
IPv4:  20.205.243.166              32 bits, 4 decimal parts, dots
IPv6:  2606:4700:10::6814:179a     128 bits, 8 hex parts of 16 bits, colons
                    ↑ "::" = a run of all-zero parts, written once to save space
```

128 bits is 2^128 addresses, more than enough to give every device a public address with no sharing. The same idea holds: left part = network, right part = host (`/64` is the usual home prefix).

On your laptop today, `ipconfig` shows only `fe80::...` on Wi-Fi: a local-only IPv6 address (🔵 Session 5.1), not a public one. So your current network reaches the Internet over **IPv4**. That's why this course uses IPv4 for its examples.

> 🔵 **Later (Session 5.1):** IPv6 writing rules, `fe80::`, and how IPv4 and IPv6 live side by side.

---

## Part 8: Watch It With Your Own Eyes (Labs)

All commands were run on your laptop on 2026-10-19. Run them yourself; your numbers should match unless your router handed you a different address today.

### Lab A: `ipconfig`, your addresses

```powershell
ipconfig
```

```text
Wireless LAN adapter Wi-Fi:
   Link-local IPv6 Address . . . . . : fe80::d9c1:fd32:d3ce:5d%4   ← IPv6, local only (Part 7)
   IPv4 Address. . . . . . . . . . . : 192.168.0.102               ← YOU: private (192.168.0.0/16)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0               ← 🔵 Session 2.0: the /24, written as an address
   Default Gateway . . . . . . . . . : 192.168.0.1                 ← 🔵 Session 2.1: your router

Ethernet adapter vEthernet (WSL (Hyper-V firewall)):
   IPv4 Address. . . . . . . . . . . : 172.19.160.1                ← WSL's virtual network: private (172.16.0.0/12)
   Subnet Mask . . . . . . . . . . . : 255.255.240.0               ← 🔵 the /20

Ethernet adapter Ethernet:
   Media State . . . . . . . . . . . : Media disconnected          ← no cable plugged in: no address
```

**Task:** your laptop and the router share which octets? Which octet is "you"?

### Lab B: the prefix, written as `/X`

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Select-Object IPAddress, PrefixLength, InterfaceAlias
```

```text
IPAddress       PrefixLength InterfaceAlias
---------       ------------ --------------
172.19.160.1              20 vEthernet (WSL (Hyper-V firewall))   ← /20: line inside octet 3 (Part 5)
169.254.163.53            16 Ethernet                             ← 🔵 self-assigned, Session 2.2
169.254.23.122            16 Local Area Connection* 10            ← 🔵 same
169.254.110.171           16 Local Area Connection* 8             ← 🔵 same
192.168.0.102             24 Wi-Fi                                ← /24: 192.168.0 | 102
127.0.0.1                  8 Loopback Pseudo-Interface 1          ← localhost (Part 6)
```

**Tasks:**
1. For each row, say private, public, loopback or "🔵 later". *(None is public. That's normal: your laptop holds no public address at all.)*
2. How many addresses are in your Wi-Fi network? In the WSL network? *(256 and 4,096.)*

### Lab C: an IP is one number

```powershell
ping -n 2 3232235521
ping -n 1 349041574
```

Predict the dotted quad each one becomes, then check the `Pinging ...` line. *(Answers in Part 3.)*

---

## Part 9: Build: Look Inside Any Address

**The script:** [hands-on-lab/act1-1.3-ip-explorer.py](../hands-on-lab/act1-1.3-ip-explorer.py). In plain words:
- `to_bits` splits on dots, checks each part is 0–255, and writes each as 8 bits: Part 2's rule as code.
- `int(bits, 2)` reads the 32 bits as **one number**: Part 3.
- With `/X`, it cuts the 32 bits after X characters (network | host), then fills the host bits with all 0s and all 1s to get the first and last address: Parts 4 and 5.
- `kind` compares only the first X bits with each private block: "same network part" means "inside the block". (Act 2 does this same comparison the way your OS does it, with a mask.)
- Given a name (`github.com`), it asks DNS first: today's lesson sitting right after last session's.

**Run it** from the course folder (no arguments = the lesson's examples):

```powershell
python hands-on-lab/act1-1.3-ip-explorer.py
python hands-on-lab/act1-1.3-ip-explorer.py 192.168.0.102/24
```

**Experiments** (predict first, then run):
1. `192.168.1.256` → *refused: "256 is not 0-255: one part has only 8 bits, and 8 bits stop at 255".*
2. `10.0.0.5/8` → *private, inside `10.0.0.0/8`; block `10.0.0.0` to `10.255.255.255`, 16,777,216 addresses.*
3. `172.19.160.1/20` → *network bits `10101100000100111010`, last address `172.19.175.255`, 4,096 addresses.*
4. `wikipedia.org` (or any site) → *DNS, then public.* Then try a `/16` and a `/32` of the same address and watch the block size: 65,536 and 1.

---

## Watch Guide (optional: you've watched both)

| Video | Watch? | Notes |
|---|---|---|
| **C3** IP address structure (4 min) | 🟡 Optional rewatch | Matches Parts 2–3. He says "127.0.1": he means `127.0.0.1` (Part 6). The list of "future topics" (subnet mask, default gateway, MAC, routing) are Acts 2, 3 and 5. |
| **C4** Network, host, CIDR (10 min) | 🟡 Optional rewatch | Matches Parts 4–5. **DHCP** → Session 2.2; **LAN/WAN** → LAN today, WAN Act 5. "256 hosts per network" → really **254** usable (Part 4). "65,000 if I'm not wrong" → exactly 65,536. Where the transcript reads "0.0" and "/6", he means `0.0.0.0/0` and a `/16`. "The network IP helps decide if a device is inside or outside my network" → that decision is Session 2.0. |

---

## Common Confusions

* **"The dots are part of the address."** They're only for humans. The address is one 32-bit number (`ping 3232235521` works).
* **"`/24` means 24 addresses."** It means 24 bits are the *network* part. The addresses come from the *other* 8 bits: 2^8 = 256.
* **"Every address starting with 172 is private."** Only `172.16` to `172.31`. `172.66.147.243` is public.
* **"`192.168.0.102` is my address on the Internet."** It's your address *inside your home*. The Internet sees your router's public address (🔵 Session 5.4).
* **"A bigger `/X` is a bigger network."** The opposite: more network bits, fewer host bits, fewer addresses.

---

## Active Recall

1. A form lets users type an IPv4 address. Name two quick checks that reject garbage like `10.0.300.1` or `10.0.1`, and explain the reason behind the first.
2. Your AWS VPC is `10.0.0.0/16`. Which part of every address in it is fixed, how many addresses does it hold, and why would a subnet `10.0.1.0/24` inside it give you 251 usable addresses and not 256?
3. A teammate says, "The API server at `172.31.5.9` is public, I can call it from home." Are they right? What about `172.32.5.9`?
4. Your WSL adapter is `172.19.160.1/20`. Is `172.19.170.4` in the same network? Is `172.19.180.4`? Explain using the bits of the third octet.
5. Why does it help routers that the network part sits on the **left** of every address?

<details>
<summary><b>Answers</b></summary>

1. Exactly 4 parts separated by dots, and each part an integer from 0 to 255. The 0–255 limit is because each part is one octet, 8 bits, and 8 bits stop at 255.
2. The first 16 bits (`10.0`) are fixed; it holds 2^16 = 65,536 addresses. A `/24` has 256 addresses; `.0` names the network and `.255` is the "everyone" address (254 left), and AWS also reserves `.1`, `.2`, `.3` → 251.
3. No: `172.31.5.9` is inside `172.16.0.0/12` (172.16–172.31), so it's private and unreachable from the Internet (it's probably inside an AWS VPC). `172.32.5.9` is outside that block, so it's public.
4. `/20` locks the first 4 bits of the third octet: `1010xxxx`, i.e. 160–175. 170 = `10101010` starts with `1010` → same network. 180 = `10110100` starts with `1011` → different network.
5. A router far away only needs to look at the left bits to know which direction to send a packet (like `+880` for Bangladesh). It can store one line per *network* instead of one per *machine*. (🔵 How routers use this: Act 5.)

</details>

---

## Close the Loop

**Revisit Log line** for the anchor:
`2026-10-19 | IP & CIDR (reworked) | The number DNS returns in step 2 is one 32-bit value written as four octets. Its left X bits (/X) name a network, the rest name a host in it, so routers can work with whole networks. 192.168.x, 10.x, 172.16–31.x are private: reused in every home, never seen on the Internet.`

**The cliffhanger.** You now hold two numbers: `192.168.0.102/24` (you) and `20.205.243.166` (GitHub). Your router `192.168.0.1` is in your network. GitHub, clearly, is not. But your OS can't "see" that the way you just did. It needs a rule it can run in a nanosecond for every packet: *is this destination in my network, or do I hand it to someone else?*

→ **Act 2, Session 2.0: The subnet mask.** The `255.255.255.0` line you skipped in Lab A is that rule.

---

## Previous Versions
