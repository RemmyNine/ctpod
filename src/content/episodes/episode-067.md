---
title: "VDPs & Accidental Program VS Hacker Debate Part 2"
episode: 67
---


# Episode 67 VDPs & Accidental Program VS Hacker Debate Part 2

**Guests:** Justin Gardner, Joel Margolis
**Format:** Full transcript (feed)
**Topics:** Vulnerability Disclosure Programs, leaderboard accuracy, program vs hacker debate, walling off endpoints

### TL;DR
- In-depth debate on VDPs: whether they're harmful to the ecosystem vs appropriate for certain orgs
- Nagli's braindump claims: VDPs are free labor, skew leaderboards, create same-scope conflicts with private bounty programs
- Joel argues VDPs are "worse for bug bounty hunters, worse for paid programs"
- Justin describes a company with VDP + private bounty where lows stay unpriced but higher findings are moved to bounty program and paid — a hybrid model
- Bounty table inflation: crits went from 10K (2019) to 50K-100K (2024) at top programs; 5K crits are now below the threshold for many top hunters
- Walling off endpoints with WAF/reverse proxy rules is common for emergency fixes (break-glass process) — creates opportunity for bypass researchers

### Key Takeaways
- HackerOne should separate VDP rep from bounty rep on leaderboards — Bugcrowd already removed VDP points
- Program leaderboards should default to last 365 days, not all-time — top hackers often haven't touched a program in years
- Finance justification for bounties is harder than AppSec justification — bug bounty puts a direct dollar value on developer mistakes, creating internal tension
- VDPs make sense for companies that can't afford to pay for every vulnerability OR have such a massive footprint that paying per-bug is unsustainable
- "Security is a feature" analogy: features are funded, maintained, and tested continuously — security should be too

### Techniques and Primitives
- **Same-scope VDP + private bounty harvesting:** Find bugs through VDP (free), get invited to private program after good submissions — but lows stay unpaid unless researcher negotiates moving them
- **WAF-as-emergency-fix bypass:** When a vulnerability is WAF-blocked rather than code-fixed, study the edge proxy behavior — Nginx/Akamai/Cloudflare configs often have bypassable regex

### Suggestions and Advices
- **Justin:** "If you make a POC that demonstrates full attack path and wormability, you can get 150% of standard bounty"
- **Joel:** "VDPs are not the same as bounties. If we're going to have points, let's keep it separate."
- **Joel:** "If you're a 50 billion dollar company, you should have at least a little bit of money where your mouth is on your security team."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
In-depth debate on VDPs: whether they're harmful to the ecosystem vs appropriate for certain orgs

#### 2. What you should learn
- Understand **hackerone should separate vdp rep from bounty rep on leaderboards — bugcrowd already removed vdp points**
- Understand **program leaderboards should default to last 365 days, not all-time — top hackers often haven't touched a program in years**
- Understand **finance justification for bounties is harder than appsec justification — bug bounty puts a direct dollar value on developer mistakes, creating internal tension**
- Understand **vdps make sense for companies that can't afford to pay for every vulnerability or have such a massive footprint that paying per-bug is unsustainable**
- Understand **"security is a feature" analogy: features are funded, maintained, and tested continuously — security should be too**

#### 3. Core concepts explained
**Same-scope VDP + private bounty harvesting: Find bugs through VDP (free), get invited to private program after good submissions**
- but lows stay unpaid unless researcher negotiates moving them

**WAF-as-emergency-fix bypass: When a vulnerability is WAF-blocked rather than code-fixed, study the edge proxy behavior**
- Nginx/Akamai/Cloudflare configs often have bypassable regex


#### 4. Techniques and tactics
**Same-scope VDP + private bounty harvesting: Find bugs through VDP (free), get invited to private program after good submissions**
- **What it is:** but lows stay unpaid unless researcher negotiates moving them
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WAF-as-emergency-fix bypass: When a vulnerability is WAF-blocked rather than code-fixed, study the edge proxy behavior**
- **What it is:** Nginx/Akamai/Cloudflare configs often have bypassable regex
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Justin: "If you make a POC that demonstrates full attack path and wormability, you can get 150% of standard bounty"*
- *"Joel: "VDPs are not the same as bounties. If we're going to have points, let's keep it separate."*
- *"Joel: "If you're a 50 billion dollar company, you should have at least a little bit of money where your mouth is on your security team."*

#### 6. Mental models
- **Justin: "If you make a POC that demonstrates full attack pat** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: "VDPs are not the same as bounties. If we're going to ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: "If you're a 50 billion dollar company, you should hav** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** HackerOne should separate VDP rep from bounty rep on leaderboards — Bugcrowd already removed VDP points
- **Try this:** Program leaderboards should default to last 365 days, not all-time — top hackers often haven't touched a program in years
- **Try this:** Finance justification for bounties is harder than AppSec justification — bug bounty puts a direct dollar value on developer mistakes, creating internal tension
- **Try this:** VDPs make sense for companies that can't afford to pay for every vulnerability OR have such a massive footprint that paying per-bug is unsustainable

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **In-depth debate on VDPs: whether they're harmful to the ecosystem vs appropriate**
2. **HackerOne should separate VDP rep from bounty rep on leaderboards — Bugcrowd alr**
3. **Program leaderboards should default to last 365 days, not all-time — top hackers**
