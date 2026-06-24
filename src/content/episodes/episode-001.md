---
title: "Introductions, Bug Bounty Reports, and BB Tips"
episode: 1
---


# Episode 1 Introductions, Bug Bounty Reports, and BB Tips

### TL;DR
- GitLab RCE via GitHub import using Sawyer class object injection leading to Redis injection, then to full RCE
- Justin's SSRF on a grocery provider: JS file analysis → hidden signup → IDOR enumeration → remote image URL SSRF → AWS metadata → RCE on 56 EC2 instances
- ADB reverse proxy tip for mobile hacking
- Java class re-use for reversing Android cryptography
- Chrome DevTools Protocol remote debugging port (9222) as attack surface

### Key takeaways
- Read minified JS files; signup endpoints, hidden routes, and admin cookies can be found there
- When you encounter an S3 file upload, find where the file lands (other upload endpoints often reveal the bucket)
- Always hit AWS metadata endpoint `169.254.169.254` on SSRF; also check `/latest/user-data`
- Use `adb reverse tcp:8080 tcp:8080` to tunnel Burp through USB — bypasses Wi-Fi proxy issues
- For Android reversing: convert DEX → JAR, drop into classpath, call decryption functions directly in Java
- Use beautifier.io or p-prettier for JS beautification

### Bugs and Findings

#### GitLab RCE via GitHub Import — Deserialization → Redis Injection → RCE
- **Target/context:** GitLab self-hosted, importing repos from GitHub via OctoKit/Sawyer
- **Root cause:** GitLab trusts and misuses the Sawyer class object — ID parameter can be replaced with a crafted Ruby object that injects Redis commands
- **Technique / how found:** Researcher (YVVDWF) analyzed the GitHub import feature, noticed IDs being hashed into cache entries via Sawyer class, found injection point
- **Exploitation steps:**
  1. Import a repo from GitHub; intercept/modify the ID parameter to inject Redis commands via byte-size limiting
  2. Redis injection achieved; outbound blocked by firewall — used `SLAVEOF` to replicate Redis to attacker's server instead
  3. To escalate to RCE: poisoned own GitLab profile/project image with XSS payload that 500'd the page
  4. Used existing Redis gadget (system hook push type) to achieve code execution
- **Key technical details:** Sawyer class in OctoKit; Redis injection via crafted object payload; `SLAVEOF` for exfiltration; system hook push gadget
- **Impact / severity / bounty:** $33,000 (GitLab max bounty)
- **Obstacles & how solved:** Outbound firewall blocked reverse shells; solved by replicating Redis to attacker-controlled server instead

#### Grocery Provider SSRF → AWS Metadata → RCE on 56 Instances
- **Target/context:** Grocery delivery provider's retailer portal (undisclosed)
- **Root cause:** Hidden retailer signup endpoint found in JS files; after signup + password reset, IDOR on product/remote image URL parameter enabled full read SSRF
- **Technique / how found:**
  1. Examined JS files, found hidden signup endpoint
  2. Signed up, did password reset, gained access (no company association)
  3. Mentee started enumerating endpoints from bottom of JS — first hit was a numeric IDOR
  4. Found "add product" endpoint on a different host with a remote image URL parameter
- **Exploitation steps:**
  1. Pop malicious URL into remote image URL param → hit on attacker server
  2. Response returned CloudFront URL (Access Denied), but found the actual S3 bucket from another upload endpoint
  3. Hit `http://169.254.169.254/latest/meta-data/iam/security-credentials/` → got AWS creds
  4. Used creds to access 56 EC2 instances, achieved RCE
- **Key technical details:** AWS metadata IP: `169.254.169.254`; `latest/meta-data/iam/security-credentials/` for IAM creds; also `latest/user-data` for startup scripts
- **Impact / severity / bounty:** RCE on 56 instances; max bounty (amount not disclosed)
- **Obstacles & how solved:** Couldn't find S3 bucket from response; solved by checking other upload endpoints in the app that revealed the bucket name

### Techniques and Primitives
- **JS file enumeration** — search minified JS for hidden endpoints, routes, API schemas
- **AWS metadata SSRF** — from any SSRF, hit `169.254.169.254` for IAM creds and user-data
- **ADB reverse proxy** — `adb reverse tcp:8080 tcp:8080` tunnels Burp to Android device over USB
- **Java class reuse for crypto reversing** — DEX → JAR, place JAR in classpath, call decrypt functions directly from Java/Python
- **307 redirect preservation** — 307 redirect does not change POST to GET; useful for CSRF/XSS chains

### Tooling and Resources
- beautifier.io (JS beautification)
- p-prettier (parallelized JS beautifier, from Mixer team)
- Dex2Jar
- JD-GUI / JADX
- Frida
- Chrome DevTools Protocol (port 9222)
- Burp Copy as Python Requests extension / curlconverter.com
- CyberChef
- Caido (Burp alternative in public beta)

