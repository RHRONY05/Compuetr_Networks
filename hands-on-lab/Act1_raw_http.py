import socket

# A "socket" is a phone line from your program to a program on another machine.
# How it works is Act 4. Today, just use it: open, send text, read the reply.
sock = socket.create_connection(("httpbin.org", 80))

request = (
    "GET /get HTTP/1.1\r\n"          # ① request line
    "Host: httpbin.org\r\n"          # ② headers...
    "User-Agent: raw-socket/1.0\r\n"
    "Accept: */*\r\n"
    "Connection: close\r\n"          #    "close the line after answering" (🔵 Act 7)
    "\r\n"                           # ③ the empty line: headers are over
)

sock.sendall(request.encode("ascii"))   # text → bytes (Part 4!)

response = b""
while True:
    chunk = sock.recv(4096)          # read the reply in pieces
    if not chunk:                    # the server closed the line: we're done
        break
    response += chunk
sock.close()

print(response.decode("utf-8"))       # bytes → text