---
title: "Google's Top AI Hackers: Busfactor and Monke"
episode: 144
---


# Episode 144 Google's Top AI Hackers: Busfactor and Monke

**Source:** Show notes (feed) — condensed.

### TL;DR
- Vitor + Kieran at Google LHE Mexico: 16 reports (14 valid), 2nd overall, Best AI VRP.
- Vitor's chain: postMessage → prototype pollution → WebSocket host override → XSS → iframe sandwich → ATO.
- Google LHE: focus on AI features (Kieran's advice paid off).
- Full-time: lock into ONE program 100+ hours.
- Google AI VRP: pays CRIT for data exfiltration.

### Key takeaways
- [ ] Google LHE: AI features are priority. Pay crit for exfiltration.
- [ ] PostMessage chain: no origin check + prototype pollution (JSON.parse+Object.assign) → WebSocket host → XSS → iframe sandwich.
- [ ] LHE strategy: prioritize bonus features, avoid rabbit holes.
- [ ] Full-time: lock into ONE program for 100+ hours. Pomodoro, exercise, accept bad days.
- [ ] AI VRP: non-AI bugs in AI products = fast-moving dev mistakes.

### Bugs and Findings

#### PostMessage → PPT → WS Override → XSS → ATO — ATO
- **Chain:** PostMessage (no origin) → JSON.parse+Object.assign config → `version` property controls WebSocket host → setup malicious Socket.IO server → XSS on chat domain → iframe sandwich opens product page (same origin) → steal auth token.
- **Key details:** `version` property → WebSocket endpoint. Socket.IO compatible server. Iframe sandwich: two same-origin windows communicate.
- **Impact:** Session takeover across all products. 50% bonus.

### Techniques and Primitives
- **PostMessage → PPT chain** — Look for `JSON.parse()` + `Object.assign()`.
- **Iframe sandwich** — `window.open()` two same-origin pages → they communicate.
- **LHE AI focus** — Google AI VRP pays crit for exfiltration.
- **Prototype pollution via config** — Deep config properties affecting runtime behavior.

### Suggestions and Advices from Hunter
- "At Google LHEs, focus entirely on AI features. They pay crit." (Kieran)
- "Lock into ONE program for 100+ hours." (Vitor via Justin)
- "Use Pomodoro. Set micro-tasks. Accept bad days." (Vitor)
- "Don't treat full-time like a 9-to-5. Use the flexibility." (All)
- "Don't isolate yourself when working remotely." (Vitor)


### 📘 Episode Booklet

#### 1. Episode in one sentence
Vitor + Kieran at Google LHE Mexico: 16 reports (14 valid), 2nd overall, Best AI VRP.

#### 2. What you should learn
- Understand **[ ] google lhe: ai features are priority. pay crit for exfiltration**
- Understand **[ ] postmessage chain: no origin check + prototype pollution (json.parse+object.assign) → websocket host → xss → iframe sandwich**
- Understand **[ ] lhe strategy: prioritize bonus features, avoid rabbit holes**
- Understand **[ ] full-time: lock into one program for 100+ hours. pomodoro, exercise, accept bad days**
- Understand **[ ] ai vrp: non-ai bugs in ai products = fast-moving dev mistakes**

#### 3. Core concepts explained
**PostMessage → PPT → WS Override → XSS → ATO — ATO**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**PostMessage → PPT chain**
- Look for `JSON.parse()` + `Object.assign()`.

**Iframe sandwich**
- `window.open()` two same-origin pages → they communicate.

**LHE AI focus**
- Google AI VRP pays crit for exfiltration.


#### 4. Techniques and tactics
**PostMessage → PPT chain**
- **What it is:** Look for `JSON.parse()` + `Object.assign()`.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Iframe sandwich**
- **What it is:** `window.open()` two same-origin pages → they communicate.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**LHE AI focus**
- **What it is:** Google AI VRP pays crit for exfiltration.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Prototype pollution via config**
- **What it is:** Deep config properties affecting runtime behavior.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"At Google LHEs, focus entirely on AI features. They pay crit." (Kieran)"*
- *"Lock into ONE program for 100+ hours." (Vitor via Justin)"*
- *"Use Pomodoro. Set micro-tasks. Accept bad days." (Vitor)"*
- *"Don't treat full-time like a 9-to-5. Use the flexibility." (All)"*
- *"Don't isolate yourself when working remotely." (Vitor)"*

#### 6. Mental models
- **At Google LHEs, focus entirely on AI features. They pay crit** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Lock into ONE program for 100+ hours." (Vitor via Justin)** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use Pomodoro. Set micro-tasks. Accept bad days." (Vitor)** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Google LHE: AI features are priority. Pay crit for exfiltration.
- **Try this:** [ ] PostMessage chain: no origin check + prototype pollution (JSON.parse+Object.assign) → WebSocket host → XSS → iframe sandwich.
- **Try this:** [ ] LHE strategy: prioritize bonus features, avoid rabbit holes.
- **Try this:** [ ] Full-time: lock into ONE program for 100+ hours. Pomodoro, exercise, accept bad days.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in PostMessage → PPT → WS Override → XSS → ATO — ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Vitor + Kieran at Google LHE Mexico: 16 reports (14 valid), 2nd overall, Best AI**
2. **[ ] Google LHE: AI features are priority. Pay crit for exfiltration.**
3. **[ ] PostMessage chain: no origin check + prototype pollution (JSON.parse+Object.**
