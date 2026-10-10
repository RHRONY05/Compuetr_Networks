# How DNS Works

## Primary Learning Resource

[How DNS Works - interactive walkthrough](https://howdns.works/)

## Big Idea

DNS turns a human-friendly domain, such as `www.google.com`, into an IP address that a browser can contact. DNS is distributed: each level knows only the next responsible level, rather than one server storing every domain's IP address.

## Why It Matters

Before a browser can make an HTTPS request to a domain, it normally needs DNS. DNS failures can make a working server appear unreachable.

## DNS Lookup Flow

```text
Browser: www.example.com
  |
  +-- Browser cache hit? ---- yes --> IP address --> TCP/TLS/HTTP connection
  |
  no
  v
OS DNS cache hit? ----------- yes --> IP address --> TCP/TLS/HTTP connection
  |
  no
  v
Recursive resolver cache hit? ----- yes --> IP address --> OS --> Browser
  |
  no
  v
Root DNS server
  |  referral: "ask the .com TLD servers"
  v
.com TLD DNS server
  |  referral: authoritative server names, plus possible glue IP addresses
  v
Authoritative DNS server for example.com
  |  final answer: A/AAAA record (the IP address)
  v
Recursive resolver --> caches answer --> OS --> Browser
  |
  v
Browser connects to the IP, then uses TCP/TLS/HTTP
```

## Hierarchy

```text
Root zone
  .com TLD registry
    example.com authoritative DNS servers
      www.example.com DNS records
```

- Root servers know which name servers are responsible for each top-level domain (TLD), such as `.com`, `.net`, `.org`, `.jp`, and `.hot`.
- A TLD server knows which authoritative name servers are responsible for a registered domain, such as `example.com`.
- An authoritative name server holds the DNS records for that domain and returns the requested answer.

## Key Terms

- DNS resolver: the server that performs the lookup for the browser; often supplied by an ISP, but it can be a public resolver such as Cloudflare or Google. It checks caches and asks the DNS hierarchy when needed.
- Root server: authoritative for the DNS root zone. One of 13 named root-server systems; it gives a referral to the correct TLD rather than the final domain IP.
- TLD: the last label in a domain, such as `.com`, `.org`, `.bd`, or `.jp`.
- Generic TLD: a general top-level domain, such as `.com`, `.net`, `.org`, or `.hot`.
- Country-code TLD: a country/territory code, such as `.bd` or `.jp`.
- Authoritative name server: the source of DNS records for a domain. It returns the final answer for names in its zone.
- ICANN: coordinates global unique identifiers and DNS root-zone policy through the IANA functions. It helps ensure one global naming system, but it does not run the entire Internet, every root server, or every DNS provider.
- Glue record: an A/AAAA address record sent with a delegation so a resolver can reach an in-domain name server without a circular lookup.
- TTL: cache lifetime for a DNS answer.

## Why Multiple Authoritative Servers?

Domains use multiple authoritative name servers for availability, geographic reach, request sharing, and resilience against outages or attacks. They should serve the same DNS zone data, so a resolver can try another if one fails.

## Glue Record Example

```text
.com TLD server says:
  example.com -> ns1.example.com, ns2.example.com

Glue records included:
  ns1.example.com -> 203.0.113.10
  ns2.example.com -> 203.0.113.11
```

Without glue, the resolver might need to ask `ns1.example.com` for the IP address of `ns1.example.com`, creating a circular dependency.

## Developer Connection

For `fetch("https://api.example.com/users")`, DNS resolves `api.example.com` before the browser can connect. A DNS record may return several IPs or point to a load balancer/CDN rather than one fixed backend machine.

## Common Confusions

- Root and TLD servers usually give referrals; they do not normally return the final IP address for a domain.
- DNS finds an address. TCP/TLS/HTTP happen after that to request the actual page or API response.
- A resolver cache hit avoids the root-to-authoritative journey, which is why DNS is usually fast.

## Quick Practice

1. Which DNS server normally returns the final A/AAAA record for `www.example.com`?
2. Why would a `.com` TLD server include a glue record for `ns1.example.com`?
3. Why should a domain use more than one authoritative name server?

## The Story: Typing `https://google.com`

You type `https://google.com` into your browser. Before the browser can ask Google for a page, it needs an IP address for `google.com`. It first looks in its own DNS cache: “Have I recently learned where `google.com` is?” If the cached answer has not expired, the browser can immediately use that IP. If it has no usable answer, it asks the operating system's DNS service.

The OS checks its own cache for the same answer. If it has one, it returns the IP to the browser. Otherwise, the OS sends a DNS query to its configured **recursive resolver**. This resolver might be provided by the ISP, home router, Google, Cloudflare, or another DNS provider. Its job is to do the lookup work on behalf of the OS and to reuse answers it has cached for many users.

The resolver also checks its cache. On a miss, it starts at the top of the DNS hierarchy. It already knows how to reach the root because DNS software carries a list of root-server addresses called *root hints*. The 13 named root-server systems, `A` through `M`, are implemented by many physical servers around the world. The resolver asks one: “Where can I find `google.com`?” The root server does not know Google's IP address. It sees that the name ends in `.com` and replies: “I do not know `google.com`, but these are the name servers responsible for the `.com` TLD.” This reply is called a referral.

The resolver then asks a `.com` TLD server: “Where can I find `google.com`?” The TLD server does not usually know Google's final IP address either. Instead, it replies with the names of Google's **authoritative name servers** - the servers responsible for the `google.com` DNS zone. If a listed name server is inside the domain it serves, the TLD response can also include its IP address as a **glue record**. Glue prevents the resolver from getting stuck trying to find the address of a name server by asking that same name server.

Now the resolver can contact one of Google's authoritative name servers and ask: “What is the address for `google.com`?” This server holds Google's DNS records and returns the requested answer, such as an IPv4 `A` record or IPv6 `AAAA` record. Google uses multiple authoritative servers so that DNS remains available when a server, network route, or location fails, and so queries can be shared across the world.

Finally, the resolver stores the answer for the record's TTL and sends it back to the OS. The OS can cache it and returns it to the browser, which may cache it too. At last, the browser has an IP address. It can connect to it, establish TCP and TLS for HTTPS, and send the HTTP request for the page.

## Status

- Tracker status: Learning
- Student approval: Not requested; no topic is completed.
