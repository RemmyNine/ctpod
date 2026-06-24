---
title: "The Life of a Full-Time Bug Bounty Hunter + BB News + Reports from Mentees"
episode: 10
---


# Episode 10 The Life of a Full-Time Bug Bounty Hunter + BB News + Reports from Mentees

### TL;DR
- PortSwigger Daily Swig newsletter discontinued; new XSS vectors published by PortSwigger Research
- Life as full-time bug bounty: 6-12 hour days; energy management over time management; take Sundays off
- Mariah (Justin's wife) runs his business operations; LLC taxed as S-Corp for optimization
- Health insurance for self-employed: catastrophic coverage (healthshare ~$182/mo) + DPC subscription (~$100/mo)
- Mentee reports: hardcoded Japanese parameter name `kagi` (key) decrypted secrets; GraphQL IDOR with 500 responses that still succeeded
- Rezo's "5 Ways to Maximize Luck" tweet — rebuttal on "don't rabbit hole" advice

### Key takeaways
- PortSwigger new XSS vectors: `navigation.navigate()` and `a` tag with `href` containing `%0a` + JavaScript protocol
- For full-timers: pipeline of unpaid bugs funding current expenses while finding new ones
- Take at least one day off per week (Sunday)
- Use Windows+V (clipboard history) for quick note-taking across sessions
- Rezo's tip "don't rabbit hole" — Justin rebuts: going deep is how you find the best bugs
- Mentee Koda: ID on a GraphQL endpoint caused 500 but still made changes — verify changes on victim account even on error responses

### Bugs and Findings

#### GraphQL IDOR with False Negative Response — Address Takeover
- **Target/context:** Food delivery service
- **Root cause:** Server validated address change via numeric `address_id` only, no user ownership check
- **Technique / how found:** Observed address info in UI; intercepted address change request; modified `address_id` in GraphQL POST; got 500 error but change still propagated to victim account
- **Exploitation steps:**
  1. Capture address change POST request
  2. Modify `address_id` to another user's address ID
  3. Request returns 500 (server error)
  4. Check victim account — address changed successfully
- **Key technical details:** GraphQL POST; numeric `address_id`; 500 error is misleading — mutation still commits
- **Impact / severity / bounty:** Address takeover, PII leakage

#### Hardcoded Encrypted Secrets in Android App (Japanese param name)
- **Target/context:** Large American company's Japanese app
- **Root cause:** Encrypted strings stored in `strings.xml`; decryption parameter named `kagi` (Japanese: "key")
- **Technique / how found:** Decompiled APK, found `kagi` parameter in `strings.xml` — recognized Japanese word; used it to decrypt all hardcoded secrets
- **Key technical details:** Non-English parameter names create security-through-obscurity that non-Japanese hackers miss
- **Impact / severity / bounty:** Credential/secret disclosure

### Techniques and Primitives
- **Ghost account privilege escalation** — guest/ghost accounts may have PR:None instead of PR:Low; convert to full account
- **CVSS attack complexity high** — use for "depends on race condition" or "requires specific condition outside attacker control"
- **CVSS privilege required None via guest accounts** — sign up without email verification, use pre-existing session
- **Hash-based request signing bypass** — if all GET requests are signed, use a login endpoint with `return_to` URL parameter to have the server generate the hash for you

### Tooling and Resources
- Hackvertor (Gareth Hayes' Burp plugin)
- "JavaScript for Hackers" ebook by Gareth Hayes
- Cookie Monster (default crypto key checker)
- HashCollision tool
- Cookie-editor browser extension

### Suggestions and Advices from Hunter
- "On a new target, spend at least 16 hours on one part before moving along" — Justin on deep diving
- "Paying on triage is the way to go — Shopify does this" — Joel
- "Self-sign-up accounts should be PR:None, not PR:Low" — Justin on CVSS argument
- "Don't rabbit hole is wrong rabbit hole is how you win" — Justin on Rezo's tweet

### AI Takeaway
The concept of a "pipeline" for full-time bug bounty is critical: unpaid bugs in queue fund current expenses, while current hacking finds future bugs. The hidden value in the mentee bug: always verify that a 500 error doesn't mean the mutation failed. GraphQL in particular may commit changes before returning errors.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
PortSwigger Daily Swig newsletter discontinued; new XSS vectors published by PortSwigger Research

#### 2. What you should learn
- Understand **portswigger new xss vectors: `navigation.navigate()` and `a` tag with `href` containing `%0a` + javascript protocol**
- Understand **for full-timers: pipeline of unpaid bugs funding current expenses while finding new ones**
- Understand **take at least one day off per week (sunday)**
- Understand **use windows+v (clipboard history) for quick note-taking across sessions**
- Understand **rezo's tip "don't rabbit hole" — justin rebuts: going deep is how you find the best bugs**

#### 3. Core concepts explained
**GraphQL IDOR with False Negative Response — Address Takeover**
- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.
- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.
- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.

**Hardcoded Encrypted Secrets in Android App (Japanese param name)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Ghost account privilege escalation**
- guest/ghost accounts may have PR:None instead of PR:Low; convert to full account

**CVSS attack complexity high**
- use for "depends on race condition" or "requires specific condition outside attacker control"

**CVSS privilege required None via guest accounts**
- sign up without email verification, use pre-existing session


#### 4. Techniques and tactics
**Ghost account privilege escalation**
- **What it is:** guest/ghost accounts may have PR:None instead of PR:Low; convert to full account
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CVSS attack complexity high**
- **What it is:** use for "depends on race condition" or "requires specific condition outside attacker control"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CVSS privilege required None via guest accounts**
- **What it is:** sign up without email verification, use pre-existing session
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Hash-based request signing bypass**
- **What it is:** if all GET requests are signed, use a login endpoint with `return_to` URL parameter to have the server generate the hash for you
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"On a new target, spend at least 16 hours on one part before moving along"* — **Justin on deep diving**
- *"Paying on triage is the way to go"* — **Shopify does this" — Joel**
- *"Self-sign-up accounts should be PR:None, not PR:Low"* — **Justin on CVSS argument**
- *"Don't rabbit hole is wrong rabbit hole is how you win"* — **Justin on Rezo's tweet**

#### 6. Mental models
- **On a new target, spend at least 16 hours on one part before ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Paying on triage is the way to go — Shopify does this" — Joe** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Self-sign-up accounts should be PR:None, not PR:Low" — Justi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** PortSwigger new XSS vectors: `navigation.navigate()` and `a` tag with `href` containing `%0a` + JavaScript protocol
- **Try this:** For full-timers: pipeline of unpaid bugs funding current expenses while finding new ones
- **Try this:** Take at least one day off per week (Sunday)
- **Try this:** Use Windows+V (clipboard history) for quick note-taking across sessions

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GraphQL IDOR with False Negative Response — Address Takeover?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **PortSwigger Daily Swig newsletter discontinued; new XSS vectors published by Por**
2. **PortSwigger new XSS vectors: `navigation.navigate()` and `a` tag with `href` con**
3. **For full-timers: pipeline of unpaid bugs funding current expenses while finding **
