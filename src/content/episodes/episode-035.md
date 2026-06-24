---
title: "King of Collaboration: Douglas Day (Archangel)"
episode: 35
---


# Episode 35 King of Collaboration: Douglas Day (Archangel)

**Guests/Hosts:** Justin Gardner, Joel Margolis, Douglas Day (Archangel)  
**Date:** 2023-09-07 | **Duration:** 1:25:24

### TL;DR
- Douglas is known for collaboration (9x Best Collaboration awards at live hacking events)
- Unique methodology: reads documentation religiously, maps "no"s in the application (trust boundaries), tests permission matrices
- 100 Very Short Bug Bounty Rules thread (inspired by Ryan Holiday's Stoic rules)
- Program churning: small programs, 30-min assessment, 3-hr no-bug limit, then move on
- Hacks max 3 hrs/day — family commitments force discipline; uses pre-planned hacking sessions

### Key Takeaways
- **"No"s are bugs**: Every place the app tells you "no" (can't do this, disabled button, documentation restriction) is a potential vulnerability — test it
- **Auth matrix testing**: Create a spreadsheet of roles vs. endpoints; find cases where a lower-privilege role can call a higher-privilege endpoint
- **Intercom widget booting**: Open browser console, type `Intercom('boot', { email: 'test@test.com' })` — if no identity verification, you see another user's conversations
- **Match and replace for endpoint discovery**: Change `"isAdmin": false` to `true` in responses via Burp match-and-replace → UI reveals hidden endpoints
- **Pre-plan hacking sessions**: When not in the zone, pre-decide which targets to hack for how long; execute the plan, not the anxiety

### Bugs and Findings

#### Intercom Identity Verification Bypass — ATO / Data leak
- **Target/context:** Any website using Intercom widget without identity verification
- **Root cause:** Intercom's `identity_verification` is optional; if not implemented, anyone can `Intercom('boot', { email: 'any@email.com' })` and see that user's conversations
- **Technique / how found:** Douglas tested the Intercom boot method with test emails
- **Exploitation steps:**
  1. Open browser console on target
  2. `Intercom('boot', { email: 'test@test.com' })`
  3. Intercom widget loads with that user's conversation history
  4. Often `test@test.com` is a sales team test account with access to sensitive data
- **Key technical details:** 10-20% of Intercom implementations lack identity verification | Blog post details: one vendor had password reset with hardcoded temp password `summer@123`
- **Impact / severity / bounty:** Access to other users' conversations, PII; $10K+ over multiple programs

### Techniques and Primitives
- **Intercom boot hijacking** — `Intercom('boot', { email: '...' })` in console; also works via URL params on sites that auto-boot from URL
- **No-centric testing** — Identify all "no"s in the application (disabled buttons, docs saying "can't", greyed-out features); test each with direct API calls
- **Permission matrix testing** — Build a spreadsheet of roles vs endpoints; systematically test each cell; one "yes" where there should be a "no" = bug
- **Canary reports** — On a new program, submit 2 medium bugs first to gauge response time/tone before investing deeper

### Tooling and Resources
- Burp Match and Replace — for client-side authorization bypass
- `request-minimizer` Burp plugin
- Intercom's identity verification docs
- Douglas Day's blog (dday.us) — Intercom hijacking writeup

### Suggestions and Advices from Hunter
- "If the app is using Intercom, try booting it with another email. 10-20% of the time, you can see other users' chats."
- "Read the freaking documentation. If it says a user shouldn't be able to do something and they can, that's your bug — and they can't argue with you."
- "Pin your success on whether you followed your plan, not if you found bugs."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Douglas is known for collaboration (9x Best Collaboration awards at live hacking events)

#### 2. What you should learn
- Understand **"no"s are bugs**: every place the app tells you "no" (can't do this, disabled button, documentation restriction) is a potential vulnerability — test it**
- Understand **auth matrix testing**: create a spreadsheet of roles vs. endpoints; find cases where a lower-privilege role can call a higher-privilege endpoint**
- Understand **intercom widget booting**: open browser console, type `intercom('boot', { email: 'test@test.com' })` — if no identity verification, you see another user's conversations**
- Understand **match and replace for endpoint discovery**: change `"isadmin": false` to `true` in responses via burp match-and-replace → ui reveals hidden endpoints**
- Understand **pre-plan hacking sessions**: when not in the zone, pre-decide which targets to hack for how long; execute the plan, not the anxiety**

#### 3. Core concepts explained
**Intercom Identity Verification Bypass — ATO / Data leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Intercom boot hijacking**
- `Intercom('boot', { email: '...' })` in console; also works via URL params on sites that auto-boot from URL

**No-centric testing**
- Identify all "no"s in the application (disabled buttons, docs saying "can't", greyed-out features); test each with direct API calls

**Permission matrix testing**
- Build a spreadsheet of roles vs endpoints; systematically test each cell; one "yes" where there should be a "no" = bug


#### 4. Techniques and tactics
**Intercom boot hijacking**
- **What it is:** `Intercom('boot', { email: '...' })` in console; also works via URL params on sites that auto-boot from URL
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**No-centric testing**
- **What it is:** Identify all "no"s in the application (disabled buttons, docs saying "can't", greyed-out features); test each with direct API calls
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Permission matrix testing**
- **What it is:** Build a spreadsheet of roles vs endpoints; systematically test each cell; one "yes" where there should be a "no" = bug
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Canary reports**
- **What it is:** On a new program, submit 2 medium bugs first to gauge response time/tone before investing deeper
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If the app is using Intercom, try booting it with another email. 10-20% of the time, you can see other users' chats."*
- *"Read the freaking documentation. If it says a user shouldn't be able to do something and they can, that's your bug"* — **and they can't argue with you.**
- *"Pin your success on whether you followed your plan, not if you found bugs."*

#### 6. Mental models
- **If the app is using Intercom, try booting it with another em** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Read the freaking documentation. If it says a user shouldn't** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Pin your success on whether you followed your plan, not if y** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** "No"s are bugs**: Every place the app tells you "no" (can't do this, disabled button, documentation restriction) is a potential vulnerability — test it
- **Try this:** Auth matrix testing**: Create a spreadsheet of roles vs. endpoints; find cases where a lower-privilege role can call a higher-privilege endpoint
- **Try this:** Intercom widget booting**: Open browser console, type `Intercom('boot', { email: 'test@test.com' })` — if no identity verification, you see another user's conversations
- **Try this:** Match and replace for endpoint discovery**: Change `"isAdmin": false` to `true` in responses via Burp match-and-replace → UI reveals hidden endpoints

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Intercom Identity Verification Bypass — ATO / Data leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Douglas is known for collaboration (9x Best Collaboration awards at live hacking**
2. **"No"s are bugs**: Every place the app tells you "no" (can't do this, disabled bu**
3. **Auth matrix testing**: Create a spreadsheet of roles vs. endpoints; find cases w**
