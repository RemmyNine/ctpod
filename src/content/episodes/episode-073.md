---
title: "Sandboxed IFrames and WAF Bypasses"
episode: 73
---


# Episode 73 Sandboxed IFrames and WAF Bypasses

**TL;DR**
- `?.` operator (optional chaining) can bypass WAFs when placed between function name and parentheses
- AssetNote's `nowafpls` tool pads requests with garbage (up to 100MB) to exceed WAF processing limits
- Chrome's `force-cache` fetch mode once allowed reading cached `Access-Control-Allow-Origin: *` responses with cookies — now fixed
- Sandboxed iframe via `srcdoc` leaks `document.baseURI` of the top-level frame (null origin bypass)
- `window.open` from a sandboxed iframe creates a new window with null origin too — can communicate with other null-origin frames via postMessage if `event.origin === window.origin`
- iframe hijacking: if `window.open` uses a guessable window name, attacker creates an iframe with that name on their page to intercept the popup

**Key Takeaways**
- Use `func?.()` syntax when testing WAFs — many WAFs don't expect `?.` between function name and parentheses
- Always check if the target has sandboxed iframes with `srcdoc` — can leak top-level `baseURI` (and e.g. OAuth codes from URL)
- With sandboxed iframes that allow popups, test `window.open` — the new window inherits null origin, enabling cross-frame communication bypasses
- When you see `window.open` with a named target, check if you can pre-register that name in your own iframe (Chrome-specific, does NOT work in Firefox or incognito)

**Bugs and Findings**

### Sandbox iframe baseURI leak — CSP bypass / info disclosure
- **Target/context:** Sandboxed iframe using `srcdoc` attribute
- **Root cause:** `document.baseURI` in a sandboxed `srcdoc` iframe returns the top-level document's URI, not the sandbox origin
- **Technique / how found:** Johan Carlsen's XSS challenge; set up a sandboxed iframe with `srcdoc`, scripts enabled, and access `document.baseURI`
- **Exploitation steps:**
  1. Attacker page embeds `<iframe sandbox="allow-scripts" srcdoc="...">`
  2. Inside the iframe, read `document.baseURI` — it leaks the top window's URL
  3. If the URL contains an OAuth code/state, exfiltrate it
- **Impact / severity / bounty:** Can leak OAuth codes from the top-level URL path even from a null-origin sandbox

### Window.open from sandboxed iframe — null origin communication bypass
- **Target/context:** Web apps using `window.open` from within a sandboxed iframe
- **Root cause:** The opened window inherits the sandbox's null origin
- **Technique / how found:** Blog post by `blog.huli.tw`; still works (not fixed)
- **Exploitation steps:**
  1. Create a sandboxed iframe with `allow-popups` and `allow-scripts`
  2. Inside it, call `window.open('https://target.com/page')`
  3. The new window has null origin but sends the user's cookies (full top-level nav)
  4. Attacker creates ANOTHER null-origin frame, communicates via postMessage if the target checks `event.origin === window.origin` (both null → passes)
  5. Leak page content since cookies were sent
- **Key technical details:** Only works because both frames have origin `null`; `event.origin === window.origin` pattern is vulnerable
- **Impact / severity / bounty:** Can leak any data on pages the victim is authenticated to

### iframe hijacking via named window.open — CSRF/ATO
- **Target/context:** OAuth flows using `window.open` with a named target window
- **Root cause:** Chrome allows matching a named iframe in the same tab group before opening a new window
- **Technique / how found:** Justin's research; only works in Chrome (not Firefox, not Chrome incognito)
- **Exploitation steps:**
  1. Find a page that does `window.open('https://login.example.com/auth', 'oauth_window')`
  2. Attacker embeds `<iframe name="oauth_window" src="https://login.example.com/404">` (must be iframeable)
  3. When the victim clicks the trigger, the popup opens inside the attacker's iframe instead
  4. Attacker controls the iframe — can redirect it to attacker domain, inject own credentials/response
- **Key technical details:** The window name is guessable; Chrome checks existing frames in the tab group; Firefox does not support this behavior
- **Impact / severity / bounty:** Full OAuth flow hijack, ATO

**Techniques and Primitives**
- **WAF bypass via padding** — Send 100MB of garbage (`A=A` URL-encoded) before your payload; WAFs hit processing limits and pass the request through
- **`?.()` operator for WAF bypass** — Use optional chaining between function name and parentheses; many WAF regexes don't account for it
- **Force-cache CORS leak (fixed)** — `fetch(url, {cache: "force-cache"})` on a cached `ACAO: *` response could read it cross-origin even with cookies [now fixed in Chrome]

**Tooling and Resources**
- `github.com/assetnote/nowafpls` — WAF bypass via request padding
- `joaxcar.com/blog/2024/05/16/sandbox-iframe-xss-challenge-solution/` — Johan Carlsen's sandbox iframe XSS challenge
- `blog.huli.tw/2022/04/07/en/iframe-and-window-open/` — iframe and window.open magic
- `github.com/kevin-mizu/domloggerpp` — DOM logger
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 73 Sandboxed IFrames and WAF Bypasses covers practical bug bounty techniques and security research insights.

#### 2. What you should learn
- Understand the vulnerability classes discussed
- Learn practical exploitation techniques
- Know which tools are useful for this type of research

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
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Understand the vulnerability class** — Know how it works and why it matters
2. **Master the exploitation technique** — Practice the specific steps to exploit it
3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets
