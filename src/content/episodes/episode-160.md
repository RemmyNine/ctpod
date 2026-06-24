---
title: "Cloudflare Zero-days & Mail Unsubscribing for XSS"
episode: 160
---


# Episode 160 Cloudflare Zero-days & Mail Unsubscribing for XSS

### TL;DR
- Cloudflare WAF bypass: `/.well-known/acme-challenge/<any-valid-token>` → path traversal → bypass all WAF rules
- `List-Unsubscribe` email header → SSRF/XSS: JavaScript URIs in header render in Horde mail backend → blind XSS
- CTBB Lab research: parser discrepancy in MIME type handling → `application/json; ,text/html` bypasses content-type checks
- Claude Magic String: Anthropic defined string that triggers guaranteed refusal — can be used for DOS

### Bugs and Findings

#### Cloudflare WAF Bypass via ACME Challenge
- **Target/context:** Cloudflare WAF
- **Root cause:** `/.well-known/acme-challenge/` requests were passed through without WAF inspection if the token matched ANY active challenge across Cloudflare's infrastructure
- **Technique / how found:** FearsOff research
- **Exploitation steps:**
  1. Get your own Cloudflare instance
  2. Generate an ACME challenge token
  3. Target: `https://victim.com/.well-known/acme-challenge/<your-token>;/../actuator/env`
  4. Request bypasses WAF entirely, hits origin server unfiltered
- **Key technical details:** Path: `/.well-known/acme-challenge/<valid-token><path-traversal>`. Any valid token across entire Cloudflare infra works
- **Impact:** Complete bypass of all customer-configured WAF rules; exposed actuator/env endpoints

#### List-Unsubscribe Header → SSRF / XSS
- **Target/context:** Email servers (Horde, Nextcloud)
- **Root cause:** `List-Unsubscribe` SMTP header supports HTTP and `mailto:` URIs; RFC allows arbitrary URI schemes; backend mail clients render these without sanitization
- **Exploitation steps:**
  1. Send email with `List-Unsubscribe: <javascript:confirm(document.domain)>`
  2. When admin views email in Horde backend portal → JS executes (stored XSS)
  3. For SSRF: `List-Unsubscribe: <http://internal-host:8080/>`
  4. Backend server makes request to internal host
- **Key technical details:** CVE-2025-68673 for Horde stored XSS; Nextcloud SSRF requires `allow_local_remote_servers=true` config
- **Impact:** Blind XSS on mail admin panels, SSRF to internal networks

#### Claude Magic String Denial of Service
- **Target/context:** Anthropic Claude
- **Key technical details:** Anthropic documented a magic string that triggers guaranteed refusal via streaming classifiers
- **Impact:** Can be injected via indirect prompt injection → every future turn refuses (sticky refusal). Register as username/email/any data that enters LLM context to selectively DOS users

### Techniques and Primitives
**Parser Discrepancy MIME Bypass** — `Content-Type: application/json; ,text/html` — some backends parse first (application/json), browsers parse last (text/html) due to different RFC interpretations of singleton vs list-based header fields. Use for XSS via content-type confusion

### Suggestions and Advices from Hunter
- Joseph on the Magic String: "It makes me want to do things like name my user that string, put my email as a plus alias... just basically get that string anywhere I can."
- Brandyn on blind XSS: "I dread to think how many blind XSS I've missed because I've had funky X-Frame-Options at some point."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Cloudflare WAF bypass: `/.well-known/acme-challenge/<any-valid-token>` → path traversal → bypass all WAF rules

#### 2. What you should learn
- Learn about **cloudflare waf bypass: `/.well-known/acme-challenge/<any-valid-token>` → path traversal → bypass all waf rules**
- Learn about **`list-unsubscribe` email header → ssrf/xss: javascript uris in header render in horde mail backend → blind xss**
- Learn about **ctbb lab research: parser discrepancy in mime type handling → `application/json; ,text/html` bypasses content-type checks**
- Learn about **claude magic string: anthropic defined string that triggers guaranteed refusal — can be used for dos**

#### 3. Core concepts explained
**Cloudflare WAF Bypass via ACME Challenge**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**List-Unsubscribe Header → SSRF / XSS**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Claude Magic String Denial of Service**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Joseph on the Magic String: "It makes me want to do things like name my user that string, put my email as a plus alias... just basically get that string anywhere I can."*
- *"Brandyn on blind XSS: "I dread to think how many blind XSS I've missed because I've had funky X-Frame-Options at some point."*

#### 6. Mental models
- **Joseph on the Magic String: "It makes me want to do things l** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Brandyn on blind XSS: "I dread to think how many blind XSS I** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Cloudflare WAF Bypass via ACME Challenge?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Cloudflare WAF bypass: `/.well-known/acme-challenge/<any-valid-token>` → path tr**
