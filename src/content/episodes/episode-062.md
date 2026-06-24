---
title: "Frontend Language Oddities"
episode: 62
---


# Episode 62 Frontend Language Oddities

**Guests:** Justin Gardner, Joel Margolis
**Format:** Show notes with timestamps (feed)
**Topics:** Cool HTML shit, bug bounty journeys, Yelp cookie bridge bug, additional research resources, CSS exfiltration

### TL;DR
- `form` attribute on `<input>` allows elements outside `<form>` to be included in submission — useful for smuggling data via HTML injection
- `<input type="image">` triggers `onerror` — surprising WAF/XSS filter bypass
- Yelp cookie bridge ATO via self-XSS + cookie bombing (detailed in Ep 59)
- `history.pushState` hides XSS payload by updating URL bar
- CSS exfiltration research from PortSwigger — new framework for attribute-value exfiltration via CSS selectors

### Key Takeaways
- `input type=image` acts as a submit button AND triggers `onerror` if `src` fails to load — bypass WAFs that block `<img>` but allow `<input>`
- `form` attribute on inputs lets any element outside `<form>` participate in submission — useful for CSRF gadget chains
- Attack path modeling + visual POCs can increase bounty payout by 50%+ — demonstrate wormability, user impact, full exploitation chain
- Browser market share nuance: Safari has 18.5% overall but only 8% desktop — 24% mobile; useful for same-site lax exploitability arguments

### Techniques and Primitives
- **Named iframe window hijack:** If app uses `window.open(..., "targetFrame")`, an attacker can create an iframe with that name on the same origin and control its content → frame hijacking for postMessage interception
- **GoogleChrome:// URL scheme as open redirect:** On mobile, if any URL scheme is allowed, `googlechrome://navigate?url=https://evil.com` can redirect Chrome — bypasses app URL validation that restricts http/https schemes

### Tooling and Resources
- `wakatte` — JavaScript decompiler (supports Webpack/Browserify) — live demo available
- PortSwigger CSS exfiltration research — `github.com/PortSwigger/css-exfiltration`
- Even Better by Bebiks — Kaido CSS/JS customization
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
`form` attribute on `<input>` allows elements outside `<form>` to be included in submission — useful for smuggling data via HTML injection

#### 2. What you should learn
- Understand **`input type=image` acts as a submit button and triggers `onerror` if `src` fails to load — bypass wafs that block `<img>` but allow `<input>`**
- Understand **`form` attribute on inputs lets any element outside `<form>` participate in submission — useful for csrf gadget chains**
- Understand **attack path modeling + visual pocs can increase bounty payout by 50%+ — demonstrate wormability, user impact, full exploitation chain**
- Understand **browser market share nuance: safari has 18.5% overall but only 8% desktop — 24% mobile; useful for same-site lax exploitability arguments**

#### 3. Core concepts explained
**Named iframe window hijack: If app uses `window.open(..., "targetFrame")`, an attacker can create an iframe with that name on the same origin and control its content → frame hijacking for postMessage interception**
- A technique discussed in this episode for security research and bug bounty hunting.

**GoogleChrome:// URL scheme as open redirect: On mobile, if any URL scheme is allowed, `googlechrome://navigate?url=https://evil.com` can redirect Chrome**
- bypasses app URL validation that restricts http/https schemes


#### 4. Techniques and tactics
**Named iframe window hijack: If app uses `window.open(..., "targetFrame")`, an attacker can create an iframe with that name on the same origin and control its content → frame hijacking for postMessage interception**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**GoogleChrome:// URL scheme as open redirect: On mobile, if any URL scheme is allowed, `googlechrome://navigate?url=https://evil.com` can redirect Chrome**
- **What it is:** bypasses app URL validation that restricts http/https schemes
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
- **Try this:** `input type=image` acts as a submit button AND triggers `onerror` if `src` fails to load — bypass WAFs that block `<img>` but allow `<input>`
- **Try this:** `form` attribute on inputs lets any element outside `<form>` participate in submission — useful for CSRF gadget chains
- **Try this:** Attack path modeling + visual POCs can increase bounty payout by 50%+ — demonstrate wormability, user impact, full exploitation chain
- **Try this:** Browser market share nuance: Safari has 18.5% overall but only 8% desktop — 24% mobile; useful for same-site lax exploitability arguments

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **`form` attribute on `<input>` allows elements outside `<form>` to be included in**
2. **`input type=image` acts as a submit button AND triggers `onerror` if `src` fails**
3. **`form` attribute on inputs lets any element outside `<form>` participate in subm**
