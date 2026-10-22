# Recall: Think It Through

The chapters are for learning; this page is for **testing yourself**. Each section has the questions that force you to rebuild a whole chapter in your head: predict, explain why, diagnose a failure, apply it to your own setup. Answer out loud or on paper **before** opening the answers. If you can't, re-read the linked chapter.

A section is added each time a chapter is written (see "Note Rules" in [AGENTS.md](../AGENTS.md)).

---

## Act 1 · Step 1: HTTP Basics

Chapter: [HTTP Basics](04-application-layer/02-http-basics.md)

1. Write, from memory, the full request your browser sends for `fetch("https://shop.com/cart?page=2")`: request line, the one required header, and how the receiver knows the headers are over.
2. A body is `{"city":"ঢাকা"}`. Is its `Content-Length` equal to its number of characters? Explain what happens between the text and the network.
3. HTTP remembers nothing. Show, with the actual header lines, how you stay logged in across 10 requests (a) with cookies and (b) with a bearer token. Who adds each line?
4. Your backend uses cookie auth. The web app works, but the mobile app gets `401` on every request. Diagnose it.
5. You delete the `Host:` line from a hand-written request and get `400 Bad Request`. Why does the server need that line if it already received the message?
6. In `curl -v` output, which lines did you send, which came from the server, and which were curl describing other steps of the journey?

<details>
<summary><b>Answers</b></summary>

