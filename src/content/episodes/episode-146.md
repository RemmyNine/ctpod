---
title: "Hacking Horror Stories"
episode: 146
---


# Episode 146 Hacking Horror Stories

### TL;DR
- Halloween special — three hosts share scariest bug stories
- Brandyn: SSRF → discovered private Firefox browser extension for remote internal network access with full auth token leakage
- Joseph: web.zip at Yahoo LHE — 8-12GB source code dump from broken load balancer, 1-in-12 requests returned plaintext PHP
- Justin: IoT tabletop device (Amazon Echo-like) — SIP protocol exploitation → zero-click call pickup with camera/mic access
- Brandyn (second story): Open Banking payment field injection → account takeover via crafted international payment with extended character set (40-47 chars)

### Bugs and Findings

#### SSRF → Private Browser Extension Token Leakage — Info Disclosure / Network Access
- **Target/context:** [undisclosed] company with IoT/devices
- **Root cause:** Company had a private Firefox extension for employee remote access to internal apps; extension was published publicly on Firefox store
- **Technique / how found:** Recon for SSRF on a non-standard attack surface; got callbacks with a custom header from two callback servers — only one reproduced it. Investigated browser extensions (Chrome → nothing → Firefox → found private extension)
- **Exploitation steps:**
  1. Set up SSRF callback and observed custom auth header being appended
  2. Noticed only one callback server (with company subdomain) triggered the header
  3. Found the private Firefox extension via Google dorking for "internal only" extensions
  4. Reversed extension source code — header was the main auth token for remote network access
  5. Extension matcher matched the subdomain pattern, so it thought SSRF server was an internal company host
- **Key technical details:** Custom auth header; extension was publicly listed on Firefox store but private/internal-only; header contained exotic certificate authority
- **Impact:** Full internal network access as an employee
- **Obstacles & how solved:** Couldn't reproduce on one callback server because that server's domain didn't match the extension's matcher pattern; solved by checking the matcher and using a domain that satisfied it

#### Yahoo LHE Source Code Leak via Web.zip — Information Disclosure
- **Target/context:** Yahoo live hacking event
- **Root cause:** Broken load balancer — round-robin intermittently returned plaintext PHP files instead of executing them
- **Technique / how found:** Fuzzing with ffuf; saw a green hit with unusual response size (multi-GB). Couldn't access consistently — only ~1-in-12 requests hit the misconfigured backend
- **Exploitation steps:**
  1. ffuf found a web.zip endpoint with huge response size
  2. Re-fuzzed with random hash to re-hit the same request pattern
  3. Eventually downloaded the zip (~8-12 GB) after discovering the 1-in-12 load balancer quirk
  4. Extracted paths from the archive; all paths existed on the live host
  5. PHP files on the broken load balancer returned plaintext source; on normal load balancers they executed
  6. Used plaintext PHP to extract hardcoded credentials and SQL injection
- **Key technical details:** ffuf with random suffix to bypass load balancer caching; 1-in-12 probability of hitting the misconfigured backend; 8-12 GB source code dump
- **Impact:** Full source code access, hardcoded credentials, multiple SQL injections; $20K max payout + police stop on the host
- **Obstacles & how solved:** Inconsistent access (1-in-12); solved by repeatedly sending identical requests

#### IoT Tabletop Device Zero-Click SIP Exploit — RCE / ATO
- **Target/context:** Major consumer IoT tabletop device (camera/mic/speaker)
- **Root cause:** SIP auth token generation accepted injection characters; FROM field could be overwritten via parameter injection in the token-generation HTTP request
- **Technique / how found:** Decompiled mobile app, bypassed root detection + cert pinning on both HTTP and SIP (SIPs). Proxied SIP through PolarProxy, analyzed in Wireshark. Used Frida to turn mobile app into SIP repeater
- **Exploitation steps:**
  1. Decompile mobile app, bypass root detection and cert pinning
  2. Proxy SIP through PolarProxy → Wireshark to understand flow
  3. Write Frida script to act as SIP repeater
  4. HTTP request generates SIP auth token; inject `>` and `;` into the FROM field parameter
  5. Overwrite FROM field to make call appear as if from victim to themselves
  6. When calling yourself, device auto-picks up ("drop-in" feature) — zero user interaction
