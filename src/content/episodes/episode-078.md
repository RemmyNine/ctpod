---
title: "Less Writing, More Hacking — Reporting Efficiency Techniques"
episode: 78
---


# Episode 78 Less Writing, More Hacking — Reporting Efficiency Techniques

**TL;DR**
- XSS WAF bypass via multi-character HTML entities (e.g., `&nvgt;` → `>`, `&nvlt;` → `<`)
- Next.js cache poisoning — cache poisoning is the new subdomain takeover for mass automation
- Sean Yo's "Hey, why can't you fix this one bug?" blog — security engineer perspective on why fixes take so long
- Fabric AI framework + report generation: `write_hackerone_report` pattern
- Report templates, POC videos, and friction reduction tools

**Key Takeaways**
- Use `&nvgt;` (new greater-than) and `&nvlt;` (new less-than) HTML entities to bypass WAF filters — they decode to `<` and `>` along with other characters
- Shazzer now has a fuzz for all ASCII/URL-encoded values that work in JavaScript URLs — run your payloads through it
- When you see a cache buster in source code, the app was likely cache-poisoning itself — dig into git blame to find when and why it was added
- For mass automation: cache poisoning has replaced subdomain takeover as the high-volume payout vector
- Use Fabric (`github.com/danielmiessler/fabric`) with custom patterns to auto-generate reports from request/response pairs
- Record POC videos with OBS; change encoder to `x264` and output to `mp4` to get a pause button

**Bugs and Findings**

### XSS WAF bypass via multi-character HTML entities
- **Target/context:** WAFs that filter `<` and `>` in user input
- **Root cause:** HTML entities like `&nvgt;` and `&nvlt;` decode to `<` and `>` after WAF inspection
- **Technique / how found:** The RCE man tweet; Gareth Hayes added fuzz to Shazzer
- **Exploitation steps:**
  1. Input `&nvgt;` where you need `>` — it decodes to `>` + Unicode character
  2. For JavaScript URLs: use `javascript:&hat;alert(1)` — `&hat;` (circumflex accent) decodes to `^` which is accepted in some contexts
- **Key technical details:** `&nvgt;` = `>` + combining character; `&nvlt;` = `<` + combining character; check Shazzer for full list
- **Impact / severity / bounty:** WAF bypass leading to XSS

### Next.js cache poisoning
- **Target/context:** Next.js applications
- **Root cause:** Custom headers reflected in cached responses; application was "cache poisoning itself" leading developers to add cache busters
- **Technique / how found:** Writeup linked in show notes (no specific author named in transcript)
- **Exploitation steps:**
  1. Grep the Next.js codebase for `x-` headers or custom header handling
  2. Find a header that modifies the response content
  3. Send a request with the malicious header → response gets cached
  4. Subsequent users receive the poisoned cache entry
- **Key technical details:** Look for cache busters in source code (they indicate a prior cache poisoning vulnerability); git blame reveals the commit that introduced the fix
- **Impact / severity / bounty:** Widespread impact — any user hitting the cached page gets the poisoned content

**Techniques and Primitives**
- **Cache buster as vulnerability signal** — If you see a cache buster in the codebase, the app was likely cache-poisoning itself — dig into the fix and bypass it
- **Git blame for vulnerability archaeology** — Find the commit that added a security fix, then analyze the PR for incomplete fixes or bypasses
- **Fabric pattern for report generation** — Use `write_hackerone_report` pattern with `bpreportformatter` to pipe request/response pairs into AI for auto-report generation

**Tooling and Resources**
- `shazzer.co.uk` — WAF bypass fuzzing
- `github.com/danielmiessler/fabric` — AI pattern framework
- `github.com/rhynorater/bpreportformatter` — Report formatter tool
- `github.com/rhynorater/reports` — Report templating software (Python 2.7, needs conversion)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 78 Less Writing, More Hacking — Reporting Efficiency Techniques covers practical bug bounty techniques and security research insights.

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
