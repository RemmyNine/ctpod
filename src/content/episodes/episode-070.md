---
title: "NahamCon and CSP Bypasses Everywhere"
episode: 70
---


# Episode 70 NahamCon and CSP Bypasses Everywhere

**Guests:** Ben (NahamSec), Justin Gardner, Joel Margolis
**Format:** Full transcript (ASR)
**Topics:** NahamCon 2024 (May 24-25), Meta bug bounty program, CSP bypasses via Google JSONP endpoints, CI/CD dependency confusion, .gitignore recon

### TL;DR
- Meta's bug bounty is one of the best-run programs: up to 300K bounties, loyalty tier bonuses (20K+), "explore authorization" for researchers to demonstrate full impact
- JSONP CSP bypasses for Google: `www.youtube.com`, `www.googleapis.com`, `www.google.com` — callback parameters that allow arbitrary function execution
- CI/CD recon: `.gitignore` files leaking paths → correlate with web server paths → find exposed config/credential files
- NahamCon 2024 has 50K in Yahoo bounties + full Defcon scholarship for one winner

### Key Takeaways
- Meta program highlights: they give time-limited authorization to explore beyond the initial finding; if you prove broader impact, they increase payout and do their own variant analysis
- Google JSONP endpoints for CSP bypass: search for `?callback=` or `?jsonp=` parameters on `*.google.com` — many are well-known but some are undocumented
- `.gitignore` file analysis: extract paths (logs/, uploads/, config.json, .gitlab-ci.yml) and test on web server — if exposed, often leads to credential leaks
- AI + recon: give GPT 6 configuration filenames → ask for 50 more → test across web assets
- The `;` and `+` are valid in email addresses per RFC — `"@` can also appear; developers copying Stack Overflow regex blindly miss these

### Bugs and Findings

#### YouTube/Google JSONP CSP Bypass
- **Target:** CSP-protected sites that allowlist `*.google.com`, `www.youtube.com`, etc.
- **Endpoint examples:**
  - `www.youtube.com` — JSONP callback (specific endpoint redacted)
  - `www.googleapis.com` — JSONP callback
  - `oauth.google.com` — callback parameter
- **Technique:** `<script src="https://www.youtube.com/...?callback=alert(1)">` → executes `alert(1)` in the context of the page

### Techniques and Primitives
- **JSONP CSP Bypass:** When CSP allows a domain that has a JSONP endpoint, include `<script>` tag with `?callback=` parameter — the response wraps data in a function call that executes in your context
- **`.gitignore` recon workflow:** Download `.gitignore` from target → extract paths → test each path on live web server for accessible config files, CI/CD configs, uploaded files
- **Auth header stripping (OKHTTP):** On redirect to different host, OKHTTP strips `Authorization` header but passes other custom headers — exploit via open redirect to leak non-auth tokens

### Tooling and Resources
- NahamCon 2024: `nahamcon.com`
- Project Discovery — Nuclei 3.2 (authenticated scanning, advanced fuzzing)
- Depshield/Loophin's "Deppy" — CI/CD dependency scanning tool
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Meta's bug bounty is one of the best-run programs: up to 300K bounties, loyalty tier bonuses (20K+), "explore authorization" for researchers to demonstrate full impact

#### 2. What you should learn
- Understand **meta program highlights: they give time-limited authorization to explore beyond the initial finding; if you prove broader impact, they increase payout and do their own variant analysis**
- Understand **google jsonp endpoints for csp bypass: search for `?callback=` or `?jsonp=` parameters on `*.google.com` — many are well-known but some are undocumented**
- Understand **`.gitignore` file analysis: extract paths (logs/, uploads/, config.json, .gitlab-ci.yml) and test on web server — if exposed, often leads to credential leaks**
- Understand **ai + recon: give gpt 6 configuration filenames → ask for 50 more → test across web assets**
- Understand **the `;` and `+` are valid in email addresses per rfc — `"@` can also appear; developers copying stack overflow regex blindly miss these**

#### 3. Core concepts explained
**YouTube/Google JSONP CSP Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**JSONP CSP Bypass: When CSP allows a domain that has a JSONP endpoint, include `<script>` tag with `?callback=` parameter**
- the response wraps data in a function call that executes in your context

**`.gitignore` recon workflow: Download `.gitignore` from target → extract paths → test each path on live web server for accessible config files, CI/CD configs, uploaded files**
- A technique discussed in this episode for security research and bug bounty hunting.

**Auth header stripping (OKHTTP): On redirect to different host, OKHTTP strips `Authorization` header but passes other custom headers**
- exploit via open redirect to leak non-auth tokens


#### 4. Techniques and tactics
**JSONP CSP Bypass: When CSP allows a domain that has a JSONP endpoint, include `<script>` tag with `?callback=` parameter**
- **What it is:** the response wraps data in a function call that executes in your context
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`.gitignore` recon workflow: Download `.gitignore` from target → extract paths → test each path on live web server for accessible config files, CI/CD configs, uploaded files**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Auth header stripping (OKHTTP): On redirect to different host, OKHTTP strips `Authorization` header but passes other custom headers**
- **What it is:** exploit via open redirect to leak non-auth tokens
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** Meta program highlights: they give time-limited authorization to explore beyond the initial finding; if you prove broader impact, they increase payout and do their own variant analysis
- **Try this:** Google JSONP endpoints for CSP bypass: search for `?callback=` or `?jsonp=` parameters on `*.google.com` — many are well-known but some are undocumented
- **Try this:** `.gitignore` file analysis: extract paths (logs/, uploads/, config.json, .gitlab-ci.yml) and test on web server — if exposed, often leads to credential leaks
- **Try this:** AI + recon: give GPT 6 configuration filenames → ask for 50 more → test across web assets

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in YouTube/Google JSONP CSP Bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Meta's bug bounty is one of the best-run programs: up to 300K bounties, loyalty **
2. **Meta program highlights: they give time-limited authorization to explore beyond **
3. **Google JSONP endpoints for CSP bypass: search for `?callback=` or `?jsonp=` para**
