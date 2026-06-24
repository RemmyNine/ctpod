---
title: "2xMVH & Multi-million dollar hacker Inhibitor181 (Cosmin)"
episode: 25
---


# Episode 25 2xMVH & Multi-million dollar hacker Inhibitor181 (Cosmin)

**Guests/Hosts:** Justin Gardner, Joel Margolis, Cosmin (Inhibitor181)  
**Date:** 2023-06-29 | **Duration:** 1:11:35

### TL;DR
- Cosmin is a 2x MVP (Most Valuable Hacker) at HackerOne live events, specializing in a single technology across multiple targets
- Deep expertise on one tech stack = transferable bug classes across any company using it
- Recorded live after Cosmin won MVH at the London live hacking event (two targets)
- Methodology: split time per target, go deep, use gut + intuition honed by years of experience
- Bug pipeline philosophy: submit and forget; do not chase bounties — let them come

### Key Takeaways
- In multi-target live events, pick ONE target per event and go deep; splitting attention reduces success rate
- Build "tricks.txt" — a file of small quirks/behaviors that inform your gut instinct on new targets
- Use custom word lists (not off-the-shelf) built from JS files, documentation, and map files
- Report writing: structured format — summary, explanation (for unfamiliar tech), reproduction steps, video PoC, impact section
- Financial stability enables long-term single-program focus; vulnerability pipeline (submit and forget) reduces stress

### Techniques and Primitives
- **Single-technology deep expertise** — Learn one prevalent tech stack across all its configurations; recognize patterns in any company using it
- **Word list from documentation** — Scrape the product's own docs and JS map files for a targeted, small (<10K) wordlist that hits hidden endpoints
- **Gut-driven iteration** — Try 5-6 mental iterations; if stuck, walk away; the solution often comes subconsciously after a break
- **Video PoC for complex bugs** — Always include a video for multi-step exploits; also write clear text steps because triagers copy-paste into Jira

### Bugs and Findings
*(No named bugs disclosed; Cosmin focuses on one specific unrevealed technology)*

### Tooling and Resources
- Cosmin's modified Burp Reflector plugin
- Custom automation tool that re-tests past findings in new environments
- Notion / text files for notes (Cosmin uses 7 text files: `notes`, `tricks`, `mobile`, and program names)

### Suggestions and Advices from Hunter
- "When I'm in the zone, I'm not switching targets. But if I exhaust the things I wanted to try, I move to something else that may come back later."
- On relationship with program: "I never felt like tricked. It's mutual respect. I was there for them, they were there for me."
- "You have to like hacking the technology. If I see a tech I hate, I just close the program."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Cosmin is a 2x MVP (Most Valuable Hacker) at HackerOne live events, specializing in a single technology across multiple targets

#### 2. What you should learn
- Understand **in multi-target live events, pick one target per event and go deep; splitting attention reduces success rate**
- Understand **build "tricks.txt" — a file of small quirks/behaviors that inform your gut instinct on new targets**
- Understand **use custom word lists (not off-the-shelf) built from js files, documentation, and map files**
- Understand **report writing: structured format — summary, explanation (for unfamiliar tech), reproduction steps, video poc, impact section**
- Understand **financial stability enables long-term single-program focus; vulnerability pipeline (submit and forget) reduces stress**

#### 3. Core concepts explained
**Single-technology deep expertise**
- Learn one prevalent tech stack across all its configurations; recognize patterns in any company using it

**Word list from documentation**
- Scrape the product's own docs and JS map files for a targeted, small (<10K) wordlist that hits hidden endpoints

**Gut-driven iteration**
- Try 5-6 mental iterations; if stuck, walk away; the solution often comes subconsciously after a break


#### 4. Techniques and tactics
**Single-technology deep expertise**
- **What it is:** Learn one prevalent tech stack across all its configurations; recognize patterns in any company using it
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Word list from documentation**
- **What it is:** Scrape the product's own docs and JS map files for a targeted, small (<10K) wordlist that hits hidden endpoints
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Gut-driven iteration**
- **What it is:** Try 5-6 mental iterations; if stuck, walk away; the solution often comes subconsciously after a break
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Video PoC for complex bugs**
- **What it is:** Always include a video for multi-step exploits; also write clear text steps because triagers copy-paste into Jira
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When I'm in the zone, I'm not switching targets. But if I exhaust the things I wanted to try, I move to something else that may come back later."*
- *"On relationship with program: "I never felt like tricked. It's mutual respect. I was there for them, they were there for me."*
- *"You have to like hacking the technology. If I see a tech I hate, I just close the program."*

#### 6. Mental models
- **When I'm in the zone, I'm not switching targets. But if I ex** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On relationship with program: "I never felt like tricked. It** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **You have to like hacking the technology. If I see a tech I h** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** In multi-target live events, pick ONE target per event and go deep; splitting attention reduces success rate
- **Try this:** Build "tricks.txt" — a file of small quirks/behaviors that inform your gut instinct on new targets
- **Try this:** Use custom word lists (not off-the-shelf) built from JS files, documentation, and map files
- **Try this:** Report writing: structured format — summary, explanation (for unfamiliar tech), reproduction steps, video PoC, impact section

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Cosmin is a 2x MVP (Most Valuable Hacker) at HackerOne live events, specializing**
2. **In multi-target live events, pick ONE target per event and go deep; splitting at**
3. **Build "tricks.txt" — a file of small quirks/behaviors that inform your gut insti**
