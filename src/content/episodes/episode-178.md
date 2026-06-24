---
title: "600k in ~3 months — BruteCat pt 2"
episode: 178
---


# Episode 178 600k in ~3 months — BruteCat pt 2

### TL;DR
- BruteCat built a full AI-driven Google API scanning system: 3,600 Google-owned API keys, 14,000 discovery documents, automated first-party auth
- Scanned all 14,000 Google APIs via AI with abstracted auth — focused AI only on constructing test request bodies
- $670K in bounties over ~3-4 months from this system
- Key components: API key harvesting (60K APKs, Chrome extension traffic capture, binary C-Handlers), first-party auth automation with correct origin/referer, operation ID tracking to prevent AI hallucination

### Key Takeaways
- [ ] Google API key harvesting: scrape 60K APKs, use Chrome extension with `chrome.debugger` to auto-capture keys, scan all Google domains
- [ ] First-party auth origin brute force — valid origins include `www.google.com`, corporate domains (`corp.google.com`); enumerate via `session cookie invalid` vs real auth errors
- [ ] Abstract auth away from AI — AI should only construct request bodies; everything else (keys, auth, routing) handled by tooling
- [ ] Map response bodies by hash to deduplicate — send one copy of each unique response to AI, not all identical ones
- [ ] Staging bypass: Google's `staging` often points to prod DB — use `alt` push hostnames for unfixed endpoints

### Bugs and Findings

#### Google Voice Provider API — No Auth, Full PII Dump
- **Target/context:** Google Fiber Voice provider API
- **Root cause:** API endpoint required only an API key (no user auth) — incremental obfuscated GAIA ID enumeration dumped phone number, Google Voice number, email, PIN for any account
- **Technique:** Increment obfuscated GAIA ID → full PII for each account
- **Key technical details:** Endpoint also had number assignment — could add phone number to victim's Google account
- **Impact / severity / bounty:** Full PII exposure for any Google account

#### LDR (Google Internal Investigation Tool) — Full Data Leak
- **Target/context:** Google's internal LDR (investigation/reporting tool)
- **Root cause:** LDR API exposed publicly at non-corp domain; no auth on most endpoints; wildcard origin allowlist (`*.google.com`)
- **Technique:** 1) AI discovered LDR endpoint 2) Used `www.google.com` origin for first-party auth 3) Accessed all investigations, logs, access requests 4) Recreated LDR UI internally
- **Key technical details:** Origin allownlist: `*.google.com`; public domain exposure; AI auto-submitted an LDR report which sent email with G Doc links to BruteCat
- **Impact / severity / bounty:** Read/write access to all Google internal investigations

#### Ad Exchange — Staging → Prod IDOR
- **Target/context:** Google Ad Exchange (critical advertising platform)
- **Root cause:** Cookie-matching API dumped all account IDs unauth; staging environment (`adx-buyer`) pointed to prod database with no access controls
- **Technique:** 1) Dump all account IDs via unauth cookie-matching API 2) Use staging endpoint to reference those IDs → full prod data access
- **Key technical details:** Staging pointing to prod is a known Google quirk ("no staging"); numeric IDs in paths with no auth
- **Impact / severity / bounty:** Unauthorized access to critical advertising platform data

#### YouTube Partner CMS — Private Video Leak
- **Target/context:** YouTube Content ID / CMS system
- **Root cause:** Every uploaded video becomes a CMS asset named `auto-generated-asset-<videoId>`; CMS search API returns all assets including private/unlisted ones
- **Technique:** Search CMS API for `auto-generated-asset-` prefix → returns ALL videos (including private) from all partner channels
- **Key technical details:** Also supports time-based filters for real-time capture of newly uploaded videos; returns video IDs of unlisted/private YouTube partner videos
- **Impact / severity / bounty:** $12K — leaks ALL unlisted/private videos from YouTube partner channels

#### PLX (Google Internal Dashboard) — IAM Policy Takeover
- **Target/context:** Google's internal PLX data dashboard
- **Root cause:** `data-hub` API on `client6.google.com` had suggest endpoint leaking table names; staging environment allowed setting IAM policy without approval
- **Technique:** 1) Suggest endpoint leaked table names including sensitive ones (employee data, petabytes-scale) 2) Staging IAM endpoint allowed setting admin policy on any table 3) Take over table → full data access
- **Key technical details:** Some tables petabytes in size; staging IAM policy endpoint lacked approval checks
- **Impact / severity / bounty:** $12K — admin access to internal Google data tables

#### Cloud Console GraphQL → Internal RPC Access
- **Target/context:** Google Cloud Console GraphQL endpoint
- **Root cause:** Cloud Console uses GraphQL as frontend; staging endpoint allowed introspection without signature; GraphQL maps to internal RPCs
- **Technique:** 1) Discover staging Cloud Console GraphQL endpoint 2) Introspect full schema 3) GraphQL queries map to internal Google RPCs not otherwise accessible
- **Impact / severity / bounty:** Access to internal APIs via GraphQL introspection

