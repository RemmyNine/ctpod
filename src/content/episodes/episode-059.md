---
title: "Bug Bounty Gadget Hunting & Hacker's Intuition"
episode: 59
---


# Episode 59 Bug Bounty Gadget Hunting & Hacker's Intuition

**Guests:** Justin Gardner, Joel Margolis
**Format:** Show notes with timestamps (feed)
**Content:** Catalog of 17+ gadgets — HTML injection, CSS injection, clickjacking, image injection, open redirects, client-side path traversal, client-side open redirect, leaking window.location.href, cookie refresh gadget, stored XSS, CRLF injection, GraphQL/IDOR, auth gadgets, web cache deception, localStorage poisoning, cookie injection, context breaks

### TL;DR
- A "gadget" is a behavior or primitive that isn't itself a vulnerability but can be chained into one — they also serve as motivation milestones
- HTML injection → multiple escalation paths: DOM clobbering, CSS exfiltration, dangling markup, clickjacking, onerror-on-input, email injection
- Open redirects are "one of the lamest bug classes by itself" but essential for chaining into OAuth token leaks, SSRF bypasses, and client-side path traversal
- Client-side path traversal + open redirect + fetch auto-follow = XSS even against hardened CSP
- CRLF injection as a context break can turn parameter injection into full header/body injection

### Key Takeaways
- DOM clobbering via HTML injection can go 5+ layers deep using nested iframes with `srcdoc` attributes, enabling `a.b.c.d.e` property access
- Image injection (stored) can be weaponized by pointing `src` to the logout endpoint → log victim out on load → CSRF login loop for ATO
- `input type=image` element can trigger `onerror` — useful when `<img>` is stripped by WAF but `<input>` is allowed
- `history.pushState` can hide XSS payloads by rewriting the URL bar to a benign path
- OKHTTP strips `Authorization` header on redirect to different host (same host → different port/scheme = stripped) — critical mobile gadget
- Cookie bridges (cross-subdomain session sharing mechanisms) are fertile ground for self-XSS escalation — combine with cookie bombing to fail the consume step and steal tokens from the URL

### Bugs and Findings

#### Yelp Cookie Bridge ATO (by researcher Lil Endian)
- **Target/context:** Yelp's cookie bridge — cross-domain session sharing via store/retrieve endpoints
- **Root cause:** Self-XSS via email field during signup; cookie bridge stores/retrieves cookies across yelp.* TLDs via one-time tokens
- **Exploitation steps:**
  1. Create account with XSS payload in email prefix → self-XSS pops on login
  2. Cookie bridge from yelp.com → yelp.dk: store cookies, get one-time token
  3. Victim clicks link → auto-logs into attacker's XSS account on yelp.dk
  4. On tab A (yelp.com), victim is still logged into their own account
  5. From tab B (attacker XSS context on yelp.dk), cookie-bomb the retrieve endpoint
  6. Navigate tab A to store new token → cookie-bomb fails consumption → token remains in URL
  7. Exfiltrate token → consume it to get victim's full session cookies → ATO
- **Impact:** Full account takeover across Yelp's entire domain set

### Techniques and Primitives
- **Dangling Markup + JSON Blob Leak:** Inject unclosed tag into page state JSON → closes script tag → remainder of JSON leaked into HTML body as text
- **401 Injection via Image `src`:** `src="http://attacker.com/401"` → browser shows auth popup under target domain (aged technique, still works in some mobile browsers)
- **Client-side Open Redirect via postMessage + iframe redirect:** Redirect a trusted iframe via postMessage to bypass CSP connect-src restrictions
- **Cookie Bombing:** Set hundreds/thousands of cookies on a specific path to exceed header size limits → parsing failure at proxy/WAF layer

### Suggestions and Advices
- Take note of gadgets even when they don't immediately yield a bug — they fuel motivation and become chain components later
- Know the difference between client-side open redirect (`.href = user_input`) and server-side open redirect (302) — they have very different exploitation profiles
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
A "gadget" is a behavior or primitive that isn't itself a vulnerability but can be chained into one — they also serve as motivation milestones

#### 2. What you should learn
- Understand **dom clobbering via html injection can go 5+ layers deep using nested iframes with `srcdoc` attributes, enabling `a.b.c.d.e` property access**
- Understand **image injection (stored) can be weaponized by pointing `src` to the logout endpoint → log victim out on load → csrf login loop for ato**
- Understand **`input type=image` element can trigger `onerror` — useful when `<img>` is stripped by waf but `<input>` is allowed**
- Understand **`history.pushstate` can hide xss payloads by rewriting the url bar to a benign path**
- Understand **okhttp strips `authorization` header on redirect to different host (same host → different port/scheme = stripped) — critical mobile gadget**

#### 3. Core concepts explained
**Yelp Cookie Bridge ATO (by researcher Lil Endian)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Dangling Markup + JSON Blob Leak: Inject unclosed tag into page state JSON → closes script tag → remainder of JSON leaked into HTML body as text**
- A technique discussed in this episode for security research and bug bounty hunting.

**401 Injection via Image `src`: `src="http://attacker.com/401"` → browser shows auth popup under target domain (aged technique, still works in some mobile browsers)**
- A technique discussed in this episode for security research and bug bounty hunting.

****Client**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**Dangling Markup + JSON Blob Leak: Inject unclosed tag into page state JSON → closes script tag → remainder of JSON leaked into HTML body as text**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**401 Injection via Image `src`: `src="http://attacker.com/401"` → browser shows auth popup under target domain (aged technique, still works in some mobile browsers)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Client-side Open Redirect via postMessage + iframe redirect: Redirect a trusted iframe via postMessage to bypass CSP connect-src restrictions**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cookie Bombing: Set hundreds/thousands of cookies on a specific path to exceed header size limits → parsing failure at proxy/WAF layer**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Take note of gadgets even when they don't immediately yield a bug"* — **they fuel motivation and become chain components later**
- *"Know the difference between client-side open redirect (`.href = user_input`) and server-side open redirect (302)"* — **they have very different exploitation profiles**

#### 6. Mental models
- **Take note of gadgets even when they don't immediately yield ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Know the difference between client-side open redirect (`.hre** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** DOM clobbering via HTML injection can go 5+ layers deep using nested iframes with `srcdoc` attributes, enabling `a.b.c.d.e` property access
- **Try this:** Image injection (stored) can be weaponized by pointing `src` to the logout endpoint → log victim out on load → CSRF login loop for ATO
- **Try this:** `input type=image` element can trigger `onerror` — useful when `<img>` is stripped by WAF but `<input>` is allowed
- **Try this:** `history.pushState` can hide XSS payloads by rewriting the URL bar to a benign path

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Yelp Cookie Bridge ATO (by researcher Lil Endian)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **A "gadget" is a behavior or primitive that isn't itself a vulnerability but can **
2. **DOM clobbering via HTML injection can go 5+ layers deep using nested iframes wit**
3. **Image injection (stored) can be weaponized by pointing `src` to the logout endpo**
