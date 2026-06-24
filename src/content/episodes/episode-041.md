---
title: "Mini Masterclass — Attack Vector Ideation"
episode: 41
---


# Episode 41 Mini Masterclass — Attack Vector Ideation

### TL;DR
- Framework for generating endless attack vectors when stuck on a web app
- Use the app "like a human, not like a hacker" — learn user journeys
- Read documentation for "CANNOT" statements — they mark security boundaries to test
- Look at grayed-out UI areas, API responses for hidden/legacy fields, differences between accounts, and paywalls

### Key takeaways
- First step: proxy all traffic but don't look at it — just use the app end-to-end as a user
- Dump docs to eReader and read them like a book; annotate every "CANNOT", limit, or boundary
- "If documentation says X user cannot do Y, and you can do Y, that's a vulnerability"
- Re-enable disabled UI elements (bookmarklet: find every `disabled` / `hidden` and remove the attribute)
- Look at API responses for data not shown in the UI — indicates legacy features, hidden attack surface
- Compare UI between admin and non-admin accounts to understand client-side permission hints
- Pay for premium — 20-30 investment can yield 2-3k+ bugs

### Techniques and Primitives
- **Nose testing** (Douglas Day / Archangel) — find things you "shouldn't be able to do" and try them
- **RBAC matrixing** — create a matrix of roles vs endpoints/actions; test cross-role access
- **Client-side path analysis** — once you understand how the app identifies user tier client-side (e.g. a JS variable `isAdmin`), replicate it on your account

### Tooling and Resources
- **Douglas Day (Archangel)** NahamCon 2023 talk on "Nose"
- **JavaScript bookmarklet** to undisable hidden/disabled elements
- **Burp/Kaide match-and-replace** to remove `disabled` from HTML responses

### Suggestions and Advices from Hunter
- "Oftentimes when I'm brain-fried, I export the documentation to PDF, put it on my eReader, and read it from a hammock"
- "If you can reference a specific line of documentation that says 'X user cannot do Y,' it is very hard for the program to debate the issue"
- "Even low/medium bugs are worth submitting — don't let deter you"

### AI Takeaway
The "CANNOT statement" enumeration is one of the highest-leverage, least-sexy techniques. It transforms documentation from a reference into a threat model.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Framework for generating endless attack vectors when stuck on a web app

#### 2. What you should learn
- Understand **first step: proxy all traffic but don't look at it — just use the app end-to-end as a user**
- Understand **dump docs to ereader and read them like a book; annotate every "cannot", limit, or boundary**
- Understand **"if documentation says x user cannot do y, and you can do y, that's a vulnerability"**
- Understand **re-enable disabled ui elements (bookmarklet: find every `disabled` / `hidden` and remove the attribute)**
- Understand **look at api responses for data not shown in the ui — indicates legacy features, hidden attack surface**

#### 3. Core concepts explained
**Nose testing (Douglas Day / Archangel)**
- find things you "shouldn't be able to do" and try them

**RBAC matrixing**
- create a matrix of roles vs endpoints/actions; test cross-role access

**Client-side path analysis**
- once you understand how the app identifies user tier client-side (e.g. a JS variable `isAdmin`), replicate it on your account


#### 4. Techniques and tactics
**Nose testing (Douglas Day / Archangel)**
- **What it is:** find things you "shouldn't be able to do" and try them
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**RBAC matrixing**
- **What it is:** create a matrix of roles vs endpoints/actions; test cross-role access
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Client-side path analysis**
- **What it is:** once you understand how the app identifies user tier client-side (e.g. a JS variable `isAdmin`), replicate it on your account
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Oftentimes when I'm brain-fried, I export the documentation to PDF, put it on my eReader, and read it from a hammock"*
- *"If you can reference a specific line of documentation that says 'X user cannot do Y,' it is very hard for the program to debate the issue"*
- *"Even low/medium bugs are worth submitting"* — **don't let deter you**

#### 6. Mental models
- **Oftentimes when I'm brain-fried, I export the documentation ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you can reference a specific line of documentation that s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Even low/medium bugs are worth submitting — don't let deter ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** First step: proxy all traffic but don't look at it — just use the app end-to-end as a user
- **Try this:** Dump docs to eReader and read them like a book; annotate every "CANNOT", limit, or boundary
- **Try this:** "If documentation says X user cannot do Y, and you can do Y, that's a vulnerability"
- **Try this:** Re-enable disabled UI elements (bookmarklet: find every `disabled` / `hidden` and remove the attribute)

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Framework for generating endless attack vectors when stuck on a web app**
2. **First step: proxy all traffic but don't look at it — just use the app end-to-end**
3. **Dump docs to eReader and read them like a book; annotate every "CANNOT", limit, **
