# Note Template

One kind of note: a **tutorial chapter**, written after a session from the lesson **and** the session's questions (see "Note Rules" in [AGENTS.md](../AGENTS.md)). Its length follows the topic: a small topic gives a short chapter, never a digest. No LaTeX; use Unicode and code blocks. Recall questions go in [RECALL.md](RECALL.md), not in the note.

```markdown
# [Topic Title]

> **Zooming into:** Step [N] of the [lifecycle](../00-foundations/02-request-lifecycle.md) · Act [X]
> **Prerequisites:** [previous chapter]
> **Key Goal:** [one sentence: what you can do or explain after this]
> **Lesson:** [lessons/act<N>-<session>-<name>.md] · **Script:** [hands-on-lab/...] · **Recall:** [RECALL.md#section]

## 🔑 Keywords in This Lesson
| Word | Plain meaning |
|---|---|
| [term] | [one line, plain language; also add to GLOSSARY.md] |

---

## 1. The Story So Far
Where the journey left off, and why this is the next step.

## 2. The Real-World Problem
What breaks or is impossible without this idea, before any jargon.

## 3. The Mental Model
An analogy that anchors the whole chapter.

## 4. Deep Dive & Mechanics
As many subsections as the topic needs. Each: problem → real worked example (student's own data where possible)
→ the name and the rule → developer connection. Keep every diagram and table from the lesson.
Answer the student's session questions where they arise. Byte-level detail in a collapsed <details>.
🟡 reality checks inline.

## 5. Hands-On & Developer Lab
What each tool shows and what to look for (a table works well); the build script and its run command;
developer impact (deployments, debugging, Docker, cloud).

## 6. Pitfalls & Production Reality
Common errors this step causes (`ENOTFOUND`, `ECONNREFUSED`...), what videos simplify.
🔵 Later: one line listing later-act topics and their acts.

## 7. The Moral of the Story (One-Look Mindmap)
A 30-second visual ASCII mindmap/flow that sits at the end of the chapter to consolidate everything into memory:
- **The Core Question:** The exact physical/architectural mystery this chapter solved.
- **The Step-by-Step Flow:** The 4-6 sequential steps of the mechanism.
- **The Golden Rule:** The one durable takeaway.

## 8. Close the Loop
* **Revisit Log line** (also added to the anchor): "[date] | [chapter] | what step N now means."
* **Bridge forward:** the open question, and the next chapter's link.
```
