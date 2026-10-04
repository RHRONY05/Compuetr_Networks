---
name: start-session
description: >
  Start a CN study session. Reads progress from the tracker, determines
  what day/week the student is on, and presents today's plan: which Kurose
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

### Step 3: Present the Session Briefing

Output a concise briefing in this format:

```
## 📍 Session Briefing — Week X, Day Y

**Status:** [X of 36 days completed] | [X of 6 weeks done]

### Today's Plan

🎬 **Watch:** [Kurose lecture section — e.g., "Ch1: 1.1–1.3 (Internet, network edge, network core)"]
- Lecture URL: [direct link to Kurose chapter videos page]

🔬 **Hands-on:** [What to practice — e.g., "Wireshark Getting Started lab" or "Run tracert google.com"]
- Lab PDF: [direct link if applicable]

🛠️ **Mini-project:** [If one is assigned for today/this week]

### When You're Done Watching

Come back and:
1. Ask me about anything that confused you
2. Say "create note about [topic]" for revision notes
3. Say "quiz me" for active recall check
4. Say "done for today" and I'll update the tracker
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

- Never start teaching a topic unprompted. The student watches Kurose lectures first, then comes to you.
- Your role is: doubt-resolver, note-taker, developer-angle explainer, quiz-giver.
- If the student asks a question about a topic, answer it deeply with developer context — but don't lecture ahead of where they are in the videos.
- Always check if Wireshark is installed before assigning a Wireshark lab for the first time.
