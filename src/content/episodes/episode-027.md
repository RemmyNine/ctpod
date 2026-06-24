---
title: "Top 7 Esoteric Web Vulnerabilities"
episode: 27
---


# Episode 27 Top 7 Esoteric Web Vulnerabilities

**Guests/Hosts:** Justin Gardner, Joel Margolis  
**Date:** 2023-07-13 | **Duration:** 1:20:16

### TL;DR
- Seven esoteric vulnerability classes that aren't mainstream but yield high-impact bugs
- Config file injection, client-side path traversal, cookie bombing, cookie jar overflow, cross-site leaks, UNC path leaks, impactful link hijacking
- AssetNote's ShareFile RCE writeup: AES padding oracle + unsanitized upload ID → file write → RCE
- BitQuark's ShortScan tool for IIS 8.3 short name enumeration
- Orange's Google Search Appliance RCE via firmware dumping from old Google Groups

### Key Takeaways
- Config file injection: escape the templated config block (e.g., DNSMasq, dhcpd, nginx, Apache); add `TFTP` to DNSMasq config for arbitrary file read via port 69
- Client-side path traversal: control a path in the browser that gets loaded as a resource (CSS, JS, fetch) — can lead to CSS injection or XSS
- Cookie bombing: set many large cookies to bloat HTTP headers → request fails (<=400); useful for DoS or forcing error states in OAuth flows to leak tokens
- Cookie jar overflow: set >180 cookies (Chrome limit) to evict HTTP-only cookies without knowing their names
- Cross-site leaks (XS-Leaks): frame counting, history.length, PDF postMessage to infer user state cross-origin
- UNC path injection: on Windows, inject `\\attacker.com\share` into file paths; the client sends NTLMv2 hash which can be cracked offline

### Bugs and Findings

#### Citrix ShareFile RCE via AES padding oracle — RCE
- **Target/context:** Citrix ShareFile (enterprise file sharing)
- **Root cause:** The `uploadID` parameter is not sanitized before concatenation with a path. The `parentID` parameter is AES-encrypted but not verified for validity — only decrypted; if AES decryption succeeds (valid PKCS7 padding), the value is accepted.
- **Technique / how found:** Source code review after dumping ShareFile binaries. Dylan Pinder (AssetNote) traced cookie handling → found `SetCurrentPrincipalFromSessionCookie` skips if no cookie → auth bypass. Then traced path building: path is sanitized, `uploadID` is not → path traversal.
- **Exploitation steps:**
  1. Brute-force a valid AES `parentID` (~128–256 attempts to find valid PKCS7 padding)
  2. Use path traversal via unsanitized `uploadID` to write a file to an arbitrary location
  3. Write an ASPX webshell → RCE on the IIS server
- **Key technical details:** `uploadID` concatenated into file path; `parentID` only checked for valid AES decryption (not for correctness) | PKCS7 padding: if 1 byte needed, last byte = `0x01`; if 2, last two = `0x02 0x02`, etc.
- **Impact / severity / bounty:** Pre-auth RCE; critical

#### Nginx alias traversal — Path traversal
- **Target/context:** Any nginx config with `location` + `alias`
- **Root cause:** If `location` has no trailing slash and `alias` has a trailing slash, the concatenation can traverse up one directory level.
- **Technique / how found:** "Hunting for nginx alias traversals in the wild" — Hawkeye Labs; used GitHub code search for vulnerable patterns
- **Exploitation steps:**
  1. Find `location /foo { alias /bar/; }` (location no slash, alias with slash)
  2. Request `/foo../` → nginx resolves to `/bar` (up one level from `/bar/`)
- **Key technical details:** Vulnerable pattern: `location` without trailing `/`, `alias` with trailing `/` | Only one directory level traversal
- **Impact / severity / bounty:** Directory listing / file read; Bitwarden self-hosted database leaked — max bounty

#### IIS Short Name Enumeration — Information disclosure
- **Target/context:** IIS servers with 8.3 short name generation enabled
- **Root cause:** IIS reveals the first 6 characters of file/folder names and first 3 of extensions via tilde (`~`) enumeration
- **Technique / how found:** BitQuark's `shortscan` (Go tool using new techniques)
- **Key technical details:** Works on most IIS versions | `~1` → first 6 chars of name + ~ + first 3 of extension
- **Impact / severity / bounty:** Enables discovery of hidden file names (`.config.bak`, etc.) for further exploitation

### Techniques and Primitives
- **Config file injection** — Identify apps that write user input into configuration files via templates; escape the block using language-native comments/control chars; inject directives for DNSMasq (TFTP), dhcpd, nginx, Apache
- **Client-side path traversal** — Inject `../` into a query/hash parameter that gets loaded as a resource URL (CSS/JS); combine with open redirect for CSS injection → data exfiltration
- **Cookie jar overflow** — Via JS, set many cookies until the browser's per-domain limit (~180 in Chrome) is reached; oldest cookies (including HttpOnly) get evicted
- **XS-Leak via frame counting** — `window.open(target)`, then check `window.frames.length` cross-origin; if the page has an iframe (e.g., search results), the length differs vs no results
- **XS-Leak via PDF postMessage** — Opening a PDF in Chrome creates a postMessage interface even cross-origin; detect if a URL returns PDF vs non-PDF

