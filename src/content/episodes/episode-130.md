---
title: "Minecraft Hacks to Google Hacking Star — Valentino"
episode: 130
---


# Episode 130 Minecraft Hacks to Google Hacking Star — Valentino

**Source:** Show notes (feed) — condensed, detailed bug descriptions.

### TL;DR
- Valentino: Tomcat JMXProxy RCE, HTML sanitizer bypass, Vertex AI command injection.
- .NET deserialization, argument injection to LFR, "free after use".
- Abstract thinking: close proxy, use UI/creative scenarios.
- HTML sanitizer bypass via multiple open `<p>` tags.

### Key takeaways
- [ ] Tomcat reverse proxy: `../;` (Orange Tsai path normalization) bypasses proxy → JMXProxy RCE via log poisoning.
- [ ] HTML sanitizer: nest many open `<p>` tags before XSS payload — depth/allowlist exhaustion.
- [ ] Command injection via content injection in code generation features.
- [ ] "Free after use" — resource becomes public after owner accesses it.
- [ ] File extension bypass: `#` (hash) or `?` in filename — URI truncation.

### Bugs and Findings

#### Tomcat JMXProxy RCE — RCE
- **Technique:** `../;` path normalization bypasses reverse proxy. JMXProxy with default creds allows log poisoning.
- **Exploitation:**
  1. `http://target/..;/manager/html` bypasses proxy.
  2. JMXProxy allows MBean operations; log poison → RCE.
- **Impact / severity / bounty:** Full RCE.

#### MercadoLibre HTML Sanitizer Bypass — XSS
- **Technique:** Nested `<p>` tags exhaust depth tracking → XSS. Later replaced with DOMPurify.
- **Impact / severity / bounty:** Stored XSS.

#### Command Injection in Vertex AI — RCE
- **Technique:** Image URL in prompt injects commands into "get code" output (curl/bash).
- **Exploitation:** Upload prompt with injected URL → victim uses "get code" → generated code has injected command.
- **Key detail:** `\n` in URL breaks out of JSON string; multi-context (JSON → curl → bash).
- **Impact / severity / bounty:** Code execution on developer's machine.

#### "Free After Use" — Authorization bypass
- **Technique:** Owner accesses resource → everyone can access it (like web cache deception).
- **Impact / severity / bounty:** Unauthorized data access.

### Techniques and Primitives
- **Semicolon path normalization** — `../;` bypasses reverse proxies.
- **Nesting depth exhaustion** — Stack open tags to exhaust sanitizer.
- **Content injection in code generation** — Inject into generated scripts via metadata.
- **URI parser truncation** — `#` or `?` in filename for extension bypass.

### Suggestions and Advices from Hunter
- "Close your proxy and think creatively. Find patterns, break stuff."
- "Abstract thinking > knowing every detail. Be comfortable guessing."
- "I find bugs in one application for two years. Most bugs came in a three-month window when I understood it like a user."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Valentino: Tomcat JMXProxy RCE, HTML sanitizer bypass, Vertex AI command injection.

#### 2. What you should learn
- Understand **[ ] tomcat reverse proxy: `../;` (orange tsai path normalization) bypasses proxy → jmxproxy rce via log poisoning**
- Understand **[ ] html sanitizer: nest many open `<p>` tags before xss payload — depth/allowlist exhaustion**
- Understand **[ ] command injection via content injection in code generation features**
- Understand **[ ] "free after use" — resource becomes public after owner accesses it**
- Understand **[ ] file extension bypass: `#` (hash) or `?` in filename — uri truncation**

#### 3. Core concepts explained
**Tomcat JMXProxy RCE — RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**MercadoLibre HTML Sanitizer Bypass — XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Command Injection in Vertex AI — RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Semicolon path normalization**
- `../;` bypasses reverse proxies.

**Nesting depth exhaustion**
- Stack open tags to exhaust sanitizer.

**Content injection in code generation**
- Inject into generated scripts via metadata.


#### 4. Techniques and tactics
**Semicolon path normalization**
- **What it is:** `../;` bypasses reverse proxies.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Nesting depth exhaustion**
- **What it is:** Stack open tags to exhaust sanitizer.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Content injection in code generation**
- **What it is:** Inject into generated scripts via metadata.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**URI parser truncation**
- **What it is:** `#` or `?` in filename for extension bypass.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Close your proxy and think creatively. Find patterns, break stuff."*
- *"Abstract thinking > knowing every detail. Be comfortable guessing."*
- *"I find bugs in one application for two years. Most bugs came in a three-month window when I understood it like a user."*

#### 6. Mental models
- **Close your proxy and think creatively. Find patterns, break ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Abstract thinking > knowing every detail. Be comfortable gue** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I find bugs in one application for two years. Most bugs came** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Tomcat reverse proxy: `../;` (Orange Tsai path normalization) bypasses proxy → JMXProxy RCE via log poisoning.
- **Try this:** [ ] HTML sanitizer: nest many open `<p>` tags before XSS payload — depth/allowlist exhaustion.
- **Try this:** [ ] Command injection via content injection in code generation features.
- **Try this:** [ ] "Free after use" — resource becomes public after owner accesses it.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **deserialization** — Converting serialized data back into objects — dangerous if attacker-controlled

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Tomcat JMXProxy RCE — RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Valentino: Tomcat JMXProxy RCE, HTML sanitizer bypass, Vertex AI command injecti**
2. **[ ] Tomcat reverse proxy: `../;` (Orange Tsai path normalization) bypasses proxy**
3. **[ ] HTML sanitizer: nest many open `<p>` tags before XSS payload — depth/allowli**
