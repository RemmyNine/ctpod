---
title: "LA Live Chat with Five Legendary Hackers"
episode: 17
---


# Episode 17 LA Live Chat with Five Legendary Hackers

### TL;DR
- Live from H1-213 (Los Angeles): Corbin, Sam Curry, Franz Rosen, n0gl3y, Dr. Bowman
- Corbin: Transatlantic cable (TAP14) — directory traversal + caching bug → admin access to critical infrastructure panel
- Sam Curry: AT&T SIM card portal → Jasper Systems compromise → could track/disable 180M SIM cards incl. Tesla/FBI/DHS
- Franz Rosen: SSRF→SSTI chain — recycled content from SSRF fed back into template engine (EJS) → RCE
- Dr. Bowman: Released lo-fi song on music distribution service → blind XSS on major label admin panel (discovered unreleased tracks)
- n0gl3y + Andre: Unauthenticated subdomain takeover on billion-dollar company's main domain; Unicode homoglyph ATO ($28k)

### Key takeaways
- When brute-forcing directories, pay attention to Set-Cookie headers in responses — cached sessions
- Jasper Systems runs the world's telecom IoT SIM management; API accessible via partner portals
- SSRF + SSTI chain: if SSRF response is rendered back into HTML/template, test for SSTI too
- For creative POCs: pay for a Fiverr gig (artist/singer) to craft realistic assets; release on distribution platforms
- Blind XSS in admin panels of content distributors can leak unreleased content
- Set a challenge goal (e.g., "we want authentication bypass") and keep iterating until you find it

### Bugs and Findings

#### Transatlantic Cable (TAP14) Admin Panel Access
- **Target/context:** Telecom company with critical undersea cable infrastructure
- **Root cause:** Tomcat caching bug — hitting a directory twice set an admin session cookie
- **Technique / how found:** Scanned company IP range; found TAP14 marketing page; directory brute-force found `/admin` directory; second visit to a specific path set admin session cookie
- **Key technical details:** Tomcat caching; directory brute-force → second visit → admin session cookie; admin page showed 30 accounts, shared password
- **Impact / severity / bounty:** Reported but program denied ownership; fixed silently
- **Obstacles & how solved:** Program claimed they didn't own it; "It went away magically"

#### AT&T SIM Portal → Jasper Systems — 180M SIM Card Access
- **Target/context:** Tesla (bug bounty), AT&T, Jasper Systems
- **Root cause:** AT&T's business SIM portal (`business.att.com`) leaked a Jasper API token via fuzzing → Jasper had API to manage ALL customers' SIM cards
- **Technique / how found:**
  1. Got Tesla SIM card via AT&T business portal
  2. Fuzzing in Burp → error message containing "Jasper" reference
  3. Google Jasper → discovered Jasper runs 90%+ of global IoT SIM management
  4. Token leaked in AT&T error allowed querying Jasper's API
- **Exploitation steps:**
  1. Get Jasper API token from AT&T portal
  2. Query Jasper XML API: `search SIM cards` → 180M results
  3. Filter by Tesla → specific Tesla SIM cards
  4. API methods: `trackLocation`, `disableSIM`, `sendSMS`, `readSMS`
  5. Via another API call: list AT&T's customers → FBI, DHS, NSA
- **Key technical details:** Jasper XML API; `search` method; partner portal authentication delegation
- **Impact / severity / bounty:** Reported to Tesla (via their bounty program, since Tesla data was accessible); Tesla paid bounty on AT&T's behalf; fixed in 48 hours

#### SSRF → SSTI via EJS Template Engine
- **Target/context:** Undisclosed web application
- **Root cause:** SSRF response was rendered back into an EJS template without sanitization
- **Technique / how found:**
  1. Franz found an SSRF — could only fetch external URLs
  2. Matias Carlson suggested testing SSTI in the SSRF response (if it gets rendered)
  3. Tried EJS template syntax `<%= 2*2 %>` in attacker-controlled response → evaluated to `4`
- **Exploitation steps:**
  1. Set up attacker server returning EJS payload `<%= process.env ... %>`
  2. Weaponized to `require('child_process').execSync('id')`
  3. Full RCE via template injection
- **Key technical details:** SSRF content recycled into EJS template; `process.mainModule.require('child_process')` for RCE
- **Impact / severity / bounty:** Critical; RCE on server
- **Obstacles & how solved:** Idea came from late-night collaboration with Matias Carlson

#### Music Distribution Blind XSS — Major Label Admin Panel
- **Target/context:** Music distribution service → major record label admin panel
- **Root cause:** Distribution platform's upload/approval process rendered artist metadata (including XSS payloads) in the label's admin panel
- **Technique / how found:**
  1. Paid Fiverr artist to create lo-fi song, Fiverr vocalist for A-Team parody, Fiverr pixel artist for cover art (~$500 total)
  2. Released music with XSS payloads embedded in metadata
  3. Distribution service pushed to major label's review queue
  4. Admin panel rendered XSS → blind XSS callback → leaked localStorage/sessionStorage
