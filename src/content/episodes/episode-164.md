---
title: "Tommy DeVoss: From Black Hat to Bug Bounty LEGEND"
episode: 164
---


# Episode 164 Tommy DeVoss: From Black Hat to Bug Bounty LEGEND

### TL;DR
- Tommy's origin story: Black hat in the 90s (IRC botnets, website defacements), caught multiple times, 2.5 years prison, reformed into bug bounty
- $180K from 18 SSRF reports on Yahoo by octal-encoding just the first octet of `169.254.169.254`
- Deep dive on SSRF bypass techniques: blacklists vs allowlists, encoding tricks
- Python pitfalls: `os.path.join()` and `urlib.parse.urljoin()` ignore prefixes when given absolute paths/URLs
- Strong opinion: scope compliance is critical — one scope violation = potential CFAA violation

### Key Takeaways
- [ ] Go back and re-test old SSRF reports with new encoding bypasses — Tommy got 18×$10K by re-finding the same bug class with a single-octet octal encoding
- [ ] Test `os.path.join("/safe/prefix", attacker_path)` with absolute paths — Python ignores the prefix entirely; same for `urlib.parse.urljoin()`
- [ ] Always record POC video immediately on discovery — document everything before the server goes down or creds expire
- [ ] Never hack from your own machine — use jump boxes (Tommy's rule from black hat days)
- [ ] For bug bounty, scope compliance is non-negotiable — "All it takes is one pissed off chief legal officer"

### Bugs and Findings

#### Yahoo SSRF — Octal-Encoded AWS Metadata IP
- **Target/context:** Yahoo SSRF endpoints with IP blacklist
- **Root cause:** Yahoo used a blacklist (not allowlist) for IP filtering; one-octet octal encoding of `169` bypassed it
- **Technique:** Instead of `169.254.169.254`, use `0251.254.169.254` (octal for 169) — only the first octet needs encoding
- **Key technical details:** `169` octal = `0251`; encoding must be only the first octet; apparently the 4-char first octet bypassed validation logic
- **Exploitation steps:** 1) Find SSRF endpoint 2) Use `http://0251.254.169.254/latest/meta-data/iam/security-credentials/` 3) Retrieve AWS creds
- **Impact / severity / bounty:** $10K per report × 18 reports = $180K; AWS metadata access

**Obstacles & how solved:** Tommy found the bypass by encoding just the first octet (not the whole IP) while bored/tinkering during idle time before going out.

#### Python `os.path.join()` Prefix Bypass
- **Target/context:** Python apps using `os.path.join(SAFE_PREFIX, user_input)` for path construction
- **Root cause:** If the second argument is an absolute path (starts with `/`), `os.path.join` discards the prefix entirely
- **Technique:** Supply `/etc/passwd` as user input → resolves to `/etc/passwd` instead of `/safe/prefix/etc/passwd`
- **Key technical details:** `os.path.join("/safe/uploads", "/etc/passwd")` → `/etc/passwd`
- **Impact / severity / bounty:** Path traversal, arbitrary file read/write

#### Python `urlib.parse.urljoin()` Domain Bypass
- **Target/context:** Python apps using `urlib.parse.urljoin(BASE_URL, user_input)` for URL construction
- **Root cause:** If the second argument is an absolute URL (has scheme), the base URL is discarded
- **Technique:** Supply `https://evil.com/` → result is `https://evil.com/` instead of `https://example.com/evil.com`
- **Key technical details:** `urlib.parse.urljoin("https://example.com", "https://evil.com")` → `https://evil.com`
- **Impact / severity / bounty:** SSRF, open redirect, server-side request hijacking

### Techniques and Primitives
- **Octal IP encoding for SSRF bypass** — Encode one octet at a time: a 4-character octet (e.g., `0251`) may bypass string-length-based blacklist checks
- **Old SSRF regression testing** — Re-test closed SSRF reports with new bypass techniques; companies often don't backport fixes
- **Absolute path/URL injection** — In Python, `os.path.join` and `urlib.parse.urljoin` treat absolute second arguments as complete replacements

