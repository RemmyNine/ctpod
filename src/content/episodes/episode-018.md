---
title: "Audit Code, Earn Bounties"
episode: 18
---


# Episode 18 Audit Code, Earn Bounties

### TL;DR
- Home Assistant RCE: path traversal on reverse proxy bypasses auth → unauthenticated RCE
- Git config injection: parsing lines >1024 chars creates misaligned sections → arbitrary config injection
- Jubobs' "Smorgasbord of a Bug Chain": postMessage + misconfigured JSONP + DOM XSS + CORS + CSRF chained together
- Cookie bugs deep-dive: underscore-prefixed cookies (`__Host-`, `__Secure-`), cookie ordering, empty cookie smuggling
- VSCode for source code review: extensions, command palette, Todo Highlight for flow analysis
- Getting source code: demos/free trials, buying, Docker Hub, LFI/LFD, GitHub search for error strings

### Key takeaways
- Home Assistant auth bypass via `path traversal + auth bypass on reverse proxy: `/some_api/../api/` skipping auth
- Git config injection: lines >1024 bytes get split mid-line; this can inject arbitrary sections
- For SSRF→SSTI: if the SSRF output appears in rendered HTML, test SSTI by serving payload in response
- Cookie names with `__Host-` and `__Secure-` prefixes enforce secure/domain attributes browser-side
- Empty cookie name can cause cookie smuggling — browser interprets adjacent cookies differently
- Always check `vendors.js` / `main.js` for leaked source maps → access to private modules

### Bugs and Findings

#### Home Assistant RCE — Path Traversal Auth Bypass
- **Target/context:** Home Assistant (open-source home automation platform)
- **Root cause:** Reverse proxy configuration allowed path traversal past auth: `/auth_endpoint/../api/unauthenticated_endpoint`
- **Technique / how found:** L. Tam researched Home Assistant's HTTP integration; tested path traversal on auth boundaries
- **Key technical details:** Path traversal `../` bypasses auth decorator; ~150 internal integrations enabled by default
- **Impact / severity / bounty:** RCE on Home Assistant instance
- **Obstacles & how solved:** [inferred] Needed to chain multiple path traversals to find unauthenticated endpoints

#### Git Config Injection — Arbitrary Command Execution
- **Target/context:** Git core (`.gitconfig` parsing)
- **Root cause:** Git reads lines 1024 bytes at a time; if a crafted line >1024 chars, the read splits mid-line, creating a synthetic second line that can define arbitrary config sections
- **Technique / how found:** Andre Z. / F-Hack analyzed Git's config parsing; found the 1024-byte read boundary creates a vulnerability when lines exceed that length
- **Key technical details:** `fgets()` reads 1024 bytes; crafted line of >1024 chars splits into section header + core directive on next read; `[core]` section can be overwritten if defined twice (second wins)
- **Impact / severity / bounty:** RCE via config file injection
- **Obstacles & how solved:** Needed to find a way to inject >1024-char line into `.gitconfig`

#### Jubobs' Chain: postMessage → XSS → CORS → CSRF → ATO
- **Target/context:** Undisclosed web application
- **Root cause:** Multiple interconnected vulnerabilities:
  1. postMessage handler without origin validation
  2. Misconfigured JSONP endpoint allowing cross-origin data read
  3. DOM-based XSS
  4. Lax CORS policy allowing credentialed cross-origin requests
  5. Weak CSRF validation
- **Technique / how found:** Jubobs enumerated postMessage listeners via Franz's extension; chained each weakness to escalate privileges
- **Key technical details:** `window.postMessage` no origin check; JSONP callback injection; CORS `Access-Control-Allow-Origin: *` with credentials
- **Impact / severity / bounty:** Full account takeover

### Techniques and Primitives
- **Path traversal auth bypass** — `../` from authenticated endpoint to unauthenticated API can skip auth middleware
- **Config file line-length injection** — >1024-byte lines get split mid-line; crafted content can inject new config sections
- **LFI→source code disclosure** — use LFD to pull source code and find deeper bugs (with permission)
- **Docker container source extraction** — pull image → `docker cp` or create Dockerfile with `FROM target` + `ENTRYPOINT /bin/bash`
- **npm/pip package auditing** — download packages from registry, audit source code for secrets and vulnerabilities
- **GitHub search for error strings** — error messages containing company-specific names often find source code repos

### Tooling and Resources
- Visual Studio Code + Todo Highlight extension
- dotPeek (JetBrains, .NET decompiler)
- Uncompyle6 (Python .pyc decompiler)
- JD-GUI / JADX
- IDA / Ghidra (for native binaries)
- Docker Hub / Docker CP
- GitHub search
- `vendors.js` / `main.js` from webpack bundles

### Suggestions and Advices from Hunter
- "If you have an LFD, ask for permission to read source code — it might bump your report to a crit" — Justin
- "Read the RFCs. The cookie spec has bugs documented by the maintainers themselves." — Joel on cookie research
- "Use Todo Highlight in VSCode to mark code flow analysis steps" — Joel
- "If you can pull Docker images cheaply, do it — source code access changes everything" — Justin
- "Check vendors.js for source maps — they often contain the full node_modules including private packages" — Justin

### AI Takeaway
The Git config injection technique (1024-byte line boundary) is both elegant and broadly applicable: any parser that reads fixed-sized chunks and processes text content is vulnerable to misalignment attacks. Combined with the "second definition wins" rule for `[core]` sections, an attacker can inject arbitrary Git config directives including `core.fsmonitor` or `core.hooksPath`.

# CTBB Episodes 019–036 — Structured Analyst Notes
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Home Assistant RCE: path traversal on reverse proxy bypasses auth → unauthenticated RCE

#### 2. What you should learn
- Understand **home assistant auth bypass via `path traversal + auth bypass on reverse proxy: `/some_api/../api/` skipping auth**
- Understand **git config injection: lines >1024 bytes get split mid-line; this can inject arbitrary sections**
- Understand **for ssrf→ssti: if the ssrf output appears in rendered html, test ssti by serving payload in response**
- Understand **cookie names with `__host-` and `__secure-` prefixes enforce secure/domain attributes browser-side**
- Understand **empty cookie name can cause cookie smuggling — browser interprets adjacent cookies differently**

