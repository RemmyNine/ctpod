---
title: "Youssef Sammouda — Client-Side & ATO War Stories"
episode: 58
---


# Episode 58 Youssef Sammouda — Client-Side & ATO War Stories

**Guest:** Youssef Sammouda
**Format:** Show notes with timestamps (feed)
**Content:** Client-side race conditions with postMessage, hash change events and scroll-to-text-fragments, finding/reporting complex bugs, postMessage methodology, ATO vulnerabilities, MessagePort, window frame relationships, recon and JS monitoring, client-side routing, MITMProxy

### TL;DR
- Youssef is one of the most technically creative client-side hackers — postMessage race conditions, browser feature abuse, Math.random seed recovery
- Facebook client-side race condition: change the targetOrigin of a postMessage *while* an async HTTP request is in-flight, bypassing origin checks
- Scroll-to-text-fragment (SCTF) used as a cross-site search oracle — leak page content word-by-word via scroll detection in iframes
- Math.random vulnerability: Facebook Messenger chat plugin used Math.random to generate callback IDs; leak 4-5 values via iframe window.name to recover the seed and predict the next ID → DOM XSS
- MessagePort and MessageChannel: once a port is transferred, it bypasses origin checks — leak the port to hijack the trusted channel

### Key Takeaways
- postMessage race conditions work when there's a delay (HTTP request) between origin verification and message dispatch — change the window reference or targetOrigin mid-flight
- Sending massive postMessages (5MB each) can bog down the receiving page's event loop, creating exploitable race windows
- Scroll-to-text-fragment (Chrome-only): detect if a word exists on a cross-origin page by observing scroll events in an iframe parent — combined with encoding tricks (UTF-16) for character-by-character search
- Math.random seed recovery: leak 4-5 consecutive values → recover V8's xorshift128+ seed → predict future values → forge callback IDs or CSRF tokens
- MessagePort transferred via postMessage eliminates need for origin checks — but if an attacker can intercept the port, they inherit full trust
- Keep notes of client-side "gadgets" — pages that do `window.opener.location =` controllable values, DOM clobbering primitives, postMessage handlers that process arbitrary data

### Bugs and Findings

#### Facebook Client-Side Race Condition — OAuth Token Leak
- **Target/context:** apps.facebook.com — games iframe requesting OAuth token from parent
- **Root cause:** Origin validated at request time but not at response time; async HTTP request to server for OAuth token; client can race to change the targetOrigin via postMessage while request is in-flight
- **Exploitation steps:**
  1. Game page requests OAuth token for app X with origin Y
  2. Server validates origin Y — starts processing
  3. While waiting for server response, attacker-controlled code changes origin to attacker.com via postMessage
  4. Server response returns OAuth token → sent to attacker.com
- **Bypass:** Facebook added locking mechanism — bypassed by flooding postMessages of 5MB each to delay the lock acquisition

#### Facebook Messenger Chat Plugin — Math.random → DOM XSS
- **Target/context:** Facebook Messenger Chat Plugin on facebook.com/goals (mobile)
- **Root cause:** Callback IDs for postMessage communication generated with Math.random(); iframe window.name also seeded with Math.random()
- **Exploitation steps:**
  1. facebook.com/goals had X-Frame-Options: allow-from <domain> (deprecated, ignored by mobile/Chrome) → page is iframeable
  2. Iframe the page on attacker.com → access inner iframe's window.name (which contains a Math.random value)
  3. Trigger plugin refresh (function accessible without callback ID) → new window.name generated each refresh
  4. Leak 4-5 Math.random values from window.name
  5. Recover xorshift128+ seed
  6. Predict next Math.random value = callback ID
  7. Send postMessage with predicted ID to trigger DOM XSS
- **Impact:** Full XSS on facebook.com

