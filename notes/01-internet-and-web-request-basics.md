# Internet and Web Request Basics

## Big Idea

The Internet is a global network of networks that lets devices communicate using agreed rules called protocols. Opening an HTTPS website involves several cooperating parts, each with a specific job.

## Why It Matters

This is the path behind every frontend API call, deployed backend, and browser page load. Knowing the roles helps you debug errors such as DNS failures, connection problems, and HTTPS issues.

## Key Terms

- Internet: connected networks communicating through standard protocols.
- Web: an application on the Internet, commonly using HTTP/HTTPS.
- Wi-Fi: a wireless way to connect to a nearby local network; it is not the Internet itself.
- Domain: human-friendly name, such as `api.example.com`.
- IP address: network address used to reach a destination machine.
- Port: identifies the program/service on a machine, such as `localhost:3000`.
- MAC address: hardware address used for delivery on a local Ethernet/Wi-Fi network.
- Packet: a small unit of data sent through a network; it contains a header and payload.
- Payload: the useful data being carried.
- Protocol: an agreed set of communication rules.

## Opening an HTTPS Website

```text
Browser -> DNS -> TCP -> TLS -> HTTP -> Server -> HTTP response -> Browser renders
```

1. DNS finds the IP address for the domain.
2. TCP creates a reliable connection to the server's port.
3. TLS protects the connection for HTTPS.
4. HTTP carries the request and response, such as `GET /api/users`.
5. The network sends data as packets; TCP makes the result feel like one reliable data stream to the application.

## Network Models

- Client-server: a client requests a service; a server provides it. Example: React frontend and Express/Next backend.
- Peer-to-peer (P2P): each participant can both request/receive and serve/share data. Example: BitTorrent-style file sharing.
- Packet switching: many communications share the same network links as packets. This is how the Internet normally works.
- Circuit switching: network capacity is reserved for an entire communication session.

## Developer Connection

When you call `fetch("https://api.example.com/users")`, your code uses HTTP, but DNS, TCP, TLS, IP, and local Wi-Fi/Ethernet work underneath. A failure can occur at any of those layers.

## Common Confusions

- DNS finds an IP address; it does not download the web page.
- TLS provides HTTPS security; it is not the same thing as TCP.
- A port identifies a service on one machine; it is not the machine's network address.
- The Web and Wi-Fi are parts that use the Internet; neither is the Internet itself.

## Quick Practice

1. Why does the browser need DNS before it can send an HTTP request to a domain?
2. In `localhost:3000`, what does `3000` identify?
3. Why can a P2P participant act as both a client and a server?

## Status

- Tracker status: Learning
- Student approval: Not requested; no topic is completed.
