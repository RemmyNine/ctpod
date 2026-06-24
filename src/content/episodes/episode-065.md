---
title: "Motivation and Methodology with Sam Curry (Zlz)"
episode: 65
---


# Episode 65 Motivation and Methodology with Sam Curry (Zlz)

**Guest:** Sam Curry
**Format:** Show notes with timestamps (feed) — full transcript (long episode, 2:29:05)

### TL;DR
- Sam Curry's hacking is driven by curiosity/interest, not money — "don't force yourself to be a bug bounty hunter" (his 2020 blog post)
- Getting detained at Dulles airport by IRS CI + DHS for wire fraud suspicion over taking a scammer's private key from a JS file
- Online casino hack: replay requests to generate unlimited balance (reported, didn't withdraw) — but caused business damage between casino and game provider
- Car hacking: Spearion (connected vehicle platform) had SQL injection — `admin'` — gave access to millions of vehicles; license plate → VIN API for $0.015/call
- Hacking philosophy: "You don't have to cross the line to extract fun from dancing around it"

### Key Takeaways
- Bug bounty income is unstable even at the top — Sam experienced burnout after 4 years of full-time bug bounty despite 100K+/year
- Establishing "good intent" and a public track record as a white-hat researcher provides legal cover for borderline research
- The most fun vulnerabilities are ones that feel like black-hat scenarios: making car horns honk, unlocking hotel rooms, changing grades
- Many massive vulnerabilities are trivially simple — SQL injection on a connected car platform with millions of devices
- Collaboration happens by nagging talented friends — "I spam you with stuff and if you want to help you do"

### Techniques and Primitives
- **License Plate → VIN API:** DMV sells records to contractors; for $0.015/call you can resolve a plate to VIN → then use vehicle API to perform actions
- **Open redirect + auth header leak in OKHTTP:** Authorization header is stripped on cross-host redirect — but other custom headers pass through; critical mobile SSRF/ATO gadget
- **Cross-window forgery drag-and-drop:** Attacker page overlays victim page, captures drag-and-drop events → injects payload into victim site form fields

### Suggestions and Advices
- **Sam Curry:** "Don't force yourself to be a bug bounty hunter. If it's not working, step away. I've never found a bug under pressure — always when relaxed and curious."
- "The mentor I had for Magnus Carlsen told him to step away and have fun with chess — that's how he became the greatest."
- "Working with Shubs changed a lot for me — he wanted to do high-impact research for the sake of it, and that reframed my approach."
- Collaboration philosophy: "There's no elitist group — just 'hey I'm gonna spam you with stuff and if you want to help, help'"
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Sam Curry's hacking is driven by curiosity/interest, not money — "don't force yourself to be a bug bounty hunter" (his 2020 blog post)

#### 2. What you should learn
- Understand **bug bounty income is unstable even at the top — sam experienced burnout after 4 years of full-time bug bounty despite 100k+/year**
- Understand **establishing "good intent" and a public track record as a white-hat researcher provides legal cover for borderline research**
- Understand **the most fun vulnerabilities are ones that feel like black-hat scenarios: making car horns honk, unlocking hotel rooms, changing grades**
- Understand **many massive vulnerabilities are trivially simple — sql injection on a connected car platform with millions of devices**
- Understand **collaboration happens by nagging talented friends — "i spam you with stuff and if you want to help you do"**

#### 3. Core concepts explained
**License Plate → VIN API: DMV sells records to contractors; for $0.015/call you can resolve a plate to VIN → then use vehicle API to perform actions**
- A technique discussed in this episode for security research and bug bounty hunting.

**Open redirect + auth header leak in OKHTTP: Authorization header is stripped on cross-host redirect**
- but other custom headers pass through; critical mobile SSRF/ATO gadget

****Cross**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**License Plate → VIN API: DMV sells records to contractors; for $0.015/call you can resolve a plate to VIN → then use vehicle API to perform actions**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Open redirect + auth header leak in OKHTTP: Authorization header is stripped on cross-host redirect**
- **What it is:** but other custom headers pass through; critical mobile SSRF/ATO gadget
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cross-window forgery drag-and-drop: Attacker page overlays victim page, captures drag-and-drop events → injects payload into victim site form fields**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Sam Curry: "Don't force yourself to be a bug bounty hunter. If it's not working, step away. I've never found a bug under pressure"* — **always when relaxed and curious.**
- *"The mentor I had for Magnus Carlsen told him to step away and have fun with chess"* — **that's how he became the greatest.**
- *"Working with Shubs changed a lot for me"* — **he wanted to do high-impact research for the sake of it, and that reframed my approach.**
- *"Collaboration philosophy: "There's no elitist group"* — **just 'hey I'm gonna spam you with stuff and if you want to help, help'**

#### 6. Mental models
- **Sam Curry: "Don't force yourself to be a bug bounty hunter. ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The mentor I had for Magnus Carlsen told him to step away an** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Working with Shubs changed a lot for me — he wanted to do hi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Bug bounty income is unstable even at the top — Sam experienced burnout after 4 years of full-time bug bounty despite 100K+/year
- **Try this:** Establishing "good intent" and a public track record as a white-hat researcher provides legal cover for borderline research
- **Try this:** The most fun vulnerabilities are ones that feel like black-hat scenarios: making car horns honk, unlocking hotel rooms, changing grades
- **Try this:** Many massive vulnerabilities are trivially simple — SQL injection on a connected car platform with millions of devices

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Sam Curry's hacking is driven by curiosity/interest, not money — "don't force yo**
2. **Bug bounty income is unstable even at the top — Sam experienced burnout after 4 **
3. **Establishing "good intent" and a public track record as a white-hat researcher p**
