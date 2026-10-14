# Session 1.2: DNS, the Phone Book of the Internet

> **Act 1 · Step 2 of the journey** · [Back to the map](notes/00-foundations/02-request-lifecycle.md)
> **Time:** about 2.5–3 hours (reading ~50 min, videos ~45 min, labs and build ~60 min)
> **By the end you can:** explain how `api.example.com` becomes a number, step by step and server by server; read and pick the right DNS record (A, AAAA, CNAME, MX, NS, TXT) for a real deployment; explain why a DNS change "takes time to spread" (TTL and caches); and send a DNS question by hand.

---

## 🗺️ Where We Are in the Story

```text
   1. WRITE THE MESSAGE        ✅ last session
 ► 2. FIND THE ADDRESS (DNS)   ← today
   3. OPEN A CONNECTION
   4. LOCAL OR REMOTE?
   5. NEXT PHYSICAL HOP
   6. CROSS THE PLANET
   7. MAKE IT PRIVATE
   8. SEND, REPLY, UNWRAP
```

**Last time** (Session 1.1), we wrote the message: `GET /profile HTTP/1.1` plus `Host: api.example.com`, turned into bytes. It was complete except for one thing: it carries only a **name**, and the network can only deliver to **numbers**.

**Today** we follow the lookup that turns the name into a number: who your computer asks, who *they* ask, what the answer looks like, and why it is usually instant.

**We stop** when we hold the number, `20.205.243.166` for `github.com`, and realize we don't actually know what that number *is*. That's Session 1.3.

> **How to read this lesson.** Boxes marked 🔵 **Later** are words that belong to a later act. They tell you *where a word lives*, not what to learn now. Read them, note the act number, move on. 🟡 boxes are **reality checks**: where videos simplify and production differs.

---

## ⏪ Warm-up: Recall From Session 1.1 (5 min, no peeking)

1. Write from memory the request for `fetch("https://shop.com/cart?page=2")`: request line and the one required header.
2. Why does `Content-Length` for `{"city":"ঢাকা"}` not equal its number of characters?
3. HTTP remembers nothing. Which two header lines keep you logged in, and who adds each one?

<details>
<summary><b>Answers</b></summary>

1. `GET /cart?page=2 HTTP/1.1`, then `Host: shop.com`, then an empty line.
2. It counts **bytes**. Each Bengali letter takes 3 bytes in UTF-8.
3. `Cookie:` (added automatically by the browser, after a `Set-Cookie:` from the server) and `Authorization: Bearer ...` (added by your code).

</details>

Notice the answer to question 1: `Host: shop.com`. That name is today's problem.

---

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **IP address** | The number that identifies a machine on the Internet, like `20.205.243.166`. *What the number means inside* is Session 1.3; today it's just "the number we need" |
| **Domain name** | The human name for a machine or service: `github.com`, `api.example.com` |
| **DNS** (Domain Name System) | The worldwide system that answers "which number belongs to this name?" |
| **Resolver** | The server your computer asks. It does the whole search for you and remembers answers. Usually run by your ISP or router, or a public one like `1.1.1.1` (Cloudflare) or `8.8.8.8` (Google) |
| **Root server** | The top of the DNS tree. Knows only who is in charge of each ending (`.com`, `.org`, `.bd`...) |
| **TLD** (top-level domain) | The last part of a name: `.com`, `.io`, `.bd`. Also the servers in charge of that ending |
| **Authoritative name server** | The server that holds the real records for one domain. Its answer is final |
| **Referral** | An answer that says "I don't know, but ask *these* servers" |
| **Record** | One entry in DNS: a name, a type, a value, and a TTL |
| **TTL** (time to live) | How many seconds an answer may be remembered before it must be asked again |
| **Cache** | A saved copy of a recent answer, so the question needn't be asked again |
| **NXDOMAIN** | DNS's "this name does not exist" answer |

---

## Part 1: The Problem DNS Solves

Your message says `Host: api.example.com`. But in [Internet Basics](notes/00-foundations/01-internet-basics.md) we saw that data travels in packets addressed to **numbers**, and every machine on the path only understands numbers. A name like `api.example.com` means nothing to them.

So *something* has to turn the name into a number before anything can be sent. Why not just skip names and type numbers?

