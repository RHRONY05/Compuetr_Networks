# Session 1.1: HTTP, the Message Your Code Writes

> **Act 1 · Step 1 of the journey** · [Back to the map](notes/00-foundations/02-request-lifecycle.md)
> **Time:** about 2–3 hours (reading ~45 min, videos ~30 min, labs and build ~60 min)
> **By the end you can:** read any HTTP request and response line by line, explain how text becomes bytes, explain how a "stateless" protocol still keeps you logged in, and send an HTTP request by hand.

---

## 🗺️ Where We Are in the Story

```text
 ► 1. WRITE THE MESSAGE        ← today
   2. FIND THE ADDRESS (DNS)   ← next session
   3. OPEN A CONNECTION
   4. LOCAL OR REMOTE?
   5. NEXT PHYSICAL HOP
   6. CROSS THE PLANET
   7. MAKE IT PRIVATE
   8. SEND, REPLY, UNWRAP
```

**Last time** (Act 0), we saw the whole journey from the outside: your code calls `fetch()`, and eight things happen before the JSON comes back. Step 1 said only: *"the browser writes the message as text and turns it into bytes."*

**Today** we open that box. What exactly does the message say? What does the reply look like? And how do bytes come out of text?

**We stop** at the moment the message is ready but has nowhere to go: it contains only a *name*, `api.example.com`. That is the cliffhanger for Session 1.2 (DNS).

> **How to read this lesson.** Boxes marked 🔵 **Later** are things you will hear about (in videos, or from colleagues) that belong to a later act. They exist so you know *where a word lives*, not so you learn it now. Read them, notice the act number, and move on without guilt.

---

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **HTTP** | The agreed rules for one program to ask another for something, and get an answer |
| **Request** | The message the client sends: "please give me / do this" |
| **Response** | The message the server sends back: "here it is / here's what happened" |
| **URL** | The full address of a thing on the web: `https://api.example.com/profile` |
| **Method** | The verb of a request: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| **Path** | Which thing on the server: `/profile` |
| **Header** | One line of extra information about the message, written as `Name: value` |
| **Body** | The actual data carried by the message (JSON, HTML, an image...) |
| **Status code** | A 3-digit number in the response that says how it went: `200`, `404`, `500` |
| **Byte** | A small number (0–255). Everything a network carries is a sequence of bytes |
| **Stateless** | The server keeps no memory of earlier requests |
| **Cookie** | A small named value the server asks the browser to store and send back automatically |

---

## Part 1: The Problem HTTP Solves

From [Internet Basics](notes/00-foundations/01-internet-basics.md): two machines that have never met can only cooperate if they follow the same **protocol**, an agreement on message format, order, and what to do when things go wrong.

Picture the situation without one. Your React app (JavaScript) wants a profile from a FastAPI server (Python). The two programs are written in different languages, by different people, running on different machines. If the client sent *"hey, could you give me the user's profile please?"*, the server would have no idea how to read it.

**HTTP is the agreement.** It fixes:
* **who speaks first:** the client always asks; the server only answers,
* **what a question looks like:** a *request* in a fixed format,
* **what an answer looks like:** a *response* in a fixed format,
* **how to say what happened:** status codes.

Because both sides follow it, *any* client (browser, mobile app, `curl`, Postman, your Node.js backend) can talk to *any* server (Express, FastAPI, Nginx, Spring), regardless of the language they're written in.

**The name, briefly.** HyperText Transfer Protocol: *hypertext* is text with links to other documents (the `<a href>` of HTML), *transfer* is moving it between machines, *protocol* is the rules. It was built in 1989–91 to fetch linked documents. Today it carries almost everything apps exchange: JSON APIs, images, video, file uploads. HTTP isn't the only protocol on the Internet (see the Epilogue in the roadmap), but it's the one our story follows.

---

## Part 2: A Request Is Just Text

When your code runs:

```javascript
const res = await fetch("https://api.example.com/profile?tab=posts");
```

