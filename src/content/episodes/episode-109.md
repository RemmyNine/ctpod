---
title: "Creative Recon - Alternative Techniques"
episode: 109
---


# Episode 109 Creative Recon - Alternative Techniques

### TL;DR
- DeepSeek exposed ClickHouse database found via nmap scan — dev DB wide open on the internet
- Cookie Sandwich attack: `$Version=1` cookie triggers legacy RFC parsing in Apache Tomcat, enabling double-quote encapsulation of HttpOnly cookies
- Clone2Leak: Git credential protocol vs ECMAScript line-terminator mismatch (U+2028, U+2029) leaks credentials
- Cache geolocation deanonymization for Signal/Discord via CDN edge behavior
- Alternative recon: URL scan for JS references, GitHub code search for subdomains/tokens

### Key Takeaways
- When you find a dev database open to the internet (ClickHouse, etc.), query it — even "just telemetry" can contain training data, user records, or secrets
- Test cookie parsing with `$Version=1` (capital V) to force legacy RFC parsing; then use double-quote encapsulation (`param1="value1; sessionid=secret; param2=value"`) to encapsulate HttpOnly cookies
- Remember Unicode code points U+2028 (line separator) and U+2029 (paragraph separator) — ECMAScript regex multiline treats these as line terminators, most protocols don't
- For recon: search target subdomains on urlscan.io, GitHub code search, and Shodan — not just passive DNS
- Investigate what pages reference your target in JS files; cloud resources often only appear in JS references

### Bugs and Findings

#### DeepSeek Exposed ClickHouse Database — Information Disclosure
- **Target/context:** DeepSeek dev environment at dev.deepseek.com
- **Root cause:** No network segmentation — dev database exposed to internet
- **Technique / how found:** Nmap scan on host showed 50+ open ports including ClickHouse (port 5140, 8002, 80040, 80041, etc.)
- **Key technical details:** ClickHouse DB wide open, no auth; ports included 443, 1090, 1091, 2053, 2087, 2096, 5140, 8002, 80040, 80041
- **Impact / severity / bounty:** [inferred] Critical data exposure — telemetry, potentially training data or user PII
- **Obstacles & how solved:** Company presumed dev server was internal; attacker simply scanned and found open ports

#### Cookie Sandwich Attack — HttpOnly Cookie Theft via Legacy Parsing
- **Target/context:** Apache Tomcat and other servers with legacy cookie compatibility mode
- **Root cause:** Servers switch to legacy RFC parsing when receiving `$Version=1` (capital V) cookie; legacy mode allows double-quote quoting, enabling cookie encapsulation
- **Technique / how found:** Set `$Version=1` cookie to trigger legacy parsing; then use `param1="value; sessionid=secret; param2="` — browser sees three cookies, server sees one quoted value encapsulating the HttpOnly cookie
- **Exploitation steps:**
  1. Obtain XSS on a subdomain or cookie-setting surface
  2. Use cookie jar ordering (path specificity) to bump attacker's cookie to front
  3. Set `$Version=1` cookie to force legacy parsing mode
  4. Craft `param1="<value>; <HttpOnly-session-cookie>; param2="` to encapsulate
  5. Server reflects the encapsulated cookie (via the quoted attribute) allowing JS exfiltration
- **Key technical details:** `$Version=1` with capital V triggers legacy mode; double quotes encapsulate across semicolons; path specificity controls cookie ordering
- **Impact / severity / bounty:** HttpOnly session theft — bypasses HttpOnly flag
- **Obstacles & how solved:** Attacker needs XSS on subdomain to set cookies; cookie jar overflow can evict victim cookies

#### Clone2Leak — Git Credentials Belong To Us
- **Target/context:** Git credential protocol, affecting CLI, Git Desktop, Codespaces
- **Root cause:** ECMAScript regex multiline (`/m` flag) recognizes U+2028 and U+2029 as line terminators; Git credential protocol only expects `\n` as terminator — mismatch allows injection
- **Technique / how found:** Source code review of multiple Git implementations; crafted `.gitattributes` or repo files with U+2028/U+2029 to break out of credential helper parsing
- **Key technical details:** Unicode U+2028 (Line Separator), U+2029 (Paragraph Separator) — ECMAScript multiline regex treats these as line terminators; most other parsers do not. Similar issues with .NET StreamReader, C, Go implementations.
- **Impact / severity / bounty:** 6 CVEs on Git-related products; credentials leaked when cloning a malicious repo
- **Obstacles & how solved:** Needed deep understanding of each parser's newline semantics

