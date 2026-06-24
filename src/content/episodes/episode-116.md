---
title: "Auth Bypasses and Google VRP Writeups"
episode: 116
---


# Episode 116 Auth Bypasses and Google VRP Writeups

### TL;DR
- SAML Roulette: Ruby-SAML double-parse attack using XML doctype `ATTLIST` to hijack signature validation
- Google VRP: Google Form/Sheet link via Apps Script `SpreadsheetApp.openById().getFormUrl()` — $7.5k
- Google VRP: Read-only doc editor list leak via `getEditors()` in Apps Script — $15k
- Google VRP: Cloud Tools for Eclipse OAuth callback to localhost:8080 + open redirect — $500
- Next.js middleware bypass: `x-middleware-subrequest: pages/_middleware` (pre-12.2) or `x-middleware-subrequest: middleware` (12.2+)

### Key Takeaways
- SAML round-trip attack: when two parsers process the same XML (reXML for validation, Nokogiri for attribute access), discrepancies between attribute quoting enable signature hijacking
- Use XML doctype `<!ATTLIST>` to override attribute values on signature elements — reXML looks for `xmlns:ds="..."` on one element, `ATTLIST` can reassign it
- Google Apps Script: even with read-only access to a Sheet/Doc, `SpreadsheetApp.openById(id).getFormUrl()` returns the linked form's URL; `getEditors()` returns full editor list
- Next.js auth bypass: just add header `x-middleware-subrequest: middleware` (or `source/middleware`, `pages/_middleware`)
- OAuth localhost redirect: if `http://localhost:8080` is allowed as redirect URI, any app on port 8080 can intercept the callback

### Bugs and Findings

#### SAML Roulette — Unauthenticated ATO in GitLab (Ruby-SAML)
- **Target/context:** GitLab via Ruby-SAML library
- **Root cause:** reXML (signature validation) and Nokogiri (attribute access) are different parsers. reXML saw single-quoted attribute; when serialized back to string, it became double-quoted — then Nokogiri parsed the modified XML.
- **Technique / how found:**
  1. Use single-quoted attribute value containing `"` — reXML parses as single-quoted, the `"` is data
  2. When reXML serializes, single quotes become double quotes — the `"` closes the attribute
  3. Use XML doctype `<!ATTLIST>` to define a new value for `xmlns:ds` on the signature element
  4. Hijack which assertion is validated; insert malicious assertion
- **Exploitation steps:**
  1. Obtain signed XML document from IdP metadata endpoint (WS-Federation provides signed metadata)
  2. Craft SAML response with single-quoted attribute containing `"`, `<!--`, entities
  3. Include `<!ATTLIST>` doctype to reassign signature namespace
  4. On second parse (Nokogiri), attribute breaks, comment/entities become active, malicious assertion inserted
- **Key technical details:** reXML validates signature, Nokogiri accesses attributes; `<!ATTLIST>` in doctype can override attribute values at parse time; WS-Federation metadata endpoint provides a signed XML; attribute can be `<!ATTLIST>` or entity `<!ENTITY>`
- **Impact / severity / bounty:** Unauthenticated account takeover in GitLab
- **Obstacles & how solved:** Needed a signed XML document — found via WS-Federation metadata endpoint; attribute manipulation via doctype

#### Google Apps Script: Read-Only to Form URL Leak
- **Target/context:** Google Forms + Sheets
- **Root cause:** `SpreadsheetApp.openById(id)` opens a spreadsheet with read-only access; `getFormUrl()` returns the associated form URL — this should only be accessible to editors
- **Technique / how found:** Get the document ID from the results spreadsheet; create a new Sheet and add an Apps Script; call `SpreadsheetApp.openById(existingSheetId).getFormUrl()` — returns the form URL
- **Key technical details:** Apps Script runs under the user's auth context; `openById` allows read-only access; `getFormUrl()` is not gated on owner/editor status
- **Impact / severity / bounty:** $7,500
- **Obstacles & how solved:** Required knowing Apps Script and the specific API method