the browser writes this message (the real thing; every character matters):

```http
GET /profile?tab=posts HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0 ...
Accept: application/json

```

That's it: four lines of text and one empty line. Every HTTP/1.1 request has the same **four parts**:

```text
┌──────────────────────────────────────────────────────────────────┐
│ ① REQUEST LINE   GET /profile?tab=posts HTTP/1.1                 │  what to do, to what
├──────────────────────────────────────────────────────────────────┤
│ ② HEADERS        Host: api.example.com                           │  extra information,
│                  Accept: application/json                        │  one per line
├──────────────────────────────────────────────────────────────────┤
│ ③ EMPTY LINE     (nothing)                                       │  "headers are over"
├──────────────────────────────────────────────────────────────────┤
│ ④ BODY           (empty for a GET)                               │  the data, if any
└──────────────────────────────────────────────────────────────────┘
```

### ① The request line: three words
| Word | Example | Meaning |
|---|---|---|
| Method | `GET` | What you want done |
| Target | `/profile?tab=posts` | Which thing on the server (path), plus options (query) |
| Version | `HTTP/1.1` | Which edition of the rules you're following |

### Where do these come from? Taking the URL apart

```text
  https://  api.example.com  /profile  ?tab=posts
  ───┬────  ───────┬───────  ────┬───  ────┬────
  scheme       host           path       query
```

* **path + query** go into the request line.
* **host** goes into the `Host:` header. It also tells your computer *which machine* to contact. Finding that machine from a name is exactly what DNS does, in Session 1.2.
* **scheme** (`https`) says "use the secure version".

> 🔵 **Later (Act 6):** the `s` in `https` means the message is encrypted before it leaves (TLS). Today we look at the message itself, as if no encryption existed. The format is exactly the same inside the encryption.

### Methods: verbs you already use
If you've built a CRUD API, you already know these:

| Method | Usual meaning | Has a body? | Example |
|---|---|---|---|
| `GET` | Read something | No | `GET /posts/42` |
| `POST` | Create something / perform an action | Yes | `POST /posts` with the new post as JSON |
| `PUT` | Replace something entirely | Yes | `PUT /posts/42` |
| `PATCH` | Change part of something | Yes | `PATCH /posts/42` `{"title":"new"}` |
| `DELETE` | Remove something | Usually no | `DELETE /posts/42` |

A `POST` with a body looks like this. Notice the body comes **after** the empty line:

```http
POST /posts HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 15

{"name":"Rony"}
```

> 🔵 **Later (when you design APIs):** methods have properties called *safe* and *idempotent*. They matter for retries, for example why a double-clicked "Pay" button that sends `POST` twice can charge a card twice. Useful API-design knowledge, but not networking; it isn't needed to follow the story.

---

## Part 3: The Response Is Text Too

The server answers in nearly the same shape. Only the first line differs:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 40

{"id":1,"name":"Rony","posts":["hello"]}
```

```text
① STATUS LINE   HTTP/1.1   200      OK
                version    code     a phrase for humans
② HEADERS       information about the reply
③ EMPTY LINE
④ BODY          the data you asked for
```

### Status codes: the first digit tells the story

| Family | Meaning | Examples you've met | What your frontend usually does |
|---|---|---|---|
| `2xx` | It worked | `200 OK`, `201 Created`, `204 No Content` | Use the data |
| `3xx` | Look somewhere else | `301 Moved Permanently`, `302 Found`, `304 Not Modified` | Browser follows automatically |
| `4xx` | **You** (the client) made a mistake | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` | Show a message, redirect to login |
| `5xx` | **The server** failed | `500 Internal Server Error`, `502 Bad Gateway`, `503`, `504` | Show "try again", maybe retry |

Programs only read the number. `OK` and `Not Found` are just for humans.

> 🟡 **Reality check:** `200` only means *the HTTP exchange* succeeded. An API can return `200` with `{"error":"card declined"}` in the body. Status codes describe the conversation, not your business logic.

