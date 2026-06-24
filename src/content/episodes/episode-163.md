---
title: "Best Technical Takeaways from Portswigger Top 10 2025"
episode: 163
---


# Episode 163 Best Technical Takeaways from Portswigger Top 10 2025

### TL;DR
- Parser differentials across different tech stacks (JS vs Erlang, JS vs Java)
- HTTP/2 CONNECT verb enables SSRF/port scanning against internal hosts
- Next.js internal cache poisoning via `__nextDataRequest` query param — framework-level root cause
- ORM filter injection (password leak via `password__startswith`) — widespread across frameworks
- Boolean error-based SSTI using division-by-zero payloads as detection oracle

### Key Takeaways
- [ ] When you see duplicate headers (e.g., two `Authorization` headers), check if frontend and backend parsers disagree — first vs last wins differential
- [ ] Audit any YAML processing for parser differentials: `!!binary` tags, Merge (`<<`), confusable booleans
- [ ] For Next.js or any SSR framework, audit internal caching mechanisms, not just CDN — check if query params are part of cache key
- [ ] Scan for ORM filter injection by testing `__` suffix patterns: `email__startswith`, `password__gt` — logical operators enable binary search exfiltration
- [ ] Test SSTI with `(1/0).zxy.zxy` — universal error-based detection polyglot

### Bugs and Findings

#### Parser Differential — Multi-role Bypass
- **Target/context:** App using JS frontend parser and Erlang (or Java) backend parser
- **Root cause:** JS JSON parser takes the last duplicate key; Java/Erlang takes the first
- **Technique:** Send `{"role":["admin"],"role":[]}` — JS sees empty array (safe), backend sees admin
- **Exploitation steps:** 1) Identify JSON endpoint with role/permission field 2) Supply duplicate keys with first being privileged 3) Frontend validates on second key 4) Backend uses first key
- **Key technical details:** Duplicate key in JSON; frontend reads last, backend reads first
- **Impact / severity / bounty:** Auth bypass, privilege escalation

#### Double Authorization Header Smuggling
- **Target/context:** Application with JWT middleware
- **Root cause:** Frontend middleware checks second `Authorization` header (legit JWT); backend uses first `Authorization` header (forged, algorithm none)
- **Technique:** Supply two `Authorization` headers — first is a forged JWT with `"alg":"none"` containing desired claims; second is a legit low-priv JWT
- **Exploitation steps:** 1) Craft a JWT with `alg: none` containing elevated claims 2) Send as first `Authorization` header 3) Include a legitimate JWT as second `Authorization` header 4) Frontend validates the legit one; backend accepts the forged one
- **Impact / severity / bounty:** Full account takeover / privilege escalation

#### Parser Differential — YAML `!!binary` Tag Confusion
- **Target/context:** Any YAML-processing pipeline (CI/CD, config, etc.)
- **Root cause:** YAML `!!binary` tag triggers base64 decoding; parser differential between environments on whether tag is resolved before or after key merging
- **Technique:** Define a key like `lang: Python` then `!!binary bGFuZw==: <value>` — the binary-decoded key may override `lang` depending on tag resolution order
- **Key technical details:** `!!binary` tag base64-encodes arbitrary binary data; usable in keys or values
- **Impact / severity / bounty:** Config injection, parser differential exploitation

#### HTTP/2 CONNECT SSRF/Port Scanner
- **Target/context:** Any server supporting HTTP/2 CONNECT
- **Root cause:** HTTP/2 CONNECT allows multiplexed tunnels to arbitrary IP:port; successful connection returns 200, failure returns 503
- **Technique:** Send HTTP/2 CONNECT frames to arbitrary internal IP:port — 200 vs 503 tells you if port is open
- **Exploitation steps:** 1) Check if target supports HTTP/2 CONNECT 2) Send CONNECT requests to internal IPs:ports 3) Read status frames — 200 = open, 503 = closed
- **Key technical details:** HTTP/2 CONNECT uses binary frames with stream identifiers; multiplexing allows simultaneous tunnels; can also write raw HTTP/1.1 requests through the tunnel
- **Impact / severity / bounty:** Full internal network scan via SSRF, potential MITM/proxy abuse