1. **Humans can't remember numbers.** You know `github.com`, not `20.205.243.166`.
2. **Numbers change; names don't.** You move your backend from one server to another and its number changes. If 100,000 users had the old number saved, they'd all break. With a name, you change **one record**, and everyone gets the new number on their next lookup.
3. **One name can mean many machines.** A big site runs on many servers. The name can hand out different numbers to spread the load or send you to a server near you.

### First attempt: one big file

In the early Internet (1970s–80s), this really was solved with one text file, `HOSTS.TXT`, listing every name and number. Everyone downloaded a fresh copy regularly from one central computer. It broke as the Internet grew: millions of names, changing every second, one file, one place to download it.

That file still survives on your machine, for local use:

```text
C:\Windows\System32\drivers\etc\hosts      (Windows)
/etc/hosts                                  (Linux, macOS)

127.0.0.1   localhost
```

That's why `localhost` works with no network at all. Developers still add lines like `127.0.0.1 myapp.test` to test a site locally under a real-looking name. Your computer checks this file **before** asking DNS.

**DNS is the replacement:** instead of one file in one place, the phone book is **split into pieces**, and each piece is kept by whoever owns that part of the name. Nobody holds the whole book. The trick is knowing who to ask.

---

## Part 2: Read a Name Right to Left

To split the book, DNS uses the name's own structure. Read it **from the right**:

```text
     api  .  example  .  com  .
     ───     ───────     ───  ─
  subdomain   domain     TLD  root (the hidden final dot)
```

* **The root** is an invisible dot at the very end. `github.com.` is the full, official form; browsers hide the last dot. It's the starting point of every search.
* **TLD:** `.com`, `.org`, `.io`, `.bd`, `.dev`...
* **Domain:** `example`, the part you buy (from a registrar like Namecheap or GoDaddy).
* **Subdomain:** `api`, `www`, `blog`: anything you create yourself, for free, under your domain.

This is a tree, and **each level is only responsible for the level directly below it**:

```text
                         .  (root)
            ┌────────────┼──────────────┐
          com           org             bd
       ┌────┴─────┐      │               │
    github     example  wikipedia      gov.bd
                  │
          ┌───────┴──────┐
         api            www
```

* The **root servers** know only: "who is in charge of `.com`? of `.bd`?"
* The **`.com` servers** know only: "who is in charge of `example.com`?" (millions of entries, but nothing *inside* those domains)
* The **`example.com` servers** (authoritative) know the actual records: `api.example.com` is `203.0.113.10`.

Handing responsibility for a part of the tree to someone else is called **delegation**. When you buy `myapp.dev`, you're really paying to have the `.dev` servers point to *your* chosen authoritative servers.

---

## Part 3: The Lookup, Step by Step

### Step 0: Does anyone already know?

Before any network question, your computer checks its memory, nearest first:

```text
  1. Browser cache       "did I look this up a minute ago?"
  2. OS cache + hosts file
  3. The resolver's cache   (one network question, but the resolver may answer from memory)
  4. Only if all miss: the resolver walks the tree
```

Most lookups stop at 1, 2 or 3. That's why DNS feels instant.

### The full walk, with real data

Suppose nobody has `github.com` cached. Your laptop sends **one** question to its resolver: *"What is the address of github.com? Please do the whole search for me."* The resolver then asks three servers in turn.

This is real output from today's build script ([Part 8](#part-8-build-a2-ask-dns-yourself)), run on 2026-10-14. It does exactly what a resolver does: start at a root server and follow the referrals. Trimmed slightly:

```text
Step 1: ask a.root-servers.net (198.41.0.4) for github.com A
    authority  com          NS   l.gtld-servers.net        ┐ the root: "I don't know github.com.
    authority  com          NS   j.gtld-servers.net        │  .com is handled by these servers."
    authority  ... and 11 more                             ┘  (a REFERRAL, no answer)
    additional l.gtld-servers.net   A   192.41.162.30      ← and here are their numbers

Step 2: ask l.gtld-servers.net (192.41.162.30) for github.com A
    authority  github.com   NS   ns-421.awsdns-52.com      ┐ the .com server: "I don't know either.
    authority  github.com   NS   ns-520.awsdns-01.net      │  github.com's records are kept by these."
    authority  ... and 6 more                              ┘  (another REFERRAL)
    additional ns-421.awsdns-52.com A  205.251.193.165

Step 3: ask ns-421.awsdns-52.com (205.251.193.165) for github.com A
  ... authoritative=True
    answer     github.com   A    TTL=60   20.205.243.166    ← THE ANSWER. Final, from the source.

Done in 3 questions.
```