#### 3. Core concepts explained
**Home Assistant RCE — Path Traversal Auth Bypass**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Git Config Injection — Arbitrary Command Execution**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Jubobs' Chain: postMessage → XSS → CORS → CSRF → ATO**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Path traversal auth bypass**
- `../` from authenticated endpoint to unauthenticated API can skip auth middleware

**Config file line-length injection**
- >1024-byte lines get split mid-line; crafted content can inject new config sections

**LFI→source code disclosure**
- use LFD to pull source code and find deeper bugs (with permission)


#### 4. Techniques and tactics
**Path traversal auth bypass**
- **What it is:** `../` from authenticated endpoint to unauthenticated API can skip auth middleware
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Config file line-length injection**
- **What it is:** >1024-byte lines get split mid-line; crafted content can inject new config sections
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**LFI→source code disclosure**
- **What it is:** use LFD to pull source code and find deeper bugs (with permission)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Docker container source extraction**
- **What it is:** pull image → `docker cp` or create Dockerfile with `FROM target` + `ENTRYPOINT /bin/bash`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**npm/pip package auditing**
- **What it is:** download packages from registry, audit source code for secrets and vulnerabilities
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have an LFD, ask for permission to read source code"* — **it might bump your report to a crit" — Justin**
- *"Read the RFCs. The cookie spec has bugs documented by the maintainers themselves."* — **Joel on cookie research**
- *"Use Todo Highlight in VSCode to mark code flow analysis steps"* — **Joel**
- *"If you can pull Docker images cheaply, do it"* — **source code access changes everything" — Justin**
- *"Check vendors.js for source maps"* — **they often contain the full node_modules including private packages" — Justin**

#### 6. Mental models
- **If you have an LFD, ask for permission to read source code —** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Read the RFCs. The cookie spec has bugs documented by the ma** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use Todo Highlight in VSCode to mark code flow analysis step** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Home Assistant auth bypass via `path traversal + auth bypass on reverse proxy: `/some_api/../api/` skipping auth
- **Try this:** Git config injection: lines >1024 bytes get split mid-line; this can inject arbitrary sections
- **Try this:** For SSRF→SSTI: if the SSRF output appears in rendered HTML, test SSTI by serving payload in response
- **Try this:** Cookie names with `__Host-` and `__Secure-` prefixes enforce secure/domain attributes browser-side

#### 8. Red flags and pitfalls
- - Obstacles & how solved: [inferred] Needed to chain multiple path traversals to find unauthenticated endpoints
- - Obstacles & how solved: Needed to find a way to inject >1024-char line into `.gitconfig`

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **CORS** — Cross-Origin Resource Sharing — browser mechanism for cross-domain requests
- **SSTI** — Server-Side Template Injection — injecting template syntax that executes on server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Home Assistant RCE — Path Traversal Auth Bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Home Assistant RCE: path traversal on reverse proxy bypasses auth → unauthentica**
2. **Home Assistant auth bypass via `path traversal + auth bypass on reverse proxy: `**
3. **Git config injection: lines >1024 bytes get split mid-line; this can inject arbi**
