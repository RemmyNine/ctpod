---
title: "New Cohost + Client-Side Gadgets, LHE Meta — Instant Global Admin in Entra!"
episode: 143
---


# Episode 143 New Cohost + Client-Side Gadgets, LHE Meta — Instant Global Admin in Entra!

**Source:** Show notes (feed) — condensed.

### TL;DR
- Brandyn announced as 3rd co-host.
- LHE strategy: volume in ONE app → deep bugs after dupe window.
- WAF bypass: internal employees resolve without WAF.
- `attributes[0].value` + `URL` = char-restricted XSS.
- Entra ID "One Token to Rule Them All": signed actor in unsigned JWT.
- FlareProx: Cloudflare-based proxy rotation.

### Key takeaways
- [ ] LHE: focus volume on ONE app; deep bugs after dupe window.
- [ ] WAF bypass via internal DNS: employees → no WAF → deliver through business logic.
- [ ] React: `onfocus=attributes[0].value` → `URL` = documentURI → backtick template with hash payload.
- [ ] Microsoft Entra: signed actor token in unsigned JWT → impersonate ANY user cross-tenant.
- [ ] Google SafeContentFrame: bulletproof HTML sandbox (hash subdomain + PSL).

### Bugs and Findings

#### Microsoft Entra Actor Token — Global admin ATO
- **Root cause:** Signed actor token wrapped in unsigned JWT. Resource provider reads claims from UNSIGNED wrapper.
- **Key details:**
  - Actor token = signed, `trustedfordelegation: true`, 24h valid.
  - Wrapper = unsigned, `upn` claim controls impersonation.
  - No logs. No revocation. Bypasses conditional access.
- **Exploitation:**
  1. Get valid actor token from own tenant.
  2. Craft unsigned wrapper with target UPN.
  3. Send to resource provider → full impersonation.
  4. List Global Admins → impersonate them.
- **Impact:** Instant Global Admin in ANY Entra tenant.

### Techniques and Primitives
- **`attributes[0].value` XSS** — `onfocus=attributes[0].value` → backtick + URL.
- **Internal DNS WAF bypass** — Employees → no WAF.
- **Secondary context RBAC bypass** — Front-end validates org ID; backend path traversal bypasses.
- **Unsigned JWT with signed inner token** — Server reads outer, not inner.

### Suggestions and Advices from Hunter
- "One megacrit seals an event."
- "If you get XSS, work backwards from it."
- "Hackers are going to hack — ToS be damned."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Brandyn announced as 3rd co-host.

#### 2. What you should learn
- Understand **[ ] lhe: focus volume on one app; deep bugs after dupe window**
- Understand **[ ] waf bypass via internal dns: employees → no waf → deliver through business logic**
- Understand **[ ] react: `onfocus=attributes[0].value` → `url` = documenturi → backtick template with hash payload**
- Understand **[ ] microsoft entra: signed actor token in unsigned jwt → impersonate any user cross-tenant**
- Understand **[ ] google safecontentframe: bulletproof html sandbox (hash subdomain + psl)**

#### 3. Core concepts explained
**Microsoft Entra Actor Token — Global admin ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**`attributes[0].value` XSS**
- `onfocus=attributes[0].value` → backtick + URL.

**Internal DNS WAF bypass**
- Employees → no WAF.

**Secondary context RBAC bypass**
- Front-end validates org ID; backend path traversal bypasses.


#### 4. Techniques and tactics
**`attributes[0].value` XSS**
- **What it is:** `onfocus=attributes[0].value` → backtick + URL.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Internal DNS WAF bypass**
- **What it is:** Employees → no WAF.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Secondary context RBAC bypass**
- **What it is:** Front-end validates org ID; backend path traversal bypasses.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Unsigned JWT with signed inner token**
- **What it is:** Server reads outer, not inner.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"One megacrit seals an event."*
- *"If you get XSS, work backwards from it."*
- *"Hackers are going to hack"* — **ToS be damned.**

#### 6. Mental models
- **One megacrit seals an event.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you get XSS, work backwards from it.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Hackers are going to hack — ToS be damned.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] LHE: focus volume on ONE app; deep bugs after dupe window.
- **Try this:** [ ] WAF bypass via internal DNS: employees → no WAF → deliver through business logic.
- **Try this:** [ ] React: `onfocus=attributes[0].value` → `URL` = documentURI → backtick template with hash payload.
- **Try this:** [ ] Microsoft Entra: signed actor token in unsigned JWT → impersonate ANY user cross-tenant.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **JWT** — JSON Web Token — compact token format for authentication
- **DNS** — Domain Name System — translates domain names to IP addresses
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Microsoft Entra Actor Token — Global admin ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Brandyn announced as 3rd co-host.**
2. **[ ] LHE: focus volume on ONE app; deep bugs after dupe window.**
3. **[ ] WAF bypass via internal DNS: employees → no WAF → deliver through business l**
