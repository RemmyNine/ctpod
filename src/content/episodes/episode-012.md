---
title: "JHaddix on Hacker→Hacker CISO, OG Hacking Techniques, and Crazy Reports"
episode: 12
---


# Episode 12 JHaddix on Hacker→Hacker CISO, OG Hacking Techniques, and Crazy Reports

### TL;DR
- Jason Haddix interview: from bug bounty on Bugcrowd (SurveyMonkey era) to Ubisoft CISO to ButtoBot CISO
- Recon technique: recursive spidering with company name keyword in scope to discover rogue dev infrastructure
- Unsecured Jenkins + Sonatype Nexus found via content discovery on an unknown domain with company name
- COTS software attack: find demo/install instance → dump endpoints → replay against target to find authorization bypasses
- LFI via CodeIgniter dot→underscore conversion led to full source code disclosure → Gmail creds → phpMyAdmin → full pwn

### Key takeaways
- Recursive recon: put company name (not domain) in scope, recursively spider to find all linked assets with that keyword
- COTS (commercial off-the-shelf) testing: install/demo the software yourself, map all endpoints, replay against target
- Docker Hub: search for company software images — often contain full source code
- For authorization bypass, make an Excel table of all endpoints available in one role, then test from another role
- Burp Analyzer Target → Dynamic URLs reveals all endpoints with passed data — focus on these
- Sensitive (Status, Size, Words, Lines, Return Time) acronym for fuzz result analysis

### Bugs and Findings

#### Unsecured Jenkins + Sonatype Nexus — Full Source Code Exposure
- **Target/context:** Major auto manufacturer
- **Root cause:** Rogue DevOps team purchased their own domain and set up Jenkins, Nexus, TeamForge without org knowledge; no authentication
- **Technique / how found:** Justin's recursive recon (company name keyword scope) found 4-letter-abbreviation domain; content discovery revealed Jenkins, Nexus paths
- **Exploitation steps:**
  1. Content discovery on blank domain → found Jenkins, Sonatype Nexus, TeamForge
  2. Jenkins had script console — could run arbitrary jobs
  3. Nexus had all infotainment source code with hardcoded creds
- **Key technical details:** Recursive recon with company name (not domain) in scope; unauthenticated CI/CD tools
- **Impact / severity / bounty:** Full org source code exposure; multiple critical findings

#### CRM Authorization Bypass — Full Admin Access
- **Target/context:** Large global company that acquired a CRM company
- **Root cause:** New instance of acquired CRM had missing authorization on several endpoints
- **Technique / how found:**
  1. Found CRM demo portal on old company's site
  2. Logged in with demo creds, spidered all endpoints via Burp
  3. Exported URLs, replaced domain with target instance
  4. Found unprotected paths (SMS API with API key, user profile API leaking password)
- **Key technical details:** Demo portal → Burp spider → replace domain → test auth on target; brute forced 6-char numeric user IDs for admin profile
- **Impact / severity / bounty:** Admin access; could send SMS to 4M clients; full app pwn

#### CodeIgniter LFI via dot→underscore → Full Pwn
- **Target/context:** Password manager company
- **Root cause:** CodeIgniter dot→underscore feature allowed path traversal in minify function → LFI
- **Technique / how found:**
  1. Content discovery found `gmail.php`, `phpmyadmin`, etc. paths (locked down)
  2. Fuzzing a minify parameter produced weird errors about pathing
  3. CodeIgniter docs: dots in paths can be replaced with underscores
  4. Replaced dots with underscores → LFI
  5. Read source code → found Gmail integration with plaintext creds → Gmail access → Google Drive → phpMyAdmin creds → db superuser
- **Exploitation steps:**
  1. LFI via minify function: use underscores instead of dots in path
  2. Echo source code of all known pages
  3. Use LFI to read `gmail.php` → developer's Gmail creds
  4. Gmail → Google Drive → more creds
  5. Creds → phpMyAdmin (locked down login, but creds worked)
  6. Add superuser hash to database → full app control
- **Key technical details:** CodeIgniter dot→underscore feature; minify function LFI; Gmail integration script; phpMyAdmin bypass
- **Impact / severity / bounty:** Full application and infrastructure compromise