#### Scroll-to-Text-Fragment Cross-Site Search Oracle
- **Target/context:** Any Chrome-browsed page
- **Technique:**
  1. Find a page on target domain that sets `window.opener.location` to a user-controllable URL (hash injection)
  2. Open that page as a popup from attacker.com → attacker controls the hash
  3. On hash change, Chrome searches for text matching SCTF syntax (`#:~:text=prefix,suffix`)
  4. If text found, page scrolls — both in iframe AND unexpectedly in parent window
  5. Detect scroll → confirm word exists
  6. Character-by-character brute-force using encoding tricks (UTF-16 BOM) to handle spacing
- **Impact:** Read cross-origin page content word-by-word without XSS

### Tooling and Resources
- PostMessage tracker browser extension
- `ysamm.com` — Youssef's blog
- Every Known Way to Get References to Windows in JavaScript (bluepnume)
- MITMProxy with Python plugins for live scraping/secrets extraction

### Suggestions and Advices
- **Youssef:** "When a new feature comes out, go to the standard page, read it, and the discussion page... Sometimes they'll have accepted risk, and you can use it for another attack."
- Keep a notebook of gadgets: "this page returns client side code that would change window.opener" — even if not immediately exploitable
- Youssef hasn't duped since 2018/2019 — because his chains are so specific and multifaceted

### AI Takeaway
Youssef's work exemplifies that client-side vulnerability research is moving from single-bug exploits to multi-gadget chains spanning browser features, cryptographic weaknesses, and application-specific logic. The Math.random seed recovery + window.name leak + postMessage callback forgery + DOM XSS chain is a modern classic.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Youssef is one of the most technically creative client-side hackers — postMessage race conditions, browser feature abuse, Math.random seed recovery

#### 2. What you should learn
- Understand **postmessage race conditions work when there's a delay (http request) between origin verification and message dispatch — change the window reference or targetorigin mid-flight**
- Understand **sending massive postmessages (5mb each) can bog down the receiving page's event loop, creating exploitable race windows**
- Understand **scroll-to-text-fragment (chrome-only): detect if a word exists on a cross-origin page by observing scroll events in an iframe parent — combined with encoding tricks (utf-16) for character-by-character search**
- Understand **math.random seed recovery: leak 4-5 consecutive values → recover v8's xorshift128+ seed → predict future values → forge callback ids or csrf tokens**
- Understand **messageport transferred via postmessage eliminates need for origin checks — but if an attacker can intercept the port, they inherit full trust**

#### 3. Core concepts explained
**Facebook Client-Side Race Condition — OAuth Token Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Facebook Messenger Chat Plugin — Math.random → DOM XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Scroll-to-Text-Fragment Cross-Site Search Oracle**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Youssef: "When a new feature comes out, go to the standard page, read it, and the discussion page... Sometimes they'll have accepted risk, and you can use it for another attack."*
- *"Keep a notebook of gadgets: "this page returns client side code that would change window.opener"* — **even if not immediately exploitable**
- *"Youssef hasn't duped since 2018/2019"* — **because his chains are so specific and multifaceted**

#### 6. Mental models
- **Youssef: "When a new feature comes out, go to the standard p** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Keep a notebook of gadgets: "this page returns client side c** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Youssef hasn't duped since 2018/2019 — because his chains ar** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** postMessage race conditions work when there's a delay (HTTP request) between origin verification and message dispatch — change the window reference or targetOrigin mid-flight
- **Try this:** Sending massive postMessages (5MB each) can bog down the receiving page's event loop, creating exploitable race windows
- **Try this:** Scroll-to-text-fragment (Chrome-only): detect if a word exists on a cross-origin page by observing scroll events in an iframe parent — combined with encoding tricks (UTF-16) for character-by-character search
- **Try this:** Math.random seed recovery: leak 4-5 consecutive values → recover V8's xorshift128+ seed → predict future values → forge callback IDs or CSRF tokens

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Facebook Client-Side Race Condition — OAuth Token Leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Youssef is one of the most technically creative client-side hackers — postMessag**
2. **postMessage race conditions work when there's a delay (HTTP request) between ori**
3. **Sending massive postMessages (5MB each) can bog down the receiving page's event **
