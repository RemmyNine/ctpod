---
title: "Building Hacker Communities — Bug Bounty Village, getDisclosed, and the LHE Squad"
episode: 133
---


# Episode 133 Building Hacker Communities — Bug Bounty Village, getDisclosed, and the LHE Squad

**Source:** Show notes (feed) — condensed.

### TL;DR
- Harley (Infinite Logins) and Ari on Bug Bounty Village at DEFCON.
- Disclose.io VDP safe harbor templates.
- BBV 2025: bigger, CTF with real app + triage, challenge badges.
- Ari's origin story: networked at HackerOne 5411 Buenos Aires event.

### Key takeaways
- [ ] BBV at DEFCON 2025: 30% more space, 70 chairs, CTF with real web app + triage.
- [ ] CTF: intentionally-vulnerable multi-app system (APIs, LLM) — no instructions, just scope.
- [ ] Badges: 400 free blue, 200 green pre-order ($). Binary challenge coins interact.
- [ ] Disclose.io: template VDP with safe harbor.
- [ ] Supabase: PostgreSQL views bypass RLS (view runs as creator, not viewer).

### Bugs and Findings

#### Supabase View RLS Bypass — Data exposure
- **Root cause:** PostgreSQL views don't inherit RLS. View created as admin = public read/write to entire table.
- **Technique:** Created view to exclude email column; view exposed all rows.
- **Impact:** Complete database access to attacker.

### Techniques and Primitives
- **API path truncation** — Fuzz intermediate levels of deep API paths for swagger files.
- **Vibe-coded app security** — Supabase/Firebase misconfigs are primary vulns.

### Suggestions and Advices from Hunter
- "Just ask." (Douglas Day / Ari)
- "The transition from pentest to bug bounty mindset is a whole different piece." (Harley)
- "Bug bounty is life-changing for non-US researchers."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Harley (Infinite Logins) and Ari on Bug Bounty Village at DEFCON.

#### 2. What you should learn
- Understand **[ ] bbv at defcon 2025: 30% more space, 70 chairs, ctf with real web app + triage**
- Understand **[ ] ctf: intentionally-vulnerable multi-app system (apis, llm) — no instructions, just scope**
- Understand **[ ] badges: 400 free blue, 200 green pre-order ($). binary challenge coins interact**
- Understand **[ ] disclose.io: template vdp with safe harbor**
- Understand **[ ] supabase: postgresql views bypass rls (view runs as creator, not viewer)**

#### 3. Core concepts explained
**Supabase View RLS Bypass — Data exposure**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**API path truncation**
- Fuzz intermediate levels of deep API paths for swagger files.

**Vibe-coded app security**
- Supabase/Firebase misconfigs are primary vulns.


#### 4. Techniques and tactics
**API path truncation**
- **What it is:** Fuzz intermediate levels of deep API paths for swagger files.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Vibe-coded app security**
- **What it is:** Supabase/Firebase misconfigs are primary vulns.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Just ask." (Douglas Day / Ari)"*
- *"The transition from pentest to bug bounty mindset is a whole different piece." (Harley)"*
- *"Bug bounty is life-changing for non-US researchers."*

#### 6. Mental models
- **Just ask." (Douglas Day / Ari)** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The transition from pentest to bug bounty mindset is a whole** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Bug bounty is life-changing for non-US researchers.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] BBV at DEFCON 2025: 30% more space, 70 chairs, CTF with real web app + triage.
- **Try this:** [ ] CTF: intentionally-vulnerable multi-app system (APIs, LLM) — no instructions, just scope.
- **Try this:** [ ] Badges: 400 free blue, 200 green pre-order ($). Binary challenge coins interact.
- **Try this:** [ ] Disclose.io: template VDP with safe harbor.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Supabase View RLS Bypass — Data exposure?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Harley (Infinite Logins) and Ari on Bug Bounty Village at DEFCON.**
2. **[ ] BBV at DEFCON 2025: 30% more space, 70 chairs, CTF with real web app + triag**
3. **[ ] CTF: intentionally-vulnerable multi-app system (APIs, LLM) — no instructions**
