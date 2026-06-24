---
title: "Client-side Advanced Topics"
episode: 151
---


# Episode 151 Client-side Advanced Topics

### TL;DR
- Deep dive on third-party cookie partitioning (CHIPS), postMessage advanced techniques, iframe sandbox inheritance, URL parsing quirks, CSPT, and client-side route analysis
- Iframe sandbox origin inheritance: a sandboxed iframe with `allow-popups` can window.open to any site, and that new window **inherits the sandboxed properties** (null origin, no scripts, no forms, etc.)
- `event.origin === window.origin` check bypass via null origins — both are string "null" so they match
- JavaScript URI hostname handling: `javascript://comment%0Aalert(1)` — Chrome now parses JS URIs with hostnames, enabling new bypasses
- CSPT → CSRF: use callback/finalize routes to force state-changing requests from victim's session

### Key Takeaways
- **CHIPS (Cookies Having Independent Partitioned State)**: Partitioned cookies are keyed by `(scheme + eTLD+1 of top-level site) + (host of iframe)`. Same eTLD+1 top-level + same iframe host = cookie shared; otherwise isolated
- **PostMessage advanced:**
  - `event.data` can be complex types (BigInt, RegExp) not just JSON-stringifiable
  - `event.source` can be null (iframe with no src → `frames[0].eval()` → postMessage → immediately set `innerHTML` to something else)
  - **MessagePorts**: can-like communication; port is passed once, communication is private; standard postMessage trackers may miss port-based messages
- **Iframe sandbox inheritance**: A sandboxed iframe's properties (null origin, no scripts, no forms) are inherited by any window it opens via `window.open()`
- **URL Parsing tricks:**
  - `\` (backslash) → `/` (slash) in URL context, enabling relative→absolute URL conversion
  - `javascript://comment%0Acode` — `//` is a JS comment, `%0A` creates newline, code executes
  - Parsing `event.origin` via `document.createElement('a')` with `href = event.origin` — if null origin, `a.hostname` returns the current page's hostname (since "null" is treated as relative path `./null`)
- **Client-side route analysis**: Search all JS files for route definitions; look at every route, every query parameter parsed via `URLSearchParams`, every hash handler

### Techniques and Primitives
**Null Origin Bypass for PostMessage** — Use sandboxed iframe + allow-popups → window.open(target) → inherited null origin → `event.origin === window.origin` passes because both are string "null"

**Sandbox Constraint Imposition** — Missing `allow-forms` means forms can't auto-submit; use to break form-dependent flows. Missing `allow-scripts` means no JS — use `<a target="_blank">` to open pages without JS

**Window Hijacking via Name** — Iframe named `abc` on attacker page; victim page does `window.open(name='abc')` → opens into attacker's iframe instead of new tab (same-origin required). Attacker can redirect/monitor

**Hash Change Triggers** — `window.open(url)`, then `window.open(url + '#newhash')` triggers `onhashchange` on the existing window without reload — useful for forcing state changes

### AI Takeaway
The null origin inheritance via sandboxed iframe + window.open is extraordinarily powerful — it bypasses `event.origin === window.origin` checks which is one of the most robust postMessage security patterns.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Deep dive on third-party cookie partitioning (CHIPS), postMessage advanced techniques, iframe sandbox inheritance, URL parsing quirks, CSPT, and client-side route analysis

#### 2. What you should learn
- Understand **chips (cookies having independent partitioned state)**: partitioned cookies are keyed by `(scheme + etld+1 of top-level site) + (host of iframe)`. same etld+1 top-level + same iframe host = cookie shared; otherwise isolated**
- Understand **postmessage advanced:**
- Understand **`event.data` can be complex types (bigint, regexp) not just json-stringifiable**
- Understand **`event.source` can be null (iframe with no src → `frames[0].eval()` → postmessage → immediately set `innerhtml` to something else)**
- Understand **messageports**: can-like communication; port is passed once, communication is private; standard postmessage trackers may miss port-based messages**

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** CHIPS (Cookies Having Independent Partitioned State)**: Partitioned cookies are keyed by `(scheme + eTLD+1 of top-level site) + (host of iframe)`. Same eTLD+1 top-level + same iframe host = cookie shared; otherwise isolated
- **Try this:** PostMessage advanced:
- **Try this:** `event.data` can be complex types (BigInt, RegExp) not just JSON-stringifiable
- **Try this:** `event.source` can be null (iframe with no src → `frames[0].eval()` → postMessage → immediately set `innerHTML` to something else)

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Deep dive on third-party cookie partitioning (CHIPS), postMessage advanced techn**
2. **CHIPS (Cookies Having Independent Partitioned State)**: Partitioned cookies are **
3. **PostMessage advanced:**
