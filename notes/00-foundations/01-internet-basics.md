# Internet Basics: What Is "The Internet", Really?

> **Zooming into:** Step 0 of the [lifecycle](02-request-lifecycle.md) · Act 0 (the only prerequisite for everything else)
> **Prerequisites:** None. This is where the handbook starts.
> **Key Goal:** Be able to say what the Internet, the Web and Wi-Fi each are, roughly how the Internet is shaped, and what a "protocol" and a "packet" mean, so the rest of the course has solid ground.

---

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **Internet** | The global network of connected networks |
| **Web** | One application (websites, APIs) that runs on top of the Internet |
| **Wi-Fi** | A short-range radio link from your device to a nearby box, not the Internet itself |
| **ISP** | Internet Service Provider: the company that connects you to the rest of the Internet |
| **Client / Server** | The side that asks / the side that answers |
| **Protocol** | A set of rules two machines agree on so they can understand each other |
| **Packet** | A small chunk of data with an address label on it |
| **Header / Payload** | The label (who, where, how) / the actual data inside |
| **Peer-to-peer (P2P)** | Every machine is both client and server |
| **Latency** | The time a message takes to get there (and back) |
| **Ping** | A small test tool that sends a message and times the reply (used to measure latency) |

---

## 1. The Story Starts Here

When you call Stripe, load a React bundle, or query a managed database, you rely on the largest distributed machine ever built. Most developers treat it as a black box: `fetch()` goes in, JSON comes out.

That works until an API times out, a deploy fails with `ECONNRESET`, or latency to another region jumps by 300 ms. Then "the network" stops being magic and becomes the thing you must reason about. This chapter lays the ground to do that.

---

## 2. The Internet, the Web, and Wi-Fi Are Three Different Things

| | What it is | Developer example |
|---|---|---|
| **Internet** | The global **network of networks**: cables, fiber under the oceans, routers and switches, owned by thousands of organizations | The wire path between your laptop and an AWS data center |
| **Web** | **One application** on the Internet, using HTTP(S) | A browser loading a page, a JSON API |
| **Wi-Fi** | A **short-range radio link** between your device and a local box | Full Wi-Fi bars but no Internet is entirely possible |

Plenty of things use the Internet without the Web: email, SSH, online games, video calls, BitTorrent, database connections.

---

## 3. How the Internet Is Shaped

No single company owns it. It is a **network of networks** stitched together by agreement:

```text
 YOUR HOME                 YOUR ISP                 THE BACKBONE             THEIR ISP         THE SERVER
┌──────────────┐        ┌──────────────┐        ┌────────────────┐       ┌────────────┐     ┌──────────┐
│ laptop       │  Wi-Fi │ local ISP    │  fiber │ big carriers   │       │ cloud /    │     │ api.     │
│ phone        ├────────┤ network      ├────────┤ crossing       ├───────┤ data-center├─────┤ example  │
│ router (box) │        │ (regional)   │        │ countries,     │       │ network    │     │ .com     │
└──────────────┘        └──────────────┘        │ oceans         │       └────────────┘     └──────────┘
   the edge          access network                 the core                            the edge
```

* **The edge:** end devices, your laptop and the server.
* **The access network:** how an edge device reaches the Internet (home Wi-Fi to router to ISP).
* **ISPs:** companies that connect to each other so a customer of one can reach a customer of another. Big ones connect directly with each other across the **backbone**.

**Why a developer cares:** data travels through glass at about 200,000 km/s. A server roughly 13,000 km away costs at least 65 ms one way, so more than 130 ms round trip, before any server work or router delay. That is **latency**, and it is why region choice and CDNs matter. You cannot fix physics with faster code.

> In practice, big services such as Google keep copies of their servers close to users, so the nearest one answers. The example above is the worst case, a single faraway server.

---

## 4. What Is a Protocol?

Two machines that have never met must still understand each other. They do it by following a **protocol**: an agreed set of rules for
1. the **format** of messages,
2. the **order** in which they are exchanged,
3. what to do when something goes **wrong**.

You already use protocols constantly. HTTP is a protocol: *"send `GET /profile HTTP/1.1` plus headers, and I'll reply with a status line, headers and a body; if the path is unknown I'll say `404`."* Your own JSON API contract is a small protocol too.

The Internet is a **stack of protocols**, each solving one problem. The rest of this course opens them one at a time.

---

## 5. Packets: The Premise

The Internet does not send a message as one block. It slices data into small chunks called **packets**, and each packet carries its own label:

```text
┌──────────────────────────┬───────────────────────────────────────────┐
│ HEADER                   │ PAYLOAD                                   │
│ who sent it, who is it   │ the actual data: part of a JSON body,     │
│ for, how to reassemble   │ an image, a video chunk                   │
└──────────────────────────┴───────────────────────────────────────────┘
```

