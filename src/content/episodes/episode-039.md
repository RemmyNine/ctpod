---
title: "The Art of Architectures"
episode: 39
---


# Episode 39 The Art of Architectures

### TL;DR
- Deep comparison of SPA+API vs traditional (direct endpoint) web architectures
- gRPC/protobuf hacking is painful but systematic — reverse engineer proto files for Burp
- Microservices + reverse proxy architecture creates secondary context and perimeter injection bugs
- JWT `alg: none` token accepted on a real target (first time for Justin)

### Key takeaways
- SPA + REST API: auth bearer tokens reach client side → XSS = instant ATO; stored/reflected XSS rarer, DOM-based XSS common
- Traditional architecture: more stored/reflected XSS, CSRF, web cache deception; content enumeration is critical
- Microservices: test every endpoint for path traversal in secondary context; look for discrepancies in error messages, headers, server banners between services
- gRPC: reverse engineer proto files by figuring out field numbers, then load into Burp for automated decode

### Bugs and Findings
#### JWT "alg: none" Acceptance
- **Target/context:** A specific endpoint found during a live hacking event
- **Root cause:** Server accepted JWT with `"alg":"none"` — no signature verification
- **Technique / how found:** Used JWT editor/attacker Burp extensions to modify algorithm to `none` with various capitalizations (none, None, NONE)
- **Key technical details:** JWT without signature passes validation on a real production endpoint — first such finding in Justin's career
- **Impact / severity / bounty:** Complete account takeover (arbitrary user impersonation)

#### Open Redirect -> OAuth Account Takeover (Evan Connolly — Tesla)
- **Target/context:** Tesla Retail Tool (TRT)
- **Root cause:** External IDP (used by everyone) didn't require email verification; could register with ex-employee's email
- **Technique / how found:**
  1. Found ex-employee email on LinkedIn (employee left company but account might still exist)
  2. Registered that email on Tesla's external IDP (no ownership verification)
  3. Used it to SSO into Tesla Retail Tool — got internal access
- **Impact / severity / bounty:** Access to internal Tesla sites and data

### Techniques and Primitives
- **Secondary context path traversal** — inject `../` into an ID/parameter passed to a backend microservice; can hit internal API endpoints
- **Perimeter injection** — inject `%26` (ampersand), `?` or `#` into parameters that get forwarded to third-party APIs, appending or truncating parameters
- **Request smuggling** in reverse proxy chains — different servers parse boundaries differently
- **gRPC proto reverse engineering** — identify field numbers, write `.proto` file, load into Burp

### Suggestions and Advices from Hunter
- "If you have an XSS in a SPA, it typically results in ATO because the auth bearer is accessible from JS"
- "Content enumeration is the OG art — Jay (Haze) has a whole system for it"
- On HTMX: "If a dev says the word HTMX, schedule a mandatory meeting with security"

### AI Takeaway
The secondary context bug class (injecting into parameters that become part of an internal request path) is one of the most high-impact, under-exploited vulnerability classes in microservice architectures.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Deep comparison of SPA+API vs traditional (direct endpoint) web architectures

#### 2. What you should learn
- Understand **spa + rest api: auth bearer tokens reach client side → xss = instant ato; stored/reflected xss rarer, dom-based xss common**
- Understand **traditional architecture: more stored/reflected xss, csrf, web cache deception; content enumeration is critical**
- Understand **microservices: test every endpoint for path traversal in secondary context; look for discrepancies in error messages, headers, server banners between services**
- Understand **grpc: reverse engineer proto files by figuring out field numbers, then load into burp for automated decode**

#### 3. Core concepts explained
**JWT "alg: none" Acceptance**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Open Redirect -> OAuth Account Takeover (Evan Connolly — Tesla)**
- **What it is:** An application redirects users to an attacker-controlled URL, often used in phishing or to bypass OAuth flows.
- **Why it matters:** Open redirects are building blocks for credential theft and OAuth token theft chains.
- **Common mistake:** Dismissing open redirects as low severity — they're critical links in high-impact attack chains.

**Secondary context path traversal**
- inject `../` into an ID/parameter passed to a backend microservice; can hit internal API endpoints

**Perimeter injection**
- inject `%26` (ampersand), `?` or `#` into parameters that get forwarded to third-party APIs, appending or truncating parameters

**Request smuggling in reverse proxy chains**
- different servers parse boundaries differently


#### 4. Techniques and tactics
**Secondary context path traversal**
- **What it is:** inject `../` into an ID/parameter passed to a backend microservice; can hit internal API endpoints
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Perimeter injection**
- **What it is:** inject `%26` (ampersand), `?` or `#` into parameters that get forwarded to third-party APIs, appending or truncating parameters
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Request smuggling in reverse proxy chains**
- **What it is:** different servers parse boundaries differently
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**gRPC proto reverse engineering**
- **What it is:** identify field numbers, write `.proto` file, load into Burp
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have an XSS in a SPA, it typically results in ATO because the auth bearer is accessible from JS"*
- *"Content enumeration is the OG art"* — **Jay (Haze) has a whole system for it**
- *"On HTMX: "If a dev says the word HTMX, schedule a mandatory meeting with security"*

#### 6. Mental models
- **If you have an XSS in a SPA, it typically results in ATO bec** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Content enumeration is the OG art — Jay (Haze) has a whole s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On HTMX: "If a dev says the word HTMX, schedule a mandatory ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** SPA + REST API: auth bearer tokens reach client side → XSS = instant ATO; stored/reflected XSS rarer, DOM-based XSS common
- **Try this:** Traditional architecture: more stored/reflected XSS, CSRF, web cache deception; content enumeration is critical
- **Try this:** Microservices: test every endpoint for path traversal in secondary context; look for discrepancies in error messages, headers, server banners between services
- **Try this:** gRPC: reverse engineer proto files by figuring out field numbers, then load into Burp for automated decode

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **API** — Application Programming Interface — structured endpoints for data exchange
- **JWT** — JSON Web Token — compact token format for authentication
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in JWT "alg: none" Acceptance?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Deep comparison of SPA+API vs traditional (direct endpoint) web architectures**
2. **SPA + REST API: auth bearer tokens reach client side → XSS = instant ATO; stored**
3. **Traditional architecture: more stored/reflected XSS, CSRF, web cache deception; **
