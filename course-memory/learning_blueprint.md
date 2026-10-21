# Autonomous Learning Blueprint & Study Engine Playbook

> **Purpose:** This file documents the meta-learning methodology, workflow architecture, and evolving solutions developed in this workspace. It serves as a persistent brain across chat sessions and a plug-and-play blueprint to replicate this learning engine for any future course, programming language, or technical domain.

---

## 1. The Core Learning Philosophy

1. **The Inverted Classroom (Pre-Flight Briefing):**
   * Traditional learning: Passively watch a 30-minute video, get confused, then search for answers.
   * **Our Blueprint:** The AI automatically extracts the video transcript and provides a structured **2-minute pre-flight briefing** with high-yield mental models *before* the student watches. The student reads the briefing first, then optionally watches the video at 1.5x/targeted timestamps for visual reinforcement.

2. **Tiered Concept Tagging (Anti-Rabbit-Hole Protection):**
   * 🟢 **Level 1 (Core Today):** The high-yield mental model and mechanics needed right now.
   * 🟡 **Level 2 (Nuance & Simplification Alert):** What video tutorials hand-wave or simplify vs. real-world production and exam expectations.
   * 🔵 **Level 3 (Deferred / Future Scope):** Buzzwords mentioned in passing that the student can safely ignore for now.

3. **Grounding in Local Machine Reality:**
   * Never leave concepts in abstract theory. Immediately verify them on the student's actual hardware using terminal tools (`ipconfig`, `Get-NetIPAddress`, `curl -v`, `Get-NetRoute`). Seeing `192.168.0.104/24` on their own Wi-Fi card makes the concept click permanently.

4. **Tutorial Handbook over Sparse Revision Notes:**
   * Notes should not just be quick personal cheat sheets. They are written as **self-contained tutorial chapters** that anyone can read sequentially from scratch.
   * Every chapter must have:
     * *The Story So Far* (bridge from previous chapter)
     * *Real-World Mystery* (everyday relatable problem)
     * *Deep Dive Mechanics & ASCII diagrams*
     * *Hardware / Developer Lab*
     * *Collapsible Self-Check Quizzes*
     * *The Bridge Forward* (link to next chapter using portable relative links)

5. **The Story Spine (Anchor + Zoom-ins):**
   * One end-to-end story (for networks: the life of an HTTP request) is written first as an **anchor note** with a numbered journey map, a "You Are Here" status table, and a **Revisit Log**.
   * Every other chapter opens with a zoom-in banner ("Zooming into step N") and closes by adding a line to the Revisit Log. Learning is a circle: each pass makes the anchor richer.
   * The study order is the story order, not the order of any single video playlist.

6. **Best Source Per Topic, Not One Playlist:**
   * Videos are interchangeable raw material because AI reads the transcript. Pick whichever source explains a topic best (developer-oriented playlist vs. academic lectures vs. AI-explained gaps) and tag each (`C##`, `K#.#`, AI).
   * Check source coverage against the plan early: a playlist can silently miss whole areas.

7. **Hands-On and Build Every Session:**
   * Each session runs something on the student's own machine and grows a small **project thread** ("Build the Stack"), so concepts become code and captures, not just text.

8. **Developer-First, No Deadline:**
   * Depth where it helps reason about real systems; brevity elsewhere. Progress is measured in completed acts, not dates. By-hand numericals are understanding tools, not exam targets.

---

## 2. Tooling Architecture & Infrastructure

* **Automated Headless Transcription:**
  * Script: `scripts/get_transcript.py`
  * Powered by local `yt-dlp` using Python `tempfile.TemporaryDirectory()`.
  * Auto-extracts clean English subtitle text directly into memory/temp storage and cleans up with zero workspace clutter.
* **Single-File Live Lecture Preview (`playground.md`):**
  * The AI writes active lesson explanations directly into `playground.md` in the workspace root.
  * The student keeps `playground.md` open in Markdown Preview (`Ctrl+K V` or side-by-side preview).
  * **Zero LaTeX Math Syntax:** Never use `$...$` or `$$...$$` or raw TeX macros. Use clean Unicode characters (`→`, `×`, `^`, `≈`) and code blocks so preview renders flawlessly in any editor.
* **Master Video Index (`course-memory/video_index.md`):**
  * Catalogs all course videos with titles and direct URLs for rapid lookup.
* **Master Reading Guide (`notes/README.md`):**
  * An index linking all chapters using portable relative markdown links.

---

## 3. Journey Log & Solved Friction Points

### Days 1 & 2 (Foundations, Request Lifecycle & IP Addressing)
* **Problem 1 (Passive Video Watching Friction):** Student spent too much time watching videos without knowing what mattered.
  * *Solution:* Inverted the workflow. Automated transcript fetching via `yt-dlp` and created pre-flight tiered summaries.
