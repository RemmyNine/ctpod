---
title: "Research TLDRs & Smuggling Payloads in Well-Known Data Types"
episode: 72
---


# Episode 72 Research TLDRs & Smuggling Payloads in Well-Known Data Types

**Guests:** Justin Gardner, Joel Margolis
**Format:** Show notes with timestamps (feed)
**Topics:** PDF.js XSS, NextJS SSRF (AssetNote), bounty transparency, IPv6 payload smuggling, phone number payload smuggling, automatic WordPress SQLi, DomPurify bypass, GitHub Enterprise send() bug, Kaido extension updates

### TL;DR
- PDF.js XSS (CVE-2024-4367): font glyph rendering JavaScript evals user-controlled strings from PDF font data — affects all Firefox users (built-in PDF viewer)
- IPv6 zone IDs: `[::1%25zone.example.com]` — the `%` delimiter and zone ID can append arbitrary strings, confusing hostname parsers in Go, Python, C#
- Phone number smuggling: RFC allows `;ext=X` or `;phone-context=` in phone numbers — libraries that follow RFC strictly pass through XSS payloads via these parameters
- GitHub Enterprise `send()` bug: indirect method invocation in Ruby (`object.send(:method_name)`) with user-controlled method name — results in RCE
- HackerOne launched bounty transparency: shows average payout per severity and % of reports per severity — useful but all-time stats skew current reality

### Key Takeaways
- PDF.js vulnerability: font data embedded in PDF is concatenated into a JavaScript string and `eval()`'d for glyph rendering — close the function and execute arbitrary JS
- IPv6 address ambiguity: `[::1]` is loopback, but `[::1%25eth0]` can be parsed as `::1` + arbitrary suffix depending on library — bypass origin checks and SSRF filters
- Phone number validation libraries that fully comply with RFC 3966 allow `;extension=...` and `;phone-context=...` with arbitrary content
- HackerOne bounty transparency: good start but all-time stats don't reflect recent bounty table changes — reset on table update would be better
- Kaido update: Riddle built "Refresh Replay Headers" extension — one-click update of cookies/CSRF tokens from HTTP history

### Bugs and Findings

#### PDF.js XSS (CVE-2024-4367)
- **Target:** Mozilla PDF.js (built-in Firefox PDF viewer + any app embedding the library)
- **Root cause:** Font data from PDF is concatenated into JavaScript code and `eval()`'d for glyph rendering — unsanitized string interpolation
- **Exploitation:** Craft PDF with malicious font data containing `");alert(1);//` or similar → payload executed in PDF.js context
- **Impact:** XSS in Firefox's built-in PDF viewer (every Firefox user affected) and any site using PDF.js
- **POC:** Released by Codean Labs — downloadable PDF file that triggers the XSS

#### GitHub Enterprise send() RCE
- **Target:** GitHub Enterprise
- **Root cause:** Ruby `object.send(:method_name)` where `method_name` is partially user-controlled — indirect method invocation leads to arbitrary method call
- **Exploitation steps:** Chain send() call to invoke dangerous methods (e.g., `eval`, `system`, `exec`) via parent class methods or accessible object methods
- **Impact:** Pre-auth RCE in GitHub Enterprise instances
- **Disclosure:** December 26, 2023 — published 6 months later

### Techniques and Primitives
- **IPv6 Zone ID Smuggling:** `[::1%25http://evil.com]` — URL-encoded `%25` becomes `%` after decoding, making zone ID appear as a domain suffix to poorly-validated parsers
- **Phone Number Extension Smuggling:** `+1-555-555-5555;ext=<script>alert(1)</script>` — RFC-compliant parsing includes extension as part of phone number; if echoed unsanitized → XSS
- **Indirect Method Invocation (Sink Pattern):** Look for `object.send()` in Ruby, `call_user_func()` in PHP, `getattr()` in Python, `global()[name]()` in JS, `Method.invoke()` in Java — any pattern where user input selects which method/function to call

### Tooling and Resources
- Codean Labs — PDF.js POC + writeup
- AssetNote — NextJS SSRF writeup
- Slonser — IPv6 research
- MrTuxRacer — WordPress Automatic Plugin SQLi (CVE-2024-27956)
- Riddle's Kaido Refresh Replay Headers extension (via EvenBetter)
- `creastery` — GitHub Enterprise send() bug report