### Tooling and Resources
- BitQuark's `shortscan` (GitHub) — Go-based IIS short name scanner
- `XS-Leaks.dev` — comprehensive resource on cross-site leak techniques
- `checkcookiejaroverflow.html` — runnerator.dev tool to test browser cookie limit
- HackTricks — esoteric web technique documentation
- `Responder` — tool to capture NTLMv2 hashes from UNC path leaks

### Suggestions and Advices from Hunter
- "When you see the IIS blue page, thank God. It's the easiest web server to hack." — Shubs (referenced)
- Joel: "For cookie bombing, you don't need to know the cookie name. Just set >180 cookies and the oldest ones (including HttpOnly) get removed."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Seven esoteric vulnerability classes that aren't mainstream but yield high-impact bugs

#### 2. What you should learn
- Understand **config file injection: escape the templated config block (e.g., dnsmasq, dhcpd, nginx, apache); add `tftp` to dnsmasq config for arbitrary file read via port 69**
- Understand **client-side path traversal: control a path in the browser that gets loaded as a resource (css, js, fetch) — can lead to css injection or xss**
- Understand **cookie bombing: set many large cookies to bloat http headers → request fails (<=400); useful for dos or forcing error states in oauth flows to leak tokens**
- Understand **cookie jar overflow: set >180 cookies (chrome limit) to evict http-only cookies without knowing their names**
- Understand **cross-site leaks (xs-leaks): frame counting, history.length, pdf postmessage to infer user state cross-origin**

#### 3. Core concepts explained
**Citrix ShareFile RCE via AES padding oracle — RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Nginx alias traversal — Path traversal**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**IIS Short Name Enumeration — Information disclosure**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Config file injection**
- Identify apps that write user input into configuration files via templates; escape the block using language-native comments/control chars; inject directives for DNSMasq (TFTP), dhcpd, nginx, Apache

**Client-side path traversal**
- Inject `../` into a query/hash parameter that gets loaded as a resource URL (CSS/JS); combine with open redirect for CSS injection → data exfiltration

**Cookie jar overflow**
- Via JS, set many cookies until the browser's per-domain limit (~180 in Chrome) is reached; oldest cookies (including HttpOnly) get evicted


#### 4. Techniques and tactics
**Config file injection**
- **What it is:** Identify apps that write user input into configuration files via templates; escape the block using language-native comments/control chars; inject directives for DNSMasq (TFTP), dhcpd, nginx, Apache
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Client-side path traversal**
- **What it is:** Inject `../` into a query/hash parameter that gets loaded as a resource URL (CSS/JS); combine with open redirect for CSS injection → data exfiltration
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cookie jar overflow**
- **What it is:** Via JS, set many cookies until the browser's per-domain limit (~180 in Chrome) is reached; oldest cookies (including HttpOnly) get evicted
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**XS-Leak via frame counting**
- **What it is:** `window.open(target)`, then check `window.frames.length` cross-origin; if the page has an iframe (e.g., search results), the length differs vs no results
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**XS-Leak via PDF postMessage**
- **What it is:** Opening a PDF in Chrome creates a postMessage interface even cross-origin; detect if a URL returns PDF vs non-PDF
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When you see the IIS blue page, thank God. It's the easiest web server to hack."* — **Shubs (referenced)**
- *"Joel: "For cookie bombing, you don't need to know the cookie name. Just set >180 cookies and the oldest ones (including HttpOnly) get removed."*

#### 6. Mental models
- **When you see the IIS blue page, thank God. It's the easiest ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: "For cookie bombing, you don't need to know the cookie** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Config file injection: escape the templated config block (e.g., DNSMasq, dhcpd, nginx, Apache); add `TFTP` to DNSMasq config for arbitrary file read via port 69
- **Try this:** Client-side path traversal: control a path in the browser that gets loaded as a resource (CSS, JS, fetch) — can lead to CSS injection or XSS
- **Try this:** Cookie bombing: set many large cookies to bloat HTTP headers → request fails (<=400); useful for DoS or forcing error states in OAuth flows to leak tokens
- **Try this:** Cookie jar overflow: set >180 cookies (Chrome limit) to evict HTTP-only cookies without knowing their names

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **DNS** — Domain Name System — translates domain names to IP addresses
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Citrix ShareFile RCE via AES padding oracle — RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Seven esoteric vulnerability classes that aren't mainstream but yield high-impac**
2. **Config file injection: escape the templated config block (e.g., DNSMasq, dhcpd, **
3. **Client-side path traversal: control a path in the browser that gets loaded as a **
