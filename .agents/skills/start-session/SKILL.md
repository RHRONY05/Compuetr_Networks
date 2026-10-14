---
name: start-session
description: >
  Start a Computer Networks study session. Reads progress from the tracker,
  finds the current act and session, anchors it in the lifecycle story, fetches
  transcripts for the session's videos, and presents a pre-flight briefing with
  a hands-on task. Use at the beginning of every session in this workspace.
---

# Start Session Skill

## When to Activate

- The student opens this workspace and starts a conversation
- The student says "start session", "what should I study today", "continue", or similar
- The student uses `/start-session`
- At the beginning of any CN learning conversation

## Execution Steps

### Step 1: Read Progress State

Read in order:
1. `course-memory/tracker.md`: current act and session, completion status
2. `course-memory/roadmap.md`: the session's sources, hands-on and project milestone
3. `notes/00-foundations/02-request-lifecycle.md`: the anchor note (for the "You Are Here" map and Revisit Log)

### Step 2: Determine Today's Position

1. Read `Current Position` in the tracker (act + session).
2. If all of that session's items are checked, advance to the next session.
3. If the student's request differs from the plan (curiosity detour, a doubt), answer it, locate it in the story, then offer to return.

### Step 2.5: Fetch Transcripts

For each video tagged in the session (`C##` Chai, `K#.#` Kurose):
1. Look up the URL in `course-memory/video_index.md`.
2. Run `python scripts/get_transcript.py "<URL>"`. The full transcript is saved to `.agents/transcripts/<video id>.md` in 30-minute parts; read **all** parts of the file (use `--part-minutes N` to change the size).
3. Synthesize into a high-yield pre-flight breakdown.
4. If a topic has no video (tag **AI**), prepare the explanation yourself.

### Step 3: Present the Session Briefing

```
## 📍 Session Briefing: Act X · Session X.Y
**Progress:** N of 33 sessions · Act X: <name>

### 🗺️ Where we are in the story
Lifecycle step N: "<the question this step answers>"
Last time: <where we ended>. Today: <what we zoom into>. Next: <what follows>.

### 🔑 Keywords we meet today
Each new word with a one-line plain meaning. Introduce words here, just before they are needed; do not explain terms from later acts.

### 🎬 Today's sources
- C## <title> <link> | K#.# <title> <link> | AI-explained: <topic>

### 🟢 Core concepts
Mental model + mechanics for today, tied to the story.
### 🟡 Nuance & simplifications
What the videos simplify vs how production actually works.
### 🔵 Deferred
Buzzwords to recognize and park.

### ⭐ Hands-on & Build
Terminal / Wireshark / DevTools task (what to run, what to look for).
Project milestone for this act (A#), if scheduled.

### Next Steps
1. Read the briefing; watch targeted sections only if something is unclear.
2. Do the hands-on task.
3. Ask doubts. Say "create note about <topic>" for notes, "quiz me" for recall.
4. Say "done for today" to update progress.
```

Then write the full lesson into `playground.md` following the **Lesson Writing Standard** in `.agents/AGENTS.md` (reference: `.agents/examples/lesson-1.1-http.md`). Put any scripts in `hands-on-lab/` (`act<N>-<session>-<name>`), run every command and script before including it, and complete the **self-review checklist** before telling the student the lesson is ready.

### Step 4: Check Pace Calmly

The plan has no deadline. If the student is slow or has been away, do not guilt-trip. Offer to resume, shorten sessions (trim BUILD or NOTE, never RECALL, ANCHOR or HANDS-ON), or re-run a quick recall of the last session.

### Step 5: Handle "Done for Today"

1. Mark completed items `[x]` in the tracker; advance Current Position.
1b. Archive the lesson: move `playground.md` to `lessons/act<N>-<session>-<name>.md` (fix relative links), reset `playground.md` to a placeholder for the next session (see "Lesson files and versions" in AGENTS.md).
2. Ensure the anchor note has a **Revisit Log** entry for any note finished today and the "You Are Here" status is current.
3. Show progress, e.g. `Act 4: ██░░░░ 2/6 · Overall: 9/33`.

   When recapping "last time", use the **act and session names exactly as written in the tracker** and only what the tracker marks done. Never merge sessions from different acts into one recap.
4. Log any workflow breakthroughs or friction points in `course-memory/learning_blueprint.md`.

### Step 6: Handle Skipping and Detours

- Core developer topics (DNS, HTTP, TCP/UDP, IP and subnets, ARP, routing basics, NAT, TLS, HTTP/2/3, proxies/load balancers) should not be skipped.
- Legacy or niche items (ATM, Frame Relay, Token Ring, FDDI, HDLC, PPP, MPLS, Mobile IP, Blockchain) are on request only: brief AI notes.
- Adjust the tracker accordingly.

## Important Rules

- Always anchor to the story at the start and close the loop (Revisit Log) at the end.
- Pre-flight first, video second. The student should know what matters before spending time.
- Always give a hands-on task; verify tools (Wireshark, Docker, Python) are installed before first use.
- Answer doubts deeply with a developer angle, but do not lecture far ahead of today's scope.
- No LaTeX in any output.
