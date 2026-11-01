# Computer Networks Hands-On Terminal & PowerShell Commands Reference

> **Purpose:** A single, centralized cheat-sheet and practical guide for every terminal command, PowerShell cmdlet, and utility used throughout this course. Look up any command here to inspect your system, troubleshoot networking issues, and run experiments on your own.

---

## Quick Jump Table

| Category | Commands Covered | Core Purpose |
|---|---|---|
| **1. Hardware & Interfaces (L2)** | `getmac`, `Get-NetAdapter`, `Get-NetIPInterface` | Inspect physical NICs, MAC addresses, link speeds, MTU |
| **2. ARP & Link-Layer Neighbors** | `arp -a`, `arp -d`, `Get-NetNeighbor` | Inspect and clear the kernel IP-to-MAC resolution cache |
| **3. IP Addressing & Subnets (L3)** | `ipconfig`, `ipconfig /all`, `Get-NetIPAddress` | View local IP, prefix (/24), lease times, DHCP/DNS servers |
| **4. Routing & Default Gateway** | `route print`, `Get-NetRoute`, `Test-NetConnection` | Inspect routing table, default route `0.0.0.0/0`, next hops |
| **5. DNS Resolution (L7)** | `nslookup`, `ipconfig /displaydns`, `ipconfig /flushdns` | Query DNS records (A, MX, TXT, NS), inspect local DNS cache |
| **6. End-to-End Connectivity & Latency**| `ping`, `tracert`, `Test-NetConnection -Port` | Check packet reachability, hop-by-hop latency, port status |
| **7. Ports, Sockets & Connections (L4)**| `netstat -ano`, `Get-NetTCPConnection` | View active sockets, listening ports, process PIDs, TCP states |
| **8. HTTP & APIs (L7)** | `curl -v`, `Invoke-WebRequest` | Send raw HTTP requests, inspect headers, status codes, cookies |

---

## 1. Physical Hardware & Network Interfaces (Layer 2)

### `getmac /v /fo list`
Shows every Network Interface Card (NIC) with its connection name, hardware description, and physical MAC address.
```powershell
getmac /v /fo list
```
* **What to look for:**
  - `Physical Address`: 48-bit hex MAC (`XX-XX-XX-XX-XX-XX`).
  - First 3 bytes: Manufacturer OUI (e.g. `94-BB-43` = MediaTek, `CC-28-AA` = Realtek).
  - Look for matching Wi-Fi / Bluetooth chips (often differ by only 1 bit at the end).

### `Get-NetAdapter` (PowerShell)
Shows all network adapters, their link speed, status, and physical MAC.
```powershell
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress
```

### `Get-NetIPInterface`
Shows Layer 2 / Layer 3 interface properties, including MTU (Maximum Transmission Unit, typically 1500 bytes) and DHCP status.
```powershell
Get-NetIPInterface -AddressFamily IPv4
```

---

## 2. ARP & Neighbor Discovery (Layer 2 ↔ Layer 3)

### `arp -a`
Dumps the operating system kernel's ARP cache (IP address to physical MAC address table).
```powershell
arp -a
```
* **What to look for:**
  - `dynamic`: Learned dynamically over the wire via ARP request/reply; expires automatically.
  - `static`: Hardcoded mappings (e.g. `192.168.0.255` mapped to `ff-ff-ff-ff-ff-ff` broadcast).
  - Your Default Gateway (`192.168.0.1`) and its router MAC.

### `Get-NetNeighbor` (Modern PowerShell equivalent of `arp -a`)
Lists all link-layer neighbor cache entries with explicit state (`Reachable`, `Permanent`, `Stale`).
```powershell
Get-NetNeighbor -AddressFamily IPv4
```

### `arp -d *` (Clear ARP Cache - requires Admin)
Flushes the kernel ARP cache to force the OS to send fresh ARP broadcasts on the next packet.
```powershell
# In Administrator PowerShell:
arp -d *
```

---

## 3. IP Addressing, Subnets & DHCP (Layer 3)

### `ipconfig`
Quick summary of IP address, subnet mask, and default gateway for active adapters.
```powershell
ipconfig
```

### `ipconfig /all`
Complete detailed network configuration: Hostname, physical MAC address, DHCP server IP, lease times, and DNS servers.
```powershell
ipconfig /all
```
* **What to look for:**
  - `IPv4 Address`: Your host IP (e.g. `192.168.0.108`).
  - `Subnet Mask`: e.g. `255.255.255.0` (`/24`).
  - `Default Gateway`: Your router (`192.168.0.1`).
  - `DHCP Lease Obtained / Expires`: Shows DHCP lease duration.
  - `169.254.x.x`: Indicates an unconfigured adapter using APIPA because DHCP failed or no cable is plugged in.

