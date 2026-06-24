---
title: "600+ CVEs on Adobe AEM with Jim Green (GreenJam)"
episode: 176
---


# Episode 176 600+ CVEs on Adobe AEM with Jim Green (GreenJam)

### TL;DR
- AEM architecture: Author (internal) → Publisher (public) → Dispatcher (Apache HTTPD reverse proxy) → WAF
- Apache Sling selectors/suffixes in URLs: `.form`, `.listparagraphs`, `.rawcontent` — internal servlets that bypass dispatcher ACLs
- AEM's `querybuilder` servlet enumerates entire JCR database — should never be exposed publicly
- Key folder structure: `/libs` (Adobe core), `/apps` (customer code), `/etc/packages` (deployment packages), `/content` (web pages), `/content/dam` (assets)
- 600+ CVEs on AEM; the Apache Sling selector research alone resulted in $75K in bounties

### Key Takeaways
- [ ] AEM selectors like `.rawcontent`, `.listparagraphs`, `.form` can bypass dispatcher rules — use them to hit internal endpoints like `querybuilder.json`
- [ ] `querybuilder` on AEM = SQL for the JCR database — dump all content, metadata, assets in one shot
- [ ] Anonymous user is a member of the `everyone` group in AEM — if `everyone` gets permissions, unauthenticated users inherit them
- [ ] `/etc/packages` contains full customer deployment code — including plaintext DB creds and API keys
- [ ] `Content-Disposition: attachment` can be bypassed by uploading to a different path (e.g., `/uploads/custom/` vs `/uploads/`)
- [ ] Moment.js format injection: square brackets `[<script>alert(1)</script>]` in the format string = XSS

### Bugs and Findings

#### Rawcontent Selector — Stored XSS via 404 Reflection
- **Target/context:** AEM core product
- **Root cause:** `.rawcontent` selector removes JS/CSS from page but also strips HTML sanitization; reflected in default 404 page path
- **Technique:** `/path/.rawcontent.html` + non-existent path → 404 reflects path with XSS; `.savesearch` selector triggers 400 for instances with custom 404 pages
- **Key technical details:** `.rawcontent` registered for CQ pages with HTML extension; default 404 reflects the requested path
- **Impact / severity / bounty:** Stored XSS on any AEM instance; widespread (every AEM instance affected)

#### Listparagraphs Selector — Dispatcher Bypass → JCR Enumeration
- **Target/context:** AEM core product
- **Root cause:** `.listparagraphs` selector allows specifying `itemresourcetype` parameter — forwards to arbitrary resources under `/libs` that are otherwise blocked by dispatcher
- **Technique:** `/page.listparagraphs.html?itemresourcetype=/libs/cq/statistics/components/queriesresults.html&path=<xss>` → accesses internal JSP with reflected XSS
- **Key technical details:** Parameter `itemresourcetype` controls what resource is rendered; bypasses dispatcher ACLs because request appears to be for a content page
- **Impact / severity / bounty:** XSS on internal JSPs; `querybuilder` access for full JCR dump

#### Form Selector — Universal Dispatcher Bypass
- **Target/context:** AEM core product
- **Root cause:** `.form` selector has no extension limitation; processes the suffix as a separate URL to fetch and include server-side
- **Technique:** `/content/page.form.css/bin/querybuilder.json` — `.form` selector, any extension, suffix is target URL; bypasses all dispatcher path-based rules
- **Key technical details:** No extension restriction on `.form`; suffix (`/bin/querybuilder.json`) processed as internal forward; chains with other selectors (e.g., `.listparagraphs`)
- **Impact / severity / bounty:** Universal dispatcher bypass; access to `querybuilder`, internal JSPs, and arbitrary `/libs` resources

#### Content Discovery via `/content` Folder
- **Target/context:** AEM instances with weak ACLs
- **Findings:** Excel spreadsheets of employees with SSNs, plaintext usernames/passwords, IP addresses for entire architecture, confidential documents marked "strictly confidential"
- **Technique:** Use `.infinity.json` selector or `querybuilder` to recursively enumerate `/content` folder contents

#### Moment.js Format String XSS
- **Target/context:** Any app using Moment.js with user-controlled format string
- **Root cause:** Moment.js format syntax allows arbitrary text via square brackets: `[<script>alert(1)</script>]`
- **Technique:** Set format parameter to `[<script>alert(document.domain)</script>]YYYY` — square-bracketed content is inserted verbatim
- **Impact / severity / bounty:** XSS via format string injection

#### jQuery.text() / .textContent Re-encoding XSS
- **Target/context:** Any app using DOMPurify then reading value back via `.text()` or `.textContent`
- **Root cause:** `.text()` / `.textContent` returns decoded HTML entities — if that value is then inserted into DOM, escaped payloads become live
- **Technique:** `&lt;img src=x onerror=alert(1)&gt;` — DOMPurify passes it as text; `.textContent` returns `<img src=x onerror=alert(1)>` → if re-inserted to DOM, XSS fires
- **Impact / severity / bounty:** XSS bypassing DOMPurify