#### Next.js Internal Cache Poisoning (Zero's Research)
- **Target/context:** Next.js framework (version-dependent)
- **Root cause:** `__nextDataRequest=1` query param marks request as a data request; internal cache key excludes this query param; `X-Now-Route-Matches` header controls response caching behavior; JSON response rendered with `text/html` content type
- **Technique:** 1) Send request with `__nextDataRequest=1` + `X-Now-Route-Matches: <controlled-value>` 2) Response is JSON cached and served as HTML to subsequent visitors 3) User Agent (or other reflected data) in JSON becomes stored XSS when served as text/html
- **Key technical details:** `__nextDataRequest` query param; `X-Now-Route-Matches` header; internal cache key does NOT include query params; `Accept-Encoding` is in cache key (used as non-destructive test vector — browsers always send it, attackers omit it); data requests return JSON but content type is text/html
- **Impact / severity / bounty:** Six-figure sum in bounties; stored XSS, full-site DoS via cache poisoning

**Obstacles & how solved:** Zero used `Accept-Encoding` header as a cache buster — normal browsers always send it, so poisoning the cache without it doesn't affect real users. This enabled safe scanning.

#### Cross-Site ETag Length Leak
- **Target/context:** Web app where response length varies based on secret data
- **Root cause:** ETag header reflects hex-encoded content length; a 1-byte difference in response size creates a 1-byte difference in ETag; browser sends ETag back as `If-None-Match` header; overflowing `If-None-Match` past the 16KB Node.js limit triggers a 431 error; Chrome replaces navigation history entry on 431 (no history length change)
- **Technique:** 1) Use CSRF to create notes that push response size to just below Node.js 16KB limit 2) Cross-site search includes the secret in the URL 3) If secret pushes total request header size over 16KB, 431 is returned 4) Chrome 431 = no history length change (sink)
- **Key technical details:** Node.js 431 maximum request size = ~16KB; ETag -> `If-None-Match` reflection cycle; Chrome's 431 handling replaces current navigation (no history length increase)
- **Impact / severity / bounty:** Cross-site information leak; binary oracle for secret extraction

#### SOAPwn — .NET Framework RCE via HTTP Client Proxy + WSDL
- **Target/context:** .NET applications using `WebClient` protocol for SOAP messages
- **Root cause:** `as` operator cast on URI: file:// or \\ UNC paths cast to `FileWebRequest` instead of `HttpWebRequest`; cast returns null, null-check only skips HTTP-specific setup but continues processing; file URIs write XML to disk, UNC paths trigger NTLM auth
- **Technique:** Supply a `file://` URI instead of `http://` → XML written to disk as `.cshtml` or `.aspx` = instant webshell; supply `\\attacker\share` → server sends NTLM hash
- **Key technical details:** `as` operator (not a hard cast); `FileWebRequest` vs `HttpWebRequest`; CSHTML/ASPX auto-execution; UNC path forces NTLM challenge-response
- **Impact / severity / bounty:** Arbitrary file write → RCE; NTLM credential theft

#### Novel SSRF Technique — Blind to Full Read via Redirect Chain
- **Target/context:** Application with blind SSRF that parses JSON responses
- **Root cause:** Application follows multiple redirects with incrementing status codes (301→302→303→...→310); at 305+ status codes, JSON parsing fails differently and the server returns full response data including all intermediate redirect response headers; the final redirect to cloud metadata endpoint works
- **Technique:** 1) Craft redirect chain starting at 301 incrementing to 310 2) Final redirect hits `http://169.254.169.254/latest/meta-data/iam/security-credentials/` 3) Responses from 305 onward are returned in full, including AWS metadata
- **Key technical details:** Only status codes ≥305 returned; libcurl handles ≤5 redirects normally, but application error state for >5 redirects returns raw data; technique worked across multiple targets
- **Impact / severity / bounty:** Blind SSRF escalated to full read SSRF; AWS credential access

#### Error-Based SSTI — getattr Payload
- **Target/context:** Python template engines (Jinja2, etc.)
- **Root cause:** `getattr(obj, controlled_string)` returns the attribute value; if it's non-callable, error message includes the attribute name (which is the exfiltrated data)
- **Technique:** Use `getattr(self, secret_value)` to leak data into error message; no limit on data length (unlike integer conversion truncation at ~199 chars)
- **Key technical details:** `getattr()` truncation-free; division-by-zero detection polyglot: `(1/0).zxy.zxy` works cross-language; Python-specific: `().__class__.__base__.__subclasses__()`
- **Impact / severity / bounty:** Full data exfiltration via error messages (when verbose errors enabled)

#### Boolean Error-Based Blind SSTI
- **Target/context:** Template engines with error suppression (only 500 returned)
- **Root cause:** Division by zero expression: `1/(controlled_expression)` — if expression evaluates to 0, server returns 500; if non-zero, normal response
- **Technique:** 1) Detect with syntax error payloads causing 500 2) For exfiltration: `1/(ord(secret[index]) - ascii_value)` — when guess matches, denominator is 0 → 500; otherwise normal
- **Key technical details:** Boolean oracle via division-by-zero; generic detection payloads exploit syntax errors in parentheses placement
- **Impact / severity / bounty:** Blind data exfiltration over Boolean oracle