- **Key technical details:** Lo-fi track with XSS payload in metadata; blind XSS on major label internal admin; leaked unreleased music data of major artists
- **Impact / severity / bounty:** High; disclosed to label's CTO after summer holidays
- **Obstacles & how solved:** Company was in France — nobody works in August; reached CEO on LinkedIn; finally connected with CTO who fixed it

#### Unicode Homoglyph ATO (duplicate from Ep. 15) — $28k
- **Key technical details:** Unicode homoglyph `а` (Cyrillic) vs `a` (Latin); SSO normalization mismatch
- **Technique:** Registered with homoglyph email; one subdomain normalized it to the real email → logged in as that user

### Techniques and Primitives
- **SSRF→SSTI chain** — if SSRF response is rendered in HTML/template, test SSTI on attacker-controlled responses
- **Creative POC investments** — spend money ($500-1000) on Fiverr artists for realistic POC assets
- **Challenge goal-setting** — "we want auth bypass" → iterate until found
- **Cached directory session** — when hitting unknown dirs, check Set-Cookie in response; visit twice

### Tooling and Resources
- burpsuite
- Fiverr for creative POCs
- Jasper Systems (SIM management)
- EJS template engine
- AT&T business portal

### Suggestions and Advices from Hunter
- "Spend money on your POC. Even if it doesn't work, you've got a good story." — Dr. Bowman
- "Set a challenge goal like 'auth bypass' and keep pushing until you find it" — n0gl3y
- "I just have a phonebook of experts; different people for different bug classes" — n0gl3y
- "SSRF → SSTI: if the SSRF response shows up in the page, it might be evaluated as a template" — Franz Rosen

### AI Takeaway
The Jasper Systems compromise is staggering in scope: one API token leaked from a partner portal gave control over 180M SIM cards across government and enterprise customers worldwide. The SSRF→SSTI chain is a must-check pattern: whenever you see SSRF output reflected back to you, test for template injection in the response.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Live from H1-213 (Los Angeles): Corbin, Sam Curry, Franz Rosen, n0gl3y, Dr. Bowman

#### 2. What you should learn
- Understand **when brute-forcing directories, pay attention to set-cookie headers in responses — cached sessions**
- Understand **jasper systems runs the world's telecom iot sim management; api accessible via partner portals**
- Understand **ssrf + ssti chain: if ssrf response is rendered back into html/template, test for ssti too**
- Understand **for creative pocs: pay for a fiverr gig (artist/singer) to craft realistic assets; release on distribution platforms**
- Understand **blind xss in admin panels of content distributors can leak unreleased content**

#### 3. Core concepts explained
**Transatlantic Cable (TAP14) Admin Panel Access**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**AT&T SIM Portal → Jasper Systems — 180M SIM Card Access**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SSRF → SSTI via EJS Template Engine**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**SSRF→SSTI chain**
- if SSRF response is rendered in HTML/template, test SSTI on attacker-controlled responses

**Creative POC investments**
- spend money ($500-1000) on Fiverr artists for realistic POC assets

**Challenge goal-setting**
- "we want auth bypass" → iterate until found


#### 4. Techniques and tactics
**SSRF→SSTI chain**
- **What it is:** if SSRF response is rendered in HTML/template, test SSTI on attacker-controlled responses
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Creative POC investments**
- **What it is:** spend money ($500-1000) on Fiverr artists for realistic POC assets
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Challenge goal-setting**
- **What it is:** "we want auth bypass" → iterate until found
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cached directory session**
- **What it is:** when hitting unknown dirs, check Set-Cookie in response; visit twice
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Spend money on your POC. Even if it doesn't work, you've got a good story."* — **Dr. Bowman**
- *"Set a challenge goal like 'auth bypass' and keep pushing until you find it"* — **n0gl3y**
- *"I just have a phonebook of experts; different people for different bug classes"* — **n0gl3y**
- *"SSRF → SSTI: if the SSRF response shows up in the page, it might be evaluated as a template"* — **Franz Rosen**

#### 6. Mental models
- **Spend money on your POC. Even if it doesn't work, you've got** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Set a challenge goal like 'auth bypass' and keep pushing unt** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I just have a phonebook of experts; different people for dif** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** When brute-forcing directories, pay attention to Set-Cookie headers in responses — cached sessions
- **Try this:** Jasper Systems runs the world's telecom IoT SIM management; API accessible via partner portals
- **Try this:** SSRF + SSTI chain: if SSRF response is rendered back into HTML/template, test for SSTI too
- **Try this:** For creative POCs: pay for a Fiverr gig (artist/singer) to craft realistic assets; release on distribution platforms

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Program claimed they didn't own it; "It went away magically"

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **SSTI** — Server-Side Template Injection — injecting template syntax that executes on server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Transatlantic Cable (TAP14) Admin Panel Access?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Live from H1-213 (Los Angeles): Corbin, Sam Curry, Franz Rosen, n0gl3y, Dr. Bowm**
2. **When brute-forcing directories, pay attention to Set-Cookie headers in responses**
3. **Jasper Systems runs the world's telecom IoT SIM management; API accessible via p**