> 🔵 **Later (Act 7):** `304 Not Modified` is part of **caching**. The browser says "I already have version X", the server says "still the same", and no body is sent again. You'll see it in the C31 video. It belongs to Act 7, where we study making HTTP faster.

---

## Part 4: From Text to Bytes (the "conversion")

The anchor note said "text becomes bytes". Here's exactly what that means.

A network can only carry **bytes**: small numbers from 0 to 255. So every character of the message is replaced by a number, using an agreed table. For plain English characters, the table is **ASCII**:

```text
  G    E    T   (space)  /    p    r    o    f    i    l    e  ...  \r   \n
  71   69   84   32      47   112  114  111  102  105  108  101 ...  13   10
```

* The invisible **line ending** in HTTP is two characters: `\r` (13) and `\n` (10). The empty line between headers and body is simply `13 10` appearing twice in a row. That's how the receiver knows where the headers end.
* For anything beyond English, the body usually uses **UTF-8**, a bigger table where one character can take several bytes. The Bengali letter `ব` becomes **three** bytes: `224 166 172`.

That's why `Content-Length` counts **bytes, not characters**:

```text
{"name":"Rony"}   → 15 characters → 15 bytes
{"name":"রনি"}    → 14 characters → 20 bytes   (each Bengali letter = 3 bytes)
```

**Who does the conversion?** Never you. The browser, `curl`, Axios, or Python's `requests` library turns the text into bytes for you. The bytes are then handed to your **operating system**, which takes over. Everything that happens to those bytes from here on is the rest of this course.

> 🔵 **Later (Act 7):** HTTP/2 and HTTP/3 don't send readable text. They send a compact **binary** format. The meaning (method, path, headers, body) is identical, only the packaging changes. That's why we learn on HTTP/1.1: you can read it with your eyes.

---

## Part 5: Headers, the Message's Labels

A header is one line, `Name: value`, that tells the other side something **about** the message. Names are case-insensitive (`content-type` = `Content-Type`). There are dozens; these are the ones worth knowing now:

| Header | Sent by | What it says | Why you care |
|---|---|---|---|
| `Host` | client | Which website on that machine | **Required** in HTTP/1.1. One server machine often hosts many sites; this is how it knows which one you meant |
| `User-Agent` | client | Which program is asking | Server logs, analytics, bot detection |
| `Accept` | client | Which formats I can understand | `application/json` for APIs |
| `Content-Type` | both | What format the **body** is in | `application/json`, `text/html`, `multipart/form-data` |
| `Content-Length` | both | Body size in bytes | Tells the receiver where the body ends |
| `Authorization` | client | Proof of who I am | Where your access token goes |
| `Set-Cookie` / `Cookie` | server / client | "Remember this" / "here it is again" | Part 6 |

**`Host` in one picture.** One machine, one address, many sites:

```text
                      ┌────────────────────────────┐
 Host: shop.com    ──►│  ONE server (one address)  │──► shop app
 Host: blog.com    ──►│  reads the Host header and │──► blog app
 Host: api.shop.com──►│  picks the right site      │──► API
                      └────────────────────────────┘
```

> 🔵 **Later:** C31 also shows `Connection: keep-alive` (**Act 7**: reusing one connection for many requests), CORS headers like `Access-Control-Allow-Origin` (**Act 8**: browser security between sites), `ETag` / `If-None-Match` (**Act 7**: caching), and `Accept-Encoding` (compression). Recognize them, but don't study them yet.

---

## Part 6: HTTP Has No Memory, So How Do You Stay Logged In?

### The problem first

HTTP is **stateless**: the server handles each request on its own and then forgets it. Request #2 arrives as a complete stranger, even if request #1 came from you one second ago.

So picture logging in:

```text
① You:     POST /login   {"email":"rony@x.com","password":"..."}
   Server: 200 OK — "correct password!"            ... and then forgets.

② You:     GET /profile
   Server: "Who are you?"  →  401 Unauthorized
```