### Techniques and Primitives
- **AI-first-party auth abstraction** — All auth logic (key selection, origin/referer validation, first-party signature computation) handled by tooling; AI only constructs request body
- **Response dedup by hash** — API responses from multiple keys grouped by body hash; AI gets one copy per unique response
- **Error normalization** — Google's generic errors (`method not found`, `invalid argument`) mapped to standard explanations so AI doesn't waste time on false leads
- **Operation ID audit trail** — Every tool call tagged with operation ID; AI must reference operation ID in findings — prevents hallucinated reports
- **Coverage verification** — Track which API methods AI has tested; if not all methods covered, reject "done" signal and resume
- **Key filtering by project domain** — Use Cloud Marketplace endpoint to check which Google domain a key belongs to; filter out customer keys
- **Binary/ELF C-Handler dumping** — Leaked binaries from Google contain embedded C-Handlers (internal debug endpoints); reverse to find auth bypasses and stubby implementations
- **Feature flag abuse** — Enable experimental features via debugger/batch execute before public release
- **Free trial billing isolation** — Create free trial on separate Google account, grant project access to testing account, then remove billing account association — prevents AI from accidentally incurring charges

### Tooling and Resources
- BruteCat's Request to Proto tool
- BruteCat's internal API scanner with discovery doc + auth automation
- Chrome extension with `chrome.debugger` for key capture
- Google SRE Handbook, BeyondProd
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
BruteCat built a full AI-driven Google API scanning system: 3,600 Google-owned API keys, 14,000 discovery documents, automated first-party auth

#### 2. What you should learn
- Understand **[ ] google api key harvesting: scrape 60k apks, use chrome extension with `chrome.debugger` to auto-capture keys, scan all google domains**
- Understand **[ ] first-party auth origin brute force — valid origins include `www.google.com`, corporate domains (`corp.google.com`); enumerate via `session cookie invalid` vs real auth errors**
- Understand **[ ] abstract auth away from ai — ai should only construct request bodies; everything else (keys, auth, routing) handled by tooling**
- Understand **[ ] map response bodies by hash to deduplicate — send one copy of each unique response to ai, not all identical ones**
- Understand **[ ] staging bypass: google's `staging` often points to prod db — use `alt` push hostnames for unfixed endpoints**

#### 3. Core concepts explained
**Google Voice Provider API — No Auth, Full PII Dump**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**LDR (Google Internal Investigation Tool) — Full Data Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Ad Exchange — Staging → Prod IDOR**
- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.
- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.
- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.

**AI-first-party auth abstraction**
- All auth logic (key selection, origin/referer validation, first-party signature computation) handled by tooling; AI only constructs request body

**Response dedup by hash**
- API responses from multiple keys grouped by body hash; AI gets one copy per unique response

**Error normalization**
- Google's generic errors (`method not found`, `invalid argument`) mapped to standard explanations so AI doesn't waste time on false leads


#### 4. Techniques and tactics
**AI-first-party auth abstraction**
- **What it is:** All auth logic (key selection, origin/referer validation, first-party signature computation) handled by tooling; AI only constructs request body
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Response dedup by hash**
- **What it is:** API responses from multiple keys grouped by body hash; AI gets one copy per unique response
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Error normalization**
- **What it is:** Google's generic errors (`method not found`, `invalid argument`) mapped to standard explanations so AI doesn't waste time on false leads
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Operation ID audit trail**
- **What it is:** Every tool call tagged with operation ID; AI must reference operation ID in findings — prevents hallucinated reports
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Coverage verification**
- **What it is:** Track which API methods AI has tested; if not all methods covered, reject "done" signal and resume
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
- **Try this:** [ ] Google API key harvesting: scrape 60K APKs, use Chrome extension with `chrome.debugger` to auto-capture keys, scan all Google domains
- **Try this:** [ ] First-party auth origin brute force — valid origins include `www.google.com`, corporate domains (`corp.google.com`); enumerate via `session cookie invalid` vs real auth errors
- **Try this:** [ ] Abstract auth away from AI — AI should only construct request bodies; everything else (keys, auth, routing) handled by tooling
- **Try this:** [ ] Map response bodies by hash to deduplicate — send one copy of each unique response to AI, not all identical ones

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Google Voice Provider API — No Auth, Full PII Dump?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **BruteCat built a full AI-driven Google API scanning system: 3,600 Google-owned A**
2. **[ ] Google API key harvesting: scrape 60K APKs, use Chrome extension with `chrom**
3. **[ ] First-party auth origin brute force — valid origins include `www.google.com`**