- **Key technical details:** SIP protocol over SIPS with cert pinning; `>` and `;` injection into auth token generation; binary patched FROM → FRAM to remove original header; PolarProxy for TLS inspection; Frida for mobile app hooking
- **Impact:** Zero-click audio/video surveillance of any device; phone number only required
- **Obstacles & how solved:** SIP cert pinning, binary loading of native .so files preventing Frida hooks, could not remove original FROM header via Java — binary-patched `from` to `fram` to bypass

#### Open Banking Payment Injection → Bank Account Takeover — ATO via XSS
- **Target/context:** Major fintech / bank
- **Root cause:** Discrepancies in Open Banking API spec implementation; extended character set in international payment fields (40-47 chars vs local transfer restrictions); description field had 32K character limit
- **Technique / how found:** Researched Open Banking API standard, identified field length discrepancies between local and international payments, tested malformed data in payment fields
- **Exploitation steps:**
  1. Identified extended character field in international payments (40-47 chars)
  2. Injected XSS payload in payment reference/description field
  3. Sent £0.01 (or minimal amount) to target
  4. When target opened payment details, XSS fired → account takeover
- **Key technical details:** International payment fields allow 40-47 characters (vs local ~18); Open Banking API standard discrepancies; code golfed CSP bypass payload within character limit
- **Impact:** Full bank account takeover via micropayment; attack vector from publicly available company information
- **Obstacles & how solved:** 17-character restriction for local transfers; solved by using international payment fields; code golfing XSS payload for CSP bypass; fraud team investigations required program coordination

### Techniques and Primitives
**Public Browser Extension Enumeration** — Google dork for "internal only" extensions on Firefox/Chrome stores to find hidden attack surface; companies often publish private-use extensions publicly

**SIP Repeater via Frida** — Turn mobile app into SIP protocol repeater by hooking native .so functions with Frida; use PolarProxy for TLS inspection

**Open Banking Field Discrepancies** — International payment fields often have different (larger) character limits than domestic transfers; test the same field across different payment types

### Suggestions and Advices from Hunter
- Joseph on the Yahoo find: "It's one of those situations where it's like, maybe I don't tell them that I found a web zip and just report all the bugs."
- Justin on SIP exploitation: "As a network engineer, you probably understand my pain on that one. It is not nice."
- Brandyn on the bank bug: "There's a lot of discrepancies. International payments, you can use around 40 or 47 characters... whereas if it's a local bank transfer you're much more restricted."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Halloween special — three hosts share scariest bug stories

#### 2. What you should learn
- Learn about **halloween special — three hosts share scariest bug stories**
- Learn about **brandyn: ssrf → discovered private firefox browser extension for remote internal network access with full auth token leakage**
- Learn about **joseph: web.zip at yahoo lhe — 8-12gb source code dump from broken load balancer, 1-in-12 requests returned plaintext php**
- Learn about **justin: iot tabletop device (amazon echo-like) — sip protocol exploitation → zero-click call pickup with camera/mic access**
- Learn about **brandyn (second story): open banking payment field injection → account takeover via crafted international payment with extended character set (40-47 chars)**

#### 3. Core concepts explained
**SSRF → Private Browser Extension Token Leakage — Info Disclosure / Network Access**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Yahoo LHE Source Code Leak via Web.zip — Information Disclosure**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**IoT Tabletop Device Zero-Click SIP Exploit — RCE / ATO**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Joseph on the Yahoo find: "It's one of those situations where it's like, maybe I don't tell them that I found a web zip and just report all the bugs."*
- *"Justin on SIP exploitation: "As a network engineer, you probably understand my pain on that one. It is not nice."*
- *"Brandyn on the bank bug: "There's a lot of discrepancies. International payments, you can use around 40 or 47 characters... whereas if it's a local bank transfer you're much more restricted."*

#### 6. Mental models
- **Joseph on the Yahoo find: "It's one of those situations wher** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Justin on SIP exploitation: "As a network engineer, you prob** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Brandyn on the bank bug: "There's a lot of discrepancies. In** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Couldn't reproduce on one callback server because that server's domain didn't match the extension's matcher pattern; solved by checking the matcher and using a domain that satisfied it
- - Obstacles & how solved: Inconsistent access (1-in-12); solved by repeatedly sending identical requests

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in SSRF → Private Browser Extension Token Leakage — Info Disclosure / Network Access?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Halloween special — three hosts share scariest bug stories**
