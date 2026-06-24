---
title: "2x Google RCE with VRP Legend BruteCat"
episode: 177
---


# Episode 177 2x Google RCE with VRP Legend BruteCat

### TL;DR
- Google RCE #1: Found `listWorkflowExecutionLogs` leaking internal workflow logs → found `GenericStubbyTypeTaskV2` in discovery doc → created workflow with leaked `clientID: default` → bypassed approval via ACL trick → achieved arbitrary stubby RPC execution
- Google RCE #2: Application Integration API IDOR — filter injection leaked integration test cases → binary search via AIP-160 filter to extract integration UID → found staging environment bypassed patches that prod had
- First-party auth via `client6.google.com` alias with specific origin/referer headers
- Key header: `x-goog-encode-response-if-executable` converts raw Protobuf to base64 for client6 compatibility

### Key Takeaways
- [ ] Google SRE handbook and BeyondProd are essential reading for Google infrastructure hacking
- [ ] First-party auth via client6 works for APIs that have the `client6.google.com` alias (~90% of APIs that have it)
- [ ] AIP-160 filter language (`clientID > 12345`) supports binary search for data exfiltration — test any filter parameter
- [ ] Staging environments often bypass prod fixes — if an endpoint is patched in prod, check staging (different DNS load balancer)
- [ ] Splitting reports on Google: wait for fix on first bug before reporting second related one to avoid lumping

### Bugs and Findings

#### Google RCE #1 — Cloud CRM API → Stubby RCE
- **Target/context:** Google Cloud CRM API (production)
- **Root cause:** `GenericStubbyTypeTaskV2` endpoint in workflow execution API — allows executing arbitrary stubby RPC calls internally
- **Technique:** 1) Leaked workflow execution logs via `listCodeIq` endpoint 2) Found `clientID: default` in logs — used to create workflow 3) Stuck on publish approval — collaborator found ACL endpoint to add another user (approver) 4) Used `application-integration` public GCP product to discover stubby parameters 5) Found GSLB address (`alkali-bases`) for stubby target 6) Executed workflow → arbitrary stubby RPC
- **Key technical details:** `x-goog-encode-response-if-executable: base64` header converts Protobuf response; `genericStubbyTypeTaskV2` in discovery doc; system DNS alias (`1e100.net`) for regional patching differences
- **Impact / severity / bounty:** RCE on Google production — $75K (highly privileged production user)

**Obstacles & how solved:** Stuck for a month on publish approval; randomly found collaborator in Discord who had the same API but knew different bypasses (ACL modification, app integration parameters)

#### Google RCE #2 — Application Integration IDOR + Filter Injection
- **Target/context:** Google Cloud Application Integration API
- **Root cause:** Test case listing endpoint leaked all users' test cases when filter parameter removed; filter supported AIP-160 with binary search
- **Technique:** 1) Found `workflowID` was client-side filter — removing it dumped all test cases 2) Couldn't extract integration UID directly 3) Used known test case + filter binary search to extract UID character by character 4) Once UID obtained, full IDOR on all integrations 5) Created integration with `stubbyTypeTask` on staging (patching rolled slowly by region)
- **Key technical details:** AIP-160 filter language supports `clientID > value` comparisons — enables binary search; decrypted Protobuf revealed `workflowID` being client-controlled
- **Impact / severity / bounty:** Full IDOR over all Google Cloud Application Integrations → attempted stubby execution → $75K

### Techniques and Primitives
- **Binary search via AIP-160 filter** — `field > value` / `field < value` comparisons enable character-by-character UID extraction
- **`x-goog-encode-response-if-executable: base64`** — Converts raw binary Protobuf to base64 for compatibility with first-party auth endpoints
- **client6.google.com first-party auth** — Cookie-based auth requiring correct `Origin` and `Referer` headers from an allowlist
- **GSLB address alias** — Internal Google service load balancer addresses (like `alkali-bases`) expose internal APIs
- **Staging vs prod load balancer bypass** — Prod fixes apply gradually by region; staging environments may still have vulnerable code
- **Report splitting strategy** — Wait for fix on first bug before reporting second related one to avoid lumping; maximize total bounty

### Tooling and Resources
- BruteCat's Request to Proto tool — error-based oracle for Protobuf structure discovery
- Google SRE Handbook
- BeyondProd whitepaper
- bratecat.com/hunt — BruteCat's consulting
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Google RCE #1: Found `listWorkflowExecutionLogs` leaking internal workflow logs → found `GenericStubbyTypeTaskV2` in discovery doc → created workflow with leaked `clientID: default` → bypassed approval via ACL trick → achieved arbitrary stubby RPC execution

#### 2. What you should learn
- Understand **[ ] google sre handbook and beyondprod are essential reading for google infrastructure hacking**
- Understand **[ ] first-party auth via client6 works for apis that have the `client6.google.com` alias (~90% of apis that have it)**
- Understand **[ ] aip-160 filter language (`clientid > 12345`) supports binary search for data exfiltration — test any filter parameter**
- Understand **[ ] staging environments often bypass prod fixes — if an endpoint is patched in prod, check staging (different dns load balancer)**
- Understand **[ ] splitting reports on google: wait for fix on first bug before reporting second related one to avoid lumping**

#### 3. Core concepts explained
**Google RCE #1 — Cloud CRM API → Stubby RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Google RCE #2 — Application Integration IDOR + Filter Injection**
- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.
- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.
- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.

**Binary search via AIP-160 filter**
- `field > value` / `field < value` comparisons enable character-by-character UID extraction

**`x-goog-encode-response-if-executable: base64`**
- Converts raw binary Protobuf to base64 for compatibility with first-party auth endpoints

**client6.google.com first-party auth**
- Cookie-based auth requiring correct `Origin` and `Referer` headers from an allowlist


#### 4. Techniques and tactics
**Binary search via AIP-160 filter**
- **What it is:** `field > value` / `field < value` comparisons enable character-by-character UID extraction
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`x-goog-encode-response-if-executable: base64`**
- **What it is:** Converts raw binary Protobuf to base64 for compatibility with first-party auth endpoints
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**client6.google.com first-party auth**
- **What it is:** Cookie-based auth requiring correct `Origin` and `Referer` headers from an allowlist
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**GSLB address alias**
- **What it is:** Internal Google service load balancer addresses (like `alkali-bases`) expose internal APIs
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Staging vs prod load balancer bypass**
- **What it is:** Prod fixes apply gradually by region; staging environments may still have vulnerable code
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
- **Try this:** [ ] Google SRE handbook and BeyondProd are essential reading for Google infrastructure hacking
- **Try this:** [ ] First-party auth via client6 works for APIs that have the `client6.google.com` alias (~90% of APIs that have it)
- **Try this:** [ ] AIP-160 filter language (`clientID > 12345`) supports binary search for data exfiltration — test any filter parameter
- **Try this:** [ ] Staging environments often bypass prod fixes — if an endpoint is patched in prod, check staging (different DNS load balancer)

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **DNS** — Domain Name System — translates domain names to IP addresses
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Google RCE #1 — Cloud CRM API → Stubby RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Google RCE #1: Found `listWorkflowExecutionLogs` leaking internal workflow logs **
2. **[ ] Google SRE handbook and BeyondProd are essential reading for Google infrastr**
3. **[ ] First-party auth via client6 works for APIs that have the `client6.google.co**
