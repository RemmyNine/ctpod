---
title: "Bcrypt Hash Input Truncation & Mobile Device Threat Modeling"
episode: 97
---


# Episode 97 Bcrypt Hash Input Truncation & Mobile Device Threat Modeling

**Hosts:** Justin Gardner (Rhynorater), Joel Margolis (Teknogeek)
**Duration:** 53:05
**Transcript source:** feed (full transcript)

### TL;DR
- Okta bcrypt bug: usernames 52+ characters → bcrypt truncates the (username+password) concatenation → password is ignored
- Android Chrome intent URLs: forcing app launches without prompt (e.g., Samsung Browser) is a $3K+ vuln
- PortSwigger: concealing payloads in URL credentials (`https://user:pass@host/`) — `document.URL` reveals them but `location.href` doesn't
- Lightyear tool: PHP filter chain oracle exploit with small payloads (no URI too long problem), no warnings, fast
- Dom-Explorer by YesWeHack: browser-based HTML parser pipeline for testing mutation XSS

### Key Takeaways
- Bcrypt truncates at 72 characters (or 52 in some implementations). If username + password concatenation exceeds this, the password is ignored
- PortSwigger: `document.URL` contains URL credentials (`user:pass@host`), `window.location.href` does not — difference can be exploited
- `javascript:name` is a full XSS payload — `name` is the window.name, persists across refreshes
- Lightyear replaces PHP Filter Chain Oracle: dumps files of tens of thousands of bytes with payloads of a few thousand characters
- Dom-Explorer: visual pipeline for chaining HTML parsers (DOMParser, parse5, DOMPurify) to find mutation XSS

### Bugs and Findings

#### Okta bcrypt Authentication Bypass
- **Target/context:** Okta identity platform (without MFA sign-on policies)
- **Root cause:** bcrypt truncates input beyond 72 bytes (52 chars per Okta disclosure). Okta concatenated username + password before hashing. Username ≥ 52 chars → password portion fully truncated → any password (or none) authenticates
- **Key technical details:** bcrypt truncates after 72 bytes. If username is 52+ characters, the concatenated (username+password) reaches the truncation limit inside the username, and password is completely ignored.
- **Impact / severity / bounty:** Complete authentication bypass — logging in with just the username, no password needed
- **Obstacles & how solved:** Requires username ≥52 chars. Discovered internally by Okta (July 23 introduced, Oct 30 discovered). Switched from bcrypt to PBKDF2.

#### PortSwigger — Concealing Payloads in URL Credentials
- **Target/context:** Chrome and Firefox (not Safari — Safari discards URL credentials)
- **Root cause:** `document.URL` returns the full URL including `user:pass@` credentials. `window.location.href` does not (parsed by Location object). If a URL with credentials is embedded in an `<a>` tag with an `id`, the credentials are accessible via `[id].username` / `[id].password` via DOM clobbering
- **Key technical details:** `https://username:password@host/path` — `document.URL` includes user:pass, `location.href` does not. If embedded in `<a id="x" href="...">`, then `x.username` returns the username portion. Works in Chrome + Firefox, not Safari.
- **Impact / severity / bounty:** New way to smuggle data past WAFs into client-side contexts

#### Lightyear — PHP Filter Chain Tool
- **Target/context:** PHP applications with file read primitives via PHP filter chains
- **Root cause:** Previous PHP Filter Chain Oracle had severe limitations: GET parameter based → URI too long after ~135 chars extracted; produced PHP warnings
- **Technique:** Lightyear fixes both: can dump files of tens of thousands of bytes with payloads of a few thousand characters; faster; no errors/warnings
- **Key technical details:** Uses PHP filter chain technique but optimized to avoid size limits and PHP warnings. Payload size: ~2K chars → output: 10K+ bytes

#### NdevTK — Android/Chrome Web Attack Surface
- **Target/context:** Android Chrome, Chromium WebView, Samsung Browser
- **Root cause collection:** Various Chrome-specific behaviors on Android — intent URL parsing, cross-browser launch without prompt, iframe escapes, Google Assistant deep link invocation
- **Key technical details:** Intent URLs, registered schemes, cross-app navigation without user prompt. Samsung Browser runs on older Chromium base → launching from Chrome without prompt enables easier exploitation. Google Assistant "google://" deep links can invoke routines.
- **Obstacles & how solved:** Some issues remain unfixed ("asked and not fixed") — Google Assistant deep link control was not patched

### Techniques and Primitives
- **javascript:name XSS** — Set `window.name` to arbitrary payload (e.g., `<svg onload=alert(1)>`), then navigate to `javascript:name`. The name string becomes the document DOM, rendering the SVG. WAF cannot see the payload.
- **URL credential smuggling** — Use `https://user:pass@host/` to smuggle data that appears in `document.URL` but not `location.href` or the URL bar.
- **PHP filter chains with Lightyear** — Dump files without URI-too-long errors or PHP warnings.

