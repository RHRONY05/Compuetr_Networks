# DNS Resolution: Turning a Name Into a Number

> **Zooming into:** Step 2 of the [lifecycle](../00-foundations/02-request-lifecycle.md) · Act 1
> **Prerequisites:** [HTTP Basics](02-http-basics.md) (the message that needs an address)
> **Key Goal:** Explain, server by server, how `api.example.com` becomes a number; read and choose DNS records for a real deployment; and predict how long a DNS change takes to reach everyone.
> **Lesson with step-by-step labs:** [lessons/act1-1.2-dns.md](../../lessons/act1-1.2-dns.md) · **Script:** [hands-on-lab/act1-1.2-dns-query.py](../../hands-on-lab/act1-1.2-dns-query.py)
> **Recall:** [Think it through](../RECALL.md#act-1--step-2-dns-resolution)

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **IP address** | The number that identifies a machine on the Internet, like `20.205.243.166`. What the number means inside is the next chapter, [IP & CIDR](../02-network-layer/01-ip-and-cidr.md); here it's just "the number we need" |
| **Domain name** | The human name for a machine or service: `github.com`, `api.example.com` |
| **DNS** (Domain Name System) | The worldwide system that answers "which number belongs to this name?" |
| **DNS query / response** | One question (a name + a record type) / its answer |
| **Resolver** | The server your computer asks. It does the whole search for you and remembers answers. Usually your router or your ISP, or a public one like `1.1.1.1` (Cloudflare) or `8.8.8.8` (Google) |
| **Root server** | The top of the DNS tree. Knows only who is in charge of each ending (`.com`, `.me`, `.bd`) |
| **TLD** (top-level domain) | The last part of a name: `.com`, `.io`, `.bd`. Also the servers in charge of that ending |
| **Name server** | Any server that answers DNS questions for one part of the tree |
| **Authoritative name server** | The name server that holds the real records for one domain. Its answer is final |
| **Referral** | An answer that says "I don't know, but ask *these* servers" |
| **Glue** | The numbers of the servers named in a referral, sent along so the resolver isn't stuck in a loop |
| **Record** | One entry in DNS: a name, a type, a TTL and a value |
| **TTL** (time to live) | How many seconds an answer may be remembered before it must be asked again |
| **Cache** | A saved copy of a recent answer, so the question needn't be asked again |
| **NXDOMAIN** | DNS's "this name does not exist" answer |
| **Registrar** | The company you buy (rent) a domain name from, e.g. Namecheap |
| **Apex** | The bare domain with nothing in front: `rhrony05.me` (as opposed to `www.rhrony05.me`) |

---

## 1. The Story So Far

In [HTTP Basics](02-http-basics.md) we wrote the message:

```http
GET /profile HTTP/1.1
Host: api.example.com
```

It's complete, turned into bytes, and ready to go, except for one thing. It names its destination with **letters**, and the network can only deliver to **numbers**. In [Internet Basics](../00-foundations/01-internet-basics.md) we saw that data travels in packets addressed to numbers, and every machine on the path only understands numbers. Your computer has no idea where `api.example.com` is.

So before anything is sent, the name must become a number. That is step 2 of the journey. It's a **separate, earlier conversation** with a different server, and the HTTP message waits until it's done.

## 2. The Real-World Problem

Why not skip names and type numbers?

1. **Humans can't remember numbers.** You know `github.com`, not `20.205.243.166`.
2. **Numbers change; names don't.** You move your backend to a new server and its number changes. If 100,000 users had the old number saved, they'd all break. With a name in between, you change **one record**, and everyone gets the new number on their next lookup.
3. **One name can mean many machines.** A big site runs on many servers. The name can hand out different numbers to spread the load, or to send you to a server near you. When you looked up `play.googleapis.com`, your computer got **8** different numbers for that one name.

### First attempt: one big file

In the early Internet (1970s–80s), this really was solved with one text file, `HOSTS.TXT`, listing every name and its number. Everyone downloaded a fresh copy regularly from one central computer. It broke as the Internet grew: millions of names, changing every second, one file, one place to download it from.

That file still survives on your machine, for local use:

```text
C:\Windows\System32\drivers\etc\hosts      (Windows)
/etc/hosts                                  (Linux, macOS)

127.0.0.1   localhost
```

That's why `localhost` works with no network at all. Developers still add lines like `127.0.0.1 myapp.test` to test a site locally under a real-looking name. Your computer checks this file **before** asking DNS.

**DNS is the replacement:** instead of one file in one place, the phone book is **split into pieces**, and each piece is kept by whoever owns that part of the name. Nobody holds the whole book. The trick is knowing who to ask.

## 3. The Mental Model: Asking for Directions in a Huge Office Building

You want to find "Rony, API team, Engineering". The receptionist on the ground floor (the **root**) doesn't know Rony, but knows Engineering is on floor 7. The floor 7 desk (the **TLD**) doesn't know Rony either, but knows which room the API team is in. The API team (the **authoritative server**) knows exactly where Rony sits.

Nobody holds the whole directory; each desk knows only the next one down. And you don't walk it yourself: you ask an assistant (the **resolver**), who does the walk, **remembers every answer**, and answers the next person who asks instantly.

## 4. Deep Dive & Mechanics

### 4.1 Read a name right to left

To split the phone book, DNS uses the name's own structure. Read it **from the right**:

```text
     api  .  example  .  com  .
     ───     ───────     ───  ─
  subdomain   domain     TLD  root (the hidden final dot)
```

* **The root** is an invisible dot at the very end. `github.com.` is the full, official form; browsers hide the last dot. It's the starting point of every search.
* **TLD:** `.com`, `.org`, `.io`, `.me`, `.bd`, `.dev`...
* **Domain:** `example`, the part you **buy** from a registrar (Namecheap, GoDaddy).
* **Subdomain:** `api`, `www`, `blog`: anything you **create yourself, for free**, under your domain.

This forms a tree, and **each level is responsible only for the level directly below it**:

```text
                         .  (root)
            ┌────────────┼──────────────┐
          com           me              bd
       ┌────┴─────┐      │               │
    github     example  rhrony05       ac.bd
                  │                      │
          ┌───────┴──────┐            cuet.ac.bd
         api            www
```

* The **root servers** know only: "who is in charge of `.com`? of `.me`? of `.bd`?"
* The **`.com` servers** know only: "who is in charge of `example.com`?" That's millions of entries, but nothing *inside* those domains.
* The **`example.com` servers** (authoritative) know the actual records: `api.example.com` is `203.0.113.10`.

Handing responsibility for a part of the tree to someone else is called **delegation**. When you bought `rhrony05.me`, you were really paying to have the `.me` servers point to the authoritative servers *you* chose.

### 4.2 Step 0: does anyone already know?

Before any network question, your computer checks its memory, nearest first:

```text
  1. Browser cache          "did I look this up a minute ago?"
  2. OS cache + hosts file
  3. The resolver's cache   (one network question, but the resolver may answer from memory)
  4. Only if all miss: the resolver walks the tree
```

Most lookups stop at 1, 2 or 3. That's why DNS feels instant. Your own `ipconfig /displaydns` showed dozens of remembered answers: Docker, OneDrive, Google, Adobe names, all from the last few minutes.

### 4.3 The full walk, with real data

Suppose nobody has `rhrony05.me` cached. Your laptop sends **one** question to its resolver: *"What is the address of rhrony05.me? Please do the whole search for me."* The resolver then asks the tree, top to bottom. This is real output from the [script](../../hands-on-lab/act1-1.2-dns-query.py), which does exactly what a resolver does (2026-10-15, trimmed):

```text
Step 1: ask a.root-servers.net (198.41.0.4) for rhrony05.me A
    authority  me            NS   b0.nic.me                 ┐ the root: "I don't know rhrony05.me.
    authority  me            NS   a0.nic.me                 │  .me is handled by these servers."
    authority  ... and 3 more                               ┘  (a REFERRAL, no answer)
    additional b0.nic.me     A    199.253.60.1              ← and here are their numbers (glue)

Step 2: ask b0.nic.me (199.253.60.1) for rhrony05.me A
    authority  rhrony05.me   NS   odin.ns.cloudflare.com    ┐ the .me server: "I don't know either.
    authority  rhrony05.me   NS   courtney.ns.cloudflare.com┘  rhrony05.me's records are at Cloudflare."
  (no glue: looked up odin.ns.cloudflare.com -> 162.159.44.208 separately)

Step 3: ask odin.ns.cloudflare.com (162.159.44.208) for rhrony05.me A
  ... authoritative=True
    answer     rhrony05.me   A    TTL=300   172.67.184.140  ← THE ANSWER. Final, from the source.
    answer     rhrony05.me   A    TTL=300   104.21.75.251

Done in 3 questions.
```

The same thing as a picture:

```text
                       ① "rhrony05.me?"                ┌──────────────────────┐
  ┌──────────┐  ─────────────────────────────►         │     ROOT server      │
  │  YOUR    │  ⑧ "172.67.184.140"            ┌──②──►  │  "ask the .me ones"  │
  │  LAPTOP  │  ◄─────────────────── ┌────────┴───┐◄─③─┘└──────────────────────┘
  └──────────┘                       │  RESOLVER  │      ┌──────────────────────┐
                                     │ (router,   │──④──►│   .me TLD server     │
   one question, one answer          │  ISP,      │◄─⑤───│  "ask Cloudflare"    │
   ("do it all for me")              │  1.1.1.1)  │      └──────────────────────┘
                                     │ remembers  │      ┌──────────────────────┐
                                     │ everything │──⑥──►│ AUTHORITATIVE        │
                                     └────────────┘◄─⑦───│ odin.ns.cloudflare   │
                                                          │ "172.67.184.140"     │
                                                          └──────────────────────┘
```

**Two kinds of asking** appear in that picture:
* **Laptop → resolver** is a *recursive* question: "do the whole search and bring me the final answer."
* **Resolver → root, TLD, authoritative** are *iterative* questions: each server answers only what it knows, usually with a referral, and the resolver takes the next step itself.

**What the resolver does with what it learned:** it remembers *everything*. That includes the `.me` servers (for 2 days), Cloudflare as the server for `rhrony05.me` (1 hour), and the answer itself (300 s). The next person asking for *any* `.me` name skips step 1. The next person asking for `rhrony05.me` within 5 minutes gets an instant answer from memory.

### 4.4 Is it always three steps?

The **shape** is always the same: start at the root and follow referrals until a server answers with authority. The **number of questions** varies:

| Situation | Questions asked |
|---|---|
| Something is already cached (most lookups) | **0–1**. The resolver may already know where `.com` or `.me` lives, and skips the root. |
| A simple `name.tld` with nothing cached | **3**, like `github.com` |
| No glue (`rhrony05.me`!) | **3 + a side trip** to find Cloudflare's server number: a full walk of its own (root → `.com` → `cloudflare.com`) |
| A subdomain handed to another provider (e.g. `api.` hosted on AWS Route 53 while the main domain is on Netlify) | **4**: one extra referral |
| A CNAME pointing to another company's name (§4.6) | A **whole new walk** for that name |
| A server doesn't reply | Retry with **another server from the list**. That's why GitHub lists 8 name servers, and the root has 13 names |

Which machine gets asked can change too: the resolver picks any one of the listed servers.

### 4.5 Glue: names AND numbers, but only when needed

In step 1, the root gave the `.me` servers' **names** *and* their **numbers** (`b0.nic.me A 199.253.60.1`). In step 2, the `.me` server gave Cloudflare's server **names only**. Why the difference?

* **Glue is required only when the name server's name lives inside the zone being handed over.** `b0.nic.me` lives inside `.me`. To find its number you would have to ask the `.me` servers... which are the servers you're trying to find. To break that loop, the numbers must come along.
* `odin.ns.cloudflare.com` lives under `.com`, not `.me`, so there's no loop. The `.me` server gives no glue, and the resolver looks Cloudflare's server up separately, starting from the root again.

> 🟡 **13 root servers?** There are 13 root server *names* (`a.root-servers.net` to `m.root-servers.net`), but each name is served by many machines worldwide: over 1,500 in total. Their numbers are built into every resolver (a small "root hints" file), which is how the walk can start from nothing.

### 4.6 Records: one table per domain, one type per question

#### The problem

One domain gets asked **different kinds of questions** by different programs. Take `rhrony05.me`:

* A **browser** asks: *which number serves the website?*
* A **mail server** somewhere, delivering to `hello@rhrony05.me`, asks: *which server accepts email for this domain?*
* A **resolver** walking the tree asks: *which servers hold this domain's records at all?*
* A service like Google Search Console or Vercel asks: *can you prove you own this domain?*

One "name → number" table can't answer all four. So the domain's authoritative server keeps a small table of **typed records**, and each type answers one kind of question. Every record has the same four parts:

```text
  name           type   TTL    value
  github.com     A      60     20.205.243.166
```

#### The record types you'll actually meet

| Type | Full name | Question it answers | Real example | When you set one |
|---|---|---|---|---|
| **A** | **A**ddress | What is this name's IPv4 number? | `github.com A 20.205.243.166` | Pointing your domain at your server |
| **AAAA** | "quad-A", an IPv6 address | What is its IPv6 number? | `google.com AAAA 2404:6800:4013:807::66` | Same, for the newer, longer format |
| **CNAME** | **C**anonical **NAME** (canonical = official, real) | This name is a nickname: what's the real name? | `www.github.com CNAME github.com` | `www` → your main site; `app.myco.com` → `myco.vercel.app` |
| **MX** | **M**ail e**X**changer | Which servers receive email for @this-domain? | `rhrony05.me MX 18 route1.mx.cloudflare.net` | Email on your domain |
| **NS** | **N**ame **S**erver | Which servers hold this domain's records? | `rhrony05.me NS odin.ns.cloudflare.com` | Moving DNS to Cloudflare, Route 53... |
| **TXT** | **T**e**XT** | Free text, read by other programs | `rhrony05.me TXT "v=spf1 include:_spf.mx.cloudflare.net ~all"` | Proving ownership, email anti-spoofing |
| SOA | **S**tart **O**f **A**uthority | Zone bookkeeping; shows up when a name or record doesn't exist | `cuet.ac.bd SOA aitana.ns.cloudflare.com` | Never by hand; your DNS host makes it |

**Why "AAAA"?** An IPv4 address is 32 bits; an IPv6 address is 128 bits, four times longer: four A's.

#### How to read a few of them

* **CNAME is not "asking another server".** It's an answer that says *"go look up this other name instead"*. Who answers that next lookup depends on where the other name lives. `www.github.com → github.com` is on the same server, so both lines came back in one answer. `app.myco.com → myco.vercel.app` is someone else's domain, so it needs a new walk. The chain must end at an A or AAAA record, or there's no number. Real chains get long. From your own OS cache:

  ```text
  login.docker.com
    → CNAME docker-prod-cd-egdvd1hron6jfkf7.edge.tenants.us.auth0.com
    → CNAME docker-prod.us.auth0.com
    → CNAME qcegpk.us.auth0.com.pivot.prod.auth0edge.com
    → CNAME auth0-ingress.us.auth0.com.cdn.cloudflare.net
    → A     104.18.43.182
  ```

  Docker's login is run by Auth0, which sits behind Cloudflare. Each hop is one company handing traffic to another.

* **MX gives names, not numbers, plus a priority.** Lower number = try first. Gmail lists 5, 10, 20, 30, 40: if the `5` server is down, senders try `10`, and so on. Your domain lists 18, 76, 91. The sending server then does *another* A lookup on the chosen name.

* **NS is what makes delegation work.** GitHub lists 8 name servers from **two different companies** (`nsone.net` and AWS's `awsdns`). If one provider has an outage, GitHub's name still resolves.

* **TXT means nothing to DNS itself.** `v=spf1 ...` is read by *email servers*: "only these servers may send email as @this-domain". Verification codes for Google Search Console or Vercel also live in TXT records.

### 4.7 Your own domain, end to end

#### The three jobs behind "my domain"

Buying a domain and putting a site on it involves **three separate jobs**. They feel like one because the instructions mix them together:

```text
 ┌─────────────────────┐   "rhrony05.me's records are kept by Cloudflare"
 │ 1. REGISTRAR        │ ─────────────────────────────────────────────► .me TLD servers
 │    Namecheap        │   (you did this by changing "Nameservers"         (step 2 of the walk)
 │    = you own the    │    to odin / courtney.ns.cloudflare.com)
 │      name, yearly   │
 └─────────────────────┘
 ┌─────────────────────┐   holds your table: A, MX, TXT ...
 │ 2. DNS HOST         │   = the AUTHORITATIVE server
 │    Cloudflare       │   (step 3 of the walk)
 └─────────────────────┘
 ┌─────────────────────┐   the machine that actually sends your HTML or JSON
 │ 3. WEB HOST         │   (Vercel, Netlify, GitHub Pages, a VPS...)
 │                     │   the A / CNAME records lead to it
 └─────────────────────┘
```

Read it against your own walk:
* **Step 1:** the root sends the resolver to the `.me` servers. You didn't touch this.
* **Step 2:** the `.me` servers say "ask Cloudflare". That's the "Nameservers" setting you changed at Namecheap. Namecheap passed it to the `.me` registry, and that is all Namecheap does for you now.
* **Step 3:** Cloudflare answers from the records you typed in its dashboard.

**Changing a record** (a new server address) happens at the **DNS host**. **Changing who holds the records** (moving DNS to another company) happens at the **registrar**, through the name servers.

> 🔵 **Later (Act 8):** your A records (`172.67.184.140`, `104.21.75.251`) are **Cloudflare's own** addresses, not your web host's. Cloudflare stands in front of your real server (the "orange cloud" in its dashboard) as a **proxy**. For now: DNS gave the browser a number, and that number belongs to Cloudflare.

#### Email on your domain

`@gmail.com` has nothing to do with a domain you buy: Google owns `gmail.com` and set its MX records. Your domain matters for email only if you want addresses like `hello@rhrony05.me`, and yours already has that set up:

```text
rhrony05.me  MX   18 route1.mx.cloudflare.net     ← tried first (lowest number)
rhrony05.me  MX   76 route3.mx.cloudflare.net
rhrony05.me  MX   91 route2.mx.cloudflare.net
rhrony05.me  TXT  "v=spf1 include:_spf.mx.cloudflare.net ~all"
```

That's **Cloudflare Email Routing**: mail sent to `@rhrony05.me` goes to Cloudflare, which forwards it. In the same way, `student.cuet.ac.bd MX → aspmx.l.google.com` shows that CUET's student email runs on **Google Workspace**: CUET owns the name, Google runs the mail servers. A domain is a name you aim at whatever services you choose. The one sentence to keep: *MX = where mail for @domain goes, and the sender finds it with a DNS lookup.* (How mail servers talk to each other is the Epilogue.)

#### `www`, the apex, and `https`

```text
https://www.rhrony05.me
└─┬──┘  └──────┬──────┘
  │            └── the NAME: DNS's job. www.rhrony05.me and rhrony05.me are TWO separate
  │                names, each with its own records.
  └── the SCHEME: "talk to it encrypted". Nothing to do with DNS (Act 6).
```

Your site, checked on 2026-10-17:

```text
http://rhrony05.me        → 308 Permanent Redirect → https://rhrony05.me/
http://www.rhrony05.me    → 308 Permanent Redirect → https://www.rhrony05.me/
https://www.rhrony05.me   → 200 OK
```

The `http → https` step is an ordinary **HTTP redirect** (the `3xx` family from [HTTP Basics](02-http-basics.md)): Cloudflare pushes everyone to the encrypted version. Both `www` and the bare name have their own A records, so both work. Many sites pick one as the main address and redirect the other to it, so search engines see one site instead of two.

**The apex rule.** A name that has a CNAME **can't have any other records**. The apex (`rhrony05.me`) must carry NS and SOA records, so it **can't be a CNAME**. `www` has no other records, so it can. That's why Vercel and Netlify ask for:

```text
myapp.dev        A       76.76.21.21            ← the apex needs a number
www.myapp.dev    CNAME   cname.vercel-dns.com   ← subdomains can just follow Vercel's name
myapp.dev        TXT     "vercel-verify=..."    ← proves you own it
```

*(Illustrative values; copy the real ones from your provider's dashboard.)* With a CNAME, if Vercel changes its numbers, they update `cname.vercel-dns.com` once and every customer follows automatically.

**"I only typed my domain into Vercel and it worked."** The platform did the record work in one of three ways:
1. your name servers point to the platform, so it *is* your DNS host and creates the records itself,
2. it showed you which records to add and you added them,
3. it edited your DNS host's records through an integration you allowed.

Either way, it then looks your name up with DNS to check it really points at the platform.

### 4.8 Caching and TTL: why changes "take time to spread"

#### The problem

The full walk takes 3+ questions to servers around the world. Doing it for every image, every API call, every user would flood the root servers and add delay to everything. So answers get remembered. But remembered answers can go **stale**: you changed your server's number, and people still get the old one.

#### The rule: the owner chooses how long

Each record carries a **TTL** in seconds, set by the record's owner (Cloudflare's "Auto" = 300 s). Anyone holding a copy (resolver, OS, browser) may use it until the TTL runs out, then must ask again. Real runs a few seconds apart, asking the same resolver:

```text
github.com   A   TTL=60   20.205.243.166     ← fresh from GitHub's own server
github.com   A   TTL=56   20.205.243.166     ← 4 s later, from 1.1.1.1's memory
github.com   A   TTL=44   20.205.243.166
github.com   A   TTL=40   20.205.243.166     ← the resolver didn't ask GitHub again
```

**One deadline, not one per cache.** Each cache passes on the time that's **left**, not a fresh copy of the full TTL. If your resolver got the answer 20 s ago with TTL 60, your OS receives `TTL=40`. Chrome, the OS and the resolver don't each hold it for the full time.

Your own `ipconfig /displaydns` showed it too: `play.googleapis.com` had `157` seconds left in one run and `52` a few minutes later. `daily-cloudcode-pa.googleapis.com` went from `99` up to `294`: it expired and was fetched fresh.

| TTL seen | Record | Why that length |
|---|---|---|
| 60 s | `github.com A` | GitHub wants to move traffic between servers quickly |
| 300 s | `rhrony05.me A` | Cloudflare's "Auto" |
| ~1 hour | `gmail.com MX`, `www.github.com CNAME` | Changes rarely |
| 172800 s (2 days) | the `.com` name servers (from the root) | Almost never change |

#### Who holds copies, and who doesn't

* **Holds copies of your A record:** public resolvers (`1.1.1.1`, your ISP's), **your router** (`192.168.0.1`), your OS, the browser, long-running apps.
* **Never sees your A record:** the root and the `.me` servers. The `.me` servers hold only "rhrony05.me → ask Cloudflare". That's the original record, not a copy, and it changes only when you change name servers at the registrar.

#### "DNS propagation"

When you change a record and some users still reach the old server, nothing is "propagating" through the Internet. **Caches all over the world are waiting for their TTL to run out.**

| What you change | How long until (nearly) everyone sees it | Real TTL seen |
|---|---|---|
| An A record (new server) | the record's TTL | `rhrony05.me` 300 s, `github.com` 60 s |
| Name servers (new DNS host) | the **TLD's** delegation TTL | `.me` 3600 s (1 h); `.com` 172800 s (**2 days**: the registrars' "up to 48 hours" warning) |

The standard migration trick:
1. A day before moving servers, **lower the TTL** (e.g. 3600 → 60).
2. Wait for the *old* TTL to pass, so every cache now holds the short one.
3. Change the A record. Within ~60 s nearly everyone has the new number.
4. Raise the TTL again.

> 🟡 **"No" is cached too.** Asking for a name that doesn't exist returns `NXDOMAIN`, and that "no" is also remembered (900 s for `.com` names). So if you query `api.myapp.dev` *before* creating its record, you may keep getting "not found" for several minutes after you create it. A classic deployment-day confusion.

> 🟡 **TTL is a request, not a guarantee.** On 2026-10-18 both of GitHub's DNS providers answered `github.com A` with `TTL=60`. Yet in Wireshark, `1.1.1.1` replied with `Time to live: 77`, and a script run later got `161`. Both are more than 60, so Cloudflare's resolver was not simply counting down from the owner's number. Public resolvers may apply their own rules (for example a minimum cache time); which rule `1.1.1.1` uses is not confirmed. Separately, some long-running programs look a name up once at startup and keep the number forever: if your backend moved but a worker still hits the old server, restart it. Treat the TTL as the *usual* wait, not a promise.

### 4.9 The question and the answer, up close

#### The message: a small form with a ticket number

A **DNS query** is one question: **a name + a record type**. Every `nslookup` is one query:

```text
nslookup github.com              → query: "github.com, type A"
nslookup -type=MX gmail.com      → query: "gmail.com, type MX"
nslookup -type=NS cuet.ac.bd     → query: "cuet.ac.bd, type NS"
```

The question and the answer use the same form:

```text
┌─ DNS QUERY (laptop → resolver) ───────┐   ┌─ DNS RESPONSE (resolver → laptop) ─────┐
│ Ticket ID: 0x0002                     │   │ Ticket ID: 0x0002   (same number!)      │
│ Flags:  "this is a question"          │   │ Flags:  "this is an answer", "no error" │
│         "please do the whole search"  │   │                                         │
│ Question: github.com, type A          │   │ Question: github.com, type A  (copied)  │
│                                       │   │ Answer:   github.com A TTL=77           │
│                                       │   │           20.205.243.166                │
└───────────────────────────────────────┘   └─────────────────────────────────────────┘
          28 bytes                                    44 bytes
```

**Why the ticket ID?** Your laptop has many lookups going at once. When answers come back, the ID says which question each one belongs to, like the token number at a restaurant counter.

**What it looked like in Wireshark** (your capture, 2026-10-18, the answer from `1.1.1.1`):

```text
Domain Name System (response)
    Transaction ID: 0x0002                     ← the ticket; the question (frame 434) had 0x0002 too
    Flags: 0x8180 Standard query response, No error
    Questions: 1
    Answer RRs: 1                              ← one answer record
    Authority RRs: 0                           ← no referral...
    Additional RRs: 0                          ← ...and no glue: a resolver answered, no walk to report
    Answers
        github.com: type A, class IN, addr 20.205.243.166
            Time to live: 77 (1 minute, 17 seconds)
            Data length: 4                     ← an IPv4 number is 4 bytes
            Address: 20.205.243.166
    [Time: 7.487500 milliseconds]              ← the whole lookup took 7.5 ms
```

<details>
<summary><b>Where exactly do 28 and 44 bytes come from?</b></summary>

```text
  12 bytes   HEADER     ticket ID (2) + flags (2) + four counts (8): 1 question, 0 answers...
  12 bytes   NAME       6 g i t h u b 3 c o m 0   ← each part between dots (a "label"),
                                                     written as its length then its letters;
                                                     0 = the root, the end
   4 bytes   TYPE+CLASS A (=1), Internet (=1)
  ───────
  28 bytes   the question

  + 16 bytes the answer record: name (2, a "see above" pointer), type (2), class (2),
             TTL (4), length (2), the 4 bytes of 20.205.243.166
  ───────
  44 bytes   the response
```

</details>

#### The delivery: a postcard, not a phone call

There are two ways to send something across the Internet. Act 4 studies them properly; this is the idea:

| | 📞 Phone-call style | ✉️ Postcard style |
|---|---|---|
| How | Dial, "hello?", "hello!", *then* talk, then hang up | Write it, drop it in the box. No setup |
| Name | **TCP** | **UDP** |
| Good for | Long conversations that must arrive complete: web pages, HTTP | One short message, one short reply |
| Used by | HTTP (step 3 of our story) | **DNS** |

DNS picks the postcard because its whole question fits on one. Setting up a phone call first would take longer than the question itself, and it would happen before *every* website visit. In Wireshark, the line above `Domain Name System` reads `User Datagram Protocol, Src Port: 53, Dst Port: 51097`. That's the postcard. **Port 53** is the "DNS counter" at a server: the number that says "this is for the DNS program on this machine". (`51097` is a temporary number your PC picked for this one lookup. Ports are Act 4.)

Postcards come with two problems, and DNS handles both:

1. **A postcard can get lost, and nobody resends it automatically.** So the **DNS client waits a few seconds and asks again.** Seen live on a phone hotspot:

   ```text
   Question: github.com A?
     (no answer from 1.1.1.1 after 3 s, attempt 1 of 3)        ← first postcard lost
     asked 1.1.1.1: sent 28 bytes, got 44 bytes back | NOERROR  ← second one worked
   ```

   The `DNS request timed out` lines in `nslookup` are the same thing.

2. **A postcard has a size limit.** If the answer is too big (many long records), the server sends what fits and ticks a box: **"truncated, this isn't everything"**. The client then asks again by phone (TCP), which has no size limit. `github.com TXT` did exactly this: `truncated=True`, zero records.

> **In three lines:** a DNS query is one small question (name + type) with a ticket ID. It travels as a postcard (UDP, port 53), so it's fast. Lost postcards are re-sent by the DNS client; answers too big for a postcard are re-asked by phone (TCP).

## 5. Hands-On & Developer Lab

The lesson has these labs step by step. What each one shows:

| Command | What it shows | What to look for |
|---|---|---|
| `ipconfig /all` | which resolver your laptop uses | `DNS Servers`: `192.168.0.1` (home router) or the phone hotspot. **Change networks and your resolver changes too** |
| `nslookup github.com 1.1.1.1` | one query to a resolver you choose | `Non-authoritative answer` = a resolver answered, not GitHub's own server. That's normal. `Server: UnKnown` = nslookup couldn't find the resolver's own name; harmless |
| `nslookup -type=MX gmail.com 1.1.1.1` | any record type (`MX NS TXT AAAA`) | the preference numbers |
| `nslookup www.github.com 1.1.1.1` | a CNAME | `Aliases: www.github.com` |
| `ipconfig /displaydns` *(admin terminal)* | the OS cache | TTLs counting down, CNAME chains, `No records of type AAAA` (a cached "no") |
| `curl.exe -v http://example.com` | DNS inside a real request | `* Host example.com:80 was resolved.` plus the lists of IPv4 and IPv6 numbers |
| Wireshark, filter `dns` | the actual messages | query/response pairs with the same ticket ID; `Recursion desired`; `Time to live`; the lookup time |

`nslookup` **skips the OS cache** (it asks the server directly), while browsers and `curl` use the OS. So during a change they can disagree.

**Equivalents you'll meet elsewhere:** `Resolve-DnsName github.com -Type MX` (PowerShell) · `dig github.com MX` (Linux, and inside Docker containers).

**⭐ A2:** [hands-on-lab/act1-1.2-dns-query.py](../../hands-on-lab/act1-1.2-dns-query.py) builds the 28-byte question by hand, sends it as a postcard to port 53, retries if it's lost, and decodes the answer. `--walk` does the resolver's job: root → TLD → authoritative.

```powershell
python hands-on-lab/act1-1.2-dns-query.py rhrony05.me MX
python hands-on-lab/act1-1.2-dns-query.py github.com A --walk
```

**Developer impact.** Deploying to Vercel or Netlify is DNS work: an apex `A`, a `www` `CNAME`, a `TXT` for ownership. Email on your domain is `MX` + `TXT`. Long-running workers that look up a name once keep hitting a moved server until restarted.

## 6. Pitfalls & Production Reality

* `ERR_NAME_NOT_RESOLVED` / `ENOTFOUND` means step 2 failed. Causes: a typo or a missing record (possibly a **cached** NXDOMAIN), an unreachable resolver (flaky hotspots drop DNS postcards), or the domain's name servers or registration lapsed.
* "It works on my phone but not my laptop" after a change: a different resolver, with a different cache age.
* `1.1.1.1` and `8.8.8.8` are handy for debugging: "is my local resolver the problem?"
* Plain DNS is **not encrypted**: anyone on your Wi-Fi can see which names you look up.

🔵 **Later:** UDP, TCP, ports (Act 4) · what the IP address means inside (next chapter) · DNSSEC, DoH/DoT, `https://` and certificates (Act 6) · GeoDNS, CDNs, proxies such as Cloudflare's "orange cloud", traffic managers in CNAME chains (Act 8) · SPF, DKIM, PTR, SMTP (Epilogue: email).

## 🧠 The Moral of the Story (One-Look Mindmap)

> **The Core Question:**
> *Your HTTP message is addressed to `api.example.com`. How does your machine discover which 32-bit IP number that name actually belongs to?*

```text
                        THE 30-SECOND MENTAL WALKTHROUGH

 1. CACHE CHECK:      Browser Cache → OS Cache → Hosts File. If found, stop immediately.
                                           │ (Miss)
                                           ▼
 2. RECURSIVE ASK:    Laptop sends a 28-byte UDP "postcard" to local Resolver (192.168.0.1):
                      "Please find the IP for api.example.com for me."
                                           │
                                           ▼
 3. ITERATIVE WALK:   Resolver walks the hierarchical tree following referrals:
                      • Root Server (`.`):     "I don't know, ask the `.com` TLD servers."
                      • TLD Server (`.com`):   "I don't know, ask `example.com` Name Servers."
                      • Authoritative Server:  "Here is the final A record: 203.0.113.10!"
                                           │
                                           ▼
 4. CACHE & RETURN:   Resolver caches the answer for its TTL (e.g. 300s) and hands it back
                      to your laptop. "Propagation delay" is simply caches waiting to expire.
                                           │
                                           ▼
 5. THE CLIFFHANGER:  DNS handed us `203.0.113.10`. What does this number actually mean,
                      and how does it split into network vs host?
```

---

## 7. Close the Loop

**Revisit Log:** `2026-10-18 | DNS Resolution | Step 2 is a separate, earlier conversation: one small UDP question to my resolver, which answers from cache or walks root → TLD → authoritative, following referrals. Every answer carries a TTL, so "propagation" is just caches expiring.`

**Bridge forward:** DNS handed us `20.205.243.166`, and for some names a much longer form like `2606:4700:10::6814:179a`. What is this number? Why four parts separated by dots, why is each part never above 255, and how does a number say *where* in the world a machine is? **Next:** [IP Addressing & CIDR](../02-network-layer/01-ip-and-cidr.md) (Session 1.3).
