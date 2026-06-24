---
title: "Getting Live Hacking Event Invites & Bug Bounty Collab with Nagli"
episode: 49
---


# Episode 49 Getting Live Hacking Event Invites & Bug Bounty Collab with Nagli

### TL;DR
- Collab with Nagli: found ASP.NET source code leak (wwwroot.zip) -> RCE via deserialization
- Swagger file discovery -> S3 bucket arbitrary read with credit card transaction data
- PHP type juggling vulnerability requiring 70+ days of brute force to exploit
- 2023 live hacking event circuit recap; new 2024 LHE standards

### Key takeaways
- wwwroot.zip backup file in ASP.NET: contains web.config with machine key -> YSoSerial to craft deserialization viewstate -> RCE
- Source code disclosure alone is critical; chaining to RCE proves impact
- Swagger files with unauthenticated endpoints can be chained to find internal S3 bucket access
- Enumerate S3 bucket content by deleting parts of the path (ID traversal) to find pre-signed URLs
- Program-specific nuclei templates: run custom templates on priority programs with good bounties

### Bugs and Findings
#### ASP.NET Machine Key -> RCE
- **Target/context:** ASP.NET app with exposed wwwroot.zip backup file
- **Root cause:** Production machine key (`<machineKey>` in `web.config`) leaked via backup
- **Technique:**
  1. Download wwwroot.zip containing full source
  2. Extract `<machineKey>` from `web.config`
  3. Use YSoSerial to craft a malicious viewstate
  4. Send to ASPX page — even if `EnableViewState="false"` in the page, ASP.NET parses viewstate anyway (as of 2014)
  5. Deserialization -> RCE
- **Key technical details:** ViewState `EnableViewState="false"` does NOT prevent deserialization; the server parses __VIEWSTATE regardless
- **Impact / severity / bounty:** RCE on production server

#### Swagger File -> S3 Bucket Read
- **Target/context:** Internal API with publicly accessible Swagger docs
- **Technique:**
  1. Found unauthenticated Swagger endpoint
  2. No auth required on several API calls listed
  3. Traversed through multiple API calls to find an ID format
  4. Used ID to get a pre-signed S3 URL
  5. Modified path (removed endpoint, kept directory) to list bucket contents
- **Impact:** Access to S3 bucket containing credit card transaction data

### Techniques and Primitives
- **Decompile ASP.NET DLLs with .Peek** — Extract full source from bin/*.dll after source disclosure
- **PHP type juggling (0e hash collision)** — Brute force MD5 until hash starts with `0e` followed by only digits; PHP `==` treats it as scientific notation (0), bypassing checks
- **Program-specific nucleus templates** — write templates for patterns found in a specific program
- **Source code version fingerprinting via readme** — Check readme.html for small diffs (e.g., lowercase 'h' vs uppercase) to determine if a CVE patch has been applied

### Tooling and Resources
- **YSoSerial** — .NET deserialization payload generator
- **.Peek** — .NET decompiler
- **Shockwave** (shockwave.cloud) — ASM + bug bounty interface (Nagli's project)
- **Axiom** — distributed scanning

### Suggestions and Advices from Hunter
- On second bounty after source leak: "If they didn't rotate the machine key, the fix isn't complete"
- "Question everything. We got a 'not found' on one endpoint; tried removing the endpoint and checking the directory — got full S3 listing"
- On LHE invites — HackerOne's new 2024 standard: top performers (75%+ of submissions rated high/critical, 5+ high/crit in last 180 days, sorted by rewards)

### AI Takeaway
The `wwwroot.zip` -> viewstate deserialization chain shows that even "fixed" bugs (file removed) require key rotation to fully remediate. The `EnableViewState="false"` bypass is a critical detail — a 2014 ASP.NET behavior change silently disabled the impact of that config switch.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Collab with Nagli: found ASP.NET source code leak (wwwroot.zip) -> RCE via deserialization

#### 2. What you should learn
- Understand **wwwroot.zip backup file in asp.net: contains web.config with machine key -> ysoserial to craft deserialization viewstate -> rce**
- Understand **source code disclosure alone is critical; chaining to rce proves impact**
- Understand **swagger files with unauthenticated endpoints can be chained to find internal s3 bucket access**
- Understand **enumerate s3 bucket content by deleting parts of the path (id traversal) to find pre-signed urls**
- Understand **program-specific nuclei templates: run custom templates on priority programs with good bounties**

#### 3. Core concepts explained
**ASP.NET Machine Key -> RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Swagger File -> S3 Bucket Read**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Decompile ASP.NET DLLs with .Peek**
- Extract full source from bin/*.dll after source disclosure

**PHP type juggling (0e hash collision)**
- Brute force MD5 until hash starts with `0e` followed by only digits; PHP `==` treats it as scientific notation (0), bypassing checks

**Program-specific nucleus templates**
- write templates for patterns found in a specific program


#### 4. Techniques and tactics
**Decompile ASP.NET DLLs with .Peek**
- **What it is:** Extract full source from bin/*.dll after source disclosure
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**PHP type juggling (0e hash collision)**
- **What it is:** Brute force MD5 until hash starts with `0e` followed by only digits; PHP `==` treats it as scientific notation (0), bypassing checks
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Program-specific nucleus templates**
- **What it is:** write templates for patterns found in a specific program
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Source code version fingerprinting via readme**
- **What it is:** Check readme.html for small diffs (e.g., lowercase 'h' vs uppercase) to determine if a CVE patch has been applied
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"On second bounty after source leak: "If they didn't rotate the machine key, the fix isn't complete"*
- *"Question everything. We got a 'not found' on one endpoint; tried removing the endpoint and checking the directory"* — **got full S3 listing**
- *"On LHE invites"* — **HackerOne's new 2024 standard: top performers (75%+ of submissions rated high/critical, 5+ high/crit in last 180 days, sorted by rewards)**

#### 6. Mental models
- **On second bounty after source leak: "If they didn't rotate t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Question everything. We got a 'not found' on one endpoint; t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On LHE invites — HackerOne's new 2024 standard: top performe** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** wwwroot.zip backup file in ASP.NET: contains web.config with machine key -> YSoSerial to craft deserialization viewstate -> RCE
- **Try this:** Source code disclosure alone is critical; chaining to RCE proves impact
- **Try this:** Swagger files with unauthenticated endpoints can be chained to find internal S3 bucket access
- **Try this:** Enumerate S3 bucket content by deleting parts of the path (ID traversal) to find pre-signed URLs

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **deserialization** — Converting serialized data back into objects — dangerous if attacker-controlled

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in ASP.NET Machine Key -> RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Collab with Nagli: found ASP.NET source code leak (wwwroot.zip) -> RCE via deser**
2. **wwwroot.zip backup file in ASP.NET: contains web.config with machine key -> YSoS**
3. **Source code disclosure alone is critical; chaining to RCE proves impact**