1. `GET /cart?page=2 HTTP/1.1`, then `Host: shop.com`, then an empty line (the bytes `13 10` twice in a row end the headers). The `https` part means the message gets encrypted first (Act 6).
2. No. Text is turned into bytes before sending (UTF-8 here), and `Content-Length` counts bytes. Each Bengali letter takes 3 bytes, so the byte count is larger than the character count.
3. (a) The login response has `Set-Cookie: session=...`; the **browser** stores it and adds `Cookie: session=...` to every later request to that site. (b) **Your code** stores the token after login and adds `Authorization: Bearer <token>` to every request.
4. Nothing attaches cookies automatically in a mobile app (it isn't a browser), so every request arrives without proof. The app must store a token and send it itself, or the backend must accept bearer tokens.
5. One server (one address) often hosts many sites. `Host` tells it which site you meant; without it, an HTTP/1.1 request is incomplete.
6. `>` lines: your request. `<` lines: the response. `*` lines: curl's notes about other steps (DNS "resolved", "Connected"), which belong to later sessions.

</details>

---

## Act 1 · Step 2: DNS Resolution

Chapter: [DNS Resolution](04-application-layer/01-dns-resolution.md)

1. Nothing is cached anywhere. Walk through resolving `docs.python.org`: every server asked, in order, what each one answers, and which question is recursive vs iterative.
2. In the walk for `rhrony05.me`, the root sent the `.me` servers' names **and** numbers, but the `.me` server sent Cloudflare's names **only**. Explain both decisions.
3. Draw the three jobs behind `rhrony05.me` (registrar, DNS host, web host). For each change below, say where you'd make it: (a) your site moves to a new server, (b) you move all DNS from Cloudflare to Route 53, (c) you add email.
4. You changed an A record 10 minutes ago. Your phone reaches the new server; your laptop still reaches the old one. Explain, and say what you should have done the day before. Then explain why moving name servers for a `.com` domain could take up to two days.
5. Why can't the apex `rhrony05.me` be a CNAME, while `www.rhrony05.me` can? What does Vercel ask you to add for each, and why?
6. In Wireshark you see `Transaction ID: 0x0002`, `Authority RRs: 0`, `Time to live: 77`, `Src Port: 53`. Explain what each tells you about this lookup.
7. Why does DNS use a "postcard" (UDP) and not a connection? What does the client do when a postcard is lost, and when an answer is too big?
8. A user reports `ERR_NAME_NOT_RESOLVED`. Which step of the journey failed, and what are three different possible causes?

<details>
<summary><b>Answers</b></summary>

1. Browser cache, OS cache and hosts file (all miss) → your **resolver** (miss) → a **root server** ("ask the `.org` servers", with their numbers) → a **`.org` TLD server** ("ask python.org's name servers") → **python.org's authoritative server** (the answer, perhaps a CNAME needing its own lookup). Laptop → resolver is **recursive** ("do it all for me"); resolver → each server is **iterative** (each answers only what it knows). The resolver caches everything it learned.
2. Glue (names + numbers) is required only when the name server's name lies **inside** the zone being handed over: `b0.nic.me` is inside `.me`, so finding it would need the `.me` servers themselves, a loop. `odin.ns.cloudflare.com` is under `.com`, so there's no loop; the resolver looks it up separately.
3. Registrar (Namecheap): you own the name; it tells the `.me` servers which name servers hold your records. DNS host (Cloudflare): the authoritative server with your A/MX/TXT records. Web host: the machine serving your site. (a) DNS host: change the A/CNAME record. (b) Registrar: change the name servers. (c) DNS host: add MX (and TXT) records.
4. The laptop (or its resolver/router) still holds the old answer within its TTL; the phone's resolver fetched fresh. The day before: lower the TTL (e.g. to 60), wait out the old TTL, then change the record. Moving name servers changes the **delegation** held by the `.com` servers, whose TTL is 172800 s (2 days); resolvers may keep the old delegation that long. TTL is a request, not a guarantee, so some caches may be slower still.
5. A name with a CNAME can have no other records, and the apex must carry NS and SOA records. `www` has nothing else, so it can be a pure alias. Vercel asks for an **A** record on the apex (a number) and a **CNAME** on `www` (`cname.vercel-dns.com`), so if Vercel's numbers change, `www` follows automatically.
6. `0x0002`: the ticket ID; it matches this answer to the question with the same ID. `Authority RRs: 0`: no referral and no glue; a resolver gave a final answer, not a step of a walk. `Time to live: 77`: the answer may be cached 77 more seconds (more than GitHub's own 60: the resolver applied its own rule). `Src Port: 53`: it came from the DNS program on that server.
7. The question and answer are tiny (28 and 44 bytes); setting up a connection would take longer than the question, before every site visit. Lost → the client re-asks after a timeout. Too big → the server sets the "truncated" flag and the client re-asks over TCP.
8. Step 2 (DNS) found no number. Causes: a typo or a missing record (possibly a cached NXDOMAIN); the resolver is unreachable or dropping questions (like the phone hotspot); the domain's name servers are down or the registration expired.

</details>


---

## Act 1 · Step 2: IP Addresses and CIDR

Chapter: [IP Addresses and CIDR](02-network-layer/01-ip-and-cidr.md)

1. A form lets users type an IPv4 address. Which two checks reject `10.0.300.1` and `10.0.1`, and why is the limit exactly 255?
2. `ping 3232235521` reaches your router. Explain why that works, and how many IPv4 addresses can exist at all.
3. Your Wi-Fi is `192.168.0.102/24`. Which part names the network, which the host, how many addresses does the network hold, which two are reserved and why, and how many devices can join?
4. Your WSL adapter is `172.19.160.1/20`. Is `172.19.170.4` in the same network? Is `172.19.180.4`? Answer with the bits of the third octet, and give the block's first and last address.
5. Who gave WSL its `172.19.x.x` address, and why should you never hard-code it in a config file?
6. A teammate says, "The API server at `172.31.5.9` is public, I can call it from home." Right or wrong? What about `172.32.5.9`, and `172.66.147.243`?
7. Your AWS VPC is `10.0.0.0/16`. How many addresses, why does a `/24` subnet inside it give 251 usable ones, and what goes wrong with a security group rule "port 5432 from `0.0.0.0/0`"?
8. Why does it help routers that the network part sits on the **left** of every address? Use GitHub's `20.205.243.166` and its owner's block in your answer.

<details>
<summary><b>Answers</b></summary>

1. Exactly 4 parts separated by dots, and each part a whole number from 0 to 255. Each part is one octet, 8 bits, and 8 bits stop at `11111111` = 255.
2. The dotted quad is only a human way to write one 32-bit number; `3232235521` *is* `192.168.0.1`, and `ping` converts it back. 32 bits → 2^32 = 4,294,967,296 addresses (about 4.3 billion).
3. `/24` → the first 24 bits (`192.168.0`) are the network, the last 8 (`102`) the host. 2^8 = 256 addresses, `192.168.0.0` to `.255`. `.0` (host bits all 0) names the network; `.255` (all 1) is the "everyone on this network" address. 254 devices, the router `.1` included.
4. `/20` locks the first 4 bits of the third octet: `1010xxxx` = 160 to 175. 170 = `10101010` → starts `1010` → same network. 180 = `10110100` → starts `1011` → different network. Block: `172.19.160.0` to `172.19.175.255`, 4,096 addresses.
5. Windows itself. When WSL 2 starts, Windows builds a virtual network inside the laptop, picks a free private block, keeps `.1` for its own side (`PrefixOrigin: Manual`) and gives Ubuntu another address in it (`172.19.165.5/20`, with `default via 172.19.160.1`). The router never sees it. Windows may pick a different block after a reboot, so the address changes.
6. Wrong: `172.31.5.9` is inside `172.16.0.0/12` (172.16–172.31), so it's private and unreachable from the Internet. `172.32.5.9` and `172.66.147.243` are outside that block, so they're public.
7. 2^16 = 65,536 addresses. A `/24` has 256; `.0` and `.255` are reserved, and AWS also reserves `.1`, `.2`, `.3` → 251. `0.0.0.0/0` matches every address, so the whole Internet can reach the database; scanners find it fast. Use your own `/32`.
8. A router far away only reads the left bits to choose a direction, like `+880` for Bangladesh. It stores one line per *network* ("`20.192.0.0` – `20.255.255.255` → toward Microsoft") instead of one per machine.

</details>

---

## Act 2 · Step 4: Local or Remote? (Subnet Masks, Default Gateway & DHCP)

Chapters:
- [Subnet Masks & The Decision Step](02-network-layer/02-subnet-masks.md)
- [The Default Gateway & The Routing Table](02-network-layer/03-default-gateway.md)
- [DHCP: Who Gave Me These Numbers?](02-network-layer/04-dhcp.md)

1. Your laptop has IP `192.168.0.102/24`. You make a request to `192.168.0.50` (local printer) and `140.82.112.4` (GitHub). Show the exact bitwise AND calculation your OS runs for both, and state the classification (On-link vs Off-link).
2. Look at a routing table row with `Network Destination: 0.0.0.0` and `Netmask: 0.0.0.0`. Why does this rule match *every single IPv4 address on Earth*? What is it called, and why does an On-link `/24` route win over it when talking to a local IP?
3. When your laptop hands a packet destined for GitHub (`140.82.112.4`) to your Default Gateway (`192.168.0.1`), what address is written in the packet's `Destination IP` field? Why would rewriting it to the gateway's IP break communication?
4. A newly booted laptop has no IP address. How does it ask for an IP over the network without having an address? Name the four steps of the DORA handshake, and specify which steps are sent as broadcasts and why.
5. You turn off your laptop and go out of town for two days. When you return home and reconnect to Wi-Fi, you get the exact same IP (`192.168.0.102`). Explain the two mechanisms that made this happen, and describe a situation where you would be given a different IP.
6. Your laptop is halfway through its 3-hour lease (at 1.5 hours). Does it shout across the room with a broadcast to renew? What happens at T1 vs T2?
7. You plug an Ethernet cable into an office wall jack, and Windows reports "No Internet, Secured" with IP `169.254.89.23`. What does this address mean, who assigned it, and what was the root cause?
8. Does your browser send data directly into the network, or does it pass through physical hardware? Name the chain from your `fetch()` call down to the airwaves, and state the one IP destination where physical hardware is completely bypassed.

<details>
<summary><b>Answers</b></summary>

1. My network ID: `192.168.0.102 & 255.255.255.0 = 192.168.0.0`.  
   - For printer: `192.168.0.50 & 255.255.255.0 = 192.168.0.0`. Matches my network ID (`192.168.0.0 == 192.168.0.0`) → **On-link** (delivered directly over local link).  
   - For GitHub: `140.82.112.4 & 255.255.255.0 = 140.82.112.0`. Does not match my network ID (`140.82.112.0 != 192.168.0.0`) → **Off-link** (must be handed to Default Gateway `192.168.0.1`).
2. Bitwise AND with `0.0.0.0` zeroes out all 32 bits, requiring 0 matching bits. Thus, every IPv4 address matches it. It is the **Default Route** (catch-all). An on-link `/24` route wins over it because of **Longest Prefix Match (LPM)**: the kernel always chooses the most specific matching rule with the longest netmask prefix (24 bits > 0 bits).
3. **`140.82.112.4`**. The destination IP is **never** rewritten to the gateway's IP. The destination IP must identify the final destination (GitHub) across the global Internet. If you wrote `192.168.0.1`, the router would think the packet was for itself and would never forward it outside. Only the local physical delivery envelope targets the gateway.
4. It uses **DHCP** and broadcasts to `255.255.255.255` ("everyone on this local wire/radio").  
   - **D**iscover: Client broadcasts (has no IP, knows no server IP).  
   - **O**ffer: Server offers IP, mask, gateway, DNS.  
   - **R**equest: Client broadcasts naming chosen server (informs other servers to release their reserved offers).  
   - **A**cknowledge: Server confirms the lease.
5. (a) **Router MAC binding table:** The router stores `MAC -> IP` in memory and reassigns the same IP to recognized MACs if still free. (b) **Client requested IP (Option 50):** Windows stores the last IP in registry and explicitly requests `192.168.0.102`. You get a different IP if the router ran out of addresses and leased `.102` to another guest device while you were away, or if the router was rebooted/reset.
6. **No.** At 50% lease time (T1), it quietly sends a direct **unicast** DHCP Request to the known router (`192.168.0.1`). It only switches to room-wide **broadcast** if the router fails to reply and the timer hits 87.5% (T2).
7. It is an **APIPA** (Automatic Private IP Addressing) address (`169.254.0.0/16`). Your OS self-assigned it because it broadcast DHCP Discover requests and received zero responses. Root cause: no DHCP server is running or reachable on that network link.
8. It must pass through physical hardware: Browser (user-space) → OS Kernel (TCP segments & IP packets) → Network Device Driver → Physical NIC (Wi-Fi chip) → Radio waves in the air. The only exception is **`127.0.0.1` (`localhost`)**, which the kernel handles purely inside RAM on the virtual loopback adapter without touching the physical NIC.

</details>