### Suggestions and Advices
- **Justin:** "When doing source code review, pay extra attention to indirect method invocation — it's a trend that produces RCE across languages."
- "If you want unauthenticated RCE, work backwards from sinks. The apps are too large to trace forward from sources."
- On data type smuggling: "We live in the details. Any RFC that creates edge cases in data representation is a bug farming ground."


### 📘 Episode Booklet

#### 1. Episode in one sentence
PDF.js XSS (CVE-2024-4367): font glyph rendering JavaScript evals user-controlled strings from PDF font data — affects all Firefox users (built-in PDF viewer)

#### 2. What you should learn
- Understand **pdf.js vulnerability: font data embedded in pdf is concatenated into a javascript string and `eval()`'d for glyph rendering — close the function and execute arbitrary js**
- Understand **ipv6 address ambiguity: `[::1]` is loopback, but `[::1%25eth0]` can be parsed as `::1` + arbitrary suffix depending on library — bypass origin checks and ssrf filters**
- Understand **phone number validation libraries that fully comply with rfc 3966 allow `;extension=...` and `;phone-context=...` with arbitrary content**
- Understand **hackerone bounty transparency: good start but all-time stats don't reflect recent bounty table changes — reset on table update would be better**
- Understand **kaido update: riddle built "refresh replay headers" extension — one-click update of cookies/csrf tokens from http history**

#### 3. Core concepts explained
**PDF.js XSS (CVE-2024-4367)**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**GitHub Enterprise send() RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**IPv6 Zone ID Smuggling: `[::1%25http://evil.com]`**
- URL-encoded `%25` becomes `%` after decoding, making zone ID appear as a domain suffix to poorly-validated parsers

**Phone Number Extension Smuggling: `+1-555-555-5555;ext=<script>alert(1)</script>`**
- RFC-compliant parsing includes extension as part of phone number; if echoed unsanitized → XSS

**Indirect Method Invocation (Sink Pattern): Look for `object.send()` in Ruby, `call_user_func()` in PHP, `getattr()` in Python, `global()[name]()` in JS, `Method.invoke()` in Java**
- any pattern where user input selects which method/function to call


#### 4. Techniques and tactics
**IPv6 Zone ID Smuggling: `[::1%25http://evil.com]`**
- **What it is:** URL-encoded `%25` becomes `%` after decoding, making zone ID appear as a domain suffix to poorly-validated parsers
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Phone Number Extension Smuggling: `+1-555-555-5555;ext=<script>alert(1)</script>`**
- **What it is:** RFC-compliant parsing includes extension as part of phone number; if echoed unsanitized → XSS
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Indirect Method Invocation (Sink Pattern): Look for `object.send()` in Ruby, `call_user_func()` in PHP, `getattr()` in Python, `global()[name]()` in JS, `Method.invoke()` in Java**
- **What it is:** any pattern where user input selects which method/function to call
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Justin: "When doing source code review, pay extra attention to indirect method invocation"* — **it's a trend that produces RCE across languages.**
- *"If you want unauthenticated RCE, work backwards from sinks. The apps are too large to trace forward from sources."*
- *"On data type smuggling: "We live in the details. Any RFC that creates edge cases in data representation is a bug farming ground."*

#### 6. Mental models
- **Justin: "When doing source code review, pay extra attention ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you want unauthenticated RCE, work backwards from sinks. ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On data type smuggling: "We live in the details. Any RFC tha** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** PDF.js vulnerability: font data embedded in PDF is concatenated into a JavaScript string and `eval()`'d for glyph rendering — close the function and execute arbitrary JS
- **Try this:** IPv6 address ambiguity: `[::1]` is loopback, but `[::1%25eth0]` can be parsed as `::1` + arbitrary suffix depending on library — bypass origin checks and SSRF filters
- **Try this:** Phone number validation libraries that fully comply with RFC 3966 allow `;extension=...` and `;phone-context=...` with arbitrary content
- **Try this:** HackerOne bounty transparency: good start but all-time stats don't reflect recent bounty table changes — reset on table update would be better

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in PDF.js XSS (CVE-2024-4367)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **PDF.js XSS (CVE-2024-4367): font glyph rendering JavaScript evals user-controlle**
2. **PDF.js vulnerability: font data embedded in PDF is concatenated into a JavaScrip**
3. **IPv6 address ambiguity: `[::1]` is loopback, but `[::1%25eth0]` can be parsed as**
