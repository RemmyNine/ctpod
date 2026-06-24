---
title: "Crit Research Lab Update & Client-Side Tricks Galore"
episode: 140
---


# Episode 140 Crit Research Lab Update & Client-Side Tricks Galore

**Source:** Show notes (feed) — condensed.

### TL;DR
- Critical Research Lab: micro ($20-50), full ($100-250), mega ($500) research bounties.
- Jorian: Web Worker XSS with Blobs → drag-drop API.
- CVE-2022-21703: CSRF via `text/plain;` with trailing semicolon.
- CSS font-leak: static mode with keyframe animations + data URI fonts.
- Cookie Chaos (PortSwigger): `strip()` on cookie names.

### Key takeaways
- [ ] Web Worker XSS: exploit → blob → drag-and-drop → main-origin XSS.
- [ ] CSRF via content-type: `text/plain;` passes `includes()` checks.
- [ ] CSS font-leak: `@font-face` + `data:` URI + keyframe animations.
- [ ] Quirks mode: PHP warning pushes doctype down → CSS exfiltration via frame count.
- [ ] Cookie prefixes bypassed by Unicode whitespace + `strip()`.

### Bugs and Findings

#### Web Worker XSS with Blobs — XSS escalation
- **Technique:** XSS in worker → `new Blob([payload],{type:'text/html'})` → leak blob URL → attacker page with fullscreen popup + drag → blob opens in main origin.
- **Impact:** Universal main-origin XSS from web worker XSS.

#### Cookie Prefix Bypass via strip() — Cookie injection
- **Root cause:** Django `strip()` removes Unicode whitespace (U+00A0, U+1680, U+2000-200A, U+2028, U+2029, U+205F, U+3000, U+FEFF). Browser doesn't strip → attacker sets `\u00A0__Host-session=malicious`, browser sees different name, Django sees `__Host-session`.
- **Impact:** Bypass `__Host-` and `__Secure-` prefix protections.

#### CSS Font-Leak — Data exfiltration
- **Technique:** `@font-face` + keyframe anim + background-image loads = binary search of `<head>` contents.
- **Key detail:** 5k char limit; used 5-letter domain; custom font-leak flavor with TTF compression.
- **Impact:** Exfiltrate tokens from `<head>`.

#### CSRF via `text/plain;` — CSRF (CVE-2022-21703)
- **Root cause:** Server does `content-type.includes('text/plain')`. Fetch spec allows `text/plain;` cross-origin with arbitrary body.
- **Impact:** CSRF bypass.

### Techniques and Primitives
- **Frame counting for cross-site leaks** — `window.length` excludes `display:none` iframes.
- **Named window references** — `<object name="x">` → `window['x']` for cross-site leak.
- **Invisible Unicode in AI spec** — Humans can't see, LLMs read → backdoor in generated code.
- **AI business logic flaws** — Attack parsing/delivery layer, not LLM itself.
- **postMessage hunting** — FancyTracker extension; watch counter increase on clicks.

### Suggestions and Advices from Hunter
- "Study the test files — they reveal developer's security values." (Justin)
- "Knowledge mismatch between human and AI creates new vulns." (Rez0)
- "Attack the parsing layer before the LLM." (Rez0)
- "Small talk with the application — sometimes you find full SSRF." (Nick Copi)
- "Invite collaboration in CTBB Discord." (Tom Anthony story)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Critical Research Lab: micro ($20-50), full ($100-250), mega ($500) research bounties.

#### 2. What you should learn
- Understand **[ ] web worker xss: exploit → blob → drag-and-drop → main-origin xss**
- Understand **[ ] csrf via content-type: `text/plain;` passes `includes()` checks**
- Understand **[ ] css font-leak: `@font-face` + `data:` uri + keyframe animations**
- Understand **[ ] quirks mode: php warning pushes doctype down → css exfiltration via frame count**
- Understand **[ ] cookie prefixes bypassed by unicode whitespace + `strip()`**

#### 3. Core concepts explained
**Web Worker XSS with Blobs — XSS escalation**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Cookie Prefix Bypass via strip() — Cookie injection**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CSS Font-Leak — Data exfiltration**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Frame counting for cross-site leaks**
- `window.length` excludes `display:none` iframes.

**Named window references**
- `<object name="x">` → `window['x']` for cross-site leak.

**Invisible Unicode in AI spec**
- Humans can't see, LLMs read → backdoor in generated code.


#### 4. Techniques and tactics
**Frame counting for cross-site leaks**
- **What it is:** `window.length` excludes `display:none` iframes.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Named window references**
- **What it is:** `<object name="x">` → `window['x']` for cross-site leak.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Invisible Unicode in AI spec**
- **What it is:** Humans can't see, LLMs read → backdoor in generated code.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**AI business logic flaws**
- **What it is:** Attack parsing/delivery layer, not LLM itself.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**postMessage hunting**
- **What it is:** FancyTracker extension; watch counter increase on clicks.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Study the test files"* — **they reveal developer's security values." (Justin)**
- *"Knowledge mismatch between human and AI creates new vulns." (Rez0)"*
- *"Attack the parsing layer before the LLM." (Rez0)"*
- *"Small talk with the application"* — **sometimes you find full SSRF." (Nick Copi)**
- *"Invite collaboration in CTBB Discord." (Tom Anthony story)"*

#### 6. Mental models
- **Study the test files — they reveal developer's security valu** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Knowledge mismatch between human and AI creates new vulns." ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Attack the parsing layer before the LLM." (Rez0)** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Web Worker XSS: exploit → blob → drag-and-drop → main-origin XSS.
- **Try this:** [ ] CSRF via content-type: `text/plain;` passes `includes()` checks.
- **Try this:** [ ] CSS font-leak: `@font-face` + `data:` URI + keyframe animations.
- **Try this:** [ ] Quirks mode: PHP warning pushes doctype down → CSS exfiltration via frame count.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **API** — Application Programming Interface — structured endpoints for data exchange
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Web Worker XSS with Blobs — XSS escalation?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Critical Research Lab: micro ($20-50), full ($100-250), mega ($500) research bou**
2. **[ ] Web Worker XSS: exploit → blob → drag-and-drop → main-origin XSS.**
3. **[ ] CSRF via content-type: `text/plain;` passes `includes()` checks.**
