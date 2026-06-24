---
title: "Practical Applications of DEFCON 32 Web Research"
episode: 85
---


# Episode 85 Practical Applications of DEFCON 32 Web Research

**TL;DR**
- James Kettle timing attacks: dual-packet sync improves single-packet attack; scoped SSRF new vuln class
- Gareth Hayes email research: `encoded-word` (RFC 2047), UUCP protocol, source routing (percent hack), punycode decoding bugs
- Orange Tsai Apache HTTPD confusion attacks: path/directory confusion due to hidden semantic ambiguity in different modules
- Cache poisoning research: "Gotta Cache 'em All" — cache deception and poisoning techniques

**Key Takeaways**
- For timing attacks: use the lower quartile of response times (not median/mean) to filter out server-load noise
- Dual-packet sync: ensures HTTP headers are processed simultaneously with body — critical for microsecond-level timing measurements
- Scoped SSRF: reverse proxies configured with `*.domain.com` can be detected via DNS timing — if a 64-char domain label resolves but 65-char doesn't, DNS resolution is occurring
- For email validation testing: try `=?UTF-8?Q?=61=62=63?=@domain.com` (encoded-word format) — `abc@domain.com` decodes after SMTP processing
- UUCP attack: `domain!user\@allowed.com` — the `!` delimited UUCP format and `\` escaping the `@` causes SMTP to send to `user@domain` instead of `user@allowed.com`
- Source routing / percent hack: `user%attacker.com@victim.com` — SMTP source routing sends to `user@attacker.com` first, then to `user@victim.com`

**Bugs and Findings**

### Scoped SSRF via timing analysis
- **Target/context:** Reverse proxies configured with wildcard domains
- **Root cause:** The reverse proxy resolves the host header against internal DNS, creating a measurable timing difference
- **Technique / how found:** James Kettle DEFCON 2024 research
- **Exploitation steps:**
  1. Send request with `Host: <64-char-label>.target.com` — note response time
  2. Send request with `Host: <65-char-label>.target.com` — DNS resolution fails immediately
  3. If the 64-char request is significantly slower (100ms+), the proxy is resolving DNS = it's a reverse proxy, not vhost
  4. Use `Host: internal-service.internal-network.com` to pivot
- **Key technical details:** Domain labels over 64 characters are invalid per RFC; DNS libraries reject them without attempting resolution
- **Impact / severity / bounty:** Internal network pivoting, SSRF

### Encoded-word email validation bypass
- **Target/context:** Applications using email domain as an access control (e.g., Slack auto-join, GitHub enterprise)
- **Root cause:** The application sees the encoded form as a different domain; SMTP/email systems decode it
- **Technique / how found:** Gareth Hayes DEFCON 2024 research
- **Exploitation steps:**
  1. Register with email `=?UTF-8?Q?user?=@attacker.com` — the application sees `@attacker.com` and allows it
  2. The SMTP server sends the email to `user@attacker.com` (the decoded form)
  3. If the application sends a verification link to `@victim.com` instead, use encoding to make SMTP route it to attacker
- **Key technical details:** Format: `=?charset?encoding?encoded-text?=`. `Q` = quoted-printable, `B` = base64
- **Impact / severity / bounty:** Domain restriction bypass, account takeover

### UUCP SMTP bypass
- **Target/context:** Applications using Ruby's `Mail` gem or Sendmail/Postfix
- **Root cause:** UUCP format `domain!user` is still supported by Sendmail 8.15.2 and Postfix
- **Technique / how found:** Gareth Hayes; discovered by accident when fuzzing characters
- **Exploitation steps:**
  1. Input email: `victim.com!user\@allowed-domain.com`
  2. Application sees `@allowed-domain.com` — passes domain check
  3. SMTP sees `victim.com!user` (backslash escapes the `@`) — sends to `user@victim.com`
- **Key technical details:** The `!` character triggers UUCP routing; backslash escapes the `@` so it's not treated as email separator
- **Impact / severity / bounty:** Domain restriction bypass, ability to receive verification emails on attacker-controlled domains

### Source routing / percent hack
- **Target/context:** Postfix (and possibly other MTAs)
- **Root cause:** `%` character in local part interpreted as source routing delimiter
- **Exploitation steps:**
  1. Input: `user%attacker.com@victim.com`
  2. Application sees `@victim.com` — passes
  3. SMTP routes: first sends to `user%attacker.com@victim.com` (at victim.com), then to `user@attacker.com`
- **Key technical details:** Postfix expands `user%domain` as `user@domain` in source routing
- **Impact / severity / bounty:** Domain restriction bypass

### PHP punycode decoding bug → CSS injection → RCE (Joomla)
- **Target/context:** Joomla (and any app using PHP's IDN library)
- **Root cause:** PHP IDN library mis-decodes punycode with leading zeros, generating invalid characters like `@` and `,`
- **Technique / how found:** Gareth Hayes + Joomla researcher collaboration
- **Exploitation steps:**
  1. Submit punycode domain like `xn--<encoded>` with two leading zeros
  2. PHP decodes it to a string containing `@` — which was not present in the original
  3. This creates an HTML injection (opening `<style>` tag)
  4. Chain with another injection point to close the style tag and initiate CSS injection import chain
  5. Use CSS import chaining to exfiltrate CSRF token
  6. CSRF → account takeover (and potentially RCE via admin panel)
- **Key technical details:** Leading zeros in punycode produce unintended characters; CSS import chaining exfiltrates character-by-character via `@import` recursion
- **Impact / severity / bounty:** RCE via chain

**Techniques and Primitives**
- **Lower quartile timing analysis** — Use fastest 25% of response times to eliminate noise from server load
- **DNS label length fingerprinting** — 64 vs 65 character domain labels to detect DNS resolution (scoped SSRF detection)
- **Encoded-word (=?UTF-8?Q?...) entry point** — Test this format anywhere email addresses are validated
- **UUCP `!` and `\` bypass** — `domain!user\@allowed.com` for SMTP routing bypass

**Tooling and Resources**
- `portswigger.net/research/listen-to-the-whispers-web-timing-attacks-that-actually-work` — James Kettle timing attacks
- `portswigger.net/research/splitting-the-email-atom` — Gareth Hayes email research
- `portswigger.net/research/gotta-cache-em-all` — Cache poisoning research
- `github.com/narfindustries/http-garden` — HTTP test harness
- `blog.orange.tw/2024/08/confusion-attacks-en.html` — Orange Tsai Apache confusion attacks
- `github.com/filedescriptor/untrusted-types` — Untrusted types bypass
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 85 Practical Applications of DEFCON 32 Web Research covers practical bug bounty techniques and security research insights.

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
