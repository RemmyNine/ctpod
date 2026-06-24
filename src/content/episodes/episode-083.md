---
title: "Brainstorming Proxy Plugins"
episode: 83
---


# Episode 83 Brainstorming Proxy Plugins

**TL;DR**
- New HTML entities discovered: `&bsol;` = backslash; can be used in OAuth redirect validation bypass
- HackerOne leaderboard now separates BB programs from VDPs by default
- 403 bypasser: should be customized per hacker (everyone has their own tricks) — Kaido workflows make this easy
- Espanso-like text expander for HTTP proxies: Expaido plugin for Kaido
- Trace cookies: map where cookies are set, updated, and accessed

**Key Takeaways**
- `&bsol;` (backslash) HTML entity can bypass redirect URI validators — combine with `&NegativeMediumSpace;` to create protocol-relative URLs
- This works in OAuth `response_type=form_post` flows — the form's `action` attribute decodes the entity after validation
- Standard 403 bypass extensions test ~8 techniques; your custom methodology (e.g., URL encoding parts of the path, path traversal variants) is what makes you unique — build it into an automated workflow
- "Expaido" plugin for Kaido: highlight text, hit keybind, name it, then type `~name` anywhere in Kaido to paste it back
- Cookie domain leak: if a site sets a cookie with `Domain=backend.site-dev.com`, that internal hostname is now leaked — useful for vhost/SSRF recon

**Techniques and Primitives**
- **HTML entity redirect bypass** — Use `&bsol;&NegativeMediumSpace;` to create a backslash + space that bypasses relative-URL-only checks but decodes to a valid protocol-relative URL
- **Event listener breakpoints for page redirect prevention** — DevTools → Sources → Event Listener Breakpoints → `beforeunload` stops redirects from destroying debugging state
- **Cookie domain leak** — Monitor `Set-Cookie` headers for `Domain` attributes pointing to internal/development hostnames

**Tooling and Resources**
- `en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references` — HTML entity reference table
- `espanso.org` — Text expander
- `portswigger.net/bappstore/8ef2db1173e8432c8797831c2e730727` — OAuth Scan Burp plugin
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 83 Brainstorming Proxy Plugins covers practical bug bounty techniques and security research insights.

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
