---
title: "James Kettle — Pwning in Prod & How to do Web Security Research"
episode: 139
---


# Episode 139 James Kettle — Pwning in Prod & How to do Web Security Research

**Source:** Show notes (feed) — condensed.

### TL;DR
- CVE-2022-22720: Apache pause-based client-side desync via MITM.
- `TRACE` + `Max-Forwards` idea from ChatGPT.
- Research principles: hunt forgotten knowledge, collect diversity, no idea too stupid, abandon comfort.
- HTTP/2 in Burp: HP1-style view + Inspector for protocol control.
- AI = new automation; works better with human in loop.

### Key takeaways
- [ ] `TRACE` + `Max-Forwards` doubles TRACE effectiveness — found by ChatGPT.
- [ ] Burp Inspector: view pseudo-headers, inject duplicates for HTTP/2.
- [ ] Research collision: if building on promising work, publish immediately.
- [ ] Publish everything — microblogs > 6000-word papers.
- [ ] AI-powered scanning + human in loop = best results.

### Bugs and Findings

#### Apache Pause-Based Client-Side Desync via MITM — Client-side desync (CVE-2022-22720)
- **Root cause:** Apache 60s timeout. Attacker pauses request mid-way → timeout → remaining bytes = next request (desync).
- **Technique:** MITM with QDisc; Apache 60s timeout makes encrypted MITM viable.
- **Impact:** Client-side desync (high complexity).

#### Single Packet Attack — Race condition
- **Technique:** HTTP/2 multiplexing: all requests in one TCP packet → simultaneous arrival → reliable race conditions.
- **Impact:** Built into Burp Repeater as one-click button.

### Techniques and Primitives
- **Pause-based desync** — Partial headers → wait for timeout → second request as continuation.
- **TRACE + Max-Forwards** — Works on 2x more targets.
- **Single Packet Attack** — HTTP/2 race conditions via single-packet multiplexing.
- **Hunt forgotten knowledge** — 2004 whitepaper payloads work on modern CDNs.
- **No idea too stupid** — "The number one mistake is not trying."
- **Abandon comfort** — "Research what you're afraid of."

### Suggestions and Advices from Hunter
- "Publish everything, every tiny cool thing. Written down, not just in an X post."
- "If you see promising research to build on, publish immediately."
- "Research what you're afraid of."
- "Make it really easy to ask questions of your dataset. Even stupid questions."
- "Human + automation beats either alone."
- "AI is just a new kind of automation."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
CVE-2022-22720: Apache pause-based client-side desync via MITM.

#### 2. What you should learn
- Understand **[ ] `trace` + `max-forwards` doubles trace effectiveness — found by chatgpt**
- Understand **[ ] burp inspector: view pseudo-headers, inject duplicates for http/2**
- Understand **[ ] research collision: if building on promising work, publish immediately**
- Understand **[ ] publish everything — microblogs > 6000-word papers**
- Understand **[ ] ai-powered scanning + human in loop = best results**

#### 3. Core concepts explained
**Apache Pause-Based Client-Side Desync via MITM — Client-side desync (CVE-2022-22720)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Single Packet Attack — Race condition**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Pause-based desync**
- Partial headers → wait for timeout → second request as continuation.

**TRACE + Max-Forwards**
- Works on 2x more targets.

**Single Packet Attack**
- HTTP/2 race conditions via single-packet multiplexing.


#### 4. Techniques and tactics
**Pause-based desync**
- **What it is:** Partial headers → wait for timeout → second request as continuation.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**TRACE + Max-Forwards**
- **What it is:** Works on 2x more targets.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Single Packet Attack**
- **What it is:** HTTP/2 race conditions via single-packet multiplexing.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Hunt forgotten knowledge**
- **What it is:** 2004 whitepaper payloads work on modern CDNs.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**No idea too stupid**
- **What it is:** "The number one mistake is not trying."
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Publish everything, every tiny cool thing. Written down, not just in an X post."*
- *"If you see promising research to build on, publish immediately."*
- *"Research what you're afraid of."*
- *"Make it really easy to ask questions of your dataset. Even stupid questions."*
- *"Human + automation beats either alone."*
- *"AI is just a new kind of automation."*

#### 6. Mental models
- **Publish everything, every tiny cool thing. Written down, not** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you see promising research to build on, publish immediate** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Research what you're afraid of.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] `TRACE` + `Max-Forwards` doubles TRACE effectiveness — found by ChatGPT.
- **Try this:** [ ] Burp Inspector: view pseudo-headers, inject duplicates for HTTP/2.
- **Try this:** [ ] Research collision: if building on promising work, publish immediately.
- **Try this:** [ ] Publish everything — microblogs > 6000-word papers.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **DNS** — Domain Name System — translates domain names to IP addresses
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Apache Pause-Based Client-Side Desync via MITM — Client-side desync (CVE-2022-22720)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **CVE-2022-22720: Apache pause-based client-side desync via MITM.**
2. **[ ] `TRACE` + `Max-Forwards` doubles TRACE effectiveness — found by ChatGPT.**
3. **[ ] Burp Inspector: view pseudo-headers, inject duplicates for HTTP/2.**