### `Get-NetIPAddress` (PowerShell)
Inspects IP addresses with CIDR prefix length (`PrefixLength: 24`).
```powershell
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi" | Select-Object IPAddress, PrefixLength, InterfaceAlias
```

### `ipconfig /release` and `ipconfig /renew`
Triggers the DHCP DORA process: releases current lease and requests a brand new lease from the DHCP server.
```powershell
ipconfig /release
ipconfig /renew
```

---

## 4. Routing Table & Gateway Selection (Layer 3)

### `route print -4`
Displays the active IPv4 kernel routing table.
```powershell
route print -4
```
* **What to look for:**
  - `Network Destination: 0.0.0.0, Netmask: 0.0.0.0`: The **Default Route**. Matches all packets that aren't local.
  - `Gateway`: The IP of your router where all off-link traffic is sent.
  - `Metric`: Lower number = higher priority route.

### `Get-NetRoute` (PowerShell)
Filter for the active default gateway route:
```powershell
Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object DestinationPrefix, NextHop, RouteMetric, InterfaceAlias
```

---

## 5. DNS Resolution (Layer 7)

### `nslookup <domain>`
Queries your configured DNS resolver for a domain's IP address.
```powershell
nslookup api.example.com
```

### `nslookup -type=<RECORD> <domain>`
Query specific DNS record types:
```powershell
# Query Mail Exchanger (MX) records
nslookup -type=MX google.com

# Query TXT records (SPF, domain verification)
nslookup -type=TXT rhrony05.me

# Query authoritative Name Servers (NS)
nslookup -type=NS rhrony05.me
```

### `nslookup <domain> <specific-dns-server>`
Query a specific public DNS resolver directly (bypassing local router cache):
```powershell
nslookup rhrony05.me 8.8.8.8       # Google DNS
nslookup rhrony05.me 1.1.1.1       # Cloudflare DNS
```

### `ipconfig /displaydns`
Displays all DNS records currently cached in your local Windows OS DNS resolver cache.
```powershell
ipconfig /displaydns
```

### `ipconfig /flushdns`
Clears the OS local DNS cache to force fresh DNS lookups.
```powershell
ipconfig /flushdns
```

---

## 6. Connectivity, Latency & Traceroute

### `ping <target>`
Sends 4 ICMP Echo Requests to test end-to-end network reachability and round-trip time (RTT).
```powershell
ping 192.168.0.1      # Ping local gateway (should be < 2ms)
ping 8.8.8.8          # Ping remote public server
```

### `tracert <target>`
Traces the hop-by-hop path across intermediate routers using incremental TTL values.
```powershell
tracert 8.8.8.8
```
* **What to look for:**
  - Hop 1: Your default gateway (`192.168.0.1`).
  - Hop 2–3: Your ISP's local aggregation routers.
  - Later Hops: Transit providers and destination backbone.

### `Test-NetConnection -ComputerName <host> -Port <port>`
Tests both DNS resolution and TCP port reachability (clean replacement for `telnet`).
```powershell
Test-NetConnection -ComputerName google.com -Port 443
Test-NetConnection -ComputerName localhost -Port 3000
```

---

## 7. Ports, Sockets & Active Connections (Layer 4)

### `netstat -ano`
Dumps all active TCP/UDP connections, listening ports, and the owning Process ID (PID).
```powershell
netstat -ano | findstr "LISTENING"
netstat -ano | findstr ":80"
netstat -ano | findstr ":443"
```
* **What to look for:**
  - `0.0.0.0:3000`: Listening on all local network interfaces.
  - `127.0.0.1:3000`: Listening only on localhost (inaccessible from LAN).
  - Last column: PID (match with Task Manager or `tasklist | findstr <PID>`).

### `Get-NetTCPConnection` (PowerShell)
View TCP connections and states (`Listen`, `Established`, `TimeWait`):
```powershell
Get-NetTCPConnection -State Listen | Select-Object LocalAddress, LocalPort, OwningProcess
```

---

## 8. HTTP & Web API Requests (Layer 7)

### `curl -v <url>`
Sends an HTTP request with verbose output showing DNS resolution, TCP handshake, request headers, and response headers.
```powershell
curl.exe -v "http://example.com"
curl.exe -v "https://api.example.com/profile"
```
* **What to look for:**
  - `* Connected to example.com (93.184.215.14) port 80`: L3/L4 connection info.
  - `> GET / HTTP/1.1`: Request line and outgoing headers.
  - `< HTTP/1.1 200 OK`: Response line and incoming headers.