### Tooling and Resources
- Lightyear PHP filter chain tool
- Dom-Explorer (YesWeHack / BitK)
- MultiHTMLParse (Matias Carlsen)
- NdevTK's Android Chrome attack surface writeups
- PortSwigger: "Concealing Payloads in URL Credentials" (Gareth Hayes)
- curl-cffi — Python library to impersonate Chrome TLS fingerprint

### Suggestions and Advices from Hunter
- "If you're looking at auth flows and see bcrypt, immediately think: truncation. How might I trigger it?" — Rhynorater
- "Know when you should really learn something and when you should have it ready to be learned." — Joel Margolis
- "Safari is the new security champ" (regarding discarding URL credentials that Chrome/Firefox expose) — Rhynorater

### AI Takeaway
The `javascript:name` XSS payload is extraordinarily powerful because it requires no function calls, no parentheses, no backticks — making it nearly impossible for WAFs to block. Combined with URL credential smuggling, attackers have multiple WAF-bypassing delivery mechanisms.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Okta bcrypt bug: usernames 52+ characters → bcrypt truncates the (username+password) concatenation → password is ignored

#### 2. What you should learn
- Understand **bcrypt truncates at 72 characters (or 52 in some implementations). if username + password concatenation exceeds this, the password is ignored**
- Understand **portswigger: `document.url` contains url credentials (`user:pass@host`), `window.location.href` does not — difference can be exploited**
- Understand **`javascript:name` is a full xss payload — `name` is the window.name, persists across refreshes**
- Understand **lightyear replaces php filter chain oracle: dumps files of tens of thousands of bytes with payloads of a few thousand characters**
- Understand **dom-explorer: visual pipeline for chaining html parsers (domparser, parse5, dompurify) to find mutation xss**

#### 3. Core concepts explained
**Okta bcrypt Authentication Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**PortSwigger — Concealing Payloads in URL Credentials**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Lightyear — PHP Filter Chain Tool**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**javascript:name XSS**
- Set `window.name` to arbitrary payload (e.g., `<svg onload=alert(1)>`), then navigate to `javascript:name`. The name string becomes the document DOM, rendering the SVG. WAF cannot see the payload.

**URL credential smuggling**
- Use `https://user:pass@host/` to smuggle data that appears in `document.URL` but not `location.href` or the URL bar.

**PHP filter chains with Lightyear**
- Dump files without URI-too-long errors or PHP warnings.


#### 4. Techniques and tactics
**javascript:name XSS**
- **What it is:** Set `window.name` to arbitrary payload (e.g., `<svg onload=alert(1)>`), then navigate to `javascript:name`. The name string becomes the document DOM, rendering the SVG. WAF cannot see the payload.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**URL credential smuggling**
- **What it is:** Use `https://user:pass@host/` to smuggle data that appears in `document.URL` but not `location.href` or the URL bar.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**PHP filter chains with Lightyear**
- **What it is:** Dump files without URI-too-long errors or PHP warnings.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you're looking at auth flows and see bcrypt, immediately think: truncation. How might I trigger it?"* — **Rhynorater**
- *"Know when you should really learn something and when you should have it ready to be learned."* — **Joel Margolis**
- *"Safari is the new security champ" (regarding discarding URL credentials that Chrome/Firefox expose)"* — **Rhynorater**

#### 6. Mental models
- **If you're looking at auth flows and see bcrypt, immediately ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Know when you should really learn something and when you sho** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Safari is the new security champ" (regarding discarding URL ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Bcrypt truncates at 72 characters (or 52 in some implementations). If username + password concatenation exceeds this, the password is ignored
- **Try this:** PortSwigger: `document.URL` contains URL credentials (`user:pass@host`), `window.location.href` does not — difference can be exploited
- **Try this:** `javascript:name` is a full XSS payload — `name` is the window.name, persists across refreshes
- **Try this:** Lightyear replaces PHP Filter Chain Oracle: dumps files of tens of thousands of bytes with payloads of a few thousand characters

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Requires username ≥52 chars. Discovered internally by Okta (July 23 introduced, Oct 30 discovered). Switched from bcrypt to PBKDF2.

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Okta bcrypt Authentication Bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Okta bcrypt bug: usernames 52+ characters → bcrypt truncates the (username+passw**
2. **Bcrypt truncates at 72 characters (or 52 in some implementations). If username +**
3. **PortSwigger: `document.URL` contains URL credentials (`user:pass@host`), `window**