Because every packet carries its own address, thousands of conversations can share the same cables, and a lost packet can be resent without redoing everything. The older alternative, **circuit switching** (the traditional phone network), reserves a private path for a whole call. The Internet chose packets.

> *This is only the premise.* How routers actually handle packets, and why packets beat circuits, comes in **Act 5**, when we reach routers. For now: **data travels as small, individually labeled packets.**

---

## 6. Who Talks to Whom: Client-Server vs. Peer-to-Peer

```text
CLIENT-SERVER                              PEER-TO-PEER
 [Client 1] ──┐                              [Peer A] ◄────► [Peer B]
 [Client 2] ──┼──► [SERVER]                     ▲              ▲
 [Client 3] ──┘                                  ▼              ▼
                                              [Peer C] ◄────► [Peer D]
```

* **Client-server:** a server that is always on waits; clients start every conversation. Examples: a React app calling an Express API, an app calling Postgres. Simple to control and secure, but the server is a bottleneck and a single point of failure, so you add load balancers and scaling.
* **Peer-to-peer:** every node is both. Examples: BitTorrent, some video-call media paths, blockchain networks. Capacity grows with the number of peers, but finding peers and keeping data consistent is hard.

> **Reality check:** most "P2P" systems still need a central helper. WebRTC calls use a signaling server to introduce the peers, and NAT (Act 5) often blocks direct connections. Real systems are usually mixed.

Almost everything you build as a web developer is client-server, and so is the journey we follow next.

---

## 7. Hands-On: Measure Latency

`ping` is a tiny test tool: it sends a small message to another machine and tells you how long the reply took. That time is **latency**, the word from this lesson. Open a terminal and run:

```powershell
ping localhost            # "localhost" = your own machine
ping google.com           # a server on the Internet
```

Look at the `time=` value on each reply line.

* `localhost` should be about 0 to 1 ms. The message never leaves your computer.
* `google.com` takes noticeably longer. This is the cost of crossing real networks.
* Try one more site you expect to be far away, then compare. The result may surprise you, because large companies place servers close to users and the nearest copy answers.

You don't need to know how `ping` works yet. Just notice that **distance and the networks in between cost time, and you can measure it.**

---

## 8. Pitfalls & Production Reality

* **"The Wi-Fi is down" is often not Wi-Fi.** The radio link to the router can be fine while the router's connection to the ISP is broken. Local things work, but nothing beyond the router does.
* **"The cloud" is not a different network.** It is other people's servers reached through the same Internet.
* **The Web is not the Internet.** A service can be reachable by SSH or database protocol and have no website at all.
* **Latency vs. bandwidth:** bandwidth is how much you can move per second; latency is how long one trip takes. A fat pipe does not fix a long trip.

---

## 🧠 The Moral of the Story (One-Look Mindmap)

> **The Core Question:**
> *When your code calls `fetch()`, what is "The Internet" that carries it, and why can't one wire connect everyone?*

```text
                        THE 30-SECOND MENTAL WALKTHROUGH

 1. THE DISTINCTION:  • Wi-Fi:    A short-range radio link to your home router.
                      • Web:      One application (HTTP APIs, pages) on top of the network.
                      • Internet: The global mesh of independent networks bound by protocol.
                                           │
                                           ▼
 2. THE PROBLEM:      You cannot run a private dedicated copper wire from your laptop
                      to every server on Earth. Wires must be shared.
                                           │
                                           ▼
 3. THE SOLUTION:     Data is chopped into small, independent PACKETS. Each packet
                      carries its own header (address label) and payload (data).
                                           │
                                           ▼
 4. INDEPENDENCE:     Routers along the way read only the address label and forward
                      packets hop-by-hop. If one link fails or congests, packets take another.
                                           │
                                           ▼
 5. THE REALITY:      Distance is physical. Signals travel through fiber at ~200,000 km/s.
                      Bandwidth (pipe width) cannot erase speed-of-light latency across oceans.
```

---

## 9. Active Recall

1. What is the difference between the Web and the Internet? Name one thing that uses the Internet but not the Web.
2. Why does a server 13,000 km away have a minimum response time, whatever hardware it runs?
3. Why do packets each carry their own address?

<details>
<summary><b>Answers</b></summary>

1. The Internet is the global network of networks; the Web is one application on top of it (HTTP). Email, SSH, online games or database connections use the Internet without the Web.
2. Signals travel at a finite speed (about 200,000 km/s in fiber). The round trip alone costs well over 100 ms, no matter how fast the server is.
3. So each packet can be routed independently and shared cables can carry many conversations at once, and a lost packet can be resent alone.

</details>

---

## 10. Close the Loop & What's Next

**Revisit Log line:** [2026-10-10] | Internet Basics | The path is packets over a chain of real networks, not one wire. Each packet is routed on its own label.

We now know what the Internet is. Next: what actually happens, from your code, when you call `fetch()`?

* **Next Chapter:** [The Request Lifecycle: Master Map](02-request-lifecycle.md)
