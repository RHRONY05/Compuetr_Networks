# Note Templates

Two sizes. Use **Full** for core topics a developer must truly understand. Use **Compact** for supporting topics. No LaTeX (`$...$`); use Unicode and code blocks.

---

# FULL CHAPTER TEMPLATE

```markdown
# [Topic Title]

> **Zooming into:** Step [N] of the [lifecycle](../00-foundations/02-request-lifecycle.md) · Act [X]
> **Prerequisites:** [previous chapter]
> **Key Goal:** [One sentence: what you can do/explain after this]

## 🔑 Keywords in This Lesson
Introduce every new word **here, at the top**, in plain language. A word is defined in the lesson that first needs it, never earlier. Add each word to [GLOSSARY.md](../GLOSSARY.md).

| Word | Plain meaning |
|---|---|
| [term] | [one-line meaning] |

---

## 1. The Story So Far
Where did the journey leave off, and why is this the next step? One short paragraph.

## 2. The Real-World Problem
The everyday problem, before any jargon. What breaks without this mechanism?

## 3. The Mental Model
A rich analogy (post office, apartment building, roads) that anchors the concept.

## 4. Deep Dive & Mechanics
Step-by-step flow, ASCII diagrams, bit/packet-level detail, worked example.

## 5. Hands-On & Developer Lab
* A concrete command or tool task (terminal, Wireshark, DevTools, code) and **what to look for** in the output.
* Developer impact: APIs, DB connections, Docker, cloud VPCs, performance, security.
* Project milestone link (A#), if any.

## 6. Pitfalls & Production Reality
* What videos simplified vs. reality.
* How this shows up as bugs/errors (`ECONNREFUSED`, `ETIMEDOUT`, 502, cert errors).

## 7. Active Recall
3–4 questions that test understanding, not memory. Answers in a collapsible `<details>` block.

## 8. Close the Loop
* **Revisit Log line** (also paste into the anchor note): "[date] | [this chapter] | what step N now means."
* **Bridge Forward:** what question this leaves open, and the next chapter link.
```

---

# COMPACT NOTE TEMPLATE

```markdown
# [Topic Title]

> **Zooming into:** Step [N] · Act [X] · [Back to anchor](../00-foundations/02-request-lifecycle.md)

**🔑 Keywords:** [term] = [meaning]; [term] = [meaning] *(add to GLOSSARY.md)*

## Big Idea
Two or three sentences.

## Where It Sits in the Story
What step it serves, what comes before and after.

## How It Works
Key mechanics, a small diagram, key terms in a table.

## Try It
One command or tiny code snippet, and what to look for.

## Recall
3 short questions (answers in `<details>`).

## Revisit Log line
"[date] | [this note] | what step N now means."
```
