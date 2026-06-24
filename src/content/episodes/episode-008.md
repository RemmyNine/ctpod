---
title: "PostMessage Bugs, CSS Injection, and Bug Drops"
episode: 8
---


# Episode 8 PostMessage Bugs, CSS Injection, and Bug Drops

### TL;DR
- PostMessage bugs: Franz Rosen's Chrome extension detects postMessage events; easy XSS via unvalidated postMessage
- CSS injection deep dive: CSS escapes, Unicode escaping, backslash encoding for blacklist bypass
- CSS injection → CSS keylogger: race condition to inject CSS, 160 fonts + 16 classes to exfiltrate credit card numbers character by character
- CSS `@import` chaining technique (Nathaniel Latimer/d0nut): recursive imports to accelerate data extraction
- CSS Painting API (Chrome): calling JavaScript from CSS via `registerPaint` — potential exploitation vector

### Key takeaways
- Franz Rosen's postMessage Tracker Chrome extension: logs all `window.postMessage` calls with data
- Use `window.opener` reference to reach back across same-origin windows for data exfiltration
- CSS escapes: `\` encoding, Unicode `\0031` for character bypass
- CSS injection data exfiltration: define fonts per unicode range, use `background-url` for callback
- Use zero-width font so user doesn't see typed character during exfiltration
- For CSS blacklists, try backslash/Unicode escapes on payload

### Bugs and Findings

#### CSS Injection → CSS Keylogger — Credit Card Data Exfiltration (Critical)
- **Target/context:** Payment processing service with embedded iframes per checkout field
- **Root cause:**
  1. Broadcast postMessage between iframes without origin validation
  2. Race condition: attacker sends postMessage faster than parent→child to inject CSS
  3. CSS blacklist could be bypassed via Unicode escapes
  4. CSP blocked script imports but media queries not fully filtered via regex
- **Technique / how found:** Noticed broadcast postMessage system; used Franz's extension to inspect messages
- **Exploitation steps:**
  1. Victim opens checkout tab; attacker opens same tab in new window (gets `window.opener` ref)
  2. Win the race condition: send postMessage before parent, injecting CSS into credit card iframe
  3. CSS bypasses blacklist using backslash Unicode escapes
  4. CSP bypass: use media query + comment trick for arbitrary CSS
  5. Define 160 fonts (one per unicode-range) + 16 CSS classes
  6. When victim types credit card number, each digit triggers a specific font load
  7. Zero-width font initially loaded so victim doesn't see character
  8. Font load hits attacker server; attacker logs the digit
  9. After logging, attacker sends postMessage to clear field + set placeholder to show typed digit
  10. Repeats for 16 digits — full credit card number exfiltrated
- **Key technical details:** PostMessage broadcast without origin check; CSS backslash escaping; 160 fonts with unicode-range; zero-width SVG font converted to WOFF; `@media` + comment CSP bypass
- **Impact / severity / bounty:** Critical; full credit card number exfiltration; received "Best Submission" + "Customer Obsession" awards
- **Obstacles & how solved:** CSS blacklist → Unicode escapes; CSP blocking imports → media query + comment trick; 25+ hours invested

### Techniques and Primitives
- **PostMessage enumeration** — Franz's Chrome extension logs all postMessage calls
- **CSS exfiltration** — 1) Inject CSS 2) Define fonts per unicode-range 3) Load external font on matching char 4) Get callback
- **CSS blacklist bypass** — backslash encoding (e.g., `\69\6d\70\6f\72\74` for `@import`); Unicode escapes
- **CSS Painting API** — `CSS.paintWorklet.addModule('paint.js')` then use `paint(myPainter)` in CSS — potential for calling JS from CSS

### Tooling and Resources
- Franz Rosen's postMessage Tracker Chrome extension
- Matthias' blog post on CSS character escape sequences
- Nathaniel Latimer (d0nut) CSS recursive `@import` chaining technique
- res0x0's blog "Hacking with ChatGPT"

### Suggestions and Advices from Hunter
- "PostMessage is like an API for the client-side webpage" — Joel
- "When you get a reference to a window via `window.opener`, you can send postMessages and interact cross-origin" — Joel

### AI Takeaway
The CSS keylogger is a masterclass in building a complex exploit chain from an apparently limited injection primitive (CSS). The key innovations: zero-width font for stealth, font unicode-range for data encoding, media query + CSS comments for CSP bypass. This technique is portable to any CSS injection scenario.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
PostMessage bugs: Franz Rosen's Chrome extension detects postMessage events; easy XSS via unvalidated postMessage

#### 2. What you should learn
- Understand **franz rosen's postmessage tracker chrome extension: logs all `window.postmessage` calls with data**
- Understand **use `window.opener` reference to reach back across same-origin windows for data exfiltration**
- Understand **css escapes: `\` encoding, unicode `\0031` for character bypass**
- Understand **css injection data exfiltration: define fonts per unicode range, use `background-url` for callback**
- Understand **use zero-width font so user doesn't see typed character during exfiltration**

#### 3. Core concepts explained
**CSS Injection → CSS Keylogger — Credit Card Data Exfiltration (Critical)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**PostMessage enumeration**
- Franz's Chrome extension logs all postMessage calls

**CSS exfiltration**
- 1) Inject CSS 2) Define fonts per unicode-range 3) Load external font on matching char 4) Get callback

**CSS blacklist bypass**
- backslash encoding (e.g., `\69\6d\70\6f\72\74` for `@import`); Unicode escapes


#### 4. Techniques and tactics
**PostMessage enumeration**
- **What it is:** Franz's Chrome extension logs all postMessage calls
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CSS exfiltration**
- **What it is:** 1) Inject CSS 2) Define fonts per unicode-range 3) Load external font on matching char 4) Get callback
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CSS blacklist bypass**
- **What it is:** backslash encoding (e.g., `\69\6d\70\6f\72\74` for `@import`); Unicode escapes
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CSS Painting API**
- **What it is:** `CSS.paintWorklet.addModule('paint.js')` then use `paint(myPainter)` in CSS — potential for calling JS from CSS
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"PostMessage is like an API for the client-side webpage"* — **Joel**
- *"When you get a reference to a window via `window.opener`, you can send postMessages and interact cross-origin"* — **Joel**

#### 6. Mental models
- **PostMessage is like an API for the client-side webpage" — Jo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **When you get a reference to a window via `window.opener`, yo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Franz Rosen's postMessage Tracker Chrome extension: logs all `window.postMessage` calls with data
- **Try this:** Use `window.opener` reference to reach back across same-origin windows for data exfiltration
- **Try this:** CSS escapes: `\` encoding, Unicode `\0031` for character bypass
- **Try this:** CSS injection data exfiltration: define fonts per unicode range, use `background-url` for callback

#### 8. Red flags and pitfalls
- - Obstacles & how solved: CSS blacklist → Unicode escapes; CSP blocking imports → media query + comment trick; 25+ hours invested

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in CSS Injection → CSS Keylogger — Credit Card Data Exfiltration (Critical)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **PostMessage bugs: Franz Rosen's Chrome extension detects postMessage events; eas**
2. **Franz Rosen's postMessage Tracker Chrome extension: logs all `window.postMessage**
3. **Use `window.opener` reference to reach back across same-origin windows for data **
