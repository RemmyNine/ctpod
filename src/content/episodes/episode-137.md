---
title: "How We Do AI-Assisted Whitebox Review, New CSPT Gadgets, and Tools from SLCyber"
episode: 137
---


# Episode 137 How We Do AI-Assisted Whitebox Review, New CSPT Gadgets, and Tools from SLCyber

**Source:** Show notes (feed) — condensed.

### TL;DR
- Justin's AI code review: Gemini CLI analyzes SDK, identifies security controls via test files.
- CSPT + Cache Deception: chain CSPT to cache authenticated response → retrieve from CDN.
- Searchlight Cyber Tools website: hosted NewTowner, NoWafPlease, wordlists.
- Slice (Caleb Gross): CodeQL + LLM → found Linux kernel CVE-2025-37778.
- Ebka (Slonser): MCP-based Caido plugin.

### Key takeaways
- [ ] AI code review: analyze test files first — they reveal valued security controls.
- [ ] CSPT + Cache Deception: append `.css` to force cache of authenticated response.
- [ ] ch.at: ChatGPT over `dig` TXT, SSH, curl — works on planes (only DNS).
- [ ] NoWafPlease: inflate request size to bypass WAFs.
- [ ] `postMessage` targetOrigin: check for `origin.endsWith()` flaws.

### Bugs and Findings

#### CSPT + Cache Deception — Cache poisoning
- **Technique:** CSPT controls victim's URL path; append `.css` → CDN caches authenticated response.
- **Key detail:** Victim's credentials auto-included; CDN sees cacheable `.css` extension.

#### Code Assist OAuth postMessage Bypass — OAuth leak
- **Root cause:** `origin.endsWith("codesys.google.com")` → attacker registers `attacker.codesys.google.com`.
- **Impact:** $20k — OAuth code theft → ATO.

### Techniques and Primitives
- **Test file analysis** — AI analyzes tests to identify security controls.
- **Adjacent vulnerability discovery** — Find control → search for similar functions missing it.
- **dig over DNS for LLM** — `dig ch.at TXT "query"` on planes.
- **Slice (CodeQL + LLM)** — Automated CodeQL query writing + LLM ranking.
- **Ebka (Caido MCP)** — Control Caido from Claude Code.

### Suggestions and Advices from Hunter
- "Have AI look at test files — they reveal developer's security priorities."
- "Look where security controls ARE, then find adjacent functions missing them."
- "Shift Agents for focused micro-tasks, not general hacking."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Justin's AI code review: Gemini CLI analyzes SDK, identifies security controls via test files.

#### 2. What you should learn
- Understand **[ ] ai code review: analyze test files first — they reveal valued security controls**
- Understand **[ ] cspt + cache deception: append `.css` to force cache of authenticated response**
- Understand **[ ] ch.at: chatgpt over `dig` txt, ssh, curl — works on planes (only dns)**
- Understand **[ ] nowafplease: inflate request size to bypass wafs**
- Understand **[ ] `postmessage` targetorigin: check for `origin.endswith()` flaws**

#### 3. Core concepts explained
**CSPT + Cache Deception — Cache poisoning**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Code Assist OAuth postMessage Bypass — OAuth leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Test file analysis**
- AI analyzes tests to identify security controls.

**Adjacent vulnerability discovery**
- Find control → search for similar functions missing it.

**dig over DNS for LLM**
- `dig ch.at TXT "query"` on planes.


#### 4. Techniques and tactics
**Test file analysis**
- **What it is:** AI analyzes tests to identify security controls.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Adjacent vulnerability discovery**
- **What it is:** Find control → search for similar functions missing it.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**dig over DNS for LLM**
- **What it is:** `dig ch.at TXT "query"` on planes.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Slice (CodeQL + LLM)**
- **What it is:** Automated CodeQL query writing + LLM ranking.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Ebka (Caido MCP)**
- **What it is:** Control Caido from Claude Code.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Have AI look at test files"* — **they reveal developer's security priorities.**
- *"Look where security controls ARE, then find adjacent functions missing them."*
- *"Shift Agents for focused micro-tasks, not general hacking."*

#### 6. Mental models
- **Have AI look at test files — they reveal developer's securit** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Look where security controls ARE, then find adjacent functio** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Shift Agents for focused micro-tasks, not general hacking.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] AI code review: analyze test files first — they reveal valued security controls.
- **Try this:** [ ] CSPT + Cache Deception: append `.css` to force cache of authenticated response.
- **Try this:** [ ] ch.at: ChatGPT over `dig` TXT, SSH, curl — works on planes (only DNS).
- **Try this:** [ ] NoWafPlease: inflate request size to bypass WAFs.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **DNS** — Domain Name System — translates domain names to IP addresses
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in CSPT + Cache Deception — Cache poisoning?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Justin's AI code review: Gemini CLI analyzes SDK, identifies security controls v**
2. **[ ] AI code review: analyze test files first — they reveal valued security contr**
3. **[ ] CSPT + Cache Deception: append `.css` to force cache of authenticated respon**
