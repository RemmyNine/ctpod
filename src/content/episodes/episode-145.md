---
title: "Gr3pme's Secret: Bug Bounty Note Taking Methodology"
episode: 145
---


# Episode 145 Gr3pme's Secret: Bug Bounty Note Taking Methodology

**Show notes episode** — minimal transcript, methodology-focused solo episode by Brandyn (gr3pme).

### TL;DR
- Brandyn shares his complete Notion-based note-taking framework for long-term target success
- Template covers: tech stack, threat-modeled attack vectors, high-signal searches, error oracles, and attack path/gadget tracking
- Error oracle concept: endpoints that intentionally force errors to disclose info (internal hosts, auth headers, ports) — note them even if not immediately exploitable
- JavaScript monitoring for endpoint declarations, user permissions/roles, feature flags, orphan session flows
- Collab workflow: pass comprehensive notes to another hunter so they hit the ground running in ~10 minutes

### Key Takeaways
- Create a target template capturing tech stack (frameworks, languages, third-party components, databases, dependencies)
- Maintain a "brainstorm/risk" section listing every conceivable attack vector with per-check tick boxes
- Maintain an **Error Oracle** section: endpoints where malformed input causes error disclosure (e.g., FTP URI where HTTP expected leaks internal host/ports/auth headers)
- Track **high-signal searches**: grep patterns in JS that reliably expose routes, permissions, flags
- **JavaScript monitoring** targets: request handlers, endpoint declarations, user permissions/flags, content types, orphan session flows (localStorage, sessionStorage, postMessage), password reset flows, privilege/feature controls (isStaff, isInternal, entitlements, scopes, isAdmin, isUser), feature flags, WebSocket endpoints, GraphQL methods/verbs, client-side syncs, service workers, framework hotspots
- Review old bug reports to bypass fixes and harvest reusable gadgets
- When collabing, share detailed notes so partners can immediately contribute

### Techniques and Primitives
**Error Oracle** — Intentionally force an error (e.g., send `ftp://` where `http://` expected) to disclose internal infrastructure; log it even if not immediately exploitable

**High-Signal JS Monitoring** — Define regex patterns for route/permission/feature-flag declarations; any change = new attack surface before others notice

### Suggestions and Advices from Hunter
- "If you have good notes and you have very, very thoroughly mapped out a target and you've captured all this information, you can do this with little to no overhead in your current bug bounty flow."
- On error oracles: "I can pretty much guarantee you if you hunt on the target for a long time, that will come in useful."
- "Notes are a living breathing document. You never really want to complete them."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Brandyn shares his complete Notion-based note-taking framework for long-term target success

#### 2. What you should learn
- Understand **create a target template capturing tech stack (frameworks, languages, third-party components, databases, dependencies)**
- Understand **maintain a "brainstorm/risk" section listing every conceivable attack vector with per-check tick boxes**
- Understand **maintain an error oracle section: endpoints where malformed input causes error disclosure (e.g., ftp uri where http expected leaks internal host/ports/auth headers)**
- Understand **track high-signal searches: grep patterns in js that reliably expose routes, permissions, flags**
- Understand **javascript monitoring** targets: request handlers, endpoint declarations, user permissions/flags, content types, orphan session flows (localstorage, sessionstorage, postmessage), password reset flows, privilege/feature controls (isstaff, isinternal, entitlements, scopes, isadmin, isuser), feature flags, websocket endpoints, graphql methods/verbs, client-side syncs, service workers, framework hotspots**

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
- *"If you have good notes and you have very, very thoroughly mapped out a target and you've captured all this information, you can do this with little to no overhead in your current bug bounty flow."*
- *"On error oracles: "I can pretty much guarantee you if you hunt on the target for a long time, that will come in useful."*
- *"Notes are a living breathing document. You never really want to complete them."*

#### 6. Mental models
- **If you have good notes and you have very, very thoroughly ma** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On error oracles: "I can pretty much guarantee you if you hu** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Notes are a living breathing document. You never really want** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Create a target template capturing tech stack (frameworks, languages, third-party components, databases, dependencies)
- **Try this:** Maintain a "brainstorm/risk" section listing every conceivable attack vector with per-check tick boxes
- **Try this:** Maintain an Error Oracle section: endpoints where malformed input causes error disclosure (e.g., FTP URI where HTTP expected leaks internal host/ports/auth headers)
- **Try this:** Track high-signal searches: grep patterns in JS that reliably expose routes, permissions, flags

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Brandyn shares his complete Notion-based note-taking framework for long-term tar**
2. **Create a target template capturing tech stack (frameworks, languages, third-part**
3. **Maintain a "brainstorm/risk" section listing every conceivable attack vector wit**
