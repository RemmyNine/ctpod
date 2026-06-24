---
title: "XSSDoctor — Client-side Path Traversal Research"
episode: 168
---


# Episode 168 XSSDoctor — Client-side Path Traversal Research

### TL;DR
- Comprehensive research on how 8 major frontend frameworks handle client-side path traversals (CSPT) — React, Next.js, Vue, Angular, Ember, Svelte, Solid, Nuxt
- Key sink: `useParams` in React double-URL-decodes path parameters; lowercase `%25%2f` (double-encoded) differs from uppercase `%25%2F` due to React's case-sensitive regex
- Pre-production endpoints often lack `Content-Disposition: attachment` — upload to pre-prod for direct HTML render
- Next.js `await params` (server-side) auto-decodes path params unlike client-side `useParams` — enabling secondary context path traversal
- Path param injection is more impactful than query param injection for CSPT

### Key Takeaways
- [ ] CSPT exists beyond web apps — found in desktop apps, mobile apps, IoT; any HTTP client can be vulnerable
- [ ] In Next.js, test server-side `await params` for auto-decoded path traversal — client-side `useParams` may be safe but server-side can introduce secondary context path traversal
- [ ] When doing CSPT testing, always try BOTH uppercase and lowercase hex in double-encoded payloads — React only decodes `%25%2F` (uppercase F), not `%25%2f`
- [ ] For CSPT impact escalation: look for (1) controlling query params in forged requests, (2) no-body endpoints, (3) endpoints accepting similar parameter sets
- [ ] The `fetch()` API auto-normalizes `%09` (tab) to `/` — useful for WAF bypass

### Bugs and Findings

#### Pre-Prod Upload → PostMessage → XSS → AI Home Automation Takeover
- **Target/context:** Home automation AI assistant
- **Root cause:** PostMessage listener had origin check `*.target.com` — any subdomain could inject prompts; file upload rendered as HTML on pre-production domain without `Content-Disposition: attachment`
- **Technique:** 1) Upload arbitrary HTML attachment to pre-prod endpoint 2) Send postMessage to AI with prompt injection ("turn off alarm system") 3) AI executes the action; later found API with wildcard CORS `Access-Control-Allow-Origin: *.target.com` enabling same XSS via direct API calls
- **Key technical details:** PostMessage origin check: `*.target.com` (all subdomains); file upload had `Content-Disposition: attachment` on prod but not on pre-prod
- **Impact / severity / bounty:** Full home automation takeover — disarm alarms, unlock doors, open garage

**Obstacles & how solved:** First "XSS" was actually self-XSS (tested on guest profile that was logged in on another window). Second upload had a `path` parameter that allowed directory control: `/uploads/` → `/uploads/custom_path/filename`, bypassing attachment disposition.

#### E-Signature Platform — Link Leak → Unauthorized Signing
- **Target/context:** E-signature platform
- **Root cause:** Creator of contract can access the recipient's signing link via a hidden API endpoint
- **Technique:** Create contract → retrieve signing link intended for recipient → sign on behalf of recipient
- **Key technical details:** Hidden API endpoint accessible by contract creator leaks the per-recipient signing URL
- **Impact / severity / bounty:** Sign any contract as any recipient; complete integrity bypass

#### Client-Side Path Traversal via Fetch — Tab in URL
- **Technique:** `fetch()` API normalizes `%09` (tab) in URL path to `/` — `some/path%09/../actual` becomes `some/path/../actual` → traversal
- **Key technical details:** `%09` = tab character; fetch treats it as a path separator; also works with `%0a`, `%0d`, `%20` in some contexts
- **Best WAF bypass:** `..%09/..%5c` or `..%2e%09%2e%5c`

### Techniques and Primitives
- **React `useParams` double-URL-decoding** — Only uppercase F in `%25%2F` decodes to `/`; lowercase `%25%2f` does NOT decode to `/`. Root cause: React's `matchPath` has a `replace(/%2F/g, "/")` that is case-sensitive
- **Next.js `await params` vs `useParams` differential** — `await params` (server-side) decodes; `useParams` (client-side) does NOT — creating secondary context path traversal on server-side where client-side looked safe
- **Splat/wildcard routes** — `/files/*` captures everything (including `../` and `//`) in one parameter while dynamic params (`/files/:id`) break on `/`
- **Content-Disposition: attachment bypass via directory** — Same upload in `/uploads/` may have attachment but `/uploads/other_dir/` may not
- **Window.open from keydown event** — Not just clicks; keydown also satisfies user gesture requirement; useful for POC
- **Control-click from iframe → top-level navigation** — Clickjacking + CSRF chain: login CSRF in iframe → user Ctrl+click button → top-level navigation triggers CSRF with cookies