### Techniques and Primitives
- **Duplicate header smuggling** — Send two `Authorization` headers: frontend checks one, backend uses the other
- **ETag → If-None-Match reflection chain** — Response header reflected into next request's header; overflow → 431 → cross-site leak via history length
- **YAML `!!binary` tag abuse** — Base64-encode arbitrary YAML keys/values to create parser differentials
- **ORM `__` operator injection** — `email__startswith`, `password__gt`, etc.; bypass filters with `[` bracket notation: `resetToken[__not]=E`
- **Division-by-zero SSTI oracle** — `(1/0).zxy.zxy` triggers error universally; Boolean variant for blind
- **Internal cache poisoning via framework-level caching** — Target framework's own cache (Next.js, etc.), not just CDN
- **Multiple redirect status code chain escalation** — Increment status codes (301→310) to break JSON parsing and get full response data from blind SSRF

### Tooling and Resources
- SSTIMAP — Vladko312's SSTI exploitation tool
- Protoscope — binary Protobuf decode/encode CLI tool
- Portswigger Research Top 10 2025
- Jorchen's OffensiveCon 25 talk on parser differentials
- blog.flomb.net — HTTP/2 CONNECT research
- zhero-web-sec.github.io — Next.js cache poisoning
- watchtowr.com — SOAPwn whitepaper
- blog.arkark.dev — ETag length leak
- elttam.com — Unicode normalization/ORM leaks
- slcyber.io — SSRF redirect loop technique
- github.com/vladko312/Research_Successful_Errors
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Parser differentials across different tech stacks (JS vs Erlang, JS vs Java)

#### 2. What you should learn
- Understand **[ ] when you see duplicate headers (e.g., two `authorization` headers), check if frontend and backend parsers disagree — first vs last wins differential**
- Understand **[ ] audit any yaml processing for parser differentials: `!!binary` tags, merge (`<<`), confusable booleans**
- Understand **[ ] for next.js or any ssr framework, audit internal caching mechanisms, not just cdn — check if query params are part of cache key**
- Understand **[ ] scan for orm filter injection by testing `__` suffix patterns: `email__startswith`, `password__gt` — logical operators enable binary search exfiltration**
- Understand **[ ] test ssti with `(1/0).zxy.zxy` — universal error-based detection polyglot**

#### 3. Core concepts explained
**Parser Differential — Multi-role Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Double Authorization Header Smuggling**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Parser Differential — YAML `!!binary` Tag Confusion**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Duplicate header smuggling**
- Send two `Authorization` headers: frontend checks one, backend uses the other

**ETag → If-None-Match reflection chain**
- Response header reflected into next request's header; overflow → 431 → cross-site leak via history length

**YAML `!!binary` tag abuse**
- Base64-encode arbitrary YAML keys/values to create parser differentials


#### 4. Techniques and tactics
**Duplicate header smuggling**
- **What it is:** Send two `Authorization` headers: frontend checks one, backend uses the other
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**ETag → If-None-Match reflection chain**
- **What it is:** Response header reflected into next request's header; overflow → 431 → cross-site leak via history length
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**YAML `!!binary` tag abuse**
- **What it is:** Base64-encode arbitrary YAML keys/values to create parser differentials
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**ORM `__` operator injection**
- **What it is:** `email__startswith`, `password__gt`, etc.; bypass filters with `[` bracket notation: `resetToken[__not]=E`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Division-by-zero SSTI oracle**
- **What it is:** `(1/0).zxy.zxy` triggers error universally; Boolean variant for blind
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** [ ] When you see duplicate headers (e.g., two `Authorization` headers), check if frontend and backend parsers disagree — first vs last wins differential
- **Try this:** [ ] Audit any YAML processing for parser differentials: `!!binary` tags, Merge (`<<`), confusable booleans
- **Try this:** [ ] For Next.js or any SSR framework, audit internal caching mechanisms, not just CDN — check if query params are part of cache key
- **Try this:** [ ] Scan for ORM filter injection by testing `__` suffix patterns: `email__startswith`, `password__gt` — logical operators enable binary search exfiltration

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **ACL** — Access Control List — permissions defining who can access what
- **SSTI** — Server-Side Template Injection — injecting template syntax that executes on server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Parser Differential — Multi-role Bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Parser differentials across different tech stacks (JS vs Erlang, JS vs Java)**
2. **[ ] When you see duplicate headers (e.g., two `Authorization` headers), check if**
3. **[ ] Audit any YAML processing for parser differentials: `!!binary` tags, Merge (**