Without help, you'd have to send your password with every request.

### The solution: send proof with every message

Since the server won't remember you, **the client must carry the proof and send it with every request**. "Proof" is just text, and HTTP already has a place for extra text: headers. There are two common ways to do it.

**Way A: Cookies (the browser does the work)**

```http
① POST /login HTTP/1.1
   Host: api.example.com
   Content-Type: application/json

   {"email":"rony@x.com","password":"..."}
```
```http
② HTTP/1.1 200 OK
   Set-Cookie: session=abc123; HttpOnly; Secure        ← "browser, please remember this"
```
```http
③ GET /profile HTTP/1.1
   Host: api.example.com
   Cookie: session=abc123                               ← the browser adds this by itself
```

The server sees `session=abc123`, looks it up ("abc123 is Rony"), and answers. **You wrote no code for step ③.** The browser stores the cookie and attaches it to every request to that same site.

**Way B: Bearer tokens (your code does the work)**

```http
GET /profile HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...           ← YOUR code adds this line
```

The server checks the token's signature and knows who you are.

### Connecting this to what you already build

| | Cookie | Bearer token |
|---|---|---|
| Where it lives in the message | `Cookie:` header | `Authorization:` header |
| Who attaches it | The **browser**, automatically | **Your code** (for example, an Axios interceptor) |
| What's inside | Anything: often a session ID, sometimes a token | Usually a signed token (JWT) |
| Your typical use | **Refresh token**, in an `HttpOnly` cookie (JavaScript can't read it, so it can't be stolen by scripts) | **Access token**, short-lived, sent on every API call |

So your access/refresh-token login flow is **HTTP's statelessness being worked around with two header lines**. When your access token expires, your code calls `/refresh`. The browser automatically attaches the refresh-token cookie, and you get a new access token.

> 🔵 **Later:** cookie flags like `Secure` (only over HTTPS, **Act 6**) and `SameSite`, plus why browsers block some cross-site requests (CORS, **Act 8**). For now: *a cookie is a header line the browser remembers and resends.*

---

## Part 7: Watch It With Your Own Eyes (Labs)

### Lab A: Read a real request and response with `curl -v`

`curl` is a command-line HTTP client; `-v` (verbose) shows the messages. We use `http://` (not https) so everything is readable. In PowerShell:

```powershell
curl.exe -v http://httpbin.org/get
```

Real output (from 2026-10-13), with notes:

```text
* Host httpbin.org:80 was resolved.            ┐
* IPv4: 52.21.224.34, 18.233.182.23, ...       │ 🔵 lines starting with * are curl's own
*   Trying 52.21.224.34:80...                  │ notes about LATER steps: "resolved" = DNS
* Connected to httpbin.org (52.21.224.34) port 80 ┘ (next session), "Connected" = Act 4. Skip.
> GET /get HTTP/1.1                            ┐
> Host: httpbin.org                            │ > lines = YOUR REQUEST, exactly as sent.
> User-Agent: curl/8.11.0                      │ Request line, three headers,
> Accept: */*                                  │ and the empty line.
>                                              ┘
< HTTP/1.1 200 OK                              ┐
< Content-Type: application/json               │ < lines = THE RESPONSE.
< Content-Length: 255                          │ Status line, then headers,
< Connection: keep-alive                       │ then the empty line.
< Server: gunicorn/19.9.0                      │
<                                              ┘
{ "headers": { "Accept": "*/*", "Host": "httpbin.org", ... } }     ← the BODY (255 bytes)
```

**Your tasks:**
1. Find the four parts of the request and the four parts of the response.
2. Read the body: httpbin echoes back the headers it received. Find your own `Host` and `User-Agent` there.
3. Run `curl.exe -v http://httpbin.org/status/404`. What changes in the status line?

### Lab B: Prove HTTP has no memory, then give it one

