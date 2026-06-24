---
title: "Attacking Chrome Extensions with MatanBer"
episode: 95
---


# Episode 95 Attacking Chrome Extensions with MatanBer

**Guest:** MatanBer
**Host:** Justin Gardner (Rhynorater)
**Duration:** 1:56:23
**Transcript source:** feed (full transcript)

### TL;DR
- Manifest V3 extension structure: content script (isolated world), injected script (main world), service worker (background), extension pages
- Content script in attacker-controlled page: UI injection can be clickjacked, CSS-leaked, or accessed via shadow DOM tricks
- History.back() timing attack can get window reference to non-web-accessible extension pages
- External connectability (`onConnectExternal`/`onMessageExternal`) allows direct service worker communication from whitelisted origins
- MetaMask 120K bug: phishing warning page (web accessible) → redirects to sensitive notification page → clickjacked

### Key Takeaways
- Check `externally_connectable` in manifest.json — if present, `chrome.runtime` API is exposed on those origins → direct service worker access
- Content scripts share DOM but not JS environment with the page — but custom events and postMessage are still attackable
- Extension pages with strict CSP still allow CSS injection for data exfiltration (text-node leaking via animation/keyframe timing)
- To get extension source: download CRX from Chrome Web Store URL, or find in `<profile>/Extensions/<id>/` after installing
- For debugging: enable "Search in anonymous and content scripts" in DevTools preferences, remove content scripts from ignore list

### Bugs and Findings

#### MetaMask Clickjacking (120K Bug)
- **Target/context:** MetaMask Chrome extension
- **Root cause:** Phishing warning page was web-accessible; it had a link parameter pointing to its URL. The notification page (accept transaction) was NOT web-accessible, but could be reached via redirect from the accessible page
- **Exploitation steps:**
  1. On attacker page, open the web-accessible phishing warning page via iframe with URL param pointing to sensitive notification page
  2. Victim clicks the link inside the phishing warning page (ironically, a page warning about phishing)
  3. The phishing page redirects to the notification page (which was not web-accessible, but now accessible because it arrived via redirect from an accessible page)
  4. Clickjack the accept-transaction button
- **Impact / severity / bounty:** $120,000
- **Key technical details:** `web_accessible_resources` in manifest defines which files are accessible to websites. The phishing page was in WAR, the notification page was not. Redirect from accessible page → non-accessible page inherits accessibility.

#### Extension Page History.Back Bypass
- **Target/context:** Chrome extensions with non-web-accessible pages
- **Root cause:** If a user navigates to a non-web-accessible extension page, then later navigates to an attacker page in the same tab, the attacker page can do `history.back()` to go back to the extension page
- **Exploitation steps:**
  1. Victim visits extension page (e.g., options page, right-click extension icon)
  2. From that page, opens an attacker-controlled link
  3. Attacker page uses `window.open('', 'windowName')` to get a reference via the name
  4. Use timing to detect when `history.back()` lands on extension page (extension pages load locally → very fast)
  5. Incrementally step back through history until the fast-loading extension page is reached
- **Key technical details:** Extension pages served locally → sub-ms response time vs network requests. Use `window.location` navigation to skip non-extension pages in history.
- **Obstacles & how solved:** Requires user to visit extension page first (not common but possible via right-click → options)

### Techniques and Primitives
- **Isolated world → main world bridge hijack** — Injected scripts (running in main page world) communicate with content script via postMessage/custom events. Since main world is attacker-controlled, any message can be forged.
- **CSS injection in extension pages** — Manifest V3 CSP only restricts scripts (`script-src: self`), not styles. HTML injection + CSS injection = data exfiltration from extension pages.
- **`web_accessible_resources` → redirect → clickjack** — Find WAR page that accepts URL params for redirect, chain to non-WAR sensitive page.
- **Chrome extension debugging** — DevTools → Sources → Content Scripts picker; `about:inspect` → Service Workers for service worker debugging; Extension ID from `chrome://extensions` with developer mode

### Tooling and Resources
- Space Raccoon's blog on browser extension hacking
- DOMLogger++ (kevin-mizu)
- Chrome Extension Download URL: `https://clients2.google.com/service/update2/crx?response=redirect&prodversion=9999&acceptformat=crx2,crx3&x=id%3D<EXTENSION_ID>%26uc`
- PS Paul's text-node leaking with CSS research
- Masato Kinagawa's closed shadow DOM research

