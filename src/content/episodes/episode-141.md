---
title: "Hacking the Pod — Google Docs 0-day & React CreateElement Exploits with Nick Copi (7urb0)"
episode: 141
---


# Episode 141 Hacking the Pod — Google Docs 0-day & React CreateElement Exploits with Nick Copi (7urb0)

**Source:** Full ASR transcript.

### TL;DR
- Nick left a ReDoS in the prep Google Doc: rich content paste → OOM crash.
- React `createElement` sink: JSON → XSS via type+props (iframe), type+children (style), props only (dangerouslySetInnerHTML).
- Electron RCE: React XSS → IPC persistence → C2 with screenshots.
- `attributes[0].value` + `URL` for char-restricted XSS.

### Key takeaways
- [ ] Google Docs ReDoS via rich paste: inefficient regex causes hang.
- [ ] React `createElement(type, props, children)`: type=string → tag name. Props=attributes.
- [ ] Electron IPC persistence: background window with IPC access re-spawns XSS on restart.
- [ ] `throw` + `onerror=eval` for code execution in restricted char environments.
- [ ] `attributes[0].value` inside event handler redefines the attribute using `URL` = documentURI.

### Bugs and Findings

#### Google Docs ReDoS — DoS
- **Technique:** `monitor(RegExp.prototype.exec)` to collect regexes → ReDoS detector → rich content paste triggers catastrophic backtracking.
- **Exploitation:** Click button on attacker page → malicious rich content copied → paste in Docs → hang.
- **Impact:** DoS of Docs editor.

#### React CreateElement Sink — XSS
- **Scenarios:**
  - type+props: `<iframe src="javascript:alert(1)">`
  - type+children: `<style>...</style>` CSS injection
  - props only (no children): `dangerouslySetInnerHTML={{__html: payload}}`
- **Key detail:** `Symbol` check in React 18+ prevents fake elements from JSON.

#### Electron RCE via React XSS → IPC — RCE
- **Exploitation:**
  1. React createElement XSS.
  2. Open background window with IPC access.
  3. IPC `setLatestPageVisited` spammed → persisting XSS on restart.
  4. Additional IPC: list processes, screenshot, JS console (BeEF-like C2).
- **Impact:** Full persistent C2 on desktop app.

### Techniques and Primitives
- **Regex debug with `monitor()`** — Capture all regex executions.
- **React createElement cheat sheet** — Type+props=iframe XSS; Type+children=style; Props only=dangerouslySetInnerHTML.
- **Electron IPC persistence** — Re-spawn XSS after app restart via IPC.
- **Attributes reference XSS** — `attributes[0].value = \`${URL}\`` in event handler.

### Tooling and Resources
- `debug()` and `monitor()` in Chrome DevTools
- Open-source ReDoS detector

### Suggestions and Advices from Hunter
- "Small talk with the application — poke it lightly when you don't understand it."
- "If you get XSS too fast, work backwards from it."
- "JSON reaching `React.createElement` = XSS goldmine."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Nick left a ReDoS in the prep Google Doc: rich content paste → OOM crash.

#### 2. What you should learn
- Understand **[ ] google docs redos via rich paste: inefficient regex causes hang**
- Understand **[ ] react `createelement(type, props, children)`: type=string → tag name. props=attributes**
- Understand **[ ] electron ipc persistence: background window with ipc access re-spawns xss on restart**
- Understand **[ ] `throw` + `onerror=eval` for code execution in restricted char environments**
- Understand **[ ] `attributes[0].value` inside event handler redefines the attribute using `url` = documenturi**

#### 3. Core concepts explained
**Google Docs ReDoS — DoS**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**React CreateElement Sink — XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Electron RCE via React XSS → IPC — RCE**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Regex debug with `monitor()`**
- Capture all regex executions.

**React createElement cheat sheet**
- Type+props=iframe XSS; Type+children=style; Props only=dangerouslySetInnerHTML.

**Electron IPC persistence**
- Re-spawn XSS after app restart via IPC.


#### 4. Techniques and tactics
**Regex debug with `monitor()`**
- **What it is:** Capture all regex executions.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**React createElement cheat sheet**
- **What it is:** Type+props=iframe XSS; Type+children=style; Props only=dangerouslySetInnerHTML.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Electron IPC persistence**
- **What it is:** Re-spawn XSS after app restart via IPC.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Attributes reference XSS**
- **What it is:** `attributes[0].value = \`${URL}\`` in event handler.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Small talk with the application"* — **poke it lightly when you don't understand it.**
- *"If you get XSS too fast, work backwards from it."*
- *"JSON reaching `React.createElement` = XSS goldmine."*

#### 6. Mental models
- **Small talk with the application — poke it lightly when you d** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you get XSS too fast, work backwards from it.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **JSON reaching `React.createElement` = XSS goldmine.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Google Docs ReDoS via rich paste: inefficient regex causes hang.
- **Try this:** [ ] React `createElement(type, props, children)`: type=string → tag name. Props=attributes.
- **Try this:** [ ] Electron IPC persistence: background window with IPC access re-spawns XSS on restart.
- **Try this:** [ ] `throw` + `onerror=eval` for code execution in restricted char environments.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Google Docs ReDoS — DoS?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Nick left a ReDoS in the prep Google Doc: rich content paste → OOM crash.**
2. **[ ] Google Docs ReDoS via rich paste: inefficient regex causes hang.**
3. **[ ] React `createElement(type, props, children)`: type=string → tag name. Props=**
