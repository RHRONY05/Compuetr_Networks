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
| IP address | The number that identifies a machine on a network (IPv4: 32 bits, IPv6: 128 bits) | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Subnet mask | Bitmask of 1s then 0s that separates an IP's network part from host part | [Subnet Masks](02-network-layer/02-subnet-masks.md) |
| Default gateway | The local router that serves as the exit door for packets leaving the subnet | [Default Gateway](02-network-layer/03-default-gateway.md) |
| Bit | A single 0 or 1; 8 bits make a byte | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| IPv4 address | 32-bit number naming a machine's connection to a network, e.g. `20.205.243.166` | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Octet | One of the four 8-bit parts of an IPv4 address (0–255) | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Dotted quad | Four octets in decimal with dots: the human way to write IPv4 | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Host | Any device that holds an IP address | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Network | A group of hosts that reach each other directly | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| LAN | Local area network: a network in one place (home, office) | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Network part / host part | Left bits = which network; right bits = which host in it | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Prefix (`/X`) | Number of left bits that form the network part | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| CIDR | `address/X` notation, with the network/host line at any bit | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Network address | First address of a block (host bits all 0); names the network | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Private address | From `10/8`, `172.16/12`, `192.168/16`: reused everywhere, not reachable from the Internet | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Public address | Unique on the whole Internet | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| Loopback | `127.0.0.1` / `localhost`: this same machine | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) |
| IPv6 | 128-bit address format written in hex with colons | [IP & CIDR](02-network-layer/01-ip-and-cidr.md) *(details: Act 5)* |
| On-link / Off-link | Reachable directly on the local link / requires forwarding via a router | [Subnet Masks](02-network-layer/02-subnet-masks.md) |
| Routing table | In-memory kernel table mapping destination prefixes to next hops | [Default Gateway](02-network-layer/03-default-gateway.md) |
| Default route (`0.0.0.0/0`) | Universal wildcard rule matching every IPv4 address on Earth | [Default Gateway](02-network-layer/03-default-gateway.md) |
| Longest prefix match (LPM) | Routing rule: most specific (longest) netmask prefix always wins | [Default Gateway](02-network-layer/03-default-gateway.md) |
| Hop | One leg of a packet's journey between routers; gateway is Hop 1 | [Default Gateway](02-network-layer/03-default-gateway.md) |
| DHCP | Protocol that automatically leases IP, mask, gateway, and DNS to a device | [DHCP](02-network-layer/04-dhcp.md) |
| DORA | 4-step DHCP exchange: Discover, Offer, Request, Acknowledge | [DHCP](02-network-layer/04-dhcp.md) |
| Lease time | Duration an IP address is rented to a machine by DHCP | [DHCP](02-network-layer/04-dhcp.md) |
| Broadcast address (`255.255.255.255`) | Deliver to every machine on the local physical network | [DHCP](02-network-layer/04-dhcp.md) |
| APIPA (`169.254.x.x`) | Automatic private IP self-assigned when DHCP fails | [DHCP](02-network-layer/04-dhcp.md) |

| NIC | Physical hardware chip/card that sends and receives electrical/radio signals | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| MAC address | 48-bit (6-byte) permanent hardware identifier burned onto a network card | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| OUI | Organizationally Unique Identifier: first 3 bytes of a MAC identifying the manufacturer | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| Link layer (Layer 2) | Moves data across a single physical hop between directly connected cards | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| Ethernet frame | Layer 2 envelope wrapping an IP packet (or ARP) with Source & Destination MACs | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| ARP | Address Resolution Protocol: discovers the physical MAC matching a local IP | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| ARP cache | In-memory kernel table storing recent IP -> MAC resolutions | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| Broadcast MAC | `FF-FF-FF-FF-FF-FF`: delivers to every network card on the local link | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| Unicast | Transmission addressed directly to one specific hardware card | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
| EtherType | 2-byte frame field indicating the payload protocol (`0x0800` IPv4, `0x0806` ARP) | [MAC and ARP](01-data-link/01-mac-and-arp.md) |
