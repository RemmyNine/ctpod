---
title: "How to Find a Good BBP + Acropalypse + ZDI"
episode: 13
---


# Episode 13 How to Find a Good BBP + Acropalypse + ZDI

### TL;DR
- Acropalypse (Cropalypse): Google Pixel screenshot cropping tool left original image data; Windows Snipping Tool also vulnerable
- NPM `request` SSRF filter bypass: HTTPS→HTTP redirect deletes agent, bypasses `request` filter
- ZDI Pwn2Own: Tesla, Microsoft Teams targeted; $1M+ paid; 5-minute demo window per exploit
- How to evaluate a bug bounty program: bounty table, response efficiency, total/90-day bounties, scope, known issues, top hacker gap

### Key takeaways
- For SSRF testing: test HTTPS→HTTP redirect — may bypass restrictive filters that only check origin
- ZDI requires 5-minute exploit demo window — race-condition-based attacks may fail
- Evaluate programs by: average bounty vs advertised max, launch date, last 90 days bounty paid and reports resolved
- Internal dupes: if a bug has been known internally for months and unfixed, attacker will still exploit it
- Known issues tab (Bugcrowd) should exist on HackerOne too

### Bugs and Findings

#### OAuth Path Traversal + Google Analytics URL Leak — ATO (High)
- **Target/context:** Pixiv (Japanese program)
- **Root cause:** OAuth callback path only validated prefix start; path traversal allowed reaching any endpoint; Google Analytics tracking ID on user page leaked the full OAuth URL (including tokens)
- **Technique / how found:** Observed OAuth return URL path only checked prefix; used `../` traversal; noticed user-controlled Google Analytics tracking ID leaked full URL to attacker's GA
- **Key technical details:** Path prefix check bypassed via `../`; GA tracking ID on user's page sends full URL as referrer
- **Impact / severity / bounty:** High; OAuth token leakage → account takeover
- **Obstacles & how solved:** Browsers stopped leaking full URL in Referrer; GA custom ID on user's page leaks URL via page load instead

### Techniques and Primitives
- **SSRF filter bypass via HTTPS→HTTP redirect** — `request` library deletes agent on protocol change, bypassing agent-based URL filters
- **Acropalypse-like testing** — check if cropped/screenshotted images retain original data in truncated file
- **Program selection checklist** — bounty table, response efficiency, 90-day stats, scope breadth, known issues, top hacker gap
- **Numeric IDOR mindset** — even with UUIDs, look for oracle leaks, error messages, email disclosure

### Tooling and Resources
- ZDI Pwn2Own
- Acropalypse writeup (David Buchanan)
- SSRF Sheriff (Joel's tool)

### Suggestions and Advices from Hunter
- "If an internal dupe has been open for 6+ months, should still pay — attacker will exploit it" — Justin
- "Medium bounties at 3K: that's where the real money is, not just crits" — Justin on program selection
- "Look at the gap between #1 and #2 on leaderboard — if it's someone who goes deep, that's interesting" — Joel
- "Instacart pre-seeds test accounts and gives premium access — that's a sign of a good program" — Justin

### AI Takeaway
The program selection framework (bounty table + last 90 days + efficiency + known issues) is a systematic way to evaluate where to invest hacking time. The "top hacker gap" signal is especially valuable: if #1 has 2K rep and #2 has 400, someone has figured out a systemic vulnerability. Find it.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Acropalypse (Cropalypse): Google Pixel screenshot cropping tool left original image data; Windows Snipping Tool also vulnerable

#### 2. What you should learn
- Understand **for ssrf testing: test https→http redirect — may bypass restrictive filters that only check origin**
- Understand **zdi requires 5-minute exploit demo window — race-condition-based attacks may fail**
- Understand **evaluate programs by: average bounty vs advertised max, launch date, last 90 days bounty paid and reports resolved**
- Understand **internal dupes: if a bug has been known internally for months and unfixed, attacker will still exploit it**
- Understand **known issues tab (bugcrowd) should exist on hackerone too**

#### 3. Core concepts explained
**OAuth Path Traversal + Google Analytics URL Leak — ATO (High)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SSRF filter bypass via HTTPS→HTTP redirect**
- `request` library deletes agent on protocol change, bypassing agent-based URL filters

**Acropalypse-like testing**
- check if cropped/screenshotted images retain original data in truncated file

**Program selection checklist**
- bounty table, response efficiency, 90-day stats, scope breadth, known issues, top hacker gap


#### 4. Techniques and tactics
**SSRF filter bypass via HTTPS→HTTP redirect**
- **What it is:** `request` library deletes agent on protocol change, bypassing agent-based URL filters
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Acropalypse-like testing**
- **What it is:** check if cropped/screenshotted images retain original data in truncated file
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Program selection checklist**
- **What it is:** bounty table, response efficiency, 90-day stats, scope breadth, known issues, top hacker gap
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Numeric IDOR mindset**
- **What it is:** even with UUIDs, look for oracle leaks, error messages, email disclosure
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If an internal dupe has been open for 6+ months, should still pay"* — **attacker will exploit it" — Justin**
- *"Medium bounties at 3K: that's where the real money is, not just crits"* — **Justin on program selection**
- *"Look at the gap between #1 and #2 on leaderboard"* — **if it's someone who goes deep, that's interesting" — Joel**
- *"Instacart pre-seeds test accounts and gives premium access"* — **that's a sign of a good program" — Justin**

#### 6. Mental models
- **If an internal dupe has been open for 6+ months, should stil** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Medium bounties at 3K: that's where the real money is, not j** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Look at the gap between #1 and #2 on leaderboard — if it's s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** For SSRF testing: test HTTPS→HTTP redirect — may bypass restrictive filters that only check origin
- **Try this:** ZDI requires 5-minute exploit demo window — race-condition-based attacks may fail
- **Try this:** Evaluate programs by: average bounty vs advertised max, launch date, last 90 days bounty paid and reports resolved
- **Try this:** Internal dupes: if a bug has been known internally for months and unfixed, attacker will still exploit it

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Browsers stopped leaking full URL in Referrer; GA custom ID on user's page leaks URL via page load instead

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **agent** — AI system that can use tools and make decisions autonomously
- **0-day** — Vulnerability unknown to the vendor — no patch available
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in OAuth Path Traversal + Google Analytics URL Leak — ATO (High)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Acropalypse (Cropalypse): Google Pixel screenshot cropping tool left original im**
2. **For SSRF testing: test HTTPS→HTTP redirect — may bypass restrictive filters that**
3. **ZDI requires 5-minute exploit demo window — race-condition-based attacks may fai**