#### Google Apps Script: Editor List Leak from Read-Only Doc
- **Target/context:** Google Docs
- **Root cause:** `getEditors()` returns full editor email list; accessible via Apps Script even with only read access
- **Technique / how found:** Same pattern: `DocumentApp.openById(docId).getEditors()` — dumps all editor email addresses
- **Key technical details:** Users with read-only access should not see editor identities; Apps Script bypasses this check
- **Impact / severity / bounty:** $15,000
- **Obstacles & how solved:** Finding the right Apps Script method

#### Cloud Tools for Eclipse — OAuth Token Leak via localhost Redirect
- **Target/context:** Google Cloud Tools for Eclipse
- **Root cause:** OAuth client allowed redirect to `http://localhost:8080`; Cloud Tools for Eclipse happened to listen on that port and had an open redirect
- **Technique / how found:**
  1. Identify OAuth client with `http://localhost:8080` as allowed redirect URI
  2. Cloud Tools for Eclipse listens on port 8080 and has an open redirector
  3. Chain: OAuth callback → localhost:8080 → open redirect → attacker's server captures the token
- **Key technical details:** Any app on localhost:8080 can receive the OAuth callback; on mobile, any app can bind to ports >1024 without permissions
- **Impact / severity / bounty:** $500
- **Obstacles & how solved:** Google argued localhost access requires device ownership; researcher chained with own product's open redirect

#### Next.js Middleware Auth Bypass
- **Target/context:** Next.js applications using middleware for auth
- **Root cause:** Internal header `x-middleware-subrequest` is used to prevent infinite middleware loops; if it contains specific strings, middleware is skipped entirely
- **Technique / how found:** Just add header: `x-middleware-subrequest: pages/_middleware` (pre-12.2) or `x-middleware-subrequest: middleware` (12.2+), or `x-middleware-subrequest: source/middleware`
- **Key technical details:** 
  - Pre-12.2: value = `pages/_middleware`
  - 12.2+: value = `middleware` (or `src/middleware` if in /src)
  - The check is deep in Next.js source code; the header completely bypasses all middleware including auth
- **Impact / severity / bounty:** Auth bypass, CSP bypass, DoS via cache poisoning
- **Obstacles & how solved:** Found via source code review of Next.js

### Techniques and Primitives
- **SAML doctype attribute override** — `<!ATTLIST ds:Signature xmlns:ds CDATA "http://www.w3.org/2000/09/xmldsig#">` can override signature resolution
- **WS-Federation metadata for signed XML** — IdP's WS-Federation endpoint provides signed metadata; reuse the signature for SAML attacks
- **Google Apps Script gadget chain** — `openById()` + `getFormUrl()` / `getEditors()` — works with read-only access
- **Next.js middleware bypass** — header `x-middleware-subrequest: middleware` skips all middleware
- **OAuth localhost redirect abuse** — Any port >1024 on mobile is bindable by any app; chain with open redirect on that port

### Tooling and Resources
- Portswigger Research: SAML Roulette
- zhero-web-sec.github.io: Next.js cache and chains
- Google VRP disclosed reports

### Suggestions and Advices from Hunter
- "SAML libraries often parse an XML document as a string and then later reparse it — differentials between two parsers = vulnerabilities"
- "What data can be stored in a child element or in an attribute in XML — they're interchangeable"
- "For mobile OAuth callbacks: any app can bind to port >1024 without extra permissions"

### AI Takeaway
The SAML round-trip attack technique (single-quote attribute → double-quote serialization → doctype ATTLIST override) is highly creative. The Next.js middleware bypass is extremely exploitable in bug bounty — spray `x-middleware-subrequest: middleware` at every Next.js site with 403'd endpoints.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
SAML Roulette: Ruby-SAML double-parse attack using XML doctype `ATTLIST` to hijack signature validation