* **Problem 2 (LaTeX Rendering Broken in IDE Preview):** Raw `$$...$$` and `\mathbf` appeared as ugly unrendered text in the editor.
  * *Solution:* Banned LaTeX math syntax workspace-wide. Replaced with Unicode characters (`→`, `×`, `^`) and code blocks. Established `playground.md` as the dedicated preview canvas.
* **Problem 3 (Isolated Revision Notes vs. Cohesive Tutorial):** Notes felt like sparse personal summaries that assumed prior context and lacked narrative flow.
  * *Solution:* Restructured all notes into a sequential **Developer Tutorial Handbook** with "The Story So Far" and "What's Next" relative links.
* **Problem 4 (Mental Disconnect Between LAN, Wi-Fi, and Internet):** Confusion regarding why every home router has `192.168.0.1` and what "the Wi-Fi box" actually is.
  * *Solution:* Developed the **Global Postal / Office Desk Analogy** (Private vs. Public IPs) and demystified the home box as three distinct components: Access Point (antenna) + Switch (Layer 2 local) + Router Engine (Layer 3 Internet gateway).

### Day 2 Evening (2026-10-11): Re-architecting the Plan Around a Story
* **Problem 5 (Topics Felt Disconnected):** Following a topic-ordered playlist, IP/subnet/gateway/ARP felt like separate lessons. The request-lifecycle note had skipped the "local or remote?" decision that links them.
  * *Solution:* Rewrote the lifecycle note as the course **anchor** (8-step journey, "You Are Here" map, Revisit Log, the missing decision step, the return trip). Rebuilt the roadmap into 9 Acts that follow the journey.
* **Problem 6 (Source Lock-In):** The plan was tied to one playlist that turned out to cover only part of the topic space, and the old tracker's later video numbers did not match the real catalog (no proxy/load-balancer/CDN/VPN videos existed).
  * *Solution:* Audited both playlists, indexed the Kurose lectures (Ch1–6 have videos; none found for Ch7–8), and assigned sources per topic. Transcripts work for both, which removed the accent barrier that originally pushed the student away from Kurose.
* **Problem 7 (Reading vs. Doing):** Transcript-plus-AI learning risks passive understanding and loses diagrams.
  * *Solution:* Added a hands-on step to every session, a project thread (A1–A9), optional Packet Tracer, and AI-built interactive visualizers; kept the daily recall check.
* **Decision:** Dropped exam-centric framing. The plan is developer-first with no end date; the syllabus is kept as a coverage appendix only.

### Day 3 (2026-10-13): Lesson Quality, Versions and Archives
* **Problem 8 (Correct but un-learnable lessons):** A lesson named mechanisms (cookies, tokens) before the problem they solve, mixed in later-act jargon, and had a factual error (port 443 "plaintext"). The student "couldn't feel the picture".
  * *Solution:* A written **Lesson Writing Standard** + **self-review checklist** in AGENTS.md, and a concrete **reference lesson** (`.agents/examples/lesson-1.1-http.md`). Pattern: problem → real worked example → name → developer link; 🔵 "Later (Act N)" boxes; verified real outputs.
* **Problem 9 (Silent tool bug):** `get_transcript.py` printed only the first 3,000 characters, so every briefing was built from a video's first ~3 minutes; it also missed `en-orig` captions.
  * *Solution:* Print the full transcript; request `en-orig` first. Lesson: verify the tools the method depends on.
* **Problem 10 (Losing versions and clutter):** Rewrites overwrote earlier lessons; scripts were pasted into lessons.
  * *Solution:* Old versions go into collapsed `<details>` blocks; finished lessons are archived to `lessons/`; scripts live in `hands-on-lab/act<N>-<session>-<name>`.

### Day 4 to 6 (2026-10-14 to 10-18): Session 1.2 DNS, and the first GUI tool
* **Problem 11 (Abstract analogy + vague deployment story):** Part 4 said "your domain needs a website address and email and proof for Google", and the student couldn't tell why Google appeared. Their own bought domain (`rhrony05.me`) was an unexplained black box.
  * *Solution:* Ran the DNS script against **the student's own domain** and rebuilt the explanation on it (registrar vs DNS host vs web host, their real MX and TXT records). Examples from the student's own machine and own output land much better than invented ones.
* **Problem 12 (Byte-level before picture):** Part 6 (DNS message format) began with bytes and used UDP/TCP before giving any picture.
  * *Solution:* Rewrote it with two pictures (a form with a ticket ID; a postcard vs a phone call) and moved the byte counting into a collapsed `<details>`.
