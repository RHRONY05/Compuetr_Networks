# Glossary

Words are introduced properly at the **start of the lesson that needs them** (see each lesson's "🔑 Keywords" block). This index grows as chapters are written. Look a word up here, then jump to its chapter.

| Word | One-line meaning | Introduced in |
|---|---|---|
| Internet | The global network of connected networks | [Internet Basics](00-foundations/01-internet-basics.md) |
| Web | One application (HTTP) running on top of the Internet | [Internet Basics](00-foundations/01-internet-basics.md) |
| Wi-Fi | Short-range radio link from your device to a nearby box | [Internet Basics](00-foundations/01-internet-basics.md) |
| ISP | Company that connects you to the rest of the Internet | [Internet Basics](00-foundations/01-internet-basics.md) |
| Client / Server | Side that asks / side that answers | [Internet Basics](00-foundations/01-internet-basics.md) |
| Protocol | Agreed rules for message format, order and errors | [Internet Basics](00-foundations/01-internet-basics.md) |
| Packet | Small chunk of data with its own address label | [Internet Basics](00-foundations/01-internet-basics.md) |
| Header / Payload | The label / the data inside a packet | [Internet Basics](00-foundations/01-internet-basics.md) |
| Peer-to-peer | Every node is both client and server | [Internet Basics](00-foundations/01-internet-basics.md) |
| Latency | Time for a message to travel (one way or round trip) | [Internet Basics](00-foundations/01-internet-basics.md) |
| Ping | Test tool that sends a small message and times the reply | [Internet Basics](00-foundations/01-internet-basics.md) *(full mechanics: Act 5)* |
| HTTP | Agreed rules for asking another program for something and getting an answer | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Request / Response | The client's message / the server's reply | [HTTP Basics](04-application-layer/02-http-basics.md) |
| URL | Scheme + host + path + query | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Method | Verb of a request: GET, POST, PUT, PATCH, DELETE | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Header | One `Name: value` line of information about a message | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Body | The data a message carries | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Status code | 3-digit result of an exchange (2xx ok, 4xx client error, 5xx server error) | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Byte | A number 0–255; the only thing networks carry | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Stateless | The server keeps no memory between requests | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Cookie | Small value the server asks the browser to store and resend automatically | [HTTP Basics](04-application-layer/02-http-basics.md) |
| Domain name | Human name for a machine or service, e.g. `github.com` | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| DNS | System that turns names into numbers (IP addresses) | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| DNS query / response | One question (name + record type) / its answer, matched by a ticket ID | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Resolver | Server your computer asks; walks the DNS tree for you and caches answers | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Root server | Top of the DNS tree; knows only who runs each TLD | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| TLD | Top-level domain (`.com`, `.me`, `.bd`) and the servers that run it | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Name server / authoritative server | Server answering for part of the tree / the one holding a domain's real records | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Referral | DNS answer meaning "I don't know, ask these servers" | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Glue record | Numbers of the servers in a referral, sent along to avoid a loop | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Record (A, AAAA, CNAME, MX, NS, TXT) | One DNS entry: name, type, TTL, value; each type answers one question | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| TTL (DNS) | Seconds an answer may be cached; one shared deadline for every cache | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Cache | Remembered copy of a recent answer | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| NXDOMAIN | DNS answer: this name does not exist (also cached) | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Registrar / DNS host / web host | Sells you the name / holds its records / serves the site | [DNS Resolution](04-application-layer/01-dns-resolution.md) |
| Encapsulation | Wrapping data in a header per layer, like nested envelopes | [Request Lifecycle](00-foundations/02-request-lifecycle.md) |
| IP address, CIDR | 32-bit address; prefix notation splitting network from host | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Subnet mask | Bitmask that separates the network part of an address | [Subnet Masks](02-network-layer/02-subnet-masks-and-switches.md) |
| Default gateway | The router that takes traffic leaving the local network | [Subnet Masks](02-network-layer/02-subnet-masks-and-switches.md) *(own chapter: Act 2)* |
