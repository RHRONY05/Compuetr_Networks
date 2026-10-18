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
