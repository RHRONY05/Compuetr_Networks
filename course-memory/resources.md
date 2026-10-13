# Computer Networks Resources

## Principle

Choose the **best source per topic**, not one fixed playlist. No resource-browsing during sessions: if a sub-topic does not click, the AI explains it, or points to ONE short targeted source, then you return to the act.

## Video Sources (catalog in [video_index.md](video_index.md))

* **Chai aur Computer Network** (Chai aur Code), 49 videos, tag `C##`. Strength: developer angle, Wireshark demos, HTTP/2/3, TLS, NAT, IP anatomy.
  * Playlist: https://youtube.com/playlist?list=PLd1s-PEC5Pio&si=R6xQAoPXt29Fm_Ji
* **Kurose & Ross official lectures**, Ch1–6, tag `K#.#`. Strength: structure, principles, routing, link layer.
  * Pages: https://gaia.cs.umass.edu/kurose_ross/videos/1 (through /6). No official videos found for Ch7 (Wireless) or Ch8 (Security).
* **Transcripts:** `python scripts/get_transcript.py "<URL>"` (uses local `yt-dlp`; works on both sources).

## Hands-On & Visualization

* **Terminal:** `curl -v`, `ipconfig /all`, `route print`, `arp -a`, `tracert`, `nslookup`, `netstat -ano`, `ping`
* **Wireshark:** packet capture and analysis. Kurose lab sheets: https://gaia.cs.umass.edu/kurose_ross/wireshark.php · Trace files: https://www-net.cs.umass.edu/wireshark-labs/wireshark-traces-9e.zip
* **Browser DevTools → Network:** protocol column (`http/1.1`, `h2`, `h3`), waterfall, timing, headers
* **Python:** `socket`, `ssl` (and optionally `scapy`) for the project thread
* **OpenSSL:** `openssl s_client -connect host:443`, self-signed certificates
* **Docker / Docker Compose:** network labs and the A9 reverse-proxy project
* **Cisco Packet Tracer** (optional, free): simulate switches, subnets and routing visually
* **Interactive visualizers:** small HTML pages the AI builds on request (subnet calculator, TCP handshake stepper, routing-algorithm stepper)
* **Kurose animations:** https://gaia.cs.umass.edu/kurose_ross/animations.php
* **How DNS Works (interactive):** https://howdns.works/

## Reference Only

* [syllabus.md](syllabus.md): university syllabus, used as a coverage checklist (see roadmap appendix).
* **Kurose & Ross, *Computer Networking: A Top-Down Approach*:** book and slides, for depth where videos are missing.