```powershell
# 1. Ask the server to set a cookie
curl.exe -v "http://httpbin.org/cookies/set?session=abc123"
```
Look for this response line: `< Set-Cookie: session=abc123; Path=/`. The server asked for it to be remembered.

```powershell
# 2. Ask "what cookies do I have?"
curl.exe http://httpbin.org/cookies
```
Answer: `{"cookies": {}}`. **Empty.** `curl` is not a browser and doesn't remember anything, so the server sees a stranger. That's statelessness, live.

```powershell
# 3. Now send the proof yourself (-b = send this cookie)
curl.exe -v -b "session=abc123" http://httpbin.org/cookies
```
Look for `> Cookie: session=abc123` in your request, and `"session": "abc123"` in the response. You just did by hand what a browser does automatically.

### Lab C: The same thing in your browser

1. Open any site you're logged into (GitHub, for example). Press `F12`, then go to the **Network** tab and reload.
2. Click any request. In the **Headers** tab, find the request line parts (method, URL), the **status code**, and the request and response headers.
3. Find the `Cookie:` request header. Then open the **Application** tab, go to **Cookies**, and see the same values stored by the browser.
4. Optional: in the Network tab, right-click a request and choose **Copy as cURL**. It's the same message, in curl form.

> 🔵 **Later (Act 7):** the Network tab's **Protocol** column may show `h2` or `h3` instead of `http/1.1`. That's HTTP/2 and HTTP/3. Ignore it until Act 7.

---

## Part 8: Build A1, Write the Message Yourself

Libraries hide the message. Let's send one by hand to prove that HTTP really is just text.

**The script:** [hands-on-lab/act1-1.1-raw-http.py](hands-on-lab/act1-1.1-raw-http.py). Open it and read the comments first. It's about 20 lines, and each line maps to a part of this lesson:
* it opens a **socket** (a phone line to a program on another machine; how it works is Act 4, today just use it),
* writes the request line, headers and empty line **by hand** (Part 2),
* turns the text into bytes with `.encode("ascii")` (Part 4),
* reads the reply bytes and turns them back into text.

**Run it** from the course folder:

```powershell
python hands-on-lab/act1-1.1-raw-http.py
```

You should see `HTTP/1.1 200 OK`, the headers, an empty line, and a JSON body. **No library wrote this request. You did.**