* **Problem 13 (Parking Lot too late):** The student wanted to know what belongs to later acts *before* reading. Moved the 🔵 Parking Lot to right after Keywords and made that the standard (AGENTS.md item 5).
* **Problem 14 (Wireshark: a GUI tool taught as a block of instructions):** Lab F listed 7 steps at once and assumed the student knew the tool. They could not find where to "run a DNS lookup" (Wireshark can't; it only records), and the first single step ("compare these two rows' ticket numbers") gave no action, so it was unclear what to do and why. They said it became boring enough to make them leave the lesson.
  * *What failed:* (1) a pile of instructions with no order; (2) never saying what the tool IS and what it can't do; (3) an observation task instead of an action; (4) naming screen areas the student could not locate.
  * *Solution (rule for every new GUI/CLI tool):* give ONE experiment at a time in the form **"1. In window A, do exactly this. 2. In window B, look at exactly this place. 3. You should see exactly this."**, state which window does what before the first step, point at the real rows/columns from the student's own screenshot, and wait for the reply before the next step. Only write the full lab into the lesson after it has been walked through successfully once.
* **Problem 15 (Note shorter than the lesson):** The DNS note was written as a dense digest: diagrams dropped (the name tree, the walk picture), explanations cut to one line. The student found the lesson clearer than the note, which defeats the purpose of a handbook.
  * *Cause:* copying the compact style of the HTTP note, and a rule that warned "note-writing is the main time sink".
  * *Solution:* a full chapter keeps every explanation, diagram and real example from the lesson, plus the session's Q&A; only session scaffolding is dropped. Rule added to AGENTS.md (Note Rules). The DNS note was rewritten on that basis.
* **Process note:** the Anthropic-side memory is not where the study approach lives. Every approach change that works or fails gets logged HERE (the start-session skill's "Done for today" step also says so).

* **Decision (2026-10-18): notes vs recall, and when notes are written.** Notes are tutorial chapters written **after** a finished session, when the student asks, built from the lesson **and** the session's questions/confusions/answers, merged (not appended). Recall moved out of notes into one file, `notes/RECALL.md` (5–8 think-through questions per chapter), updated in the same step, so the student never has to ask for it. The Compact note type was dropped. AGENTS.md was rewritten (≈200 → 123 lines) to remove duplication with the start-session skill.

### Day 7–8 (2026-10-19 to 10-21): Session 1.3 IP & CIDR, Act 1 closed
* **What worked:** building the lesson entirely from the student's own machine: Wi-Fi `192.168.0.102/24`, the WSL adapter `172.19.160.1/20` (a real non-octet prefix), `ping 3232235521` → `192.168.0.1` (proof that an IP is one number), and the "172 trap" using `example.com`'s address from the DNS session. The student's own question ("is WSL's IP assigned by Windows?") came straight out of that data and was answered with output from inside Ubuntu.
* **Student preference:** when they feel a topic is clear and the remaining questions belong to later lessons, they move on rather than doing every lab step. Don't force each lab; keep the practice for a dedicated wrap-up (here: Wireshark lab + quiz at the end of the act).
* **Problem 16 (tutor's test polluted the student's cache):** checking `curl wikipedia.org` before a cache experiment cached the name on the student's laptop (the tutor runs on the same machine), which would have spoiled the "first run shows DNS" step. *Solution:* never pre-run a name the student will use in a cache experiment; give a fresh name (`bn.wikipedia.org`).
* **Process note:** a paused session's lesson was archived early (1.2 → `lessons/`) so the next lesson could use `playground.md`; its open items stay as checkboxes in the tracker.

### Upcoming Challenges & Roadmaps
* **Day 6 (Visual Wireshark Labs without Screen Access):** Transcripts cannot capture Wireshark packet bytes on screen. 
  * *Anticipated Solution:* Pre-load Kurose & Ross sample trace files (`.pcap`) and analyze them with terminal inspection tools (`tshark` or python `scapy`) alongside Wireshark walkthroughs.

---

## 4. Replication Blueprint for Future Courses

To spin up this exact autonomous learning environment for any new subject (e.g. Operating Systems, Distributed Systems, Rust):

1. **Create the workspace structure:**
   ```text
   .agents/
     ├── AGENTS.md (Tutor instructions, teaching rules, handbook rules)
     └── skills/start-session/SKILL.md (Session bootstrap logic)
   course-memory/
     ├── tracker.md (Current act/session & checkboxes)
     ├── roadmap.md (Story-based acts: sources, hands-on, project milestones)
     ├── video_index.md (All candidate video sources, tagged)
     └── learning_blueprint.md (Meta-learning journal)
   notes/
     ├── README.md (Book table of contents in reading order)
     ├── NOTE_TEMPLATE.md (Full + Compact templates, zoom-in banner)
     ├── 00-foundations/02-request-lifecycle.md (THE ANCHOR: journey map, You Are Here, Revisit Log)
     └── [Layered/Modular Folders]
   playground.md (Live study canvas)
   scripts/get_transcript.py (yt-dlp automated transcript fetcher)
   ```
2. **Bootstrap Prompt for Future AI:**
   > *"I am starting a self-study course for [Course Name]. Read `course-memory/learning_blueprint.md`. Adopt the Inverted Pre-Flight Briefing workflow, maintain `playground.md` as my live preview canvas, auto-fetch lecture transcripts, and write all revision notes as interconnected handbook chapters following `NOTE_TEMPLATE.md`."*
