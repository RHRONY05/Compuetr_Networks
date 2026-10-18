# HTTP Basics: The Message Your Code Writes

> **Zooming into:** Step 1 of the [lifecycle](../00-foundations/02-request-lifecycle.md) · Act 1
> **Prerequisites:** [Internet Basics](../00-foundations/01-internet-basics.md), [The Request Lifecycle](../00-foundations/02-request-lifecycle.md)
> **Key Goal:** Read any HTTP request and response line by line, explain how the text becomes bytes, and explain how a protocol with no memory still keeps you logged in.
> **Full lesson with labs:** [lessons/act1-1.1-http.md](../../lessons/act1-1.1-http.md) · **Script:** [hands-on-lab/act1-1.1-raw-http.py](../../hands-on-lab/act1-1.1-raw-http.py)
> **Recall:** [Think it through](../RECALL.md#act-1--step-1-http-basics)

## 🔑 Keywords in This Lesson

| Word | Plain meaning |
|---|---|
| **HTTP** | The agreed rules for one program to ask another for something and get an answer |
| **Request / Response** | The client's message ("give me / do this") / the server's reply |
| **URL** | Full address of a resource: scheme + host + path + query |
| **Method** | The verb of a request: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| **Header** | One line of information about the message: `Name: value` |
| **Body** | The data the message carries (JSON, HTML, an image...) |
| **Status code** | 3-digit result of the exchange: `200`, `404`, `500` |
| **Byte** | A number from 0 to 255; networks carry only bytes |
| **Stateless** | The server keeps no memory between requests |
| **Cookie** | A small named value the server asks the browser to store and send back automatically |

---
**What Does "HTTP" Literally Mean?**
`HyperText(hypertext is text with functionalities)`: In the 1980s, computer files were isolated islands on disks. "Hypertext" was the revolutionary concept of text containing hyperlinks to other documents. It allowed a reader to click a link in a document hosted on a server in Geneva and jump directly to a document hosted at Stanford.
`Transfer`: Moving those documents from the machine that stores them (the server) to the machine that wants to read them (the client).
`Protocol`: A strict, agreed-upon set of rules and grammar. Just like human diplomats follow protocol so both sides know who speaks first and what greetings mean, two programs need an unambiguous grammar so they don't misunderstand each other over a wire.
## 1. The Story So Far

The [anchor](../00-foundations/02-request-lifecycle.md) says step 1 is "the browser writes the message as text and turns it into bytes." This chapter opens that box. The message is ready at the end, but it holds only a **name** (`api.example.com`). Turning that name into an address is step 2, DNS.

## 2. The Problem: Strangers Need a Shared Format

A React app (JavaScript) and a FastAPI server (Python) were written separately, in different languages, on different machines. To cooperate, they need an agreed format for asking and answering. HTTP fixes four things:
* **who speaks first** (the client always asks),
* **what a request looks like,**
* **what a response looks like,**
* **how to report the outcome** (status codes).

Any client (browser, app, `curl`) can then talk to any server (Express, FastAPI, Nginx).

## 3. The Mental Model: A Form Letter

An HTTP message is a letter with a fixed layout: a **subject line** (what you want), **labels** (who it's for, what's inside, who you are), a **blank line**, then the **contents**. The reply uses the same layout, with a result code instead of a subject line.

## 4. Mechanics

### 4.1 The request: four parts

```http
GET /profile?tab=posts HTTP/1.1          ← ① request line: method, target, version
Host: api.example.com                    ← ② headers, one per line
Accept: application/json
                                         ← ③ empty line: "headers are over"
                                         ← ④ body (empty for GET)
```

A URL splits into those parts:

```text
  https://  api.example.com  /profile  ?tab=posts
  scheme    host             path      query
            → Host header    → request line
```

| Method | Usual meaning | Body? |
|---|---|---|
| `GET` | read | no |
| `POST` | create / perform an action | yes |
| `PUT` | replace | yes |
| `PATCH` | partly update | yes |
| `DELETE` | remove | usually no |

### 4.2 The response: same shape, different first line

```http
HTTP/1.1 200 OK                          ← ① status line: version, code, phrase
Content-Type: application/json           ← ② headers
Content-Length: 40
                                         ← ③ empty line
{"id":1,"name":"Rony","posts":["hello"]} ← ④ body
```

| Family | Meaning | Examples |
|---|---|---|
| `2xx` | worked | `200`, `201`, `204` |
| `3xx` | look elsewhere | `301`, `302`, `304` |
| `4xx` | client's mistake | `400`, `401`, `403`, `404` |
| `5xx` | server failed | `500`, `502`, `503`, `504` |

Programs read only the number; the phrase (`OK`) is for humans.

### 4.3 Text → bytes

Every character becomes a number from an agreed table (ASCII for English, UTF-8 for everything):

```text
G=71  E=69  T=84  space=32  /=47 ...   line ending \r\n = 13 10
Empty line between headers and body = 13 10 13 10
Bengali "ব" in UTF-8 = 3 bytes: 224 166 172
```

`Content-Length` counts **bytes**, not characters: `{"name":"রনি"}` is 14 characters but 20 bytes. The library (browser, `curl`, Axios) does the conversion and hands the bytes to the operating system.

### 4.4 Headers worth knowing now

| Header | Purpose |
|---|---|
| `Host` | Which site on that machine. **Required** in HTTP/1.1, because one server often hosts many sites. Missing → `400 Bad Request` |
| `User-Agent` | Which program is asking |
| `Accept` | Formats the client understands |
| `Content-Type` | Format of the body |
| `Content-Length` | Body size in bytes (where the body ends) |
| `Authorization` | Proof of identity, e.g. `Bearer <token>` |
| `Set-Cookie` / `Cookie` | "Remember this" / "here it is again" |

### 4.5 Stateless, yet logged in

The server forgets each request after answering, so **the client must send proof with every request**, as a header line:

```http
POST /login ...                →  HTTP/1.1 200 OK
                                  Set-Cookie: session=abc123; HttpOnly; Secure
GET /profile                   ←  the browser adds this itself:
Cookie: session=abc123
```

| | Cookie | Bearer token |
|---|---|---|
| Header | `Cookie:` | `Authorization: Bearer ...` |
| Attached by | the **browser**, automatically | **your code** |
| Created by | backend: `res.cookie(...)` writes `Set-Cookie` | backend returns it; frontend stores it |
| Typical use | refresh token in an `HttpOnly` cookie, session IDs | short-lived access token |

A cookie is a **delivery method**; a token is a **kind of proof**. A token can travel inside a cookie.

**What else cookies are used for:** login sessions (a session ID instead of a token), "remember me", preferences (theme, language), a guest's shopping cart, CSRF-protection values, A/B-test groups, cookie-consent choices, and analytics/advertising tracking. Two costs come with them: they're sent on **every** request to that site (keep them small; about 4 KB max each), and they're a security surface, which is why the flags exist.

### 4.6 HTTP vs. HTTPS

HTTPS is the **same message inside TLS**. It adds privacy (nobody on the path can read it), integrity (nobody can change it unnoticed) and identity (a certificate proves the server is who it claims). Plain HTTP (port 80) is still used for localhost development, inside private networks behind a load balancer, for the first redirect to HTTPS, and for some certificate checks. Anything public and user-facing should be HTTPS. *(Details: Act 6.)*

## 5. Hands-On & Developer Lab

* `curl.exe -v http://httpbin.org/get`: `>` lines are your request, `<` lines the response, `*` lines are curl's notes about later steps (DNS, connecting).
* Statelessness live: `curl.exe http://httpbin.org/cookies` returns `{"cookies": {}}`, while `curl.exe -b "session=abc123" http://httpbin.org/cookies` returns it, because now *you* sent the proof.
* DevTools (F12) → Network: inspect method, status and headers; Application → Cookies: the stored values.
* ⭐ **A1:** [hands-on-lab/act1-1.1-raw-http.py](../../hands-on-lab/act1-1.1-raw-http.py) sends a request written by hand over a socket. Remove `Host:` → `400`; path `/status/404` → `404`.

## 6. Pitfalls & Production Reality

* `200` means the exchange worked, not that your business logic did. Check the body.
* Mobile apps get `401` everywhere if the backend relies on cookies: no browser attaches them automatically.
* Cross-domain frontends must opt in to sending cookies: `credentials: "include"` (fetch) / `withCredentials: true` (Axios).
* Tokens in `localStorage` can be read by any malicious script on the page; `HttpOnly` cookies cannot.

🔵 **Later:** TCP (Act 4) · TLS and `Secure` cookies (Act 6) · keep-alive, HTTP/2/3, caching with `ETag`/`304` (Act 7) · CORS, `SameSite`, proxies, third-party cookies and tracking (Act 8).

## 7. Close the Loop

**Revisit Log:** `2026-10-13 | HTTP Basics | Step 1's message is text: request line, headers, empty line, body, turned into bytes. Proof of identity rides in every message (Cookie / Authorization) because HTTP remembers nothing.`

**Bridge forward:** the message says `Host: api.example.com`, but networks deliver to numbers, not names. **Next:** [DNS Resolution](01-dns-resolution.md) (Session 1.2).
