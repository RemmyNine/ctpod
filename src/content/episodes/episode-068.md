---
title: "0-days & HTMX-SS with Matthias (Matthias)"
episode: 68
---


# Episode 68 0-days & HTMX-SS with Matthias (Matthias)

**Guest:** Matthias (security researcher)
**Format:** Full transcript (ASR)
**Topics:** HTMX security research — 4 zero-days/findings, DomPurify + HTMX data-attribute bypass, CSP bypass via HTMX eval requirements, client-side response header injection to XSS, HX-Disabled bypass

### TL;DR
- HTMX requires `unsafe-eval` in CSP for triggers — this alone is a global CSP bypass gadget
- Client-side response header injection + HTMX `HX-Redirect` header = XSS (fetch response header triggers `window.location.href` without validation)
- HTMX `hx-disabled` attribute is meant to disable HTMX in subtrees but doesn't cover the newer trigger syntax (`hx-on:event` → colon syntax)
- DomPurify allows `data-*` attributes by default — HTMX attributes can be prefixed with `data-` → DomPurify doesn't strip them → XSS bypass
- HTMX trigger evaluation uses `eval()` on user-controlled strings inside template functions — break out of the wrapper with `);alert(1);//`

### Key Takeaways
- HTMX's `allowEval` config flag (default: true) must be set to `false` to prevent eval-based trigger execution — most users won't change this
- `HX-Redirect` response header: if you can inject response headers from a path HTMX fetches, you get `window.location.href` redirect with no origin check
- `data-hx-on:*` attributes bypass DomPurify's allowlist since `data-*` is universally allowed
- `hx-disable` is incomplete — new trigger syntax (`hx-on:click`) bypasses the disable check entirely
- HTMX is essentially "HTML over the wire" — server returns HTML fragments, HTMX swaps them into DOM; this design creates unique trust boundaries

### Bugs and Findings

#### HTMX Global CSP Bypass
- **Root cause:** HTMX triggers require `unsafe-eval` in `script-src` by default — if a site uses HTMX triggers, any HTML injection can use `hx-on:load="alert(1)"` to execute JS even if CSP explicitly blocks inline scripts
- **Mitigation:** Set `htmx.config.allowEval = false` — but this is not the default

#### HTMX + DomPurify Bypass via data- Attributes
- **Root cause:** DomPurify allows all `data-*` attributes by default; HTMX supports `data-hx-*` prefix for all its attributes
- **Exploitation:** HTML injection with `<div data-hx-on:load="alert(1)">` — DomPurify passes it, HTMX executes it
- **Exploitation steps (CTF challenge by Matthias):**
  1. Share-link path reflects user input → client-side path traversal to attacker server
  2. Server returns HTML with HTMX content + CSP bypass (unsafe-eval present)
  3. HTMX target was `hx-disable` container → bypass using `HX-Retarget` response header
  4. Response goes through HTMX extension that runs DomPurify → bypass DomPurify via `data-hx-on:*` attributes
  5. Final: `data-hx-on:load="alert(1)"` → XSS

#### HTMX HX-Redirect to XSS
- **Root cause:** `HX-Redirect` response header triggers `window.location.href = headerValue` without validation
- **Exploitation:** If HTMX fetches a path where you can inject response headers (HTTP response splitting, faulty reverse proxy), inject `HX-Redirect: javascript:alert(1)` → RCE

### Tooling and Resources
- `htmx.org` — HTMX documentation
- DomainCrawler — Cloudflare CDN-CGI enumeration via HTTP Archive

### Suggestions and Advices
- **Matthias:** Building CTF challenges around HTMX forced deep learning — "if you really want to understand something, build a CTF challenge with it"
- CTFs vs bug bounty: CTFs guarantee a bug exists, bug bounty requires intuition about whether a bug exists — different skill sets
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
HTMX requires `unsafe-eval` in CSP for triggers — this alone is a global CSP bypass gadget

#### 2. What you should learn
- Understand **htmx's `alloweval` config flag (default: true) must be set to `false` to prevent eval-based trigger execution — most users won't change this**
- Understand **`hx-redirect` response header: if you can inject response headers from a path htmx fetches, you get `window.location.href` redirect with no origin check**
- Understand **`data-hx-on:*` attributes bypass dompurify's allowlist since `data-*` is universally allowed**
- Understand **`hx-disable` is incomplete — new trigger syntax (`hx-on:click`) bypasses the disable check entirely**
- Understand **htmx is essentially "html over the wire" — server returns html fragments, htmx swaps them into dom; this design creates unique trust boundaries**

#### 3. Core concepts explained
**HTMX Global CSP Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**HTMX + DomPurify Bypass via data- Attributes**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**HTMX HX-Redirect to XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Matthias: Building CTF challenges around HTMX forced deep learning"* — **"if you really want to understand something, build a CTF challenge with it**
- *"CTFs vs bug bounty: CTFs guarantee a bug exists, bug bounty requires intuition about whether a bug exists"* — **different skill sets**

#### 6. Mental models
- **Matthias: Building CTF challenges around HTMX forced deep le** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **CTFs vs bug bounty: CTFs guarantee a bug exists, bug bounty ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** HTMX's `allowEval` config flag (default: true) must be set to `false` to prevent eval-based trigger execution — most users won't change this
- **Try this:** `HX-Redirect` response header: if you can inject response headers from a path HTMX fetches, you get `window.location.href` redirect with no origin check
- **Try this:** `data-hx-on:*` attributes bypass DomPurify's allowlist since `data-*` is universally allowed
- **Try this:** `hx-disable` is incomplete — new trigger syntax (`hx-on:click`) bypasses the disable check entirely

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in HTMX Global CSP Bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **HTMX requires `unsafe-eval` in CSP for triggers — this alone is a global CSP byp**
2. **HTMX's `allowEval` config flag (default: true) must be set to `false` to prevent**
3. **`HX-Redirect` response header: if you can inject response headers from a path HT**
