---
title: ".NET Remoting, CDN Attack Surface, and Recon vs Main App"
episode: 64
---


# Episode 64 .NET Remoting, CDN Attack Surface, and Recon vs Main App

**Guests:** Justin Gardner, Joel Margolis
**Format:** Show notes with timestamps (feed)
**Topics:** .NET remoting objref leak, DomPurify bypass, Cloudflare /cdn-cgi/ endpoint, JavaScript deobfuscation, renniepak's tweet, Naffy's tweet

### TL;DR
- Code White released .NET remoting objref leak research — use `__RequestVerb` header (Soroush's 2019 research) to cause a stack trace that leaks the object reference URL → full RCE via .NET HTTP remoting
- DomPurify bypass via XML processing instructions (`<?xml?>`) — when DOM Purify processes element nodes, processing instructions are not handled, allowing SVG context escape → XSS
- Cloudflare `/cdn-cgi/` endpoint is on every CF-protected site — contains image transformation, trace, JS detection endpoints — Masato Kinugawa found a CSP bypass there in 2017 using `data-cfemail` attribute
- XSS Doctor published a JS deobfuscation writeup for the common string-array-obfuscation pattern

### Key Takeaways
- For .NET remoting over HTTP: you need the object reference URL which is normally random/unguessable — leak it via `__RequestVerb: POST` header causing an error stack trace dump
- Code White's GitHub repo `HttpRemotingObjRefLeak` contains a Python script for automated objref leaking and payload delivery — sub-100 lines
- DomPurify processing instructions (`<?xml ?>`, `<??`) bypass: SVG + processing instruction = escape SVG context → HTML
- Cloudflare `/cdn-cgi/` image endpoint has `onerror=redirect` parameter → 307 redirect to any subdomain — useful for SSRF and CSRF chains
- JS deobfuscation: XSS Doctor's script decodes the common string-array + shift-decrypt pattern

### Bugs and Findings

#### .NET Remoting HTTP Object Reference Leak
- **Root cause:** `__RequestVerb` header (arbitrary header injection) overrides the HTTP verb in IIS pipeline → mismatch causes error stack trace → leaks the .NET remoting object reference URL
- **CVE:** Published by Microsoft January 2024, CVE assigned March 2024
- **Exploitation steps:**
  1. Send HTTP request to known .NET remoting endpoint with `__RequestVerb: POST` header
  2. Server returns error with stack trace containing object reference URL
  3. Use leaked URL to call remote methods on the server
  4. Invoke dangerous deserialization/instantiation → RCE
- **Impact:** Pre-auth RCE on any server with HTTP .NET remoting exposed
- **Key resources:** Code White's blog + GitHub repo

#### DomPurify Bypass via Processing Instructions
- **Root cause:** DOM Purify's handling of element nodes vs processing instructions — XML processing instructions (`<?target ?>`) are not properly sanitized when in SVG/MathML context
- **Exploitation:** `<svg><?xml?><img src=x onerror=alert(1)>` → processing instruction gets transformed to comment, remaining HTML escapes SVG context → XSS
- **Bypass of initial fix:** Custom element handling config also allowed similar bypass via custom tag names

### Tooling and Resources
- Code White: `github.com/codewhitesec/HttpRemotingObjRefLeak`
- Cloudflare `/cdn-cgi/` endpoint documentation
- XSS Doctor's JS deobfuscation writeup (Medium)
- `mitmproxy` — Python-based intercepting proxy

### Suggestions and Advices
- **Justin:** "When Shubz tweets something, you listen." / "Older research doesn't mean out of date — 5-year-old bugs still apply."
- **Joel:** Audit engineering blogs for infrastructure diagrams — they reveal architecture, routing, and proxy layers
- For CDN-CGI: enumerate all files under `/cdn-cgi/` using BigQuery HTTP Archive — look for JS files with loose CSP, subdomain-only redirect gadgets
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Code White released .NET remoting objref leak research — use `__RequestVerb` header (Soroush's 2019 research) to cause a stack trace that leaks the object reference URL → full RCE via .NET HTTP remoting

#### 2. What you should learn
- Understand **for .net remoting over http: you need the object reference url which is normally random/unguessable — leak it via `__requestverb: post` header causing an error stack trace dump**
- Understand **code white's github repo `httpremotingobjrefleak` contains a python script for automated objref leaking and payload delivery — sub-100 lines**
- Understand **dompurify processing instructions (`<?xml ?>`, `<??`) bypass: svg + processing instruction = escape svg context → html**
- Understand **cloudflare `/cdn-cgi/` image endpoint has `onerror=redirect` parameter → 307 redirect to any subdomain — useful for ssrf and csrf chains**
- Understand **js deobfuscation: xss doctor's script decodes the common string-array + shift-decrypt pattern**

#### 3. Core concepts explained
**.NET Remoting HTTP Object Reference Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**DomPurify Bypass via Processing Instructions**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Justin: "When Shubz tweets something, you listen." / "Older research doesn't mean out of date"* — **5-year-old bugs still apply.**
- *"Joel: Audit engineering blogs for infrastructure diagrams"* — **they reveal architecture, routing, and proxy layers**
- *"For CDN-CGI: enumerate all files under `/cdn-cgi/` using BigQuery HTTP Archive"* — **look for JS files with loose CSP, subdomain-only redirect gadgets**

#### 6. Mental models
- **Justin: "When Shubz tweets something, you listen." / "Older ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: Audit engineering blogs for infrastructure diagrams — ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For CDN-CGI: enumerate all files under `/cdn-cgi/` using Big** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** For .NET remoting over HTTP: you need the object reference URL which is normally random/unguessable — leak it via `__RequestVerb: POST` header causing an error stack trace dump
- **Try this:** Code White's GitHub repo `HttpRemotingObjRefLeak` contains a Python script for automated objref leaking and payload delivery — sub-100 lines
- **Try this:** DomPurify processing instructions (`<?xml ?>`, `<??`) bypass: SVG + processing instruction = escape SVG context → HTML
- **Try this:** Cloudflare `/cdn-cgi/` image endpoint has `onerror=redirect` parameter → 307 redirect to any subdomain — useful for SSRF and CSRF chains

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in .NET Remoting HTTP Object Reference Leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Code White released .NET remoting objref leak research — use `__RequestVerb` hea**
2. **For .NET remoting over HTTP: you need the object reference URL which is normally**
3. **Code White's GitHub repo `HttpRemotingObjRefLeak` contains a Python script for a**