#### 2. What you should learn
- Understand **saml round-trip attack: when two parsers process the same xml (rexml for validation, nokogiri for attribute access), discrepancies between attribute quoting enable signature hijacking**
- Understand **use xml doctype `<!attlist>` to override attribute values on signature elements — rexml looks for `xmlns:ds="..."` on one element, `attlist` can reassign it**
- Understand **google apps script: even with read-only access to a sheet/doc, `spreadsheetapp.openbyid(id).getformurl()` returns the linked form's url; `geteditors()` returns full editor list**
- Understand **next.js auth bypass: just add header `x-middleware-subrequest: middleware` (or `source/middleware`, `pages/_middleware`)**
- Understand **oauth localhost redirect: if `http://localhost:8080` is allowed as redirect uri, any app on port 8080 can intercept the callback**

#### 3. Core concepts explained
**SAML Roulette — Unauthenticated ATO in GitLab (Ruby-SAML)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Google Apps Script: Read-Only to Form URL Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Google Apps Script: Editor List Leak from Read-Only Doc**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SAML doctype attribute override**
- `<!ATTLIST ds:Signature xmlns:ds CDATA "http://www.w3.org/2000/09/xmldsig#">` can override signature resolution

**WS-Federation metadata for signed XML**
- IdP's WS-Federation endpoint provides signed metadata; reuse the signature for SAML attacks

**Google Apps Script gadget chain**
- `openById()` + `getFormUrl()` / `getEditors()` — works with read-only access


#### 4. Techniques and tactics
**SAML doctype attribute override**
- **What it is:** `<!ATTLIST ds:Signature xmlns:ds CDATA "http://www.w3.org/2000/09/xmldsig#">` can override signature resolution
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WS-Federation metadata for signed XML**
- **What it is:** IdP's WS-Federation endpoint provides signed metadata; reuse the signature for SAML attacks
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Google Apps Script gadget chain**
- **What it is:** `openById()` + `getFormUrl()` / `getEditors()` — works with read-only access
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Next.js middleware bypass**
- **What it is:** header `x-middleware-subrequest: middleware` skips all middleware
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**OAuth localhost redirect abuse**
- **What it is:** Any port >1024 on mobile is bindable by any app; chain with open redirect on that port
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"SAML libraries often parse an XML document as a string and then later reparse it"* — **differentials between two parsers = vulnerabilities**
- *"What data can be stored in a child element or in an attribute in XML"* — **they're interchangeable**
- *"For mobile OAuth callbacks: any app can bind to port >1024 without extra permissions"*

#### 6. Mental models
- **SAML libraries often parse an XML document as a string and t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **What data can be stored in a child element or in an attribut** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For mobile OAuth callbacks: any app can bind to port >1024 w** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** SAML round-trip attack: when two parsers process the same XML (reXML for validation, Nokogiri for attribute access), discrepancies between attribute quoting enable signature hijacking
- **Try this:** Use XML doctype `<!ATTLIST>` to override attribute values on signature elements — reXML looks for `xmlns:ds="..."` on one element, `ATTLIST` can reassign it
- **Try this:** Google Apps Script: even with read-only access to a Sheet/Doc, `SpreadsheetApp.openById(id).getFormUrl()` returns the linked form's URL; `getEditors()` returns full editor list
- **Try this:** Next.js auth bypass: just add header `x-middleware-subrequest: middleware` (or `source/middleware`, `pages/_middleware`)

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Needed a signed XML document — found via WS-Federation metadata endpoint; attribute manipulation via doctype
- - Obstacles & how solved: Required knowing Apps Script and the specific API method

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in SAML Roulette — Unauthenticated ATO in GitLab (Ruby-SAML)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **SAML Roulette: Ruby-SAML double-parse attack using XML doctype `ATTLIST` to hija**
2. **SAML round-trip attack: when two parsers process the same XML (reXML for validat**
3. **Use XML doctype `<!ATTLIST>` to override attribute values on signature elements **
