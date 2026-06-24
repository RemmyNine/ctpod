---
title: "Caido Tools and Workflows"
episode: 138
---


# Episode 138 Caido Tools and Workflows

**Source:** Show notes (feed) — condensed.

### TL;DR
- EvenBetter plugin: Common Filters, Convert Workflow command palette.
- Notes plugin: Win+Shift+N attaches Replay tab graphically.
- Shift Agents: micro-AI agents for specific tasks.
- Drop: PGP-encrypted Caido object sharing.
- RPC ID deobfuscation via workflows → $20k IDOR.

### Key takeaways
- [ ] EvenBetter: Common Filters (5min/1h/6h/12h/24h), Ctrl+K for convert workflows.
- [ ] Notes: Win+Shift+N → graphical Replay tab attachment.
- [ ] Shift Agents: system prompts for specific bugs (domain bypass, open redirect).
- [ ] Drop: PGP sharing of Caido objects between collaborators.
- [ ] Session refreshing workflow: passive workflow extracts cookies → env var → auto-refreshed placeholders.

### Techniques and Primitives
- **RPC ID deobfuscation** — Passive workflow extracts ID→name from JS → match-and-replace inserts human-readable query param.
- **Top-level nav highlighting** — Sec-Fetch-Site headers highlight page navigations vs API calls.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
EvenBetter plugin: Common Filters, Convert Workflow command palette.

#### 2. What you should learn
- Understand **[ ] evenbetter: common filters (5min/1h/6h/12h/24h), ctrl+k for convert workflows**
- Understand **[ ] notes: win+shift+n → graphical replay tab attachment**
- Understand **[ ] shift agents: system prompts for specific bugs (domain bypass, open redirect)**
- Understand **[ ] drop: pgp sharing of caido objects between collaborators**
- Understand **[ ] session refreshing workflow: passive workflow extracts cookies → env var → auto-refreshed placeholders**

#### 3. Core concepts explained
**RPC ID deobfuscation**
- Passive workflow extracts ID→name from JS → match-and-replace inserts human-readable query param.

**Top-level nav highlighting**
- Sec-Fetch-Site headers highlight page navigations vs API calls.


#### 4. Techniques and tactics
**RPC ID deobfuscation**
- **What it is:** Passive workflow extracts ID→name from JS → match-and-replace inserts human-readable query param.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Top-level nav highlighting**
- **What it is:** Sec-Fetch-Site headers highlight page navigations vs API calls.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** [ ] EvenBetter: Common Filters (5min/1h/6h/12h/24h), Ctrl+K for convert workflows.
- **Try this:** [ ] Notes: Win+Shift+N → graphical Replay tab attachment.
- **Try this:** [ ] Shift Agents: system prompts for specific bugs (domain bypass, open redirect).
- **Try this:** [ ] Drop: PGP sharing of Caido objects between collaborators.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **API** — Application Programming Interface — structured endpoints for data exchange
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **EvenBetter plugin: Common Filters, Convert Workflow command palette.**
2. **[ ] EvenBetter: Common Filters (5min/1h/6h/12h/24h), Ctrl+K for convert workflow**
3. **[ ] Notes: Win+Shift+N → graphical Replay tab attachment.**
