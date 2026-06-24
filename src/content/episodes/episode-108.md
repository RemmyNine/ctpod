---
title: "How to Hack Salesforce, ServiceNow, and Other SaaS Products With Aaron Costello"
episode: 108
---


# Episode 108 How to Hack Salesforce, ServiceNow, and Other SaaS Products With Aaron Costello

**Guest:** Aaron Costello (AppOmni)
**Host:** Justin Gardner (Rhynorater)
**Co-Host:** Joseph Thacker (Rez0)
**Duration:** 1:31:08
**Transcript source:** feed (full transcript)

### TL;DR
- SaaS misconfigurations are a bug class: same payload works across 1000s of companies because they all misconfigure the same access controls
- ServiceNow: legacy widgets (simple list, unordered list) are API endpoints that query any table/column — unauthenticated if access controls misconfigured
- Salesforce: apEX code ("without sharing" = system context) exposed via Aura API — SQL-like injection in SOQL queries possible
- The "sell" for bug bounty: find the undocumented/legacy API endpoints, then test for misconfigured access controls
- "Become the world expert" on the platform first — get developer instances, certifications, build integrations

### Key Takeaways
- SaaS misconfigurations > zero-days: you find the pattern once, apply across unlimited targets
- ServiceNow: "widgets" (simple list, unordered list, data brokers) are API endpoints that accept table name + column name → read data
- Salesforce: custom Apex exposed via Aura API; "without sharing" = system context → ignores access controls
- Entering SaaS security: pool money with other hackers for a production license ($20K/mo for enterprise SaaS)
- Legacy/deprecated APIs are gold — undocumented, often still functional, no security review

### Bugs and Findings

#### ServiceNow Widget Data Exposure
- **Target/context:** ServiceNow customer portals
- **Root cause:** Widgets (API endpoints like "simple list", "unordered list") accept user-supplied table names and column names. If the customer didn't set access controls on those tables, the widget returns the data — unauthenticated
- **Technique / how found:** Aaron went through ServiceNow's entire schema (hundreds of tables), looking for widgets that query user-input tables. Found "simple list" and "unordered list" widgets that were public by default.
- **Exploitation steps:**
  1. Identify ServiceNow instance (usually `*.service-now.com`)
  2. Find the customer portal page
  3. Call the widget API endpoint with table name + column name
  4. If access controls misconfigured → data returned
- **Key technical details:** Widget = API endpoint. Simple list, unordered list are two widgets. Also: "data brokers" from UI builder. Knowledge base widgets were separate (different access controls).
- **Impact / severity / bounty:** Access to any table data including internal knowledge bases, user PII, access tokens. Hundreds of companies affected.
- **ServiceNow response:** After KB article, ServiceNow globally pushed default access controls to all customers. For widgets: added system properties that customers must explicitly set. KB widgets still work.

#### Salesforce Object/Apex Exposure
- **Target/context:** Salesforce customer portals ("Digital Experiences" / "Lightning Communities")
- **Root cause:**
  1. **Objects (tables):** Misconfigured access controls — objects marked "public read" expose record data via standard API
  2. **Apex (custom code):** Apex classes marked "without sharing" run in system context, ignoring access controls. Exposed via Aura API
  3. **SOQL injection:** User input in SOQL queries without sanitization — SQL-like injection
- **Technique / how found:** Enumerate objects via payloads in Aaron's blog (still work unchanged since 2020). For Apex: reverse-engineer JavaScript on customer portal → find exposed Aura methods → call them directly
- **Key technical details:**
  - Objects: use payloads from enumerated.ie blog to enumerate and read object data
  - Apex: "without sharing" = system context. Aura API exposed on public sites. Methods can be enumerated from JavaScript.
  - Named credentials: shared credentials (named principal) can be brute-forced if you have "execute anonymous" API access (even as low-priv community user)
  - SOQL: SELECT-like query language (no DML — insert/update/delete). Injection via unsanitized user input
- **Impact / severity / bounty:** Read/write access to any Salesforce data (PII, credentials, business data)
- **Obstacles & how solved:** Salesforce fixed some Apex-specific issues (custom settings restriction added). Blog payloads from 2020 still work today.

#### AppCache Manifest + Cookie Bombing for File Access
- **Target/context:** Travel company using Salesforce — support ticket file uploads
- **Root cause:** Files uploaded to external S3 bucket instead of Salesforce storage. No file-type validation. AppCache manifest files could be uploaded. All files in same directory → manifest affects all files
- **Exploitation:**
  1. Upload `manifest.appcache` with `FALLBACK` pointing to malicious HTML
  2. Upload malicious HTML that exfiltrates URL ref
  3. Cookie-bomb the browser of anyone viewing the files
  4. Support engineer's browser DOS → they view next ticket → fallback fires → exfiltrate their file access key
  5. Use the key to download any customer's documents
- **Key technical details:** AppCache manifest `FALLBACK` applies to entire directory. Cookie bombing (set enough cookies to exceed browser limit) causes app to fail loading → triggers fallback. Apex was used to upload to external bucket.
- **Impact / severity / bounty:** Access to all customer support documents. Paid as high with novelty bonus.

### Techniques and Primitives
- **SaaS misconfiguration pattern** — Platform provides API endpoints (widgets, components). Customer must configure access controls. Most don't. Finding undocumented/legacy endpoints and testing access controls = infinite bug class.
- **ServiceNow widget enumeration** — Schema has hundreds of tables. Legacy widgets (simple list, unordered list, data brokers) accept user-supplied table+column names.
- **Salesforce Apex discovery** — Reverse-engineer JavaScript on Digital Experience → find Aura-enabled Apex methods → call directly. Look for "without sharing" classes.
- **Named credential brute-force** — With "execute anonymous" API access (even low-priv community user), brute-force common named credential labels to piggyback on shared API credentials.
- **AppCache + Cookie bombing** — Upload AppCache manifest with fallback → cookie-bomb viewer → fallback fires → exfiltrate data.

