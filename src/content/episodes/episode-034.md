---
title: "Program vs Hacker Debate"
episode: 34
---


# Episode 34 Program vs Hacker Debate

**Guests/Hosts:** Justin Gardner (representing hackers), Joel Margolis (representing program managers)  
**Date:** 2023-08-31 | **Duration:** 2:10:50

### TL;DR
- Long-form debate on zero-day policies, disclosure, dupes, CVSS, budgets, triage, retesting, and live hacking events
- Zero-days: programs should pay for impact on their asset, even if it's in a third-party product they use
- Disclosure: program has legal/comms concerns; researcher is bound by program terms; external disclosure via security@ vs platform bypass
- Internal dupes: transparency helps — show the internal ticket timestamp; if a bug sits for months unfixed, program should own that
- Retesting: H1 triage docs say triage should retest, but this never happens; $50 retest fee is small; bypasses should earn a bonus

### Key Takeaways
- **On zero-days**: Pay for impact, not fault. If a third-party product affects you, you're responsible. Accept reduced bounty for zero-days (not max) but don't reject them outright.
- **On disclosure**: Program terms bind you; going around them risks ban/legal. Use `security@` if you want to disclose. Transparency from both sides is key.
- **On CVSS**: Better than rigid alternatives, but impact should drive payouts, not a generic formula. Programs should communicate their threat model.
- **On budgets**: Bounty budgets come from security team allocation; paying too much signals internal security deficiencies. But paying minimum at triage is recommended.
- **On retesting**: Should be paid ($50 minimum); bypasses are the same root cause — bonus, not full bounty.

### Suggestions and Advices from Hunter
- Joel (as program): "If you really want to disclose something and the company doesn't want you to, you're setting yourself up for a rocky relationship."
- Justin: "Essentially what you just said is 'we're paying you to keep your mouth shut.' That feels sketchy."
- Joel: "On internal dupes: take a screenshot of the internal ticket. Show the researcher it's real."
- Joel: "The program that pays millions in bounties every year and that number isn't going down — either you're raising bounties or your security team isn't doing their job."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Long-form debate on zero-day policies, disclosure, dupes, CVSS, budgets, triage, retesting, and live hacking events

#### 2. What you should learn
- Understand **on zero-days**: pay for impact, not fault. if a third-party product affects you, you're responsible. accept reduced bounty for zero-days (not max) but don't reject them outright**
- Understand **on disclosure**: program terms bind you; going around them risks ban/legal. use `security@` if you want to disclose. transparency from both sides is key**
- Understand **on cvss**: better than rigid alternatives, but impact should drive payouts, not a generic formula. programs should communicate their threat model**
- Understand **on budgets**: bounty budgets come from security team allocation; paying too much signals internal security deficiencies. but paying minimum at triage is recommended**
- Understand **on retesting**: should be paid ($50 minimum); bypasses are the same root cause — bonus, not full bounty**

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Joel (as program): "If you really want to disclose something and the company doesn't want you to, you're setting yourself up for a rocky relationship."*
- *"Justin: "Essentially what you just said is 'we're paying you to keep your mouth shut.' That feels sketchy."*
- *"Joel: "On internal dupes: take a screenshot of the internal ticket. Show the researcher it's real."*
- *"Joel: "The program that pays millions in bounties every year and that number isn't going down"* — **either you're raising bounties or your security team isn't doing their job.**

#### 6. Mental models
- **Joel (as program): "If you really want to disclose something** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Justin: "Essentially what you just said is 'we're paying you** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: "On internal dupes: take a screenshot of the internal ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** On zero-days**: Pay for impact, not fault. If a third-party product affects you, you're responsible. Accept reduced bounty for zero-days (not max) but don't reject them outright.
- **Try this:** On disclosure**: Program terms bind you; going around them risks ban/legal. Use `security@` if you want to disclose. Transparency from both sides is key.
- **Try this:** On CVSS**: Better than rigid alternatives, but impact should drive payouts, not a generic formula. Programs should communicate their threat model.
- **Try this:** On budgets**: Bounty budgets come from security team allocation; paying too much signals internal security deficiencies. But paying minimum at triage is recommended.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Long-form debate on zero-day policies, disclosure, dupes, CVSS, budgets, triage,**
2. **On zero-days**: Pay for impact, not fault. If a third-party product affects you,**
3. **On disclosure**: Program terms bind you; going around them risks ban/legal. Use **
