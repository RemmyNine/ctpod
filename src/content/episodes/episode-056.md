---
title: "Using Data Science to Win Bug Bounty — Mayonaise (Jon Colston)"
episode: 56
---


# Episode 56 Using Data Science to Win Bug Bounty — Mayonaise (Jon Colston)

**Guest:** Jon Colston (Mayonaise / My Own Eyes)
**Format:** Full transcript (feed) — truncated at line 300; continues with keyword categorization, manual processes, data sources, digital marketing, M.O.A.B.s, burnout protection, dupe analysis

### TL;DR
- Jon Colston transitioned from digital marketing analytics to bug bounty and applied lead-gen/conversion-funnel methodology
- Focused on Yahoo/AOL's B2B advertising platforms — old, unhardened, pre-security-lifecycle code from acquisitions
- Built a data-driven system measuring EVERYTHING (word list hit rates, fuzz performance per subdomain, per path) to optimize recon
- "Ingredients and recipes" approach to subdomain/endpoint discovery — treat words as ingredients, paths as recipes, combine into permutations
- Automation wrapped around every tool; KPI logs for every sub-process

### Key Takeaways
- Measure everything — "what is not measured is not managed" (Peter Drucker). Track hit rates by word list, domain, path, program
- Wrap every tool with a logging layer that records inputs/outputs/hits/duration to flat files for later analysis
- Build "ingredients" from domain-word frequency analysis; combine into "recipes" for content discovery
- For B2B targets, demo accounts often have simple/default passwords; buying expired domains of defunct partner companies enables password reset hijack
- Trace every bug backwards through your recon pipeline to identify which data source/technique produced it
- When blocked by geolocation/ID requirements (e.g., Taiwan Yahoo), use Upwork to hire a local assistant
- Bug bounty is a leads game — build a system that generates "opportunities" for you to manually validate

### Techniques and Primitives
- **Ingredient/Recipe Discovery:** Break subdomains by dots/dashes, frequency-analyze words, group into categories (API, admin, env, region, version). Replace actual words with category labels. Identify common patterns/recipes. Fuzz all recipe permutations across hosts
- **KPI-Driven Fuzzing:** Track in/out/hit rate/time per word list per host. 10 top-performing lists → analyze why; replicate patterns; prune dead lists
- **Bug Traceability:** When a bug is submitted, trace backward through the recon pipeline to identify the source (SecurityTrails pull, CIDR scan, wayback, etc.) — optimize those sources

### Tooling and Resources
- Dehashed (credential search)
- Upwork (for hiring local assistants for region-locked targets)
- GoDaddy domain availability checker (for expired domains of defunct companies)

### Suggestions and Advices
- **Mayo:** "I call this practice retirement... I'm building a lead generation platform for hackers. It's gonna give me leads at the end of the day."
- On demo accounts: "The password is probably going to be very simplistic and a standard brute force password tracker will go after it."
- On getting accounts: "If you can figure out a way to overcome whatever barriers it is to get an account in your own credentials, then they can't stop you."
- On his skill ceiling: "My skill as a hacker is secondary. Whenever I watch you guys insert a hyperlink with this tag and redirect... I'm not going to go there. That's not my skillset. But if I can get to assets that nobody else has, that's what I'm going to do."

### AI Takeaway
The data-science approach is about *systematizing uncertainty reduction* — not automating exploitation. Mayo's insight is that most bug bounty recon is guesswork without measurement; his KPI-per-word-list framework transforms fuzzing from art to engineering. The "measure everything → optimize → replicate" loop is transferable to any target.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Jon Colston transitioned from digital marketing analytics to bug bounty and applied lead-gen/conversion-funnel methodology

#### 2. What you should learn
- Understand **measure everything — "what is not measured is not managed" (peter drucker). track hit rates by word list, domain, path, program**
- Understand **wrap every tool with a logging layer that records inputs/outputs/hits/duration to flat files for later analysis**
- Understand **build "ingredients" from domain-word frequency analysis; combine into "recipes" for content discovery**
- Understand **for b2b targets, demo accounts often have simple/default passwords; buying expired domains of defunct partner companies enables password reset hijack**
- Understand **trace every bug backwards through your recon pipeline to identify which data source/technique produced it**

#### 3. Core concepts explained
**Ingredient/Recipe Discovery: Break subdomains by dots/dashes, frequency**
- A technique discussed in this episode for security research and bug bounty hunting.

****KPI**
- A technique discussed in this episode for security research and bug bounty hunting.

**Bug Traceability: When a bug is submitted, trace backward through the recon pipeline to identify the source (SecurityTrails pull, CIDR scan, wayback, etc.)**
- optimize those sources


#### 4. Techniques and tactics
**Ingredient/Recipe Discovery: Break subdomains by dots/dashes, frequency-analyze words, group into categories (API, admin, env, region, version). Replace actual words with category labels. Identify common patterns/recipes. Fuzz all recipe permutations across hosts**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**KPI-Driven Fuzzing: Track in/out/hit rate/time per word list per host. 10 top-performing lists → analyze why; replicate patterns; prune dead lists**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Bug Traceability: When a bug is submitted, trace backward through the recon pipeline to identify the source (SecurityTrails pull, CIDR scan, wayback, etc.)**
- **What it is:** optimize those sources
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Mayo: "I call this practice retirement... I'm building a lead generation platform for hackers. It's gonna give me leads at the end of the day."*
- *"On demo accounts: "The password is probably going to be very simplistic and a standard brute force password tracker will go after it."*
- *"On getting accounts: "If you can figure out a way to overcome whatever barriers it is to get an account in your own credentials, then they can't stop you."*
- *"On his skill ceiling: "My skill as a hacker is secondary. Whenever I watch you guys insert a hyperlink with this tag and redirect... I'm not going to go there. That's not my skillset. But if I can get to assets that nobody else has, that's what I'm going to do."*

#### 6. Mental models
- **Mayo: "I call this practice retirement... I'm building a lea** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On demo accounts: "The password is probably going to be very** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On getting accounts: "If you can figure out a way to overcom** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Measure everything — "what is not measured is not managed" (Peter Drucker). Track hit rates by word list, domain, path, program
- **Try this:** Wrap every tool with a logging layer that records inputs/outputs/hits/duration to flat files for later analysis
- **Try this:** Build "ingredients" from domain-word frequency analysis; combine into "recipes" for content discovery
- **Try this:** For B2B targets, demo accounts often have simple/default passwords; buying expired domains of defunct partner companies enables password reset hijack

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **recon** — Reconnaissance — systematic discovery of target attack surface
- **fuzzing** — Sending unexpected or malformed data to discover vulnerabilities

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Jon Colston transitioned from digital marketing analytics to bug bounty and appl**
2. **Measure everything — "what is not measured is not managed" (Peter Drucker). Trac**
3. **Wrap every tool with a logging layer that records inputs/outputs/hits/duration t**
