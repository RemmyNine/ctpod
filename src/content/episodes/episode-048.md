---
title: "MVH, DEFCON Black Badge, Googler — Sam Erb"
episode: 48
---


# Episode 48 MVH, DEFCON Black Badge, Googler — Sam Erb

### TL;DR
- Interview with Sam Erb (erbbysam) — Google Security Engineer, DEFCON Black Badge winner
- Deep-dive hacking: focus on CVSS 10.0 (unauthenticated, no privileges, no user interaction)
- Built custom JS monitoring for Airbnb — custom parsers, webpack diffing, Discord alerts
- Emphasizes understanding the development environment: find dev servers, GitHub repos, shared secrets

### Key takeaways
- Focus on unauthenticated endpoints for highest CVSS; "aim for CVSS 10.0 and avoid places where you can't possibly get that"
- Custom automation for specific programs beats generic tooling
- Finding dev environments, origin servers, and GitHub repos gives deep insight into production
- Collaboration: pair with someone who has complementary skills; two brains > one
- Sam's recon is organized in folders with standardized formats that can be diffed across runs

### Techniques and Primitives
- **JS webpack monitoring** — reach out to target periodically, pull webpack JS, extract API endpoints via pattern matching, alert on new endpoints via Discord
- **DNS prep** (pre-sorted DNS hierarchical search) — open-sourced DNS recon tool
- **Static secrets in open source libraries** — many libraries ship with default secrets that get deployed to production

### Tooling and Resources
- **DNS prep** — Sam's DNS recon tool on GitHub
- **Custom JS parser** for Airbnb webpack

### Suggestions and Advices from Hunter
- "I want to understand how the systems work to break them"
- "I always start with auth. I just often never move on — 20-30 hours later I'm still there"
- "The most challenging thing is to not associate time spent elsewhere with dollars per hour"
- "I have a metronome in the back of my head ticking: 'Why are you hanging out with friends? You should be making money'"

### AI Takeaway
Sam's "CVSS 10.0-first" methodology is ruthlessly efficient: by constraining yourself to only the highest-impact scenarios (unauthenticated, no privs, no interaction), you naturally find the most valuable bugs.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Interview with Sam Erb (erbbysam) — Google Security Engineer, DEFCON Black Badge winner

#### 2. What you should learn
- Understand **focus on unauthenticated endpoints for highest cvss; "aim for cvss 10.0 and avoid places where you can't possibly get that"**
- Understand **custom automation for specific programs beats generic tooling**
- Understand **finding dev environments, origin servers, and github repos gives deep insight into production**
- Understand **collaboration: pair with someone who has complementary skills; two brains > one**
- Understand **sam's recon is organized in folders with standardized formats that can be diffed across runs**

#### 3. Core concepts explained
**JS webpack monitoring**
- reach out to target periodically, pull webpack JS, extract API endpoints via pattern matching, alert on new endpoints via Discord

**DNS prep (pre-sorted DNS hierarchical search)**
- open-sourced DNS recon tool

**Static secrets in open source libraries**
- many libraries ship with default secrets that get deployed to production


#### 4. Techniques and tactics
**JS webpack monitoring**
- **What it is:** reach out to target periodically, pull webpack JS, extract API endpoints via pattern matching, alert on new endpoints via Discord
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DNS prep (pre-sorted DNS hierarchical search)**
- **What it is:** open-sourced DNS recon tool
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Static secrets in open source libraries**
- **What it is:** many libraries ship with default secrets that get deployed to production
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"I want to understand how the systems work to break them"*
- *"I always start with auth. I just often never move on"* — **20-30 hours later I'm still there**
- *"The most challenging thing is to not associate time spent elsewhere with dollars per hour"*
- *"I have a metronome in the back of my head ticking: 'Why are you hanging out with friends? You should be making money'"*

#### 6. Mental models
- **I want to understand how the systems work to break them** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I always start with auth. I just often never move on — 20-30** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The most challenging thing is to not associate time spent el** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Focus on unauthenticated endpoints for highest CVSS; "aim for CVSS 10.0 and avoid places where you can't possibly get that"
- **Try this:** Custom automation for specific programs beats generic tooling
- **Try this:** Finding dev environments, origin servers, and GitHub repos gives deep insight into production
- **Try this:** Collaboration: pair with someone who has complementary skills; two brains > one

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **DNS** — Domain Name System — translates domain names to IP addresses
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Interview with Sam Erb (erbbysam) — Google Security Engineer, DEFCON Black Badge**
2. **Focus on unauthenticated endpoints for highest CVSS; "aim for CVSS 10.0 and avoi**
3. **Custom automation for specific programs beats generic tooling**