### Techniques and Primitives
- **Unicode line-terminator smuggling** — U+2028, U+2029 in ECMAScript multiline regex are line terminators; protocols not expecting this treat them as data. Test every parser boundary.
- **Cookie legacy-mode triggering** — `$Version=1` (capital V) forces RFC 2109/2965 legacy parsing; enables double-quote cookie encapsulation
- **URL scan recon** — Search target subdomain on urlscan.io to find which pages reference it in JS/HTML (Natalie's technique)
- **Cache-geolocation de-anonymization** — CDN cache servers can reveal approximate location; use multiple edge nodes to triangulate

### Tooling and Resources
- nmap, ClickHouse client
- `urlscan.io`, GitHub code search
- Portswigger Bypass Bot Detection BAP (emulates browser TLS fingerprints in Burp)
- `rsc/2fa` — command-line 2FA tool with Espanso integration (`:otp`)

### Suggestions and Advices from Hunter
- "Just search the subdomain in quotes on GitHub — sometimes people put their recon data there"
- "Pay attention to what pages reference your target in their JavaScript files — that's how Natalie landed that token"
- "When you see a cookie with a prefix like `__Host-`, you can't set it via JS — look for server-side mechanisms"

### AI Takeaway
The Unicode line-terminator smuggling (U+2028/U+2029) is a high-leverage primitive for any parser boundary — not just Git. Test it in HTTP headers, cookie values, serialization formats.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
DeepSeek exposed ClickHouse database found via nmap scan — dev DB wide open on the internet

#### 2. What you should learn
- Understand **when you find a dev database open to the internet (clickhouse, etc.), query it — even "just telemetry" can contain training data, user records, or secrets**
- Understand **test cookie parsing with `$version=1` (capital v) to force legacy rfc parsing; then use double-quote encapsulation (`param1="value1; sessionid=secret; param2=value"`) to encapsulate httponly cookies**
- Understand **remember unicode code points u+2028 (line separator) and u+2029 (paragraph separator) — ecmascript regex multiline treats these as line terminators, most protocols don't**
- Understand **for recon: search target subdomains on urlscan.io, github code search, and shodan — not just passive dns**
- Understand **investigate what pages reference your target in js files; cloud resources often only appear in js references**

#### 3. Core concepts explained
**DeepSeek Exposed ClickHouse Database — Information Disclosure**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Cookie Sandwich Attack — HttpOnly Cookie Theft via Legacy Parsing**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Clone2Leak — Git Credentials Belong To Us**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Unicode line-terminator smuggling**
- U+2028, U+2029 in ECMAScript multiline regex are line terminators; protocols not expecting this treat them as data. Test every parser boundary.

**Cookie legacy-mode triggering**
- `$Version=1` (capital V) forces RFC 2109/2965 legacy parsing; enables double-quote cookie encapsulation

**URL scan recon**
- Search target subdomain on urlscan.io to find which pages reference it in JS/HTML (Natalie's technique)


#### 4. Techniques and tactics
**Unicode line-terminator smuggling**
- **What it is:** U+2028, U+2029 in ECMAScript multiline regex are line terminators; protocols not expecting this treat them as data. Test every parser boundary.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cookie legacy-mode triggering**
- **What it is:** `$Version=1` (capital V) forces RFC 2109/2965 legacy parsing; enables double-quote cookie encapsulation
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**URL scan recon**
- **What it is:** Search target subdomain on urlscan.io to find which pages reference it in JS/HTML (Natalie's technique)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cache-geolocation de-anonymization**
- **What it is:** CDN cache servers can reveal approximate location; use multiple edge nodes to triangulate
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Just search the subdomain in quotes on GitHub"* — **sometimes people put their recon data there**
- *"Pay attention to what pages reference your target in their JavaScript files"* — **that's how Natalie landed that token**
- *"When you see a cookie with a prefix like `__Host-`, you can't set it via JS"* — **look for server-side mechanisms**

#### 6. Mental models
- **Just search the subdomain in quotes on GitHub — sometimes pe** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Pay attention to what pages reference your target in their J** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **When you see a cookie with a prefix like `__Host-`, you can'** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** When you find a dev database open to the internet (ClickHouse, etc.), query it — even "just telemetry" can contain training data, user records, or secrets
- **Try this:** Test cookie parsing with `$Version=1` (capital V) to force legacy RFC parsing; then use double-quote encapsulation (`param1="value1; sessionid=secret; param2=value"`) to encapsulate HttpOnly cookies
- **Try this:** Remember Unicode code points U+2028 (line separator) and U+2029 (paragraph separator) — ECMAScript regex multiline treats these as line terminators, most protocols don't
- **Try this:** For recon: search target subdomains on urlscan.io, GitHub code search, and Shodan — not just passive DNS

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Company presumed dev server was internal; attacker simply scanned and found open ports
- - Obstacles & how solved: Attacker needs XSS on subdomain to set cookies; cookie jar overflow can evict victim cookies

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **DNS** — Domain Name System — translates domain names to IP addresses
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in DeepSeek Exposed ClickHouse Database — Information Disclosure?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **DeepSeek exposed ClickHouse database found via nmap scan — dev DB wide open on t**
2. **When you find a dev database open to the internet (ClickHouse, etc.), query it —**
3. **Test cookie parsing with `$Version=1` (capital V) to force legacy RFC parsing; t**
