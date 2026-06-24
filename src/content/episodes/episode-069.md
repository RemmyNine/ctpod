---
title: "Johan Carlsson — 3-Month Check-in on Full-time Bug Bounty"
episode: 69
---


# Episode 69 Johan Carlsson — 3-Month Check-in on Full-time Bug Bounty

**Guest:** Johan Carlsson (joaxcar)
**Format:** Show notes with timestamps (feed) — full transcript
**Topics:** GitHub CSP bypass, script gadgets, GitLab pipeline critical, full-time bug bounty journey

### TL;DR
- Johan found a GitHub CSP bypass: HTML injection → form action hijacking → Hotwire (Turbo Frames + Turbo Streams) → SSH key upload → ATO
- CSP `form-action` directive is NOT covered by `default-src` — common oversight in CSP evaluators
- Hotwire/Turbo framework enables scriptless HTML processing — when new content enters DOM, Turbo automatically fetches/processes it
- GitHub had a hash-change click gadget (`onhashchange` → finds element with matching `href` → clicks it) enabling zero-click after drag-and-drop
- GitLab pipeline critical: unauthenticated RCE via pipeline processing logic

### Key Takeaways
- Google's CSP Evaluator does NOT warn about missing `form-action` — it only evaluates XSS-relevant directives
- `form-action` is one of the few directives NOT covered by `default-src` — if absent, forms can submit anywhere
- Hotwire/Turbo: `turbo-frame` + `turbo-stream` elements trigger automatic fetch and DOM replacement without JavaScript execution — bypasses CSP `script-src`
- `data-replace-with` (Rails UJS legacy) provides click-based content replacement — click + Turbo = multi-step gadget chain
- GitHub hash-change click gadget: `window.onhashchange` → `document.querySelector(`[href="${hash}"]`)` → `.click()` — any page with this listener and attacker-controlled hash = click jacking without user interaction

### Bugs and Findings

#### GitHub CSP Bypass → SSH Key Upload ATO
- **Target/context:** GitHub — HTML injection in error message field
- **Root cause:** Input field reflected unsanitized → HTML injection; CSP `default-src` strict but `form-action` missing; Hotwire/Turbo framework processes DOM changes
- **Exploitation steps:**
  1. Attacker page sets up drag-and-drop that injects HTML into victim's GitHub session (cross-window forgery)
  2. HTML injection creates a `turbo-frame` element that fetches the SSH key addition form
  3. Turbo processes the frame: fetches the form (with valid CSRF token by design)
  4. `turbo-stream` elements replace parts of the form with attacker's SSH public key
  5. Drag-and-drop triggers HTML injection → hash-change clock gadget clicks buttons twice (inject + submit)
  6. SSH key added to victim's account → attacker clones repos
- **Impact:** Full source code access via SSH key persistence
- **Bounty:** Medium (bounty doubled from standard for the chain)
- **Key technical detail:** The exploit requires the victim to be in "sudo mode" (recent password confirmation)

#### GitLab Pipeline Critical (RCE)
- **Target/context:** GitLab
- **Root cause:** Unauthenticated arbitrary code execution via pipeline processing [details partially transcribed]
- **Impact:** Full RCE, pre-auth

### Techniques and Primitives
- **Script gadgets + HTML injection in CSP-heavy environments:** Look for framework-specific DOM observers (Turbo, Hotwire, Stimulus, Angular) that process element attributes on insertion — these don't need JS execution, only HTML injection
- **Hash-change click gadget:** Pages with `onhashchange` listeners that click elements matching the hash value — zero-click interaction via window.open + hash change
- **Cross-origin hash change without refresh:** `window.opener.location = "https://target.com/path#hash"` doesn't reload the page — only triggers hash change event (if path matches)

### Tooling and Resources
- `cspvalidator.org` — alternative CSP evaluator that checks form-action
- `joaxcar.com/blog/` — Johan's writeups
- CSP evaluator (Google) — open source, can be extended

### Suggestions and Advices
- **Johan:** "If you want to get good at finding gadgets, study disclosed reports of top hackers on your target platform — I learned everything from William (Vax)'s GitLab writeups"
- "Script gadgets are the key to exploiting HTML injection when CSP kills inline JS"
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Johan found a GitHub CSP bypass: HTML injection → form action hijacking → Hotwire (Turbo Frames + Turbo Streams) → SSH key upload → ATO

#### 2. What you should learn
- Understand **google's csp evaluator does not warn about missing `form-action` — it only evaluates xss-relevant directives**
- Understand **`form-action` is one of the few directives not covered by `default-src` — if absent, forms can submit anywhere**
- Understand **hotwire/turbo: `turbo-frame` + `turbo-stream` elements trigger automatic fetch and dom replacement without javascript execution — bypasses csp `script-src`**
- Understand **`data-replace-with` (rails ujs legacy) provides click-based content replacement — click + turbo = multi-step gadget chain**
- Understand **github hash-change click gadget: `window.onhashchange` → `document.queryselector(`[href="${hash}"]`)` → `.click()` — any page with this listener and attacker-controlled hash = click jacking without user interaction**

#### 3. Core concepts explained
**GitHub CSP Bypass → SSH Key Upload ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**GitLab Pipeline Critical (RCE)**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Script gadgets + HTML injection in CSP-heavy environments: Look for framework-specific DOM observers (Turbo, Hotwire, Stimulus, Angular) that process element attributes on insertion**
- these don't need JS execution, only HTML injection

**Hash-change click gadget: Pages with `onhashchange` listeners that click elements matching the hash value**
- zero-click interaction via window.open + hash change

**Cross-origin hash change without refresh: `window.opener.location = "https://target.com/path#hash"` doesn't reload the page**
- only triggers hash change event (if path matches)


#### 4. Techniques and tactics
**Script gadgets + HTML injection in CSP-heavy environments: Look for framework-specific DOM observers (Turbo, Hotwire, Stimulus, Angular) that process element attributes on insertion**
- **What it is:** these don't need JS execution, only HTML injection
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Hash-change click gadget: Pages with `onhashchange` listeners that click elements matching the hash value**
- **What it is:** zero-click interaction via window.open + hash change
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cross-origin hash change without refresh: `window.opener.location = "https://target.com/path#hash"` doesn't reload the page**
- **What it is:** only triggers hash change event (if path matches)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Johan: "If you want to get good at finding gadgets, study disclosed reports of top hackers on your target platform"* — **I learned everything from William (Vax)'s GitLab writeups**
- *"Script gadgets are the key to exploiting HTML injection when CSP kills inline JS"*

#### 6. Mental models
- **Johan: "If you want to get good at finding gadgets, study di** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Script gadgets are the key to exploiting HTML injection when** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Google's CSP Evaluator does NOT warn about missing `form-action` — it only evaluates XSS-relevant directives
- **Try this:** `form-action` is one of the few directives NOT covered by `default-src` — if absent, forms can submit anywhere
- **Try this:** Hotwire/Turbo: `turbo-frame` + `turbo-stream` elements trigger automatic fetch and DOM replacement without JavaScript execution — bypasses CSP `script-src`
- **Try this:** `data-replace-with` (Rails UJS legacy) provides click-based content replacement — click + Turbo = multi-step gadget chain

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GitHub CSP Bypass → SSH Key Upload ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Johan found a GitHub CSP bypass: HTML injection → form action hijacking → Hotwir**
2. **Google's CSP Evaluator does NOT warn about missing `form-action` — it only evalu**
3. **`form-action` is one of the few directives NOT covered by `default-src` — if abs**
