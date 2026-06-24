---
title: "Headless Browser SSRF & RebindMultiA Tool Release + Web3 Bug"
episode: 9
---


# Episode 9 Headless Browser SSRF & RebindMultiA Tool Release + Web3 Bug

### TL;DR
- RebindMultiA tool release: DNS rebinding using multi-A record fallback behavior on Windows (works on Chrome, Firefox, Edge on Windows)
- Headless browser SSRF: inject HTML/JS into PDF generation → SSRF → potential AWS metadata / internal pivoting
- Multi-A DNS rebinding: list two A records (public IP + private IP/127.0.0.1); when first IP fails to respond, browser falls back to second
- Web3 bug: unauthenticated JSON-RPC method to reset entire node (development endpoint left on production)
- ChatGPT API release: bug bounty potential on AI integrations

### Key takeaways
- Headless browser SSRF: find HTML injection points in PDF/image generation; use `<script>`, `<img>`, `<iframe>` for SSRF
- For blind SSRF in headless browsers, use DNS rebinding to bypass localhost restrictions
- Multi-A rebinding (Windows only): two A records — first IP = attacker server, second = 127.0.0.1; when attacker kills connection, browser falls back to localhost
- RebindMultiA tool: `python3 rebindmultiA.py`; domain format: `<target-ip>.ns.<vps-ip>.rebindmultia.com`
- Chrome DevTools Protocol on port 9222: `GET /json/new?url=DATA` opens arbitrary URL, useful for popup bypass
- WC3 Broadcast Channel API: cross-tab communication without postMessage
- Stalling HTTP response for headless browser: send headers with `Content-Length: 1` but no body — buys ~15 seconds

### Bugs and Findings

#### Web3 RPC Server — Unauthenticated Node Reset
- **Target/context:** Web3 RPC server (2018)
- **Root cause:** Development method (`reset`) left enabled on production RPC
- **Technique / how found:** Read open source RPC server source code; enumerated JSON-RPC methods
- **Key technical details:** JSON-RPC call to reset method with no authentication
- **Impact / severity / bounty:** Node reset — full denial of service [inferred]

#### PayPal SSTI — Server-Side Template Injection → CVE-2020-12668
- **Target/context:** PayPal payment flow (paypal.com)
- **Root cause:** Gin Java template engine before 2.5.4 allowed injecting into templates; arbitrary Java method invocation
- **Technique / how found:** Fisher sent Justin a PayPal transfer with `{{7*7}}` in the note; notification rendered the template → `49` appeared. Chained to LFI.
- **Exploitation steps:**
  1. Send payment with template injection payload in memo/note field
  2. Confirmed SSTI: `{{7*7}}` → `49`
  3. Leveraged Gin Java SSTI to call arbitrary Java methods → read file `/etc/passwd`
- **Key technical details:** Gin Java < 2.5.4 SSTI; `{{constructor}}`-style payloads; CVE-2020-12668
- **Impact / severity / bounty:** $26,000 (Critical)
- **Obstacles & how solved:** Found entirely by accident via payment notification

### Techniques and Primitives
- **Multi-A DNS rebinding (Windows)** — two A records, first fails, browser falls back to second (localhost)
- **Headless browser SSRF** — inject HTML/JS into PDF/image generation; use `<script>` tags for SSRF
- **HTTP stall technique** — send headers with `Content-Length: 1` but no body; different timeout than connection timeout
- **Chrome DevTools Protocol popup bypass** — `GET /json/new?url=<url>` circumvents popup restrictions
- **WC3 BroadcastChannel API** — cross-tab/window communication via `new BroadcastChannel('name')`

