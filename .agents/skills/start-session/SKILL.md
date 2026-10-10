---
name: start-session
description: >
  Start a CN study session. Reads progress from the tracker, determines
  what day/week the student is on, and presents today's plan: which chai aur code's computer network
  lecture to watch, which Wireshark lab to do, and what hands-on practice
  to complete. Use at the beginning of every session in this workspace.
---

# Start Session Skill

## When to Activate

Activate this skill when:
- The student opens this workspace and starts a conversation
- The student says "start session", "what should I study today", "continue", or similar
- The student uses `/start-session`
- At the beginning of any CN learning conversation

## Execution Steps

### Step 1: Read Progress State

Read these files in order:
1. `course-memory/tracker.md` — current week, day, and completion status
2. `course-memory/roadmap.md` — the 6-week plan with daily breakdowns

### Step 2: Determine Today's Position

1. Check the `Current Position` section in `tracker.md` for the current week and day.
2. Look at the completion checkboxes for that day. If all items are checked, advance to the next day.
3. If the student is between days (e.g., finished yesterday, hasn't started today), suggest the next day's plan.

### Step 2.5: Auto-Fetch Transcripts for Today's Videos

For each video assigned to today in `tracker.md`:
1. Look up the video title and URL in `course-memory/video_index.md`.
2. Automatically run `python scripts/get_transcript.py "<VIDEO_URL>"` in the background to retrieve the English transcript.
3. Synthesize the transcript into a high-yield pre-flight breakdown.

### Step 3: Present the Session Briefing & Pre-Flight Explanations

Output a concise briefing in this format:

```
## 📍 Session Briefing — Week X, Day Y

**Status:** [X of 29 days completed] | [X of 5 weeks done]

---

### Today's Topic: [Topic Title]

For each assigned video:

#### 🎬 Video [N]: [Video Title]
- **Direct Link:** [YouTube URL]
- 🟢 **Core Concepts:** High-yield mental model and technical mechanics.
- 🟡 **Nuance & Simplification Alert:** What Hitesh simplified vs production / CUET syllabus.
- 🔵 **Deferred Concepts:** Terms mentioned in passing to ignore for now (saving time).

---

### 🔬 Hands-on Practice
[What terminal command or Wireshark inspection to run today]

---

### Next Steps
1. Read the breakdown above. If anything is unclear, watch the video (or target specific timestamps).
2. Ask any doubts.
3. Say "create note about [topic]" to generate notes.
4. Say "quiz me" for active recall.
5. Say "done for today" to mark progress in tracker.md.
```

### Step 4: Check for Overdue Items

If the student is behind schedule (current date is ahead of where they are in the plan):
- Do NOT panic or guilt-trip. Simply note it calmly:
  > "You're on Week X Day Y, which is [N days] behind the original schedule. No worries — the plan is flexible. Want to adjust the pace or catch up this week?"
- Offer to compress or skip lower-priority topics if needed.

### Step 5: Handle "Done for Today"

When the student says "done for today", "mark today complete", or similar:
1. Check the tracker for today's items
2. Mark completed items with `[x]`
3. Advance the current position to the next day
4. Show a quick progress bar:
   ```
   Week 1: ██████░░░░ 3/6 days
   Overall: █░░░░░░░░░ 3/36 days
   ```

### Step 6: Handle Catch-up and Skipping

If the student asks to skip a topic or compress multiple days:
- Topics from the CUET syllabus that Kurose covers lightly (ATM, Frame Relay, Token Ring, FDDI, Blockchain) can be compressed into brief note-taking sessions
- Core topics (TCP, IP, DNS, HTTP, subnetting, routing, ARP, TLS) should NOT be skipped
- Adjust the tracker accordingly

## Important Rules

- Deliver the pre-flight tiered breakdown for today's assigned videos so the student grasps the big picture before or alongside watching.
- Your role is: synthesizer, doubt-resolver, note-taker, developer-angle explainer, quiz-giver.
- If the student asks a question about a topic, answer it deeply with developer context — but keep them focused without lecturing too far ahead of today's scope.
- Always check if Wireshark is installed before assigning a Wireshark lab for the first time.
