---
title: "AI Security, Hacking WiFi, the New XSS Hunter, and more"
episode: 5
---


# Episode 5 AI Security, Hacking WiFi, the New XSS Hunter, and more

### TL;DR
- New XSS Hunter by Truffle Security (partnered with original XSS Hunter author mandatory)
- ChatGPT for JS file analysis: deminification, source/sink identification, assembly code reverse engineering
- MD5 hash collisions are trivial to generate (seconds); SHA-1 collisions computationally expensive (~$11k)
- First collab report between Justin and Joel (5 years ago): hardcoded encrypted secrets in Android app, decrypted by running Java locally
- Joel's first bug: WiFi hotspot device RCE via LFI → CGI script with command injection

### Key takeaways
- XSS Hunter payloads: prefix with a unique marker string to identify which input triggered the callback
- Save All Resources Chrome extension to bulk-download JS files from DevTools
- Resource Override Chrome extension to override JS/CSS with local files for rapid testing
- Source maps (`.map` files) can reveal full original TypeScript/JS source code — use tools to unpack locally
- MD5 collisions: use `hashcollision` tool to generate collisions in seconds
- ChatGPT: use for assembly code analysis (describes what it does), basic Python scripting; NOT for arbitrary encoding/decoding
- When hashes are used for resource deduplication, MD5 collision can lead to overwriting others' data

### Bugs and Findings

#### [Historical, 2018] WiFi Hotspot Device RCE
- **Target/context:** In-car WiFi hotspot device
- **Root cause:** Known CVE on a shared codebase; CGI script with `sprintf()` call: user input → pipe/semicolons → command injection
- **Technique / how found:**
  1. Found web interface at 192.168.x.x
  2. Googled unique endpoints → found existing CVEs on Exploit DB for same paths
  3. One CVE was an LFI; used it to read filesystem
  4. Found CGI script that called `sprintf()` with user input → command injection
- **Exploitation steps:**
  1. Connect to device's WiFi network
  2. Send semicolon + pipe + commands via vulnerable parameter
  3. Achieve RCE on device
- **Key technical details:** LFI → discover CGI scripts → `sprintf()` with semicolon injection → system call
- **Impact / severity / bounty:** Local network RCE
- **Obstacles & how solved:** Had no hardware tools; solved by using known CVE/LFI to explore filesystem

#### Hardcoded Encrypted Secrets in Android App — Credential Disclosure
- **Target/context:** Undisclosed Android app
- **Root cause:** API keys/credentials stored encrypted in the app with custom encryption; decryption key also in the app
- **Technique / how found:** Decompiled APK with APKTool, saw encrypted strings; traced decryption to custom crypto class; Joel suggested copying the Java class, stripping Android-specific imports, running locally on JVM
- **Exploitation steps:**
  1. Decompile APK, find encrypted credentials
  2. Extract Java decryptor class
  3. Remove Android dependencies (Logcat, etc.)
  4. Run locally on JVM → plaintext credentials
- **Impact / severity / bounty:** Access to user information
- **Obstacles & how solved:** Custom encryption blocked straightforward decompilation; solved by running Java directly on desktop JVM

### Techniques and Primitives
- **XSS Hunter payload tagging** — prefix payload with unique string to correlate callback to input location
- **Source map extraction** — download `.map` file, use `source-map` tool to recover original TypeScript/JS
- **Resource Override** — replace JS/CSS with local copies during dynamic analysis
- **MD5 collision for resource dedup bypass** — find where uploaded content is MD5'd for dedup, collide with another resource
- **ChatGPT for assembly analysis** — dump assembly into ChatGPT, ask "what does this do?"

### Tooling and Resources
- XSS Hunter (new version by Truffle Security)
- Save All Resources (Chrome extension)
- Resource Override (Chrome extension)
- hashcollision tool (GitHub)
- ChatGPT / OpenAI
- curlconverter.com
- Franz "postMessage tracker" Chrome extension

### Suggestions and Advices from Hunter
- "Use unique numbers/strings with XSS payloads so you can identify which field triggered it" — Justin
- "Always Google random strings you find in applications" — Joel on discovering shared codebases
- "Source maps: check if Chrome auto-unpacks them in the sources tab" — Justin
- "If you don't know the encoding, use CyberChef to test various decodings" — Joel

### AI Takeaway
The single highest-leverage takeaway is the systematic Google-search technique: when you find a unique error message, endpoint, or string in an application, search it verbatim. This consistently uncovers shared codebases, known CVEs, open-source repos, and developer training materials.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
New XSS Hunter by Truffle Security (partnered with original XSS Hunter author mandatory)

#### 2. What you should learn
- Understand **xss hunter payloads: prefix with a unique marker string to identify which input triggered the callback**
- Understand **save all resources chrome extension to bulk-download js files from devtools**
- Understand **resource override chrome extension to override js/css with local files for rapid testing**
- Understand **source maps (`.map` files) can reveal full original typescript/js source code — use tools to unpack locally**
- Understand **md5 collisions: use `hashcollision` tool to generate collisions in seconds**

#### 3. Core concepts explained
**[Historical, 2018] WiFi Hotspot Device RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Hardcoded Encrypted Secrets in Android App — Credential Disclosure**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**XSS Hunter payload tagging**
- prefix payload with unique string to correlate callback to input location

**Source map extraction**
- download `.map` file, use `source-map` tool to recover original TypeScript/JS

**Resource Override**
- replace JS/CSS with local copies during dynamic analysis


#### 4. Techniques and tactics
**XSS Hunter payload tagging**
- **What it is:** prefix payload with unique string to correlate callback to input location
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Source map extraction**
- **What it is:** download `.map` file, use `source-map` tool to recover original TypeScript/JS
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Resource Override**
- **What it is:** replace JS/CSS with local copies during dynamic analysis
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**MD5 collision for resource dedup bypass**
- **What it is:** find where uploaded content is MD5'd for dedup, collide with another resource
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**ChatGPT for assembly analysis**
- **What it is:** dump assembly into ChatGPT, ask "what does this do?"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Use unique numbers/strings with XSS payloads so you can identify which field triggered it"* — **Justin**
- *"Always Google random strings you find in applications"* — **Joel on discovering shared codebases**
- *"Source maps: check if Chrome auto-unpacks them in the sources tab"* — **Justin**
- *"If you don't know the encoding, use CyberChef to test various decodings"* — **Joel**

#### 6. Mental models
- **Use unique numbers/strings with XSS payloads so you can iden** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Always Google random strings you find in applications" — Joe** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Source maps: check if Chrome auto-unpacks them in the source** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** XSS Hunter payloads: prefix with a unique marker string to identify which input triggered the callback
- **Try this:** Save All Resources Chrome extension to bulk-download JS files from DevTools
- **Try this:** Resource Override Chrome extension to override JS/CSS with local files for rapid testing
- **Try this:** Source maps (`.map` files) can reveal full original TypeScript/JS source code — use tools to unpack locally

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Had no hardware tools; solved by using known CVE/LFI to explore filesystem
- - Obstacles & how solved: Custom encryption blocked straightforward decompilation; solved by running Java directly on desktop JVM

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in [Historical, 2018] WiFi Hotspot Device RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **New XSS Hunter by Truffle Security (partnered with original XSS Hunter author ma**
2. **XSS Hunter payloads: prefix with a unique marker string to identify which input **
3. **Save All Resources Chrome extension to bulk-download JS files from DevTools**
