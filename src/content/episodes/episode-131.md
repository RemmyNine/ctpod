---
title: "SL Cyber Writeups, Bug Bounty Metastrategy, and Orphaned Github Commits"
episode: 131
---


# Episode 131 SL Cyber Writeups, Bug Bounty Metastrategy, and Orphaned Github Commits

**Source:** Full ASR transcript.

### TL;DR
- GCP Metadata SSRF bypasses: extra slash, HTTP/0.9, semicolon.
- AEM cloud XSS via NPM reverse proxy + cache differential.
- DNN Unicode normalization + NTLM hash leak.
- Orphaned GitHub commits in GitHub Archive forever.
- "Bug Bounty Metagaming" — hacking styles, niche specialist.

### Key takeaways
- [ ] Test GCP metadata: `computeMetadata//v1/`, HTTP/0.9, `;` in URL — all bypass Metadata-Flavor header.
- [ ] Cross-customer XSS: find CDN serving user content; check HTML upload served under other customers' domains.
- [ ] Tab chars in URLs: `fetch` strips tabs — `.\t.\t/` becomes `../`.
- [ ] Unicode normalization after sanitization: overlong UTF-8 re-introduces special chars.
- [ ] GitHub Archive logs every push — orphaned force-pushed commits indexed permanently.

### Bugs and Findings

#### GCP Metadata SSRF Bypass — Metadata read
- **Bypasses:** `computeMetadata//v1/...`, HTTP/0.9, `;` in URL. All bypass `Metadata-Flavor: Google` header requirement.
- **Impact / severity / bounty:** Cloud metadata access (tokens, keys).

#### AEM Cloud NPM Reverse Proxy XSS — Stored XSS
- **Root cause:** `.rum` path proxied to unpkg (NPM); NPM packages can contain HTML served as `text/html`.
- **Bypasses:**
  - Missing trailing slash: `/rum/path` vs `/rum/path/`.
  - Tab in URL: `.\t.\t/` → fetch removes tab → path traversal.
  - 302 redirect normalization URL-decodes content.
  - Case sensitivity: jsDelivr (case-sensitive 404) vs unpkg (case-insensitive 200).
- **Impact / severity / bounty:** Stored XSS on every AEM cloud site.

#### DNN Unicode → NTLM Hash Leak — Credential leak
- **Root cause:** Sanitization runs BEFORE Unicode normalization. Overlong UTF-8 for `.` (%C0%AE) bypasses sanitizer → normalized to `.` → UNC path → SMB → NTLM leak.
- **Impact / severity / bounty:** Windows credentials leaked.

#### Orphaned GitHub Commits — Credential disclosure
- **Root cause:** Force-push deletes pointer but commit objects remain in GitHub Archive (since 2011).
- **Technique:** Query GitHub Archive for "zero commit push events" (force pushes). Extract secrets via TruffleHog.
- **Impact / severity / bounty:** $25k+ in bounties.

### Techniques and Primitives
- **Tab character path traversal** — `.\t.\t/` bypasses validation but fetch strips tabs.
- **Unicode normalization after sanitization** — Overlong UTF-8 re-introduces special chars.
- **Order of operations in sanitization** — `replace-to-empty` abusable.
- **Redirect loop for blind SSRF** — Multiple redirects exhaust max-redirect → different error handling.

### Tooling and Resources
- GitHub Archive — `data.gharchive.org`
- TruffleHog
- Searchlight Cyber Christmas in July

### Suggestions and Advices from Hunter
- "Most leaky file names: README, .env, config, dump, backup, .gitignore — add these to wordlists."
- "Unguessable IDs are STILL IDORs."
- "The niche specialist is defensible against AI."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
GCP Metadata SSRF bypasses: extra slash, HTTP/0.9, semicolon.

#### 2. What you should learn
- Understand **[ ] test gcp metadata: `computemetadata//v1/`, http/0.9, `;` in url — all bypass metadata-flavor header**
- Understand **[ ] cross-customer xss: find cdn serving user content; check html upload served under other customers' domains**
- Understand **[ ] tab chars in urls: `fetch` strips tabs — `.\t.\t/` becomes `../`**
- Understand **[ ] unicode normalization after sanitization: overlong utf-8 re-introduces special chars**
- Understand **[ ] github archive logs every push — orphaned force-pushed commits indexed permanently**

#### 3. Core concepts explained
**GCP Metadata SSRF Bypass — Metadata read**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**AEM Cloud NPM Reverse Proxy XSS — Stored XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**DNN Unicode → NTLM Hash Leak — Credential leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Tab character path traversal**
- `.\t.\t/` bypasses validation but fetch strips tabs.

**Unicode normalization after sanitization**
- Overlong UTF-8 re-introduces special chars.

**Order of operations in sanitization**
- `replace-to-empty` abusable.


#### 4. Techniques and tactics
**Tab character path traversal**
- **What it is:** `.\t.\t/` bypasses validation but fetch strips tabs.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Unicode normalization after sanitization**
- **What it is:** Overlong UTF-8 re-introduces special chars.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Order of operations in sanitization**
- **What it is:** `replace-to-empty` abusable.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Redirect loop for blind SSRF**
- **What it is:** Multiple redirects exhaust max-redirect → different error handling.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Most leaky file names: README, .env, config, dump, backup, .gitignore"* — **add these to wordlists.**
- *"Unguessable IDs are STILL IDORs."*
- *"The niche specialist is defensible against AI."*

#### 6. Mental models
- **Most leaky file names: README, .env, config, dump, backup, .** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Unguessable IDs are STILL IDORs.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The niche specialist is defensible against AI.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Test GCP metadata: `computeMetadata//v1/`, HTTP/0.9, `;` in URL — all bypass Metadata-Flavor header.
- **Try this:** [ ] Cross-customer XSS: find CDN serving user content; check HTML upload served under other customers' domains.
- **Try this:** [ ] Tab chars in URLs: `fetch` strips tabs — `.\t.\t/` becomes `../`.
- **Try this:** [ ] Unicode normalization after sanitization: overlong UTF-8 re-introduces special chars.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GCP Metadata SSRF Bypass — Metadata read?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **GCP Metadata SSRF bypasses: extra slash, HTTP/0.9, semicolon.**
2. **[ ] Test GCP metadata: `computeMetadata//v1/`, HTTP/0.9, `;` in URL — all bypass**
3. **[ ] Cross-customer XSS: find CDN serving user content; check HTML upload served **