### Techniques and Primitives
- **Recursive recon with keyword scope** — put company name string (not just domain) in Burp scope; spider recursively
- **COTS/demo endpoint harvesting** — find demo instance or purchase software; spider all endpoints; replay against target
- **Docker Hub for source code** — search Docker Hub for company's software; pull and extract
- **Burp Analyze Target → Dynamic URLs** — focus vulnerability scanning on endpoints with passed parameters
- **Sensitive acronym** — Status, sizE, words, liNes, reTurn time — analyze fuzz results across all five dimensions

### Tooling and Resources
- FeroxBuster (Rust content discovery)
- FFUF
- Seclists / all.txt / Assetnote wordlists
- Dirbuster (legacy)
- Burp Suite (Analyze Target, Intruder)
- Hunt (Jason's Burp extension for parameter analysis)

### Suggestions and Advices from Hunter
- "Recon doesn't find you bugs. It finds you more apps to hack." — Jason Haddix
- "If they bought another company, find the old demo portal — spider it, replay endpoints against the new instance" — Jason
- "Look at your fuzz results across all five dimensions: Status, Size, Words, Lines, Return Time" — Jason
- "Install the software yourself. Docker Hub often has images." — Jason on source code access

### AI Takeaway
The COTS/demo portal technique is massively underutilized. If a company acquires or white-labels a third-party software, find the original vendor's demo instance, log in with default creds, spider everything, then replay against the target's branded instance. Authorization gaps between the two instances are almost guaranteed.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Jason Haddix interview: from bug bounty on Bugcrowd (SurveyMonkey era) to Ubisoft CISO to ButtoBot CISO

#### 2. What you should learn
- Understand **recursive recon: put company name (not domain) in scope, recursively spider to find all linked assets with that keyword**
- Understand **cots (commercial off-the-shelf) testing: install/demo the software yourself, map all endpoints, replay against target**
- Understand **docker hub: search for company software images — often contain full source code**
- Understand **for authorization bypass, make an excel table of all endpoints available in one role, then test from another role**
- Understand **burp analyzer target → dynamic urls reveals all endpoints with passed data — focus on these**

#### 3. Core concepts explained
**Unsecured Jenkins + Sonatype Nexus — Full Source Code Exposure**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**CRM Authorization Bypass — Full Admin Access**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CodeIgniter LFI via dot→underscore → Full Pwn**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Recursive recon with keyword scope**
- put company name string (not just domain) in Burp scope; spider recursively

**COTS/demo endpoint harvesting**
- find demo instance or purchase software; spider all endpoints; replay against target

**Docker Hub for source code**
- search Docker Hub for company's software; pull and extract


#### 4. Techniques and tactics
**Recursive recon with keyword scope**
- **What it is:** put company name string (not just domain) in Burp scope; spider recursively
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**COTS/demo endpoint harvesting**
- **What it is:** find demo instance or purchase software; spider all endpoints; replay against target
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Docker Hub for source code**
- **What it is:** search Docker Hub for company's software; pull and extract
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Burp Analyze Target → Dynamic URLs**
- **What it is:** focus vulnerability scanning on endpoints with passed parameters
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Sensitive acronym**
- **What it is:** Status, sizE, words, liNes, reTurn time — analyze fuzz results across all five dimensions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Recon doesn't find you bugs. It finds you more apps to hack."* — **Jason Haddix**
- *"If they bought another company, find the old demo portal"* — **spider it, replay endpoints against the new instance" — Jason**
- *"Look at your fuzz results across all five dimensions: Status, Size, Words, Lines, Return Time"* — **Jason**
- *"Install the software yourself. Docker Hub often has images."* — **Jason on source code access**

#### 6. Mental models
- **Recon doesn't find you bugs. It finds you more apps to hack.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If they bought another company, find the old demo portal — s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Look at your fuzz results across all five dimensions: Status** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Recursive recon: put company name (not domain) in scope, recursively spider to find all linked assets with that keyword
- **Try this:** COTS (commercial off-the-shelf) testing: install/demo the software yourself, map all endpoints, replay against target
- **Try this:** Docker Hub: search for company software images — often contain full source code
- **Try this:** For authorization bypass, make an Excel table of all endpoints available in one role, then test from another role

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **Burp** — Burp Suite — popular web application security testing proxy
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Unsecured Jenkins + Sonatype Nexus — Full Source Code Exposure?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Jason Haddix interview: from bug bounty on Bugcrowd (SurveyMonkey era) to Ubisof**
2. **Recursive recon: put company name (not domain) in scope, recursively spider to f**
3. **COTS (commercial off-the-shelf) testing: install/demo the software yourself, map**