### Tooling and Resources
- Aaron's blog: enumerated.ie
- AppOmni — SaaS Security Posture Management
- Salesforce Lightning exploitation blog (enumerated.ie)
- ServiceNow data exposure blog (enumerated.ie)
- Apex Security white paper (AppOmni)
- Microsoft Power Pages data exposure research (AppOmni)

### Suggestions and Advices from Hunter
- "Never approach platforms with the intent of hacking. Become an expert on the platform and its functionality first." — Aaron Costello
- "Legacy is where the gold is. All the AI stuff is hip and trendy, but let's not forget the stuff that's been sitting there 10-15 years." — Aaron Costello
- "I've probably compromised 100x what threat actors are compromising via supply chain — through authorized bug bounty platforms." — Aaron Costello
- "For ServiceNow: UX data brokers, UI builder, any API endpoint that returns data — play with those." — Aaron Costello
- "Three things for Salesforce: 1) misconfigured object access 2) custom Apex exposed as API 3) privilege escalation by signing up." — Aaron Costello

### AI Takeaway
SaaS misconfigurations are the ultimate "find once, exploit everywhere" bug class. ServiceNow's widget architecture (API endpoints that accept table/column names) and Salesforce's Apex/Aura framework create an enormous, largely untapped attack surface. The pattern of "become an expert, find undocumented endpoints, test access controls" applies to every major SaaS platform.

# CTBB Episode Analyst Notes — Batch 7 (Episodes 109–126)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
SaaS misconfigurations are a bug class: same payload works across 1000s of companies because they all misconfigure the same access controls

#### 2. What you should learn
- Understand **saas misconfigurations > zero-days: you find the pattern once, apply across unlimited targets**
- Understand **servicenow: "widgets" (simple list, unordered list, data brokers) are api endpoints that accept table name + column name → read data**
- Understand **salesforce: custom apex exposed via aura api; "without sharing" = system context → ignores access controls**
- Understand **entering saas security: pool money with other hackers for a production license ($20k/mo for enterprise saas)**
- Understand **legacy/deprecated apis are gold — undocumented, often still functional, no security review**

#### 3. Core concepts explained
**ServiceNow Widget Data Exposure**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Salesforce Object/Apex Exposure**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**AppCache Manifest + Cookie Bombing for File Access**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SaaS misconfiguration pattern**
- Platform provides API endpoints (widgets, components). Customer must configure access controls. Most don't. Finding undocumented/legacy endpoints and testing access controls = infinite bug class.

**ServiceNow widget enumeration**
- Schema has hundreds of tables. Legacy widgets (simple list, unordered list, data brokers) accept user-supplied table+column names.

**Salesforce Apex discovery**
- Reverse-engineer JavaScript on Digital Experience → find Aura-enabled Apex methods → call directly. Look for "without sharing" classes.


#### 4. Techniques and tactics
**SaaS misconfiguration pattern**
- **What it is:** Platform provides API endpoints (widgets, components). Customer must configure access controls. Most don't. Finding undocumented/legacy endpoints and testing access controls = infinite bug class.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**ServiceNow widget enumeration**
- **What it is:** Schema has hundreds of tables. Legacy widgets (simple list, unordered list, data brokers) accept user-supplied table+column names.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Salesforce Apex discovery**
- **What it is:** Reverse-engineer JavaScript on Digital Experience → find Aura-enabled Apex methods → call directly. Look for "without sharing" classes.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Named credential brute-force**
- **What it is:** With "execute anonymous" API access (even low-priv community user), brute-force common named credential labels to piggyback on shared API credentials.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**AppCache + Cookie bombing**
- **What it is:** Upload AppCache manifest with fallback → cookie-bomb viewer → fallback fires → exfiltrate data.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Never approach platforms with the intent of hacking. Become an expert on the platform and its functionality first."* — **Aaron Costello**
- *"Legacy is where the gold is. All the AI stuff is hip and trendy, but let's not forget the stuff that's been sitting there 10-15 years."* — **Aaron Costello**
- *"I've probably compromised 100x what threat actors are compromising via supply chain"* — **through authorized bug bounty platforms." — Aaron Costello**
- *"For ServiceNow: UX data brokers, UI builder, any API endpoint that returns data"* — **play with those." — Aaron Costello**
- *"Three things for Salesforce: 1) misconfigured object access 2) custom Apex exposed as API 3) privilege escalation by signing up."* — **Aaron Costello**

#### 6. Mental models
- **Never approach platforms with the intent of hacking. Become ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Legacy is where the gold is. All the AI stuff is hip and tre** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I've probably compromised 100x what threat actors are compro** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** SaaS misconfigurations > zero-days: you find the pattern once, apply across unlimited targets
- **Try this:** ServiceNow: "widgets" (simple list, unordered list, data brokers) are API endpoints that accept table name + column name → read data
- **Try this:** Salesforce: custom Apex exposed via Aura API; "without sharing" = system context → ignores access controls
- **Try this:** Entering SaaS security: pool money with other hackers for a production license ($20K/mo for enterprise SaaS)

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Salesforce fixed some Apex-specific issues (custom settings restriction added). Blog payloads from 2020 still work today.

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in ServiceNow Widget Data Exposure?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **SaaS misconfigurations are a bug class: same payload works across 1000s of compa**
2. **SaaS misconfigurations > zero-days: you find the pattern once, apply across unli**
3. **ServiceNow: "widgets" (simple list, unordered list, data brokers) are API endpoi**
