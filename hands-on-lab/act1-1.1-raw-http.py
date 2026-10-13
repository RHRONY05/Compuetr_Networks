"""
Act 1 · Session 1.1 · Milestone A1: send an HTTP request by hand.

Lesson: lessons/act1-1.1-http.md, Part 8.
Run:    python hands-on-lab/act1-1.1-raw-http.py

Proves that HTTP/1.1 is just text: we write the request ourselves,
turn it into bytes, send it, and print the reply.
"""
import socket

# A "socket" is a phone line from your program to a program on another machine.
# How it works is Act 4. Today, just use it: open, send text, read the reply.
sock = socket.create_connection(("httpbin.org", 80))

request = (
    "GET /get HTTP/1.1\r\n"          # 1. request line   (experiment: try /status/404)
    "Host: httpbin.org\r\n"          # 2. headers...     (experiment: delete this line)
    "User-Agent: raw-socket/1.0\r\n"
    "Accept: */*\r\n"
    "Connection: close\r\n"          #    "close the line after answering" (Act 7)
    "\r\n"                           # 3. the empty line: headers are over
)

sock.sendall(request.encode("ascii"))   # text -> bytes

response = b""
while True:
    chunk = sock.recv(4096)          # read the reply in pieces
    if not chunk:                    # the server closed the line: we're done
        break
    response += chunk
sock.close()

print(response.decode("utf-8"))       # bytes -> text
