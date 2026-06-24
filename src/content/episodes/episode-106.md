---
title: "Announcing Our New Co-Host Rez0"
episode: 106
---


# Episode 106 Announcing Our New Co-Host Rez0

**Host:** Justin Gardner (Rhynorater)
**New Co-Host:** Joseph Thacker (Rez0)
**Duration:** 58:10
**Transcript source:** feed (full transcript)

### TL;DR
- Joseph Thacker (Rez0) joins as co-host — going full-time bug bounty
- DoubleClickJacking: two-click account takeover via popup + mousedown timing
- Gareth Hayes charset escape XSS: ISO 2022 JP escape sequences inside JS URLs bypass WAFs
- SVG XSS with XML entities: pre-define entities in SVG to execute XSS even with script tag stripping
- XPOW validation benchmarks for AI hacking agents (100+ Docker-based benchmarks)
- curl-cffi: Python library to impersonate Chrome TLS fingerprint

### Key Takeaways
- DoubleClickJacking bypasses X-Frame-Options, SameSite, and CSP — uses popups, not frames
- Gareth Hayes: ISO 2022 JP charset escape sequences in JS URLs → `jav%1B(B%20ascript:` pops XSS
- SVG XSS with XML entities: define `<!ENTITY x SYSTEM "file:">` type entities to obfuscate payload
- XPOW validation benchmarks: 100+ Docker compose labs for testing AI hacking agents
- curl-cffi: `from curl_cffi import requests` → Chrome TLS impersonation in Python
- CSPT (Client-Side Path Traversal) + PDF upload: magic bytes `%PDF` anywhere in first 1024 bytes → PDF that's also valid JSON

### Bugs and Findings

#### DoubleClickJacking — Two-Click ATO
- **Target/context:** Salesforce, Slack, Shopify, OAuth authorization pages
- **Root cause:** Mousedown closes a popup/overlay; mouseup fires on the sensitive page revealed underneath. User thinks they're clicking one button but they're clicking two different pages in sequence.
- **Exploitation steps:**
  1. Attacker page opens a popup with sensitive action (e.g., OAuth authorize)
  2. Overlay covers it with a legitimate-looking element
  3. User clicks — mousedown closes overlay, mouseup fires on the popup's button
  4. One-click OAuth authorization performed
- **Key technical details:** Bypasses X-Frame-Options, SameSite cookies, CSP. Uses popup, not iframe. Mitigation: add JavaScript to sensitive buttons requiring mouse gesture before enabling the button.

#### ISO 2022 JP Charset XSS
- **Target/context:** Chrome, Firefox — pages with no charset defined
- **Root cause:** ISO 2022 JP escape sequences inside JavaScript URLs — `jav%1B(B%20ascript:` — the escape sequence `%1B(B` changes the charset mid-URL
- **Key technical details:** Gareth Hayes tweet + Jorian Walter discovery. Spam escape sequences repeatedly to force Chrome to sniff charset. Payload: `jav%1B(B%20ascript:alert(1)` and variations.
- **Impact / severity / bounty:** WAF bypass for javascript: XSS payloads

#### SVG XSS with XML Entities
- **Target/context:** SVG file upload contexts
- **Root cause:** Even if script tags are stripped from SVGs, XML entities can be used to define vectors that only become executable at runtime when the browser parses the XML
- **Key technical details:** SVG XSS works when browser navigates directly to SVG file (not loaded as `<img src="...">`). Using XML entities, the payload is obfuscated from upload filters.

### Techniques and Primitives
- **UTF-8→ISO 2022 JP escape in URLs** — Use `%1B(B` (shift to JIS X 0201 8-bit) inside `javascript:` URLs to hide payload from WAFs
- **curl-cffi** — Drop-in replacement for Python `requests` that impersonates Chrome TLS fingerprint
- **PDF/JSON polyglot for CSPT** — Upload a file starting with `%PDF` (magic bytes) as PDF, but contains JSON body → processed by CSPT after fetch

