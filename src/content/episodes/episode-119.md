---
title: "Abusing Iframes from a Client-Side Hacker"
episode: 119
---


# Episode 119 Abusing Iframes from a Client-Side Hacker

### TL;DR
- Iframe attributes deep dive: `src`, `srcdoc`, `csp`, `allow` (permission policy), `name`, `referrerpolicy`, `sandbox`, `credentialless`
- Window name hijacking: name survives cross-origin navigation; attacker can create iframe with known name, victim's window.open goes into attacker's iframe
- Open-faced iframe sandwich: attacker XSS on embedded iframe origin → navigates to victim's iframe (same origin between the two iframed pages) → access victim's DOM
- CSP frame-ancestors overrides X-Frame-Options (is more permissive)
- `window.frames.length` is cross-origin accessible — enables cross-site leaks

### Key Takeaways
- Clickjacking is impactful when properly demonstrated: find a single-click "approve"/"authorize" action, build a full POC with iframe cursor-following code
- `srcdoc` attribute: creates new DOM, scripts execute (unlike innerHTML), same-origin as parent. Use when innerHTML blocks script tags
- `csp` attribute on iframe: you control the CSP for an embedded cross-origin page — can block specific scripts to alter page behavior
- Window name (`name`): survives cross-origin navigation. Old-school cross-domain communication: set message in `name`, redirect to other domain, read `name`
- `credentialless` iframe: isolated cookie context — no cookies sent
- `window.frames.length` accessible cross-origin: count iframes to leak data (search results, auth state)

### Bugs and Findings
*No specific bug writeups — this is an iframe methodology episode.*

### Techniques and Primitives
- **Window name hijacking** — Create iframe with known `name`; victim's `window.open('url', 'that-name')` opens in attacker's iframe
- **Open-faced iframe sandwich** — Attacker XSS on embedded origin → attacker navigates through opener chain to victim's iframed page (same origin between framed pages)
- **Cursor-following clickjacking** — Move iframe to follow user's cursor; always centers over target button
- **`window.frames.length` cross-origin leak** — Count iframes; vary hash/parameter and observe count changes
- **CSP attribute for script blocking** — `<iframe src="victim" csp="script-src 'none'">` blocks victim's scripts
- **`srcdoc` script execution** — `<iframe srcdoc="<script>alert(1)</script>">` — script executes in new DOM context
- **Referrer policy on iframe** — `<iframe src="victim" referrerpolicy="unsafe-url">` — iframe's requests leak full URL; combine with postMessage navigation for OAuth code leak

### Tooling and Resources
- Cooper Young's "Exacerbating XSS: The Iframe Sandwich" writeup
- Episode 61: JR0ch17
- Gareth Hayes' SVG onload event quirk

### Suggestions and Advices from Hunter
- "Don't submit crappy clickjacking reports. Build out the full POC and you will very likely get paid."
- "The most overpowered clickjacking technique: write code that makes the iframe follow your cursor"
- "If you find a DOMXSS and script tags are blocked by innerHTML, try `<iframe srcdoc="...">`"
- "CSP frame-ancestors overrides X-Frame-Options — if there's a conflict, the more permissive wins"

### AI Takeaway
The iframe `csp` attribute allowing attackers to control CSP of a cross-origin embedded page is underexplored. Combined with `credentialless` (no cookies), this could selectively disable victim page scripts while keeping the page functional for exploitation.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Iframe attributes deep dive: `src`, `srcdoc`, `csp`, `allow` (permission policy), `name`, `referrerpolicy`, `sandbox`, `credentialless`

#### 2. What you should learn
- Understand **clickjacking is impactful when properly demonstrated: find a single-click "approve"/"authorize" action, build a full poc with iframe cursor-following code**
- Understand **`srcdoc` attribute: creates new dom, scripts execute (unlike innerhtml), same-origin as parent. use when innerhtml blocks script tags**
- Understand **`csp` attribute on iframe: you control the csp for an embedded cross-origin page — can block specific scripts to alter page behavior**
- Understand **window name (`name`): survives cross-origin navigation. old-school cross-domain communication: set message in `name`, redirect to other domain, read `name`**
- Understand **`credentialless` iframe: isolated cookie context — no cookies sent**

#### 3. Core concepts explained
**Window name hijacking**
- Create iframe with known `name`; victim's `window.open('url', 'that-name')` opens in attacker's iframe

**Open-faced iframe sandwich**
- Attacker XSS on embedded origin → attacker navigates through opener chain to victim's iframed page (same origin between framed pages)

**Cursor-following clickjacking**
- Move iframe to follow user's cursor; always centers over target button


#### 4. Techniques and tactics
**Window name hijacking**
- **What it is:** Create iframe with known `name`; victim's `window.open('url', 'that-name')` opens in attacker's iframe
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Open-faced iframe sandwich**
- **What it is:** Attacker XSS on embedded origin → attacker navigates through opener chain to victim's iframed page (same origin between framed pages)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cursor-following clickjacking**
- **What it is:** Move iframe to follow user's cursor; always centers over target button
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`window.frames.length` cross-origin leak**
- **What it is:** Count iframes; vary hash/parameter and observe count changes
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CSP attribute for script blocking**
- **What it is:** `<iframe src="victim" csp="script-src 'none'">` blocks victim's scripts
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Don't submit crappy clickjacking reports. Build out the full POC and you will very likely get paid."*
- *"The most overpowered clickjacking technique: write code that makes the iframe follow your cursor"*
- *"If you find a DOMXSS and script tags are blocked by innerHTML, try `<iframe srcdoc="...">`"*
- *"CSP frame-ancestors overrides X-Frame-Options"* — **if there's a conflict, the more permissive wins**

#### 6. Mental models
- **Don't submit crappy clickjacking reports. Build out the full** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The most overpowered clickjacking technique: write code that** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you find a DOMXSS and script tags are blocked by innerHTM** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Clickjacking is impactful when properly demonstrated: find a single-click "approve"/"authorize" action, build a full POC with iframe cursor-following code
- **Try this:** `srcdoc` attribute: creates new DOM, scripts execute (unlike innerHTML), same-origin as parent. Use when innerHTML blocks script tags
- **Try this:** `csp` attribute on iframe: you control the CSP for an embedded cross-origin page — can block specific scripts to alter page behavior
- **Try this:** Window name (`name`): survives cross-origin navigation. Old-school cross-domain communication: set message in `name`, redirect to other domain, read `name`

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Iframe attributes deep dive: `src`, `srcdoc`, `csp`, `allow` (permission policy)**
2. **Clickjacking is impactful when properly demonstrated: find a single-click "appro**
3. **`srcdoc` attribute: creates new DOM, scripts execute (unlike innerHTML), same-or**
