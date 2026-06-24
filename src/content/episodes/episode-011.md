---
title: "CVSS, Web Cache Deception, and SSTI"
episode: 11
---


# Episode 11 CVSS, Web Cache Deception, and SSTI

### TL;DR
- Acropalypse vulnerability: Google Pixel screenshot cropping left original image data in truncated file; also affects Windows Snipping Tool
- NPM `request` library SSRF filter bypass: redirect from HTTPS→HTTP bypasses agent-based filters
- CVSS exploitation: use Attack Complexity:High, Privilege Required:None (via guest accounts), Scope:Changed for impactful scoring
- Web cache deception: trick caching server into caching authenticated responses via URL extension manipulation
- UUID vs numeric IDOR: threat model should be about impact, not about "UUIDs aren't enumerable"

### Key takeaways
- Acropalypse: cropped PNG/Screenshot files retain original data at end of file; can reconstruct full original image
- For SSRF: test HTTPS→HTTP redirect bypass for request filter libraries
- Web cache deception: find caching endpoints; use `?` (`%3F`) + extension (`.js`, `.css`, `.png`) or path append to cache authenticated responses
- Use random URL parameter to avoid poisoning production URLs
- For CVSS arguments: guest accounts = PR:None; blind XSS = Scope:Changed (browser vs server); UUID IDOR = Attack Complexity:High

### Bugs and Findings

#### Web Cache Deception — PII Leakage (High)
- **Target/context:** TechCrunch API endpoint
- **Root cause:** Caching server cached responses based on URL, including authenticated user data (tokens, PII)
- **Technique / how found:** Discovered API endpoint with cache-prevention parameter that could be bypassed; used parameter to poison cache with authenticated user's response
- **Exploitation steps:**
  1. Craft URL with unique cache key param to target user
  2. Victim visits URL → server caches authenticated response (with tokens)
  3. Attacker visits same URL from same data center (no auth) → receives cached response
  4. Extract token → access PII (full address, partial credit card info)
- **Key technical details:** Cache based on URL not content-type; same data center geolocation used for testing
- **Impact / severity / bounty:** High; sensitive PII exposure
- **Obstacles & how solved:** Only worked within same data center region; [inferred] bypassed by using VPN in same region

#### SSTI via Payment Notification — CVE-2020-12668 (Critical, $26k)
- **Target/context:** PayPal (disclosed)
- **Root cause:** Gin Java template engine < 2.5.4 SSTI
- **Technique / how found:** Fisher sent payment with `{{7*7}}` in memo; Justin received notification rendering the template → 49 appeared. Chained to LFI.
- **Key technical details:** Gin Java SSTI; CVE-2020-12668; arbitrary Java method invocation
- **Impact / severity / bounty:** $26,000 Critical — LFI on production server

### Techniques and Primitives
- **Web cache deception extension tricks** — `%3F` + `.js` at end of URL to trick caching server; path append with `.png`/`.css`
- **Cache safety** — always use random URL parameter to avoid poisoning production URLs
- **CVSS argument for guest accounts** — self-sign-up = PR:None (no verification = no barrier)
- **CVSS Scope:Changed** — applies to XSS (browser vs server) and any cross-component impact

### Tooling and Resources
- SSRF Sheriff (internal SSRF testing tool, by Joel at Uber)
- Project Wycheproof (Google crypto test suite)
- ZDI Pwn2Own results

### Suggestions and Advices from Hunter
- "Read the CVSS documentation to find arguments for your bugs" — Justin
- "For web cache deception, always add random URL parameters to avoid poisoning real user data" — Joel
- "If you have UUIDs in your system but I can get them via an oracle, they're not a mitigating factor" — Justin

### AI Takeaway
Web cache deception remains viable and widespread. The key indicators: `Age` header, `X-Cache: HIT`, and any cache-control headers on authenticated endpoints. Test by adding `.js`/`.css`/`.png` extensions or `?static.txt` to API URLs — if the response caches, you can steal authenticated data.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Acropalypse vulnerability: Google Pixel screenshot cropping left original image data in truncated file; also affects Windows Snipping Tool

#### 2. What you should learn
- Understand **acropalypse: cropped png/screenshot files retain original data at end of file; can reconstruct full original image**
- Understand **for ssrf: test https→http redirect bypass for request filter libraries**
- Understand **web cache deception: find caching endpoints; use `?` (`%3f`) + extension (`.js`, `.css`, `.png`) or path append to cache authenticated responses**
- Understand **use random url parameter to avoid poisoning production urls**
- Understand **for cvss arguments: guest accounts = pr:none; blind xss = scope:changed (browser vs server); uuid idor = attack complexity:high**

#### 3. Core concepts explained
**Web Cache Deception — PII Leakage (High)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SSTI via Payment Notification — CVE-2020-12668 (Critical, $26k)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Web cache deception extension tricks**
- `%3F` + `.js` at end of URL to trick caching server; path append with `.png`/`.css`

**Cache safety**
- always use random URL parameter to avoid poisoning production URLs

**CVSS argument for guest accounts**
- self-sign-up = PR:None (no verification = no barrier)


#### 4. Techniques and tactics
**Web cache deception extension tricks**
- **What it is:** `%3F` + `.js` at end of URL to trick caching server; path append with `.png`/`.css`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cache safety**
- **What it is:** always use random URL parameter to avoid poisoning production URLs
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CVSS argument for guest accounts**
- **What it is:** self-sign-up = PR:None (no verification = no barrier)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CVSS Scope:Changed**
- **What it is:** applies to XSS (browser vs server) and any cross-component impact
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Read the CVSS documentation to find arguments for your bugs"* — **Justin**
- *"For web cache deception, always add random URL parameters to avoid poisoning real user data"* — **Joel**
- *"If you have UUIDs in your system but I can get them via an oracle, they're not a mitigating factor"* — **Justin**

#### 6. Mental models
- **Read the CVSS documentation to find arguments for your bugs"** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For web cache deception, always add random URL parameters to** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you have UUIDs in your system but I can get them via an o** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Acropalypse: cropped PNG/Screenshot files retain original data at end of file; can reconstruct full original image
- **Try this:** For SSRF: test HTTPS→HTTP redirect bypass for request filter libraries
- **Try this:** Web cache deception: find caching endpoints; use `?` (`%3F`) + extension (`.js`, `.css`, `.png`) or path append to cache authenticated responses
- **Try this:** Use random URL parameter to avoid poisoning production URLs

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Only worked within same data center region; [inferred] bypassed by using VPN in same region

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **recon** — Reconnaissance — systematic discovery of target attack surface
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Web Cache Deception — PII Leakage (High)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Acropalypse vulnerability: Google Pixel screenshot cropping left original image **
2. **Acropalypse: cropped PNG/Screenshot files retain original data at end of file; c**
3. **For SSRF: test HTTPS→HTTP redirect bypass for request filter libraries**