### Tooling and Resources
- Portswigger URL parsing cheat sheet
- lab.ctbb.show — Client-Side Path Traversal research paper by XSSDoctor
- Lira's SVG-enhanced clickjacking research: lyra.horse/blog/2025/12/svg-clickjacking/
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Comprehensive research on how 8 major frontend frameworks handle client-side path traversals (CSPT) — React, Next.js, Vue, Angular, Ember, Svelte, Solid, Nuxt

#### 2. What you should learn
- Understand **[ ] cspt exists beyond web apps — found in desktop apps, mobile apps, iot; any http client can be vulnerable**
- Understand **[ ] in next.js, test server-side `await params` for auto-decoded path traversal — client-side `useparams` may be safe but server-side can introduce secondary context path traversal**
- Understand **[ ] when doing cspt testing, always try both uppercase and lowercase hex in double-encoded payloads — react only decodes `%25%2f` (uppercase f), not `%25%2f`**
- Understand **[ ] for cspt impact escalation: look for (1) controlling query params in forged requests, (2) no-body endpoints, (3) endpoints accepting similar parameter sets**
- Understand **[ ] the `fetch()` api auto-normalizes `%09` (tab) to `/` — useful for waf bypass**

#### 3. Core concepts explained
**Pre-Prod Upload → PostMessage → XSS → AI Home Automation Takeover**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**E-Signature Platform — Link Leak → Unauthorized Signing**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Client-Side Path Traversal via Fetch — Tab in URL**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**React `useParams` double-URL-decoding**
- Only uppercase F in `%25%2F` decodes to `/`; lowercase `%25%2f` does NOT decode to `/`. Root cause: React's `matchPath` has a `replace(/%2F/g, "/")` that is case-sensitive

**Next.js `await params` vs `useParams` differential**
- `await params` (server-side) decodes; `useParams` (client-side) does NOT — creating secondary context path traversal on server-side where client-side looked safe

**Splat/wildcard routes**
- `/files/*` captures everything (including `../` and `//`) in one parameter while dynamic params (`/files/:id`) break on `/`


#### 4. Techniques and tactics
**React `useParams` double-URL-decoding**
- **What it is:** Only uppercase F in `%25%2F` decodes to `/`; lowercase `%25%2f` does NOT decode to `/`. Root cause: React's `matchPath` has a `replace(/%2F/g, "/")` that is case-sensitive
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Next.js `await params` vs `useParams` differential**
- **What it is:** `await params` (server-side) decodes; `useParams` (client-side) does NOT — creating secondary context path traversal on server-side where client-side looked safe
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Splat/wildcard routes**
- **What it is:** `/files/*` captures everything (including `../` and `//`) in one parameter while dynamic params (`/files/:id`) break on `/`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Content-Disposition: attachment bypass via directory**
- **What it is:** Same upload in `/uploads/` may have attachment but `/uploads/other_dir/` may not
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Window.open from keydown event**
- **What it is:** Not just clicks; keydown also satisfies user gesture requirement; useful for POC
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
- **Try this:** [ ] CSPT exists beyond web apps — found in desktop apps, mobile apps, IoT; any HTTP client can be vulnerable
- **Try this:** [ ] In Next.js, test server-side `await params` for auto-decoded path traversal — client-side `useParams` may be safe but server-side can introduce secondary context path traversal
- **Try this:** [ ] When doing CSPT testing, always try BOTH uppercase and lowercase hex in double-encoded payloads — React only decodes `%25%2F` (uppercase F), not `%25%2f`
- **Try this:** [ ] For CSPT impact escalation: look for (1) controlling query params in forged requests, (2) no-body endpoints, (3) endpoints accepting similar parameter sets

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **API** — Application Programming Interface — structured endpoints for data exchange
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Pre-Prod Upload → PostMessage → XSS → AI Home Automation Takeover?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Comprehensive research on how 8 major frontend frameworks handle client-side pat**
2. **[ ] CSPT exists beyond web apps — found in desktop apps, mobile apps, IoT; any H**
3. **[ ] In Next.js, test server-side `await params` for auto-decoded path traversal **