### Tooling and Resources
- RebindMultiA (GitHub: runnerator/rebindmultia)
- Singularity (NCC Group DNS rebinding tool)
- whonow (Brandon Dorsey's DNS rebinding service)
- DNSchef (DNS spoofing tool)
- Caido
- ChatGPT APIs (released for public use)

### Suggestions and Advices from Hunter
- "If you have a headless browser, try CRLF injection in URL path to smuggle HTTP requests" — Justin
- "Research what specific library is rendering PDFs — read the docs" — Justin on Jonathan Bowman's mpdf LFI technique
- "Use Lo0p's tip: respond with headers but no body to stall HTTP requests" — Justin
- "Try Chromium CVE PoC for headless browser RCE — you don't need full exploit" — Joel

### AI Takeaway
Multi-A DNS rebinding is a Windows-specific bypass of traditional DNS rebinding limitations. Chrome ignores TTL and caches DNS for ~5 minutes, but if the first A-record server goes silent (TCP RST/timeout), the browser will try the second A record. This collapses the rebinding timeframe from minutes to ~RTT.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
RebindMultiA tool release: DNS rebinding using multi-A record fallback behavior on Windows (works on Chrome, Firefox, Edge on Windows)

#### 2. What you should learn
- Understand **headless browser ssrf: find html injection points in pdf/image generation; use `<script>`, `<img>`, `<iframe>` for ssrf**
- Understand **for blind ssrf in headless browsers, use dns rebinding to bypass localhost restrictions**
- Understand **multi-a rebinding (windows only): two a records — first ip = attacker server, second = 127.0.0.1; when attacker kills connection, browser falls back to localhost**
- Understand **rebindmultia tool: `python3 rebindmultia.py`; domain format: `<target-ip>.ns.<vps-ip>.rebindmultia.com`**
- Understand **chrome devtools protocol on port 9222: `get /json/new?url=data` opens arbitrary url, useful for popup bypass**

#### 3. Core concepts explained
**Web3 RPC Server — Unauthenticated Node Reset**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**PayPal SSTI — Server-Side Template Injection → CVE-2020-12668**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Multi-A DNS rebinding (Windows)**
- two A records, first fails, browser falls back to second (localhost)

**Headless browser SSRF**
- inject HTML/JS into PDF/image generation; use `<script>` tags for SSRF

**HTTP stall technique**
- send headers with `Content-Length: 1` but no body; different timeout than connection timeout


#### 4. Techniques and tactics
**Multi-A DNS rebinding (Windows)**
- **What it is:** two A records, first fails, browser falls back to second (localhost)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Headless browser SSRF**
- **What it is:** inject HTML/JS into PDF/image generation; use `<script>` tags for SSRF
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**HTTP stall technique**
- **What it is:** send headers with `Content-Length: 1` but no body; different timeout than connection timeout
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Chrome DevTools Protocol popup bypass**
- **What it is:** `GET /json/new?url=<url>` circumvents popup restrictions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WC3 BroadcastChannel API**
- **What it is:** cross-tab/window communication via `new BroadcastChannel('name')`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have a headless browser, try CRLF injection in URL path to smuggle HTTP requests"* — **Justin**
- *"Research what specific library is rendering PDFs"* — **read the docs" — Justin on Jonathan Bowman's mpdf LFI technique**
- *"Use Lo0p's tip: respond with headers but no body to stall HTTP requests"* — **Justin**
- *"Try Chromium CVE PoC for headless browser RCE"* — **you don't need full exploit" — Joel**

#### 6. Mental models
- **If you have a headless browser, try CRLF injection in URL pa** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Research what specific library is rendering PDFs — read the ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use Lo0p's tip: respond with headers but no body to stall HT** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Headless browser SSRF: find HTML injection points in PDF/image generation; use `<script>`, `<img>`, `<iframe>` for SSRF
- **Try this:** For blind SSRF in headless browsers, use DNS rebinding to bypass localhost restrictions
- **Try this:** Multi-A rebinding (Windows only): two A records — first IP = attacker server, second = 127.0.0.1; when attacker kills connection, browser falls back to localhost
- **Try this:** RebindMultiA tool: `python3 rebindmultiA.py`; domain format: `<target-ip>.ns.<vps-ip>.rebindmultia.com`

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Found entirely by accident via payment notification

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **API** — Application Programming Interface — structured endpoints for data exchange
- **DNS** — Domain Name System — translates domain names to IP addresses
- **AWS metadata** — Cloud instance metadata service at 169.254.169.254 — contains IAM credentials

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Web3 RPC Server — Unauthenticated Node Reset?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **RebindMultiA tool release: DNS rebinding using multi-A record fallback behavior **
2. **Headless browser SSRF: find HTML injection points in PDF/image generation; use `**
3. **For blind SSRF in headless browsers, use DNS rebinding to bypass localhost restr**