#### URL Constructor + javascript: URI XSS
- **Target/context:** App using `new URL(user_input)` to validate hostname, then `window.open(url)`
- **Root cause:** `new URL("javascript:alert(1)//example.com/test")` populates `hostname: "example.com"` and `pathname: "/test"`, passing validation, but `window.open()` executes the javascript: URI
- **Key technical details:** `new URL()` constructor parses javascript: URIs like regular URLs; `hostname` and `pathname` are populated
- **Impact / severity / bounty:** XSS via javascript: URI bypassing URL validation

### Techniques and Primitives
- **AEM selector chaining** — `.form` + `.listparagraphs` + `.rawcontent` etc. can be combined for multi-stage exploits
- **Dispatcher bypass via selectors** — `.form`, `.listparagraphs` bypass path-based dispatcher rules
- **JCR dumping** — `.infinity.json` / `querybuilder.json` for recursive node enumeration
- **Anonymous user in everyone group** — Unauthenticated users get all permissions assigned to `everyone`
- **CRX QuickStart install folder RCE** — Drop a zip into `crx-quickstart/install/` → auto-installed on next restart → arbitrary code execution

### Tooling and Resources
- greenjam.co.uk — Jim Green's CVEs and AEM research
- lab.ctbb.show — AEM research paper by XSSDoctor (client-side path traversal)
- Adobe Bug Bounty program — AI tier: 1.5× bounties on AI features; code CTBB063026 for 10% bonus
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
AEM architecture: Author (internal) → Publisher (public) → Dispatcher (Apache HTTPD reverse proxy) → WAF

#### 2. What you should learn
- Understand **[ ] aem selectors like `.rawcontent`, `.listparagraphs`, `.form` can bypass dispatcher rules — use them to hit internal endpoints like `querybuilder.json`**
- Understand **[ ] `querybuilder` on aem = sql for the jcr database — dump all content, metadata, assets in one shot**
- Understand **[ ] anonymous user is a member of the `everyone` group in aem — if `everyone` gets permissions, unauthenticated users inherit them**
- Understand **[ ] `/etc/packages` contains full customer deployment code — including plaintext db creds and api keys**
- Understand **[ ] `content-disposition: attachment` can be bypassed by uploading to a different path (e.g., `/uploads/custom/` vs `/uploads/`)**

#### 3. Core concepts explained
**Rawcontent Selector — Stored XSS via 404 Reflection**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Listparagraphs Selector — Dispatcher Bypass → JCR Enumeration**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Form Selector — Universal Dispatcher Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**AEM selector chaining**
- `.form` + `.listparagraphs` + `.rawcontent` etc. can be combined for multi-stage exploits

**Dispatcher bypass via selectors**
- `.form`, `.listparagraphs` bypass path-based dispatcher rules

**JCR dumping**
- `.infinity.json` / `querybuilder.json` for recursive node enumeration


#### 4. Techniques and tactics
**AEM selector chaining**
- **What it is:** `.form` + `.listparagraphs` + `.rawcontent` etc. can be combined for multi-stage exploits
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Dispatcher bypass via selectors**
- **What it is:** `.form`, `.listparagraphs` bypass path-based dispatcher rules
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**JCR dumping**
- **What it is:** `.infinity.json` / `querybuilder.json` for recursive node enumeration
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Anonymous user in everyone group**
- **What it is:** Unauthenticated users get all permissions assigned to `everyone`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CRX QuickStart install folder RCE**
- **What it is:** Drop a zip into `crx-quickstart/install/` → auto-installed on next restart → arbitrary code execution
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
- **Try this:** [ ] AEM selectors like `.rawcontent`, `.listparagraphs`, `.form` can bypass dispatcher rules — use them to hit internal endpoints like `querybuilder.json`
- **Try this:** [ ] `querybuilder` on AEM = SQL for the JCR database — dump all content, metadata, assets in one shot
- **Try this:** [ ] Anonymous user is a member of the `everyone` group in AEM — if `everyone` gets permissions, unauthenticated users inherit them
- **Try this:** [ ] `/etc/packages` contains full customer deployment code — including plaintext DB creds and API keys

#### 8. Red flags and pitfalls
- - Root cause: `.listparagraphs` selector allows specifying `itemresourcetype` parameter — forwards to arbitrary resources under `/libs` that are otherwise blocked by dispatcher

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Rawcontent Selector — Stored XSS via 404 Reflection?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **AEM architecture: Author (internal) → Publisher (public) → Dispatcher (Apache HT**
2. **[ ] AEM selectors like `.rawcontent`, `.listparagraphs`, `.form` can bypass disp**
3. **[ ] `querybuilder` on AEM = SQL for the JCR database — dump all content, metadat**
