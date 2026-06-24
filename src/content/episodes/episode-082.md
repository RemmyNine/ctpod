---
title: "Part-Time Bug Bounty"
episode: 82
---


# Episode 82 Part-Time Bug Bounty

**TL;DR**
- Solo Joel episode: strategies for part-time bug bounty hunting
- Program selection: optimize for payout vs impact, use program stat analysis
- Friction reduction: find your blockers (report templates, bash aliases, custom tools)
- Note-taking: Notion, Obsidian, sticky notes, video/voice memos — but reviewing notes is the critical part
- Douglas Day's "follow the nos" approach: look for things the documentation says shouldn't be possible

**Key Takeaways**
- Track your time with Clockify (free) or a spreadsheet; be honest about zeros
- If you're going deep on one program, become as knowledgeable as an engineer at that company — you'll connect gadgets across features
- Script to analyze HackerOne programs by payout statistics: look at programs that adhere tightly to their bounty table and CVSS scoring
- Map the attack surface first: find all endpoints, user info locations, permission checks, before diving into exploitation
- Use cliffhangers (stop at an exciting point) to maintain motivation for the next session
- Record 3–5 minute video/audio memos at the end of each hacking session to quickly re-enter the flow next time

**Techniques and Primitives**
- **Program payout analysis** — Use HackerOne API/cookie to scrape bounty tables; calculate avg payout vs max payout deviation to find programs that pay close to their table
- **"Follow the nos"** — Read documentation for permission/role restrictions; test every explicitly forbidden action
- **Friction audit** — List everything that annoys you during a hacking session; fix each one (or build a tool for it) before the next session
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 82 Part-Time Bug Bounty covers practical bug bounty techniques and security research insights.

#### 2. What you should learn
- Understand the vulnerability classes discussed
- Learn practical exploitation techniques
- Know which tools are useful for this type of research

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
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

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
1. **Understand the vulnerability class** — Know how it works and why it matters
2. **Master the exploitation technique** — Practice the specific steps to exploit it
3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets
