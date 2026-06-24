---
title: "Gr3pme's Full-Time Hunting Journey Update, Insane AI Research, and Some Light News"
episode: 142
---


# Episode 142 Gr3pme's Full-Time Hunting Journey Update, Insane AI Research, and Some Light News

**Source:** Show notes (feed) — condensed.

### TL;DR
- Brandon full-time since Jan: started Murtasec pen test company.
- WebSocket Turbo Intruder: threaded engine for WS race conditions; Ping of Death DoS.
- Meta $111,750 bug: path traversal in Messenger Windows E2E chat → DLL hijacking.
- Semgrep: Claude Code + Codex - 86% FP rate, high non-determinism.
- CVE Genie: 51% success, $2.77/CVE.
- PROMISQROUTE: exploit AI model routing to cheap/jailbreakable models.

### Key takeaways
- [ ] WebSocket Turbo Intruder: threaded engine for race conditions; Ping of Death in Java WS.
- [ ] E2E apps: no server validation. File path traversal → DLL hijacking → RCE.
- [ ] CVE Genie: automated PoC from CVE — 51% at $2.77. Spray across bug bounty.
- [ ] PROMISQROUTE: route AI requests to cheaper, more vulnerable models.
- [ ] Lower barrier to entry for hackbots = many snake oil companies.

### Bugs and Findings

#### Facebook Messenger E2E Path Traversal → RCE — RCE ($111,750)
- **Technique:** Path traversal in attachment filename (212 chars fixed path + 48 chars for `../`). DLL placed in app directory → loaded as missing DLL.
- **Key detail:** E2E = no server validation. All validation client-side.
- **Impact:** RCE via DLL hijacking. Initial $34,500 → reassessed to $111,750.

#### PROMISQROUTE — AI routing bypass
- **Technique:** Craft query that looks simple → routed to cheap model → cheap model more jailbreakable.
- **Key detail:** OpenAI saves ~$1.86B/year routing to cheap models.
- **Impact:** Full jailbreak of AI service.

### Techniques and Primitives
- **E2E client-side bypass** — No server to validate; all checks run on receiving client.
- **DLL hijacking for E2E RCE** — Place DLL via file write.
- **AI model routing exploitation** — Route to small models.
- **Split vulnerability by hackbot** — Dedicated agents per bug class > catch-all.

### Suggestions and Advices from Hunter
- "Weigh opportunity cost. Initial income hit is real."
- "Full-time hunting lets you say yes to more opportunities." (Brandon)
- "Any random person with Claude Code can claim to run a 'hackbot company'."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Brandon full-time since Jan: started Murtasec pen test company.

#### 2. What you should learn
- Understand **[ ] websocket turbo intruder: threaded engine for race conditions; ping of death in java ws**
- Understand **[ ] e2e apps: no server validation. file path traversal → dll hijacking → rce**
- Understand **[ ] cve genie: automated poc from cve — 51% at $2.77. spray across bug bounty**
- Understand **[ ] promisqroute: route ai requests to cheaper, more vulnerable models**
- Understand **[ ] lower barrier to entry for hackbots = many snake oil companies**

#### 3. Core concepts explained
**Facebook Messenger E2E Path Traversal → RCE — RCE ($111,750)**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**PROMISQROUTE — AI routing bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**E2E client-side bypass**
- No server to validate; all checks run on receiving client.

**DLL hijacking for E2E RCE**
- Place DLL via file write.

**AI model routing exploitation**
- Route to small models.


#### 4. Techniques and tactics
**E2E client-side bypass**
- **What it is:** No server to validate; all checks run on receiving client.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DLL hijacking for E2E RCE**
- **What it is:** Place DLL via file write.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**AI model routing exploitation**
- **What it is:** Route to small models.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Split vulnerability by hackbot**
- **What it is:** Dedicated agents per bug class > catch-all.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Weigh opportunity cost. Initial income hit is real."*
- *"Full-time hunting lets you say yes to more opportunities." (Brandon)"*
- *"Any random person with Claude Code can claim to run a 'hackbot company'."*

#### 6. Mental models
- **Weigh opportunity cost. Initial income hit is real.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Full-time hunting lets you say yes to more opportunities." (** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Any random person with Claude Code can claim to run a 'hackb** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] WebSocket Turbo Intruder: threaded engine for race conditions; Ping of Death in Java WS.
- **Try this:** [ ] E2E apps: no server validation. File path traversal → DLL hijacking → RCE.
- **Try this:** [ ] CVE Genie: automated PoC from CVE — 51% at $2.77. Spray across bug bounty.
- **Try this:** [ ] PROMISQROUTE: route AI requests to cheaper, more vulnerable models.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Facebook Messenger E2E Path Traversal → RCE — RCE ($111,750)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Brandon full-time since Jan: started Murtasec pen test company.**
2. **[ ] WebSocket Turbo Intruder: threaded engine for race conditions; Ping of Death**
3. **[ ] E2E apps: no server validation. File path traversal → DLL hijacking → RCE.**