### Suggestions and Advices from Hunter
- "Extensions are super flexible and pretty locked down by default. You have to look at how they bent the extension for their features." — MatanBer
- "The CSP default for Manifest V3 is `script-src: self; object-src: self` — no eval. But there's no restriction on styles." — MatanBer
- "If an extension has externally_connectable, `chrome.runtime` API is exposed on those origins — you can connect directly to the service worker." — MatanBer

### AI Takeaway
Chrome extension hacking is a niche with low competition and high impact (universal XSS is possible). The combination of service workers, isolated worlds, and `web_accessible_resources` creates a unique threat model. The history.back() timing technique for accessing non-web-accessible pages is novel and broadly applicable.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Manifest V3 extension structure: content script (isolated world), injected script (main world), service worker (background), extension pages

#### 2. What you should learn
- Understand **check `externally_connectable` in manifest.json — if present, `chrome.runtime` api is exposed on those origins → direct service worker access**
- Understand **content scripts share dom but not js environment with the page — but custom events and postmessage are still attackable**
- Understand **extension pages with strict csp still allow css injection for data exfiltration (text-node leaking via animation/keyframe timing)**
- Understand **to get extension source: download crx from chrome web store url, or find in `<profile>/extensions/<id>/` after installing**
- Understand **for debugging: enable "search in anonymous and content scripts" in devtools preferences, remove content scripts from ignore list**

#### 3. Core concepts explained
**MetaMask Clickjacking (120K Bug)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Extension Page History.Back Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Isolated world → main world bridge hijack**
- Injected scripts (running in main page world) communicate with content script via postMessage/custom events. Since main world is attacker-controlled, any message can be forged.

**CSS injection in extension pages**
- Manifest V3 CSP only restricts scripts (`script-src: self`), not styles. HTML injection + CSS injection = data exfiltration from extension pages.

**`web_accessible_resources` → redirect → clickjack**
- Find WAR page that accepts URL params for redirect, chain to non-WAR sensitive page.


#### 4. Techniques and tactics
**Isolated world → main world bridge hijack**
- **What it is:** Injected scripts (running in main page world) communicate with content script via postMessage/custom events. Since main world is attacker-controlled, any message can be forged.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CSS injection in extension pages**
- **What it is:** Manifest V3 CSP only restricts scripts (`script-src: self`), not styles. HTML injection + CSS injection = data exfiltration from extension pages.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`web_accessible_resources` → redirect → clickjack**
- **What it is:** Find WAR page that accepts URL params for redirect, chain to non-WAR sensitive page.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Chrome extension debugging**
- **What it is:** DevTools → Sources → Content Scripts picker; `about:inspect` → Service Workers for service worker debugging; Extension ID from `chrome://extensions` with developer mode
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Extensions are super flexible and pretty locked down by default. You have to look at how they bent the extension for their features."* — **MatanBer**
- *"The CSP default for Manifest V3 is `script-src: self; object-src: self`"* — **no eval. But there's no restriction on styles." — MatanBer**
- *"If an extension has externally_connectable, `chrome.runtime` API is exposed on those origins"* — **you can connect directly to the service worker." — MatanBer**

#### 6. Mental models
- **Extensions are super flexible and pretty locked down by defa** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The CSP default for Manifest V3 is `script-src: self; object** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If an extension has externally_connectable, `chrome.runtime`** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Check `externally_connectable` in manifest.json — if present, `chrome.runtime` API is exposed on those origins → direct service worker access
- **Try this:** Content scripts share DOM but not JS environment with the page — but custom events and postMessage are still attackable
- **Try this:** Extension pages with strict CSP still allow CSS injection for data exfiltration (text-node leaking via animation/keyframe timing)
- **Try this:** To get extension source: download CRX from Chrome Web Store URL, or find in `<profile>/Extensions/<id>/` after installing

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Requires user to visit extension page first (not common but possible via right-click → options)

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in MetaMask Clickjacking (120K Bug)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Manifest V3 extension structure: content script (isolated world), injected scrip**
2. **Check `externally_connectable` in manifest.json — if present, `chrome.runtime` A**
3. **Content scripts share DOM but not JS environment with the page — but custom even**