**Experiments** (edit the script, predict the answer, then run it):
1. Change `/get` to `/status/404`. *(You'll get `HTTP/1.1 404 NOT FOUND`.)*
2. Delete the `Host:` line. *(You'll get `HTTP/1.1 400 Bad Request`. The server can't tell which site you want, so it rejects the message as broken.)*
3. Change `/get` to `/headers` and compare the body with what `curl` sent in Lab A.

> Why port `80` and not `443`? Port 443 expects an **encrypted** conversation first (TLS), so our plain text would be rejected. That's Act 6. In Act 4 you'll write the *server* side of this; in Act 6 you'll add encryption.

---

## 🔵 Parking Lot: Words You'll Hear, and Where They Live

| You'll hear... | What it is (one line) | Studied in |
|---|---|---|
| TCP | The reliable connection HTTP rides on | Act 4 |
| "HTTP is an application-layer protocol", TCP/IP model | The layer models | Act 9 *(file the story into layers)* |
| HTTPS, TLS | Encryption around the HTTP message | Act 6 |
| Keep-alive, persistent connections | Reusing one connection for many requests | Act 7 |
| HTTP/1.0 vs 1.1 vs 2 vs 3, QUIC | How the same messages got faster | Act 7 |
| ETag, `304`, caching, CDN | Not re-sending what you already have | Acts 7–8 |
| Chunked transfer | Sending a body in pieces when its size isn't known yet | Act 7 |
| CORS | Browser rules for requests between different sites | Act 8 |
| Proxies, load balancers, `502` | Machines between you and the app | Act 8 |
| REST, idempotency | API design style and retry safety | API design; not core networking |

---

## Watch Guide (about 30 min)

Read the lesson first; the videos then confirm and show it live.

| Video | Watch? | Notes |
|---|---|---|
| **C29** HTTP overview | ✅ All | Matches Parts 1 and 6. He says "TCP, which we have already studied" and mentions the TCP/IP model: in his playlist order those came first. For you they're Act 4 and Act 9, so let those sentences pass. |
| **C31** Request/Response structure | ✅ All | Live DevTools demo of Parts 2, 3 and 5, and a great match for Lab C. When he says "we saw keep-alive in a past video", that's C30 (Act 7 for you). The ETag/`304` section at the end is a 🔵 preview of Act 7: enjoy it, don't study it. |
| **K2.2 part 1** Web and HTTP | 🟡 Optional | The academic view: message format, plus a good cookies section. Skip the "persistent vs non-persistent" timing math (Act 7). |
| K2.1, K2.2 part 2 | ❌ Not now | Part 2 is caching and HTTP/2/3, which belong to Act 7. |

---

## Common Confusions

* **"HTTP and HTTPS are different protocols."** Same messages; HTTPS wraps them in encryption (Act 6).
* **"The server remembers I'm logged in."** It doesn't. Your browser re-sends proof (a cookie or token) every time.
* **"Cookies and tokens are opposites."** A cookie is a *delivery method* (browser-managed header); a token is a *kind of proof*. A token can be delivered in a cookie.
* **"200 means my operation succeeded."** It means the HTTP exchange worked. Check the body.
* **"Content-Length is the number of characters."** It's bytes. Bengali text is about 3 bytes per letter.

---

## Active Recall

1. Write, from memory, the full request your browser sends for `fetch("https://shop.com/cart?page=2")` (request line and the one required header).
2. A body is `{"city":"ঢাকা"}`. Is its `Content-Length` equal to its number of characters? Why or why not?
3. HTTP is stateless. Explain, using the actual header lines, how you stay logged in across 10 requests (a) with cookies and (b) with a bearer token.
4. You get `401` on every request after logging in, but only from your mobile app, not the browser. Which way of carrying proof is probably broken, and why?
5. In the `curl -v` output, which lines did *you* send, which came from the server, and which were curl's notes about later steps?

<details>
<summary><b>Answers</b></summary>

1. `GET /cart?page=2 HTTP/1.1`, then `Host: shop.com`, then an empty line. (The `https` part means it gets encrypted first, in Act 6.)
2. No. `Content-Length` counts bytes. The four Bengali letters take 3 bytes each in UTF-8, so the byte count is larger than the character count.
3. (a) Login response has `Set-Cookie: session=...`. The browser stores it and adds `Cookie: session=...` to every later request automatically. (b) Your code stores the token after login and adds `Authorization: Bearer <token>` to every request itself.
4. Probably the bearer token. A mobile app is not a browser, so nothing attaches cookies automatically. If the backend relies on cookies, or the app's code forgets to add the `Authorization` header, every request arrives as a stranger.
5. `>` lines are your request, `<` lines are the response, and `*` lines are curl describing other steps of the journey (DNS, connecting), which we cover in later sessions.

</details>

---

## Close the Loop

**Write the note** (`notes/04-application-layer/`, HTTP basics) using the Full template, including its 🔑 Keywords block.

**Revisit Log line** for the anchor:
`2026-10-13 | HTTP basics | Step 1's "message" is a text request: request line, headers, empty line, body. It becomes bytes, and the server answers in the same shape. Proof of identity rides along in every message (Cookie / Authorization headers), because HTTP itself remembers nothing.`

**The cliffhanger.** Our message is ready. It even says where it's going: `Host: api.example.com`. But that's a **name**, and the network can only deliver to **numbers** (IP addresses). Your computer has no idea where `api.example.com` is.

How does a name become a number? → **Session 1.2: DNS, the phone book of the Internet.**
