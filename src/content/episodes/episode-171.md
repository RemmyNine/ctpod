---
title: "Path-Scoped Cookie Hacks with Uppercase & Post-based Raw Protobuf XSS"
episode: 171
---


# Episode 171 Path-Scoped Cookie Hacks with Uppercase & Post-based Raw Protobuf XSS

### TL;DR
- Path-scoped cookies: switching a character to uppercase in the path bypasses the cookie's path-scoping (case-sensitive cookie path vs case-insensitive HTTP server)
- Protobuf XSS via form submission: raw binary Protobuf sent as `application/x-www-form-urlencoded` via top-level form navigation — content-type not validated
- Leaking age = leaking full date of birth: observe when the age number changes to determine exact birth month/day
- CSPTs apply beyond web — found in desktop apps via WebSocket → HTTP path traversal

### Key Takeaways
- [ ] Cookie path scoping is case-sensitive; HTTP paths often aren't — `/abc` (lowercase) cookie won't be sent on `/ABC` (uppercase) request, enabling cookie-less attack
- [ ] For raw Protobuf XSS via form: ensure payload is in pure ASCII range (0x01-0x7F) to avoid DOM string mutation; handle `0x0A` (LF) by padding with `0x0D` before it
- [ ] Leaking age → derive exact DOB by noting the date when the displayed age increments
- [ ] `window.open()` can be triggered from `keydown` event (not just click) — easier to get user gesture
- [ ] CSPT applies to desktop/mobile apps using HTTP — not just web apps

### Bugs and Findings

#### Raw Protobuf XSS via Form Submission
- **Target/context:** Application accepting binary Protobuf over HTTP form POST (`application/x-www-form-urlencoded`)
- **Root cause:** Server doesn't validate Content-Type; raw binary interpreted as form data; binary injected into DOM → XSS
- **Technique:** Send raw Protobuf as form POST body with `text/plain` (browser allows this for top-level form navigation); payload must survive DOM string mutation, browser newline normalization, and equals sign insertion
- **Key technical details:**
  - DOM mutation tolerates pure ASCII (0x01-0x7F) — keep payload there
  - Protobuf string field tag `0x0A` (field 1, wire type 2) contains `0x0A` = LF — buffer with `0x0D` before it so browser sees `CRLF` not bare `LF`
  - Form submission inserts `=` between key and value — pad a field with length `0x3D` (=) exactly where needed
  - Browser appends CRLF at end of form body — define final string field 2 bytes longer than provided data to absorb this
- **Impact / severity / bounty:** Stored/reflected XSS via binary Protobuf injection

#### Path-Scoped Cookie Bypass with Uppercase
- **Target/context:** App where a cookie must be absent for a vulnerability to trigger
- **Root cause:** Cookie `Path` attribute is case-sensitive; HTTP server treats paths case-insensitively
- **Technique:** Send request to `/ABC` instead of `/abc` — server processes same endpoint but browser doesn't send the cookie scoped to `/abc`
- **Key technical details:** Cookie `Path=/abc` — request to `/ABC` excludes the cookie; server normalizes path to lowercase or treats both as equivalent
- **Impact / severity / bounty:** Authentication/cookie-dependent vulnerability bypass

#### CSPT in Desktop App via WebSocket
- **Target/context:** Desktop application using WebSockets to communicate with HTTP backend
- **Technique:** Supply path traversal in WebSocket message → truncated path hits different HTTP endpoint
- **Impact / severity / bounty:** Remote HTTP request manipulation with user-supplied path

### Techniques and Primitives
- **Protobuf form submission XSS** — Binary Protobuf sent as `text/plain` form; handle `0x0A`, `0x3D`, and trailing CRLF via precise length manipulation
- **Case-sensitive cookie path bypass** — Switch one character to uppercase to drop a path-scoped cookie while keeping all others
- **Age → DOB derivation** — Track when displayed age increments to determine exact birth date
- **Keydown user gesture** — `window.open()` allowed from `keydown` event, not just `click`
- **Control-click + hidden UI** — Make button only clickable when Ctrl is held; combine with clickjacking for top-level navigation from iframe

### Tooling and Resources
- lyra.horse/blog/2025/12/svg-clickjacking/ — SVG-enhanced clickjacking research
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Path-scoped cookies: switching a character to uppercase in the path bypasses the cookie's path-scoping (case-sensitive cookie path vs case-insensitive HTTP server)

#### 2. What you should learn
- Understand **[ ] cookie path scoping is case-sensitive; http paths often aren't — `/abc` (lowercase) cookie won't be sent on `/abc` (uppercase) request, enabling cookie-less attack**
- Understand **[ ] for raw protobuf xss via form: ensure payload is in pure ascii range (0x01-0x7f) to avoid dom string mutation; handle `0x0a` (lf) by padding with `0x0d` before it**
- Understand **[ ] leaking age → derive exact dob by noting the date when the displayed age increments**
- Understand **[ ] `window.open()` can be triggered from `keydown` event (not just click) — easier to get user gesture**
- Understand **[ ] cspt applies to desktop/mobile apps using http — not just web apps**

#### 3. Core concepts explained
**Raw Protobuf XSS via Form Submission**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Path-Scoped Cookie Bypass with Uppercase**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CSPT in Desktop App via WebSocket**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Protobuf form submission XSS**
- Binary Protobuf sent as `text/plain` form; handle `0x0A`, `0x3D`, and trailing CRLF via precise length manipulation

**Case-sensitive cookie path bypass**
- Switch one character to uppercase to drop a path-scoped cookie while keeping all others

**Age → DOB derivation**
- Track when displayed age increments to determine exact birth date


#### 4. Techniques and tactics
**Protobuf form submission XSS**
- **What it is:** Binary Protobuf sent as `text/plain` form; handle `0x0A`, `0x3D`, and trailing CRLF via precise length manipulation
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Case-sensitive cookie path bypass**
- **What it is:** Switch one character to uppercase to drop a path-scoped cookie while keeping all others
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Age → DOB derivation**
- **What it is:** Track when displayed age increments to determine exact birth date
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Keydown user gesture**
- **What it is:** `window.open()` allowed from `keydown` event, not just `click`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Control-click + hidden UI**
- **What it is:** Make button only clickable when Ctrl is held; combine with clickjacking for top-level navigation from iframe
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
- **Try this:** [ ] Cookie path scoping is case-sensitive; HTTP paths often aren't — `/abc` (lowercase) cookie won't be sent on `/ABC` (uppercase) request, enabling cookie-less attack
- **Try this:** [ ] For raw Protobuf XSS via form: ensure payload is in pure ASCII range (0x01-0x7F) to avoid DOM string mutation; handle `0x0A` (LF) by padding with `0x0D` before it
- **Try this:** [ ] Leaking age → derive exact DOB by noting the date when the displayed age increments
- **Try this:** [ ] `window.open()` can be triggered from `keydown` event (not just click) — easier to get user gesture

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Raw Protobuf XSS via Form Submission?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Path-scoped cookies: switching a character to uppercase in the path bypasses the**
2. **[ ] Cookie path scoping is case-sensitive; HTTP paths often aren't — `/abc` (low**
3. **[ ] For raw Protobuf XSS via form: ensure payload is in pure ASCII range (0x01-0**
