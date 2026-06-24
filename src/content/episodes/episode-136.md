---
title: "Hacking Cluely, AI Prod Sec, and How To Not Get Sued with Jack Cable"
episode: 136
---


# Episode 136 Hacking Cluely, AI Prod Sec, and How To Not Get Sued with Jack Cable

**Source:** Show notes (feed) — condensed.

### TL;DR
- Jack Cable found postMessage screenshot handler in Cluely desktop app — screen recording via link click.
- Cluely filed DMCA for tweet; employee admitted unauthorized; CEO donated $1k to EFF.
- Jack: Senate (open source security), CISA (Secure by Design), Corridor.dev.
- Anthropic pays $35k for universal transferable jailbreak.
- Caido Shift Agents.

### Key takeaways
- [ ] Electron apps: postMessage handlers exposed to ANY opened window.
- [ ] Publishing system prompts from desktop apps = DMCA risk, but security research exemption exists.
- [ ] AI safety: Anthropic $35k for jailbreak; OpenAI matches for biosecurity.
- [ ] Vibe-coded app vulns = Supabase permissions/RLS, not code.
- [ ] Business logic flaws in vibe-coded apps: AI lazily switches ACLs instead of fixing architecture.

### Bugs and Findings

#### Cluely Desktop PostMessage Screen Capture — Privacy violation
- **Root cause:** Electron app no sandbox; postMessage handler `takeScreenshot()` accessible to any opened window.
- **Exploitation:** User clicks link → attacker page sends postMessage → Cluely takes screenshot → stream continuously.
- **Key detail:** No origin verification on message handler.
- **Impact:** Continuous screen recording.

### Techniques and Primitives
- **Electron app audit** — Unzip `.asar`, inspect postMessage handlers, IPC channels, nodeIntegration.
- **Race conditions via curl** — Parallel curl requests for race condition testing.

### Suggestions and Advices from Hunter
- "Vibe coding breaks down at a certain app size."
- "Real CFAA risk for good-faith research is approaching zero if you disclose responsibly." (Jack)
- "AI dev tools enable 10x faster coding → 10x more vulnerabilities."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Jack Cable found postMessage screenshot handler in Cluely desktop app — screen recording via link click.

#### 2. What you should learn
- Understand **[ ] electron apps: postmessage handlers exposed to any opened window**
- Understand **[ ] publishing system prompts from desktop apps = dmca risk, but security research exemption exists**
- Understand **[ ] ai safety: anthropic $35k for jailbreak; openai matches for biosecurity**
- Understand **[ ] vibe-coded app vulns = supabase permissions/rls, not code**
- Understand **[ ] business logic flaws in vibe-coded apps: ai lazily switches acls instead of fixing architecture**

#### 3. Core concepts explained
**Cluely Desktop PostMessage Screen Capture — Privacy violation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Electron app audit**
- Unzip `.asar`, inspect postMessage handlers, IPC channels, nodeIntegration.

**Race conditions via curl**
- Parallel curl requests for race condition testing.


#### 4. Techniques and tactics
**Electron app audit**
- **What it is:** Unzip `.asar`, inspect postMessage handlers, IPC channels, nodeIntegration.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Race conditions via curl**
- **What it is:** Parallel curl requests for race condition testing.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Vibe coding breaks down at a certain app size."*
- *"Real CFAA risk for good-faith research is approaching zero if you disclose responsibly." (Jack)"*
- *"AI dev tools enable 10x faster coding → 10x more vulnerabilities."*

#### 6. Mental models
- **Vibe coding breaks down at a certain app size.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Real CFAA risk for good-faith research is approaching zero i** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **AI dev tools enable 10x faster coding → 10x more vulnerabili** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Electron apps: postMessage handlers exposed to ANY opened window.
- **Try this:** [ ] Publishing system prompts from desktop apps = DMCA risk, but security research exemption exists.
- **Try this:** [ ] AI safety: Anthropic $35k for jailbreak; OpenAI matches for biosecurity.
- **Try this:** [ ] Vibe-coded app vulns = Supabase permissions/RLS, not code.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **agent** — AI system that can use tools and make decisions autonomously
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Cluely Desktop PostMessage Screen Capture — Privacy violation?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Jack Cable found postMessage screenshot handler in Cluely desktop app — screen r**
2. **[ ] Electron apps: postMessage handlers exposed to ANY opened window.**
3. **[ ] Publishing system prompts from desktop apps = DMCA risk, but security resear**