### Tools and Resources
- XPOW validation benchmarks (github.com/xbow-engineering/validation-benchmarks)
- curl-cffi (pypi.org/project/curl-cffi/)
- Doyensec CSPT + file upload research
- AI Crash Course (github.com/henrythe9th/AI-Crash-Course)
- Paulo Yibelo's DoubleClickJacking research

### Suggestions and Advices from Hunter
- "Clickjacking gets a bad rap, but if you prove the full chain (one-click ATO), it's the highest client-side impact." — Justin Gardner
- "If you have the mitigation in the report, teams are much more likely to accept the bug." — Joseph Thacker
- "Gareth Hayes tweets anything → pay attention." — Justin Gardner

### AI Takeaway
The DoubleClickJacking technique is a genuinely novel attack that bypasses all existing clickjacking defenses. The ISO 2022 JP charset escape for JS URLs is a powerful WAF bypass that's trivial to implement (just prepend `%1B(B` to payloads).
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Joseph Thacker (Rez0) joins as co-host — going full-time bug bounty

#### 2. What you should learn
- Understand **doubleclickjacking bypasses x-frame-options, samesite, and csp — uses popups, not frames**
- Understand **gareth hayes: iso 2022 jp charset escape sequences in js urls → `jav%1b(b%20ascript:` pops xss**
- Understand **svg xss with xml entities: define `<!entity x system "file:">` type entities to obfuscate payload**
- Understand **xpow validation benchmarks: 100+ docker compose labs for testing ai hacking agents**
- Understand **curl-cffi: `from curl_cffi import requests` → chrome tls impersonation in python**

#### 3. Core concepts explained
**DoubleClickJacking — Two-Click ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**ISO 2022 JP Charset XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**SVG XSS with XML Entities**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**UTF-8→ISO 2022 JP escape in URLs**
- Use `%1B(B` (shift to JIS X 0201 8-bit) inside `javascript:` URLs to hide payload from WAFs

**curl-cffi**
- Drop-in replacement for Python `requests` that impersonates Chrome TLS fingerprint

**PDF/JSON polyglot for CSPT**
- Upload a file starting with `%PDF` (magic bytes) as PDF, but contains JSON body → processed by CSPT after fetch


#### 4. Techniques and tactics
**UTF-8→ISO 2022 JP escape in URLs**
- **What it is:** Use `%1B(B` (shift to JIS X 0201 8-bit) inside `javascript:` URLs to hide payload from WAFs
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**curl-cffi**
- **What it is:** Drop-in replacement for Python `requests` that impersonates Chrome TLS fingerprint
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**PDF/JSON polyglot for CSPT**
- **What it is:** Upload a file starting with `%PDF` (magic bytes) as PDF, but contains JSON body → processed by CSPT after fetch
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**XPOW validation benchmarks (github.com/xbow-engineering/validation-benchmarks)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**curl-cffi (pypi.org/project/curl-cffi/)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Clickjacking gets a bad rap, but if you prove the full chain (one-click ATO), it's the highest client-side impact."* — **Justin Gardner**
- *"If you have the mitigation in the report, teams are much more likely to accept the bug."* — **Joseph Thacker**
- *"Gareth Hayes tweets anything → pay attention."* — **Justin Gardner**

#### 6. Mental models
- **Clickjacking gets a bad rap, but if you prove the full chain** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you have the mitigation in the report, teams are much mor** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Gareth Hayes tweets anything → pay attention." — Justin Gard** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** DoubleClickJacking bypasses X-Frame-Options, SameSite, and CSP — uses popups, not frames
- **Try this:** Gareth Hayes: ISO 2022 JP charset escape sequences in JS URLs → `jav%1B(B%20ascript:` pops XSS
- **Try this:** SVG XSS with XML entities: define `<!ENTITY x SYSTEM "file:">` type entities to obfuscate payload
- **Try this:** XPOW validation benchmarks: 100+ Docker compose labs for testing AI hacking agents

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in DoubleClickJacking — Two-Click ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Joseph Thacker (Rez0) joins as co-host — going full-time bug bounty**
2. **DoubleClickJacking bypasses X-Frame-Options, SameSite, and CSP — uses popups, no**
3. **Gareth Hayes: ISO 2022 JP charset escape sequences in JS URLs → `jav%1B(B%20ascr**