Draw it as a picture:

```text
                       ① "github.com?"                 ┌──────────────────┐
  ┌──────────┐  ─────────────────────────────►         │   ROOT server    │
  │  YOUR    │  ⑧ "20.205.243.166"            ┌──②──►  │ "ask .com: ..."  │
  │  LAPTOP  │  ◄─────────────────── ┌────────┴───┐◄─③─┘└──────────────────┘
  └──────────┘                       │  RESOLVER  │      ┌──────────────────┐
                                     │ (1.1.1.1,  │──④──►│  .com TLD server │
   one question, one answer          │  your ISP) │◄─⑤───│ "ask awsdns..."  │
   ("do it all for me")              │ remembers  │      └──────────────────┘
                                     │ everything │      ┌──────────────────┐
                                     │  it learns │──⑥──►│  AUTHORITATIVE   │
                                     └────────────┘◄─⑦───│ "20.205.243.166" │
                                                          └──────────────────┘
```

**Two kinds of asking**, and both appear in that picture:
* **Laptop → resolver** is a *recursive* question: "do the whole search and bring me the final answer."
* **Resolver → root, TLD, authoritative** are *iterative* questions: each server answers only what it knows, usually with a referral, and the resolver does the next step itself.

> 🟡 **Reality check: glue.** In step 2 the `.com` server said "ask `ns-421.awsdns-52.com`". But that's a *name*, and finding its number would need… a DNS lookup. To avoid going round in circles, referrals usually include the name servers' numbers too (the `additional` lines). These are called **glue records**. In K2.4 and C26 you'll hear about them; this is what they are.

> 🟡 **Reality check: 13 root servers?** There are 13 root server *names* (`a.root-servers.net` to `m.root-servers.net`), but each name is served by many machines worldwide: over 1,500 in total. Their numbers are built into every resolver (a small "root hints" file), which is how the walk can start from nothing.

**What the resolver does with what it learned:** it remembers *everything*: the `.com` servers (for 2 days, `TTL=172800`), GitHub's name servers, and the answer (60 seconds). The next person asking for *any* `.com` name skips step 1 entirely. The next person asking for `github.com` within 60 seconds gets an instant answer from memory.

---

## Part 4: Records, the Entries in the Phone Book

### The problem

A domain needs more than "name → number". The same name `gmail.com` needs a website address *and* "where should email for `@gmail.com` go?". Your `www.` subdomain should just follow wherever the main site lives. You need to prove to Google that you own the domain. So DNS stores **typed records**: each answers a different question.

Every record has the same four parts:

```text
  name           type   TTL    value
  github.com     A      60     20.205.243.166
```

### The six you'll actually meet (real answers, 2026-10-14, asked via `1.1.1.1`)

| Type | Question it answers | Real example | When you set one |
|---|---|---|---|
| **A** | What is this name's IPv4 number? | `github.com A 20.205.243.166` | Pointing your domain at your server |
| **AAAA** | What is its IPv6 number? | `google.com AAAA 2404:6800:4013:807::66` | Same, for the newer, longer address format |
| **CNAME** | This name is an alias: go look up *that* name instead | `www.github.com CNAME github.com` | `www` → your main site; `app.myco.com` → `myco.vercel.app` |
| **MX** | Which servers receive email for this domain? | `gmail.com MX 5 gmail-smtp-in.l.google.com` | Setting up email on your domain |
| **NS** | Which servers hold this domain's records? | `github.com NS ns-421.awsdns-52.com` (and 7 more) | When you move DNS to Cloudflare, Route 53... |
| **TXT** | Free text, read by other programs | `example.com TXT "v=spf1 -all"` | Proving ownership (Google, Vercel), email anti-spoofing |

**How to read a few of them:**

