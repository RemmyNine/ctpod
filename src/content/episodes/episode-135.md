---
title: "Akamai's Ryan Barnett on WAFs, Unicode Confusables, and Triage Stories"
episode: 135
---


# Episode 135 Akamai's Ryan Barnett on WAFs, Unicode Confusables, and Triage Stories

**Source:** Show notes (feed) — condensed.

### TL;DR
- Ryan Barnett on WAF challenges, sources vs sinks world.
- TypePad accidental stored XSS via analytics scraping rendered content.
- Chat widget backscatter: attacker traffic leaks to Akamai customer telemetry.
- Two org types: vulnerability enumeration (let us through) vs attacker simulation (prove bypass).
- Unicode normalization: Burp Decoder not multibyte-aware (Mojibake).

### Key takeaways
- [ ] Use images of exploit code, not text — APIs/AI agents scrape and re-serve without encoding.
- [ ] Third-party chat/analytics beacon full URIs to provider — attacker payloads leak into telemetry.
- [ ] WAF = sources world; hackers = sinks world.
- [ ] Unicode normalization: Burp Decoder not multibyte-aware — use Decoder Improved.
- [ ] AWS API Gateway / Fireprox against ToS — use alternatives like Linode with Axiom.

### Bugs and Findings

#### TypePad Accidental Stored XSS — Stored XSS
- **Root cause:** Zemanta plugin scraped RENDERED blog content (not raw HTML-entity-encoded text) and injected as HTML.
- **Impact:** Stored XSS across platform.

### Techniques and Primitives
- **HTML entity encoding bypass via scraping** — Rendered content is decoded.
- **WAF bypass by context confusion** — `%22` decoded in one context, not another.
- **TLS fingerprint for whitelisting** — Unique JA3 + custom field for researcher ID.
- **Mojibake** — Encoding corruption → wrong security decisions.

### Tooling and Resources
- SonarSource UTF-8 visualizer
- "XSS Street-Fight" (Ryan Barnett, BlackHat 2011)
- "Lost in Translation: Exploiting Unicode Normalization" (BlackHat 2025)

### Suggestions and Advices from Hunter
- "WAFs live in a sources world; hackers live in a sinks world."
- "Use images of exploit code, not text — you don't know what will scrape your content."
- "If you prove a WAF bypass, customer bumps priority."
- "The browser is the ultimate decoding problem."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Ryan Barnett on WAF challenges, sources vs sinks world.

#### 2. What you should learn
- Understand **[ ] use images of exploit code, not text — apis/ai agents scrape and re-serve without encoding**
- Understand **[ ] third-party chat/analytics beacon full uris to provider — attacker payloads leak into telemetry**
- Understand **[ ] waf = sources world; hackers = sinks world**
- Understand **[ ] unicode normalization: burp decoder not multibyte-aware — use decoder improved**
- Understand **[ ] aws api gateway / fireprox against tos — use alternatives like linode with axiom**

#### 3. Core concepts explained
**TypePad Accidental Stored XSS — Stored XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**HTML entity encoding bypass via scraping**
- Rendered content is decoded.

**WAF bypass by context confusion**
- `%22` decoded in one context, not another.

**TLS fingerprint for whitelisting**
- Unique JA3 + custom field for researcher ID.


#### 4. Techniques and tactics
**HTML entity encoding bypass via scraping**
- **What it is:** Rendered content is decoded.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WAF bypass by context confusion**
- **What it is:** `%22` decoded in one context, not another.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**TLS fingerprint for whitelisting**
- **What it is:** Unique JA3 + custom field for researcher ID.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Mojibake**
- **What it is:** Encoding corruption → wrong security decisions.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"WAFs live in a sources world; hackers live in a sinks world."*
- *"Use images of exploit code, not text"* — **you don't know what will scrape your content.**
- *"If you prove a WAF bypass, customer bumps priority."*
- *"The browser is the ultimate decoding problem."*

#### 6. Mental models
- **WAFs live in a sources world; hackers live in a sinks world.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use images of exploit code, not text — you don't know what w** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you prove a WAF bypass, customer bumps priority.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Use images of exploit code, not text — APIs/AI agents scrape and re-serve without encoding.
- **Try this:** [ ] Third-party chat/analytics beacon full URIs to provider — attacker payloads leak into telemetry.
- **Try this:** [ ] WAF = sources world; hackers = sinks world.
- **Try this:** [ ] Unicode normalization: Burp Decoder not multibyte-aware — use Decoder Improved.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **Burp** — Burp Suite — popular web application security testing proxy
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in TypePad Accidental Stored XSS — Stored XSS?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Ryan Barnett on WAF challenges, sources vs sinks world.**
2. **[ ] Use images of exploit code, not text — APIs/AI agents scrape and re-serve wi**
3. **[ ] Third-party chat/analytics beacon full URIs to provider — attacker payloads **
