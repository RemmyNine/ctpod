---
title: "News, Tools, and Writeups"
episode: 88
---


# Episode 88 News, Tools, and Writeups

**TL;DR**
- PortSwigger URL validation bypass cheat sheet: interactive payload generator for redirects, host headers, CORS
- Sanic DNS: 5M+ DNS lookups per second (replacing MassDNS as the premier bulk resolver)
- Orange confusion attacks Dockerized by Hari Sekhon
- WordPress GiveWP POP chain to RCE
- XSSTools: JavaScript library for XSS payload generation (keylogger, clickjacker, exfiltrators)
- Browser tracking protection bypass: `window.open` creates a 30-day trust relationship in Firefox

**Key Takeaways**
- New PortSwigger cheat sheet: input allowed domain + attacker domain + options → generates hundreds of URL validation bypass payloads with descriptions
- Sanic DNS uses XDP sockets and i40e drivers for kernel-level packet processing — requires 10Gbps+ NIC, DPDK huge pages
- XSSTools (`github.com/yeswehack/xsstools`) provides modular XSS exfiltration: postMessage, fetch, beacon, image, iframe exfils ready to use
- Browser tracking protection (ITP) in Safari/Firefox blocks third-party credentialed requests unless a `window.open` trust relationship exists (30 days in Firefox)
- WordPress nonce-only checks: `wp_ajax_*` hooks with nonce verification but no capability check can be called by any user who can obtain the nonce

**Bugs and Findings**

### WordPress GiveWP POP chain → RCE
- **Target/context:** GiveWP WordPress plugin (PHP deserialization)
- **Root cause:** PHP object injection via `stripcslashes` deep in the POP chain
- **Technique / how found:** Mr. TuxRacer; nonce-only auth bypass on `wp_ajax_*` handler
- **Exploitation steps:**
  1. Identify `wp_ajax_*` action that lacks capability check (only nonce verification)
  2. Leak the nonce (often accessible from subscriber-level or even public pages)
  3. Trigger the action → user-controlled data enters `stripcslashes()` → PHP object injection
  4. Chain a POP gadget through 5+ classes to reach `eval()` or file write
  5. Note: use 4 backslashes to bypass `stripcslashes` (each pair `\\` → single `\`, leaving `\\` which is an escaped backslash → `\`)
- **Key technical details:** `stripcslashes` removes one level of escaping; four backslashes `\\\\` become `\\` which represents a single backslash in the final context
- **Impact / severity / bounty:** Pre-auth RCE

### Browser tracking protection bypass
- **Target/context:** Firefox/Safari users; CORS misconfigurations relying on SameSite cookies
- **Root cause:** ITP (Intelligent Tracking Protection) requires a prior `window.open` relationship for third-party credentialed requests
- **Technique / how found:** PT Security Team blog post
- **Exploitation steps:**
  1. `window.open('https://target.com/page')` from attacker origin to target
  2. Firefox stores this trust relationship for 30 days
  3. Now the attacker origin can send credentialed requests (fetch/XHR) to target.com
  4. Safari requires a 2-second `setTimeout` delay before the request
- **Key technical details:** Firefox trust lasts 30 days; Safari needs 2s delay; Chrome uses SameSite=None + Secure as the equivalent mechanism
- **Impact / severity / bounty:** Enables exploitation of CORS misconfigurations that would otherwise be blocked by SameSite cookies

**Techniques and Primitives**
- **URL validation bypass cheat sheet** — Use the new PortSwigger interactive tool for open redirect, SSRF, host header testing
- **MassDNS replacement** — Sanic DNS for bulk resolution at 5M+ requests/second (needs high-end NIC + DPDK)
- **Dockerized research** — Orange Confusion Attacks Docker image for reproducible Apache confusion attack testing
- **Four-backslash `stripcslashes` bypass** — `\\\\\\\\` in PHP payloads survives `stripcslashes()` and produces `\\\\` = two literal backslashes
- **Nonce-only auth bypass in WordPress** — Test `wp_ajax_*` hooks that only verify nonces without `current_user_can()` checks
- **Window.open for ITP bypass** — In Firefox: one `window.open` creates 30 days of cross-origin credentialed request ability

**Tooling and Resources**
- `portswigger.net/url-validation-bypass` — URL validation bypass cheat sheet
- `github.com/sanic-dns/sanic-dns` — Sanic DNS
- `github.com/narfindustries/http-garden` — Orange confusion attacks Dockerized
- `github.com/yeswehack/xsstools` — XSSTools
- `github.com/nmatt0/mitmrouter` — mitmrouter
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 88 News, Tools, and Writeups covers practical bug bounty techniques and security research insights.

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