* **CNAME follows a chain.** Asking for `www.github.com` returned two lines: first `www.github.com CNAME github.com`, then `github.com A 20.205.243.166`. The resolver followed the alias for us. Rule: whatever a CNAME points to must eventually reach an A/AAAA record, or the lookup ends with no number.
* **MX gives names, not numbers, plus a priority.** Lower number = try first. Gmail lists 5, 10, 20, 30, 40: if the `5` server is down, senders try `10`, and so on. The sending server then does *another* A lookup on the chosen name.
* **NS is what makes delegation work.** GitHub lists 8 name servers from **two different companies** (`nsone.net` and AWS's `awsdns`): if one provider has an outage, GitHub's name still resolves.
* **TXT means nothing to DNS itself.** `v=spf1 -all` is read by *email servers*: "no server is allowed to send email as @example.com". Verification codes for Google Search Console or Vercel also live here.

**Why "AAAA"?** An IPv4 address is 32 bits; an IPv6 address is 128 bits, four times longer: four A's.

### Developer connection: deploying a site

When you put a frontend on Vercel or Netlify with your own domain, the dashboard asks you to add exactly these:

```text
myapp.dev        A       76.76.21.21            ← the bare domain ("apex") needs a number
www.myapp.dev    CNAME   cname.vercel-dns.com   ← subdomains can just follow Vercel's name
myapp.dev        TXT     "vercel-verify=..."    ← proves you own it
```

*(Values above are illustrative; copy the real ones from your provider's dashboard.)* Why a CNAME for `www`? If Vercel changes its numbers, they update `cname.vercel-dns.com` once and every customer follows automatically.

> 🔵 **Later (Act 8):** a CNAME pointing to a **CDN** or **load balancer**, and DNS giving different numbers depending on where you are ("GeoDNS"), are how big sites send you to a nearby server. C26 mentions this. It's Act 8. Don't worry about it now.

> 🔵 **Later (email, Epilogue):** SPF, DKIM, DMARC (email anti-spoofing using TXT records), SMTP (how email servers talk), and PTR (number → name, "reverse DNS") are covered in C27's last ~15 minutes. Useful if you run email; not part of our story.

---

## Part 5: Caching and TTL, Why Changes "Take Time to Spread"

### The problem

The full walk takes 3+ questions to servers around the world. Doing it for every image, every API call, every user would flood the root servers and add delay to everything. So answers get remembered. But remembered answers can go **stale**: you changed your server's number, and people still get the old one.

### The rule: the owner decides how long

Each record carries a **TTL** in seconds. Anyone holding a copy (resolver, OS, browser) may use it until the TTL runs out, then must ask again. Watch it count down. Real runs today, a few seconds apart, asking the same resolver:

```text
github.com   A   TTL=60   20.205.243.166     ← fresh from GitHub's own server: 60 s
github.com   A   TTL=56   20.205.243.166     ← 4 s later, from 1.1.1.1's memory
github.com   A   TTL=44   20.205.243.166
github.com   A   TTL=40   20.205.243.166     ← the resolver didn't ask GitHub again
```

When it reaches 0, the resolver's next customer triggers a fresh lookup.

| TTL seen today | Record | Why that length |
|---|---|---|
| 60 s | `github.com A` | GitHub wants to move traffic between servers quickly |
| ~1 hour | `gmail.com MX`, `www.github.com CNAME` | Changes rarely |
| 172800 s (2 days) | `.com` name servers (from the root) | Almost never change |

### Developer connection: "DNS propagation"

When you change a record and some users still reach the old server, nothing is "propagating" through the Internet. **Caches all over the world are waiting for their TTL to run out.** The standard migration trick:

1. A day before moving servers, **lower the TTL** (e.g. 3600 → 60).
2. Wait for the *old* TTL to pass, so every cache now holds the short one.
3. Change the A record. Within ~60 s everyone has the new number.
4. Raise the TTL again.

> 🟡 **Reality check: "no" is cached too.** Asking for a name that doesn't exist returns `NXDOMAIN`, and that "no" is also remembered (900 s for `.com` names today). So if you query `api.myapp.dev` *before* creating its record, you may keep getting "not found" for several minutes after you create it. Classic deployment-day confusion.

> 🟡 **Reality check: not every program respects TTL.** Some long-running programs look a name up once at startup and keep the number forever. If your backend moved but a long-running worker still hits the old server, restart it. The C27 demo, where a deleted record was still returned until the 10 s TTL passed, shows the honest version.

---

## Part 6: What a DNS Message Looks Like, and Why It's So Small

The question and the answer are both tiny, structured messages: bytes, like HTTP, but not readable text. Our script measured them:

```text
Question: github.com A?    → 28 bytes sent
Answer:                    → 44 bytes back
```

Where do 28 bytes come from?

```text
  12 bytes   HEADER     ID (a random number, to match answer to question)
                        flags ("this is a question", "please do the whole search")
                        counts (1 question, 0 answers...)
  12 bytes   NAME       6 g i t h u b 3 c o m 0     ← each part between dots (a "label")
                                                       written as its length, then its letters;
                                                       0 = the root, the end
   4 bytes   TYPE+CLASS A (=1), Internet (=1)
  ───────
  28 bytes
```

The answer repeats the question (28 bytes) and adds one 16-byte record (name, type, TTL, length, and the 4 bytes of the number): 28 + 16 = **44**.

**The ID matters:** your laptop may have dozens of lookups in flight. The ID is how it knows which answer belongs to which question. (C28 shows this in Wireshark as "Transaction ID".)

### Why DNS uses a lighter delivery method than the web

HTTP needs a setup step before any message goes out (step 3 of our story). For a 28-byte question that would be wasteful: the setup would take longer than the question. So DNS normally uses **UDP**: just send one message and hope an answer comes back. No setup, nothing to close. DNS servers listen on **port 53**.

The price is that nobody resends a lost message. **The DNS client does it itself**: we saw this today on a real network:

```text
Question: github.com A?
  (no answer from 1.1.1.1 after 3 s, attempt 1 of 3)
  asked 1.1.1.1: sent 28 bytes, got 44 bytes back | NOERROR ...
```

And when an answer is **too big** for one message, the server sends what fits, sets a "truncated" flag, and the client asks again over the slower, set-up-first method (TCP). Today, `github.com TXT` came back truncated with zero records, because GitHub has many long TXT records.

> 🔵 **Later (Act 4):** what UDP and TCP really are, what a **port** is, and the "setup step" (the TCP handshake). Today you need only: *DNS = one small question, one small answer, usually UDP on port 53; big answers fall back to TCP.*

> 🔵 **Later (Act 6):** **DNSSEC** (signatures that prove a DNS answer wasn't forged) and **DoH/DoT** (DNS over HTTPS/TLS, so nobody on the path can read which names you look up). Plain DNS, as today, is **not encrypted**: anyone on your Wi-Fi can see which sites you're looking up.

---

## Part 7: Watch It With Your Own Eyes (Labs)

### Lab A: Who is *your* resolver?

```powershell
ipconfig /all
```

Find the **DNS Servers** line under your Wi-Fi adapter. On 2026-10-14 this machine showed:

```text
   DNS Servers . . . . . . . . . . . : 10.50.121.192
```

That's the resolver your laptop asks for every lookup: here, a phone hotspot that passes questions to the mobile operator. On home Wi-Fi it's usually your router (like `192.168.0.1`). Ignore everything else in `ipconfig /all` for now; it belongs to Act 2.

### Lab B: Ask a question with `nslookup`

```powershell
nslookup github.com 1.1.1.1
```

The last part, `1.1.1.1`, says "ask Cloudflare's resolver instead of mine". We use it because today's hotspot resolver was dropping many questions. Real output (2026-10-14):

```text
Server:  one.one.one.one          ┐ who answered: the resolver you asked
Address:  1.1.1.1                 ┘
                                     
Non-authoritative answer:         ← "I'm a resolver repeating a remembered/fetched answer,
                                     not GitHub's own server." That's normal.
DNS request timed out.            ┐ 🟡 a lost question (UDP, Part 6). nslookup asks for both
    timeout was 2 seconds.        ┘ A and AAAA; one of them got no reply. Usually harmless.
Name:    github.com
Address:  20.205.243.166          ← THE ANSWER
```

**You may also see** `Server: UnKnown`. Before asking your question, `nslookup` tries to find the resolver's own *name* from its number (a reverse lookup). If that fails, it prints `UnKnown`. Harmless: the real answer still follows.

### Lab C: Every record type

```powershell
nslookup -type=MX gmail.com 1.1.1.1
nslookup -type=NS github.com 1.1.1.1
nslookup www.github.com 1.1.1.1
nslookup -type=AAAA google.com 1.1.1.1
nslookup -type=TXT example.com 1.1.1.1
```

Real output for the MX query (2026-10-14):

```text
gmail.com	MX preference = 30, mail exchanger = alt3.gmail-smtp-in.l.google.com
gmail.com	MX preference = 5, mail exchanger = gmail-smtp-in.l.google.com      ← tried first
gmail.com	MX preference = 20, mail exchanger = alt2.gmail-smtp-in.l.google.com
gmail.com	MX preference = 40, mail exchanger = alt4.gmail-smtp-in.l.google.com
gmail.com	MX preference = 10, mail exchanger = alt1.gmail-smtp-in.l.google.com
```

and for the alias:

```text
Name:    github.com
Address:  20.205.243.166
Aliases:  www.github.com          ← www.github.com is a CNAME for github.com
```

**Your tasks:**
1. Which Gmail server is tried first, and which last? (The order of lines doesn't matter; the preference number does.)
2. How many companies run GitHub's name servers? Why would they pay two?
3. Run `nslookup -type=NS` on a site you use (your university, a Bangladeshi site with `.bd`). Who hosts its DNS?
4. Run `nslookup this-does-not-exist-xyz123.com 1.1.1.1`. What does "Non-existent domain" correspond to in this lesson?

### Lab D: Your computer's own memory (the OS cache)

```powershell
ipconfig /displaydns
```

This lists answers your OS remembers, each with its TTL counting down. Visit a new site in your browser, run it again, and find that site's entry.

> ⚠️ When I ran this on 2026-10-14 the terminal answered *"The requested operation requires elevation"*. If you see that, open PowerShell with **Run as administrator** and try again. **Paste me your output**: I haven't seen it, so I'm not showing an invented one.

**Surprise to check:** `nslookup` lookups do **not** appear here. `nslookup` talks directly to a DNS server and skips the OS cache; browsers and `curl` use the OS. (This is why `nslookup` can disagree with your browser while a change is spreading.)

### Lab E: Callback to Session 1.1

```powershell
curl.exe -v http://example.com
```

The first `*` lines you skipped last time:

```text
* Host example.com:80 was resolved.            ← TODAY'S LESSON, in one line
* IPv6: 2606:4700:10::6814:179a, 2606:4700:10::ac42:93f3      ← AAAA answers
* IPv4: 172.66.147.243, 104.20.23.154                        ← A answers (two!)
*   Trying [2606:4700:10::6814:179a]:80...     ← 🔵 Act 4 (connecting): skip
```

Two IPv4 and two IPv6 numbers for one name: several machines behind one name (Part 1, problem 3).

### Lab F (optional, needs an install): DNS in Wireshark

Wireshark isn't installed on this machine yet. If you want to see the raw messages from C28 yourself:

```powershell
winget install WiresharkFoundation.Wireshark
```

The installer also offers **Npcap** (the part that lets it capture traffic): accept it. Then start a capture on your Wi-Fi adapter, type `dns` in the filter bar, and run `nslookup github.com 1.1.1.1`. Find: the **Transaction ID** in the question and its answer (the same number), the "Recursion desired" flag, and the answer's TTL. Not required: our script in Part 8 shows the same information.

---

## Part 8: Build A2, Ask DNS Yourself

Like in Session 1.1, we drop the library and build the message by hand.

**The script:** [hands-on-lab/act1-1.2-dns-query.py](hands-on-lab/act1-1.2-dns-query.py). Read its comments first. In plain words:
* `build_query` writes the 28-byte question from Part 6: header, the name as labels (`6github3com0`), type, class.
* `ask` sends it to port 53 with UDP, retries if no answer comes in 3 s, and checks that the answer's **ID** matches.
* `read_name` / `read_record` decode the answer's records. (Answers save space by writing a repeated name as a 2-byte "see earlier" pointer; that's the one tricky part.)
* `walk` does a resolver's job: start at a root server, follow referrals, stop at an authoritative answer (Part 3).

**Run it** from the course folder:

```powershell
python hands-on-lab/act1-1.2-dns-query.py github.com                  # ask 1.1.1.1
python hands-on-lab/act1-1.2-dns-query.py gmail.com MX                # any of: A AAAA CNAME MX NS TXT
python hands-on-lab/act1-1.2-dns-query.py github.com A --walk         # root -> TLD -> authoritative
```

**Experiments** (predict first, then run):
1. Run the first command twice, 10 seconds apart. *(The TTL drops by about 10: you're reading the resolver's cache.)*
2. `--walk` for `wikipedia.org`, then for `www.bangladesh.gov.bd`. *(Step 1 points to different TLD servers: `a2.org.afilias-nst.info` for `.org`, `dns.bd` for `.bd`. The root knows nothing more than the ending. For the `.bd` site you'll also see `(no glue: looked up kobe.ns.cloudflare.com ... separately)`: its name server lives under a different domain, so no glue number came along and the walker had to do a side lookup first. That site's DNS is hosted by Cloudflare.)*
3. `--walk` for `www.github.com`. *(Today the answer had two lines: `www.github.com CNAME github.com` and `github.com A 20.205.243.166`. Because both names live on the same authoritative server, it followed the alias for us. If a CNAME pointed to a different company's domain, a resolver would have to start a new walk for that name.)*
4. Ask for a name that doesn't exist. *(`NXDOMAIN`, with a `SOA` record in the authority section: that record carries how long to remember the "no". You don't need SOA beyond that.)*
5. `github.com TXT`. *(`truncated=True`, zero records: the answer didn't fit. Stretch: a real resolver now retries over TCP.)*

---

## 🔵 Parking Lot: Words You'll Hear, and Where They Live

| You'll hear... | What it is (one line) | Studied in |
|---|---|---|
| IP address structure, IPv4 vs IPv6, CIDR | What the number DNS returns means inside | **Session 1.3** (next) |
| UDP, TCP, port 53, three-way handshake | How DNS messages are delivered; the setup step DNS avoids | Act 4 |
| "DNS is an application-layer protocol" | Where DNS sits in the layer models | Act 9 |
| `ipconfig /all` (other lines), DHCP | How your laptop learned its resolver's number | Act 2 (2.2) |
| GeoDNS, CDN, load balancing via DNS | One name → nearest/least-busy server | Act 8 |
| Anycast | Many machines sharing one IP (how 1,500 root machines share 13 names) | Act 5 / 8 |
| DNSSEC, DoH, DoT | Signed DNS answers; encrypted DNS | Act 6 |
| SPF, DKIM, DMARC, SMTP, IMAP, PTR | Email delivery and anti-spoofing | Epilogue (email) |
| Route 53, Cloudflare DNS, Netlify DNS | Companies running authoritative servers for you | (you'll use them; nothing new to learn) |
| SOA record, "Authority RRs", "Additional RRs" | Zone metadata; sections of a DNS answer | Seen today in the script; no more needed |

---

## Watch Guide (about 45 min, more if you watch C27 fully)

Read the lesson first. The videos confirm it and show it live.

| Video | Watch? | Notes |
|---|---|---|
| **C26** How DNS works | ✅ All | Matches Parts 1–3. He says "we saw in the UDP lecture" and "TCP/UDP": in his order those came first; for you they're Act 4, so let those sentences pass. The Mumbai/New York **GeoDNS** and load-balancing part is an Act 8 preview. His live `nslookup` walk from a root server is exactly our `--walk`. |
| **C27** DNS records | ✅ Up to the end of TXT, roughly the first 28 min (A, AAAA, MX, CNAME, NS, TXT) · 🟡 rest optional | The NS section includes **delegation of a subdomain** (`api.` on Route 53 while the main domain is on Netlify): good real-world detail. The MX part's email-delivery flow (SMTP, port 25, IMAP/POP3) is 🔵 Epilogue: get the idea, skip the names. From SPF onward (just before the 30 min mark, then PTR) it's email security: 🔵 Epilogue. When he says "CIDR, I covered this in the past videos", that's Session 1.3 for you. |
| **C28** DNS in Wireshark | 🟡 Optional, best after Lab F or Part 8 | Shows the Transaction ID, flags and TTL of Part 6. The middle shows **truncation → TCP fallback** live, with "SYN", "three-way handshake", "FIN": those words are Act 4, let them pass. Skip anything about "DNSSEC" bits. |
| **K2.4** Kurose: DNS | 🟡 Optional | The academic view: why not centralize, the root/TLD/authoritative hierarchy, **iterative vs recursive** queries, caching, records as a 4-tuple, the message format. Skip the last minute (DNS security, "chapter 7") and the reference to "chapter 4" for getting IP addresses (Act 2). |

---

## Common Confusions

* **"DNS is part of the HTTP request."** It's a separate, earlier conversation with a different server. HTTP doesn't start until DNS has finished.
* **"The root servers know every website."** They only know who runs each ending (`.com`, `.bd`...). Even the `.com` servers don't know any website's number.
* **"Non-authoritative means wrong or untrustworthy."** It means "a resolver gave you this, not the domain's own server". That's what happens almost every time, and it's normal.
* **"DNS propagation is a slow broadcast."** Nothing broadcasts. Caches expire on their own TTL schedule.
* **"A CNAME points to an IP."** It points to another *name*. Only A/AAAA records hold numbers.

---

## Active Recall

1. Your browser has never visited `docs.python.org`, and neither has anyone using your resolver. List every server that gets asked, in order, and what each one answers.
2. You moved your API to a new server and updated the A record 10 minutes ago. Your phone gets the new server, your laptop still gets the old one. Explain, and say what you could have done the day before.
3. A user's app shows `ERR_NAME_NOT_RESOLVED` / `ENOTFOUND`. Which step of the journey failed? Name two possible causes.
4. Why does DNS normally use a "send and hope" delivery method instead of the set-up-first one HTTP uses, and what does the client do to cope with that choice?
5. You want `www.myapp.dev` to follow Vercel, and email for `@myapp.dev` to go to Zoho. Which record types do you add, and why isn't `www` an A record?

<details>
<summary><b>Answers</b></summary>

1. Browser cache, OS cache and hosts file (all miss) → your **resolver** (cache miss) → a **root server** (referral: "ask the `.org` servers") → a **`.org` TLD server** (referral: "ask python.org's name servers", with glue numbers) → **python.org's authoritative server** (the answer, possibly a CNAME, which then needs its own lookup). The resolver caches everything and returns the number to your laptop.
2. Your laptop (or its resolver) still has the old answer cached and its TTL hasn't run out; your phone's resolver didn't have it cached or its copy expired. The day before, lower the TTL to e.g. 60 s and wait for the old TTL to pass, so all caches expire quickly after the change.
3. Step 2 (DNS) found no number. Causes: a typo or a record that doesn't exist (`NXDOMAIN`, possibly a cached "no"); the resolver is unreachable or not answering (like today's hotspot); the domain's name servers are down or the domain expired.
4. A DNS question and answer are tiny (28 and 44 bytes here), so a setup step first would take longer than the question itself. The cost: lost messages aren't resent automatically, so the DNS client retries after a timeout, and uses the ID to match answers. Answers too big for one message are flagged truncated and re-asked over TCP.
5. `www.myapp.dev CNAME <vercel's name>`: a CNAME follows Vercel, so if Vercel's numbers change you change nothing. `myapp.dev MX <zoho's mail servers>` with preferences, and usually a TXT record for verification and SPF. An A record would freeze one number that Vercel might change.

</details>

---

## Close the Loop

**Write the note:** rewrite [notes/04-application-layer/01-dns-resolution.md](notes/04-application-layer/01-dns-resolution.md) into the **Full** handbook format (Keywords block, zoom banner on Step 2, story so far from the HTTP note, this lesson's labs). Say "create note about DNS" and I'll draft it with you; the old note's glue-record and story sections can be reused.

**Revisit Log line** for the anchor:
`2026-10-14 | DNS Resolution | Step 2 is a separate, earlier conversation: one small question to my resolver, which answers from cache or walks root → TLD → authoritative, following referrals. Every answer has a TTL, so "propagation" is just caches expiring.`

**The cliffhanger.** We have it: `github.com` is **`20.205.243.166`**. `example.com` gave us two of them, plus some much longer ones like `2606:4700:10::6814:179a`. But what *is* this number? Why four parts separated by dots, why is each part never above 255, why are there two different formats, and how does a number say *where* in the world a machine is?

→ **Session 1.3: The number DNS gave us** (IP address and CIDR, which you've partly learned already, now in its place in the story).