### Suggestions and Advices from Hunter
- "Track your sources and sinks really well" — Justin on finding bugs in import features
- "Look for something dangerous like a command being executed and go backwards to see if there's an entry point" — Joel on source code auditing
- "Throw that payload in your payload list" — Joel on reusing object injection payloads across Ruby on Rails apps
- "Don't be afraid to spend 16-20 hours on a website before reassessing" — Justin on persistence
- "Think about from their perspective what the worst thing that could happen is" — Justin on impact framing
- "You can try as many times as you want, as fast as you wanted" — brute forcing with automation

### AI Takeaway
The Redis SLAVEOF exfiltration technique when outbound is firewalled is a high-leverage primitive for SSRF/Redis injection scenarios. The Java-interop reversing method (DEX→JAR→classpath) is a force multiplier for Android reversing.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
GitLab RCE via GitHub import using Sawyer class object injection leading to Redis injection, then to full RCE

#### 2. What you should learn
- Understand **read minified js files; signup endpoints, hidden routes, and admin cookies can be found there**
- Understand **when you encounter an s3 file upload, find where the file lands (other upload endpoints often reveal the bucket)**
- Understand **always hit aws metadata endpoint `169.254.169.254` on ssrf; also check `/latest/user-data`**
- Understand **use `adb reverse tcp:8080 tcp:8080` to tunnel burp through usb — bypasses wi-fi proxy issues**
- Understand **for android reversing: convert dex → jar, drop into classpath, call decryption functions directly in java**

#### 3. Core concepts explained
**GitLab RCE via GitHub Import — Deserialization → Redis Injection → RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Grocery Provider SSRF → AWS Metadata → RCE on 56 Instances**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**JS file enumeration**
- search minified JS for hidden endpoints, routes, API schemas

**AWS metadata SSRF**
- from any SSRF, hit `169.254.169.254` for IAM creds and user-data

**ADB reverse proxy**
- `adb reverse tcp:8080 tcp:8080` tunnels Burp to Android device over USB


#### 4. Techniques and tactics
**JS file enumeration**
- **What it is:** search minified JS for hidden endpoints, routes, API schemas
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**AWS metadata SSRF**
- **What it is:** from any SSRF, hit `169.254.169.254` for IAM creds and user-data
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**ADB reverse proxy**
- **What it is:** `adb reverse tcp:8080 tcp:8080` tunnels Burp to Android device over USB
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Java class reuse for crypto reversing**
- **What it is:** DEX → JAR, place JAR in classpath, call decrypt functions directly from Java/Python
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**307 redirect preservation**
- **What it is:** 307 redirect does not change POST to GET; useful for CSRF/XSS chains
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Track your sources and sinks really well"* — **Justin on finding bugs in import features**
- *"Look for something dangerous like a command being executed and go backwards to see if there's an entry point"* — **Joel on source code auditing**
- *"Throw that payload in your payload list"* — **Joel on reusing object injection payloads across Ruby on Rails apps**
- *"Don't be afraid to spend 16-20 hours on a website before reassessing"* — **Justin on persistence**
- *"Think about from their perspective what the worst thing that could happen is"* — **Justin on impact framing**
- *"You can try as many times as you want, as fast as you wanted"* — **brute forcing with automation**

#### 6. Mental models
- **Track your sources and sinks really well" — Justin on findin** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Look for something dangerous like a command being executed a** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Throw that payload in your payload list" — Joel on reusing o** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Read minified JS files; signup endpoints, hidden routes, and admin cookies can be found there
- **Try this:** When you encounter an S3 file upload, find where the file lands (other upload endpoints often reveal the bucket)
- **Try this:** Always hit AWS metadata endpoint `169.254.169.254` on SSRF; also check `/latest/user-data`
- **Try this:** Use `adb reverse tcp:8080 tcp:8080` to tunnel Burp through USB — bypasses Wi-Fi proxy issues

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Outbound firewall blocked reverse shells; solved by replicating Redis to attacker-controlled server instead
- - Obstacles & how solved: Couldn't find S3 bucket from response; solved by checking other upload endpoints in the app that revealed the bucket name

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **Burp** — Burp Suite — popular web application security testing proxy
- **Redis** — In-memory data store — often exploitable via SSRF or injection
- **AWS metadata** — Cloud instance metadata service at 169.254.169.254 — contains IAM credentials

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GitLab RCE via GitHub Import — Deserialization → Redis Injection → RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **GitLab RCE via GitHub import using Sawyer class object injection leading to Redi**
2. **Read minified JS files; signup endpoints, hidden routes, and admin cookies can b**
3. **When you encounter an S3 file upload, find where the file lands (other upload en**
