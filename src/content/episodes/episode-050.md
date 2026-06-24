---
title: "Mathias 'Fall in a well' Karlsson — Bug Bounty Prophet"
episode: 50
---


# Episode 50 Mathias 'Fall in a well' Karlsson — Bug Bounty Prophet

### TL;DR
- Interview with Mathias Karlsson (avlid) — Detectify co-founder, AssetNote contributor
- Burnout, World of Warcraft, and returning to bounty after years off (zero dupes in ~100 bugs)
- Automation with simple Python + Postgres; headless browser screenshots -> audit DNS/network logs for subdomain takeovers
- hackaplaneten.se tool: 16 HTML/XML parsers to test for Mutation XSS
- Character encoding bugs: byte order marks, multi-byte encoding confusion for WAF bypass

### Key takeaways
- Never let go of your data: store everything, grep it later when a new vulnerability class emerges
- Collaboration + specialization: become expert in one technology, distribute findings across collaborators' programs
- If you do headless browser screenshots anyway, audit the DNS/network logs — may find external resource requests to take-overable domains
- MXSS (Mutation XSS): browser's "fix bad markup" feature can turn non-exploitable input into XSS
- Encoding bugs: byte order mark (`0xFE 0xFF`) can switch encoding mid-string; some parsers accept non-standard placements

### Bugs and Findings
#### DynamoDB Injection (CTF challenge -> production)
- **Target/context:** Applications using AWS DynamoDB
- **Technique:** Research on DynamoDB query injection via malicious expressions
- Mathias built a CTF challenge, then found the same pattern in a real program weeks later

#### XSLT + Character Encoding File Read Bypass
- **Target/context:** Application accepting XML and XSLT
- **Root cause:** The XSLT parser didn't allow null bytes in output (blocking `/proc/self/environ` read)
- **Technique:**
  1. Specify encoding as UTF-16 when reading the file
  2. Null bytes become non-null multi-byte characters (e.g., Chinese characters)
  3. Transform the garbled result back to the original
- **Key technical details:** `unparsed-text()` function with encoding parameter; null bytes in UTF-16 become valid character pairs

### Techniques and Primitives
- **Headless browser DNS/network log auditing** — while taking screenshots, capture all external resource requests; check each for subdomain takeover
- **MXSS via html parsers (hackaplaneten.se)** — submit HTML through 16 different server-side parsers to see which normalize it differently
- **Byte order mark injection** — `0xFE 0xFF` at start of string tells parser to switch encoding; some parsers accept it mid-stream
- **Host header port injection for SSRF** — `Host: example.com:80@attacker.com` — some servers accept this and route to attacker

### Tooling and Resources
- **hackaplaneten.se** — MXSS testing tool (open source, Docker-based)
- **BountyDash** — (with Frans) report statistics dashboard

### Suggestions and Advices from Hunter
- "I like simple code. The less complex it is, the more beautiful it is"
- On publishing research: "It's a good challenge to get your secrets out there — then you need to find new ones"
- "One of the best ways to learn is to be wrong. Trust but verify when it comes to people teaching you"
- On data retention: "Never ever let go of your data. Storage is cheap. Grep through it later."
- "Using hash (`#`) in URL path for reverse proxy: if the front-end treats it as path, and back-end treats it as fragment, you can truncate the rest of the request"

### AI Takeaway
The headless browser -> network log auditing -> subdomain takeover pipeline is deceptively simple: since you're already running headless browsers for screenshots, extracting the side-channel resource requests costs nothing but yields takeovers others miss.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Interview with Mathias Karlsson (avlid) — Detectify co-founder, AssetNote contributor

#### 2. What you should learn
- Understand **never let go of your data: store everything, grep it later when a new vulnerability class emerges**
- Understand **collaboration + specialization: become expert in one technology, distribute findings across collaborators' programs**
- Understand **if you do headless browser screenshots anyway, audit the dns/network logs — may find external resource requests to take-overable domains**
- Understand **mxss (mutation xss): browser's "fix bad markup" feature can turn non-exploitable input into xss**
- Understand **encoding bugs: byte order mark (`0xfe 0xff`) can switch encoding mid-string; some parsers accept non-standard placements**

#### 3. Core concepts explained
**DynamoDB Injection (CTF challenge -> production)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**XSLT + Character Encoding File Read Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Headless browser DNS/network log auditing**
- while taking screenshots, capture all external resource requests; check each for subdomain takeover

**MXSS via html parsers (hackaplaneten.se)**
- submit HTML through 16 different server-side parsers to see which normalize it differently

**Byte order mark injection**
- `0xFE 0xFF` at start of string tells parser to switch encoding; some parsers accept it mid-stream


#### 4. Techniques and tactics
**Headless browser DNS/network log auditing**
- **What it is:** while taking screenshots, capture all external resource requests; check each for subdomain takeover
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**MXSS via html parsers (hackaplaneten.se)**
- **What it is:** submit HTML through 16 different server-side parsers to see which normalize it differently
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Byte order mark injection**
- **What it is:** `0xFE 0xFF` at start of string tells parser to switch encoding; some parsers accept it mid-stream
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Host header port injection for SSRF**
- **What it is:** `Host: example.com:80@attacker.com` — some servers accept this and route to attacker
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"I like simple code. The less complex it is, the more beautiful it is"*
- *"On publishing research: "It's a good challenge to get your secrets out there"* — **then you need to find new ones**
- *"One of the best ways to learn is to be wrong. Trust but verify when it comes to people teaching you"*
- *"On data retention: "Never ever let go of your data. Storage is cheap. Grep through it later."*
- *"Using hash (`#`) in URL path for reverse proxy: if the front-end treats it as path, and back-end treats it as fragment, you can truncate the rest of the request"*

#### 6. Mental models
- **I like simple code. The less complex it is, the more beautif** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On publishing research: "It's a good challenge to get your s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **One of the best ways to learn is to be wrong. Trust but veri** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Never let go of your data: store everything, grep it later when a new vulnerability class emerges
- **Try this:** Collaboration + specialization: become expert in one technology, distribute findings across collaborators' programs
- **Try this:** If you do headless browser screenshots anyway, audit the DNS/network logs — may find external resource requests to take-overable domains
- **Try this:** MXSS (Mutation XSS): browser's "fix bad markup" feature can turn non-exploitable input into XSS

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **DNS** — Domain Name System — translates domain names to IP addresses
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in DynamoDB Injection (CTF challenge -> production)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Interview with Mathias Karlsson (avlid) — Detectify co-founder, AssetNote contri**
2. **Never let go of your data: store everything, grep it later when a new vulnerabil**
3. **Collaboration + specialization: become expert in one technology, distribute find**