### Suggestions and Advices from Hunter
- "If you deviate from scope in any way, shape, or form, there is absolutely nothing you can do to prevent a CFAA violation." — Tommy DeVoss
- "Just because it hasn't happened yet doesn't mean it can't."
- "Go back and look at old reports when you have a short amount of time to hack."
- "99% of the competition is not actually competition for anybody that has any kind of skill."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Tommy's origin story: Black hat in the 90s (IRC botnets, website defacements), caught multiple times, 2.5 years prison, reformed into bug bounty

#### 2. What you should learn
- Understand **[ ] go back and re-test old ssrf reports with new encoding bypasses — tommy got 18×$10k by re-finding the same bug class with a single-octet octal encoding**
- Understand **[ ] test `os.path.join("/safe/prefix", attacker_path)` with absolute paths — python ignores the prefix entirely; same for `urlib.parse.urljoin()`**
- Understand **[ ] always record poc video immediately on discovery — document everything before the server goes down or creds expire**
- Understand **[ ] never hack from your own machine — use jump boxes (tommy's rule from black hat days)**
- Understand **[ ] for bug bounty, scope compliance is non-negotiable — "all it takes is one pissed off chief legal officer"**

#### 3. Core concepts explained
**Yahoo SSRF — Octal-Encoded AWS Metadata IP**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Python `os.path.join()` Prefix Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Python `urlib.parse.urljoin()` Domain Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Octal IP encoding for SSRF bypass**
- Encode one octet at a time: a 4-character octet (e.g., `0251`) may bypass string-length-based blacklist checks

**Old SSRF regression testing**
- Re-test closed SSRF reports with new bypass techniques; companies often don't backport fixes

**Absolute path/URL injection**
- In Python, `os.path.join` and `urlib.parse.urljoin` treat absolute second arguments as complete replacements


#### 4. Techniques and tactics
**Octal IP encoding for SSRF bypass**
- **What it is:** Encode one octet at a time: a 4-character octet (e.g., `0251`) may bypass string-length-based blacklist checks
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Old SSRF regression testing**
- **What it is:** Re-test closed SSRF reports with new bypass techniques; companies often don't backport fixes
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Absolute path/URL injection**
- **What it is:** In Python, `os.path.join` and `urlib.parse.urljoin` treat absolute second arguments as complete replacements
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you deviate from scope in any way, shape, or form, there is absolutely nothing you can do to prevent a CFAA violation."* — **Tommy DeVoss**
- *"Just because it hasn't happened yet doesn't mean it can't."*
- *"Go back and look at old reports when you have a short amount of time to hack."*
- *"99% of the competition is not actually competition for anybody that has any kind of skill."*

#### 6. Mental models
- **If you deviate from scope in any way, shape, or form, there ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Just because it hasn't happened yet doesn't mean it can't.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Go back and look at old reports when you have a short amount** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Go back and re-test old SSRF reports with new encoding bypasses — Tommy got 18×$10K by re-finding the same bug class with a single-octet octal encoding
- **Try this:** [ ] Test `os.path.join("/safe/prefix", attacker_path)` with absolute paths — Python ignores the prefix entirely; same for `urlib.parse.urljoin()`
- **Try this:** [ ] Always record POC video immediately on discovery — document everything before the server goes down or creds expire
- **Try this:** [ ] Never hack from your own machine — use jump boxes (Tommy's rule from black hat days)

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Yahoo SSRF — Octal-Encoded AWS Metadata IP?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Tommy's origin story: Black hat in the 90s (IRC botnets, website defacements), c**
2. **[ ] Go back and re-test old SSRF reports with new encoding bypasses — Tommy got **
3. **[ ] Test `os.path.join("/safe/prefix", attacker_path)` with absolute paths — Pyt**
