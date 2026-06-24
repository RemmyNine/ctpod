---
title: "SAML XPath Confusion, Chinese DNS Poisoning, and AI Powered 403 Bypasser"
episode: 92
---


# Episode 92 SAML XPath Confusion, Chinese DNS Poisoning, and AI Powered 403 Bypasser

**Hosts:** Justin Gardner (Rhynorater), Joel Margolis (Teknogeek)
**Duration:** 47:38
**Transcript source:** feed (full transcript)

### TL;DR
- Chinese Great Firewall DNS poisoning: ~700 keywords in subdomains cause DNS to resolve to attacker-controllable IPs (including Fastly) → subdomain-takeover-like attacks
- Ruby SAML / GitLab auth bypass via XPath selector confusion — asserting unsigned assertions alongside signed ones
- New tools: CSPBypass.com (community-contributed CSP bypass database), Bebiks' Caido 403 Bypasser plugin (AI-augmented, customizable scan templates)
- MediaTek Wi-Fi chipset 0-click buffer overflow found via Fuzzotron network fuzzer
- Arbitrary read/write on llama.cpp RPC server exposing raw memory primitives

### Key Takeaways
- SAML signature validation XPath selection is a critical single point of failure — check how nodes are selected and whether unsigned assertions can be smuggled alongside signed ones
- DNS poisoning via the Great Firewall of China affects any domain with sensitive subdomain keywords — 700+ known keywords; some poisoned IPs host Fastly proxies allowing registration → subdomain takeover equivalent
- WAF bypass technique: mix encodings (HTML entities + raw characters) to create perception mismatch between WAF and server
- When auditing SAML, check both XPath and XSLT (transformations) — two places where parsing mismatches occur

### Bugs and Findings

#### Ruby SAML / GitLab Authentication Bypass
- **Target/context:** Ruby SAML library (used by GitLab and others)
- **Root cause:** SAML signs a list of assertion hashes, not the full response. XPath selectors choose which assertions to hash. By smuggling an extra assertion whose hash is NOT part of the signed list, but IS checked during validation, an attacker can inject a malicious assertion without invalidating the signature
- **Technique / how found:** Project Discovery research — XPath selector confusion lets you smuggle assertions
- **Key technical details:** SAML assertions are individually hashed → list of hashes is signed. XPath selects nodes for hashing. Unsigned assertions can be inserted elsewhere in the XML without affecting signature validation
- **Impact / severity / bounty:** Full authentication bypass (any SAML identity)
- **Obstacles & how solved:** Required isolating the library from its consumer (GitLab) for testing

#### Great Firewall DNS Poisoning
- **Target/context:** Chinese GFW DNS poisoning
- **Root cause:** DNS queries routed through China get poisoned if the subdomain contains any of ~700+ blocked keywords. Resolves to specific IPs, some of which point to Fastly (CDN) — you can register those domains on Fastly and serve content
- **Technique / how found:** AssetNote research — anomaly detection from customer data
- **Key technical details:** ~700 keywords; poisoned IPs include Fastly edge servers; dnspoison.com has a check tool; some poisoned IPs host Cpanel XSS vulnerabilities
- **Impact / severity / bounty:** Subdomain-takeover-like impact at scale; could serve malicious content on otherwise trusted domains
- **Obstacles & how solved:** China-specific attack surface; committed research over months

#### XSS WAF Bypass — One Payload for All
- **Target/context:** Imperva, Amazon WAF, Akamai
- **Root cause:** WAFs need to handle multiple encoding layers; mixing double-quote (`"`) with HTML entity encoding (`&quot;`) creates parsing mismatch
- **Key technical details:** Payload structure: `x="&quot;"onerror=` — the WAF sees `x="` as attribute start+value, but the HTML parser sees the `&quot;` as the attribute delimiter, making `onerror` a separate attribute
- **Impact / severity / bounty:** XSS across three major WAFs
- **Obstacles & how solved:** The technique is "weaponizing encodings against WAFs" — odd number of quote-like entities creates mismatch

#### Arbitrary Read/Write on llama.cpp RPC Server
- **Target/context:** llama.cpp RPC server (local LLM inference)
- **Root cause:** Unauthenticated RPC server exposing raw memory primitives — `llama.cpp` RPC protocol has just: call-type integer, message length, message. Allows supplying arbitrary memory addresses to read/write on the heap
- **Technique / how found:** SideQuest research — reverse engineering the binary protocol
- **Key technical details:** Simple binary protocol: one integer = call type, message length, then message. Primitives: allocate on heap, read from arbitrary memory address, write to arbitrary memory address
- **Impact / severity / bounty:** Full RCE via crafted Python payload using RPC primitives
- **Obstacles & how solved:** Required understanding binary protocol; proof-of-concept took ~1 hour of work

#### MediaTek Wi-Fi Chipset 0-Click Buffer Overflow
- **Target/context:** MediaTek MT chipsets (6000/7000 series) used in Android and IoT devices
- **Root cause:** Buffer overflow in Wi-Fi chipset driver/SDK
- **Technique / how found:** Fuzzotron (TCP/UDP network fuzzer) — blackbox fuzzing network traffic until crash
- **Key technical details:** Affects MT60xx/MT70xx series chipsets; Python PoC on GitHub
- **Impact / severity / bounty:** 0-click RCE on affected devices
- **Obstacles & how solved:** Required dedicated hardware/setup for fuzzing

### Techniques and Primitives
- **Encoding mismatch WAF bypass** — Mix HTML entities with raw characters to create parser mismatch between WAF and backend
- **SAML assertion smuggling** — Insert unsigned assertions into SAML response alongside signed ones by exploiting XPath selector order/scope
- **Forcing cookie order via path length** — Cookies ordered by path length then chronologically; set a cookie with very specific path to control position

### Tooling and Resources
- CSPBypass.com (community database of CSP bypasses by ReniPack)
- Bebiks' Caido 403 Bypasser plugin (AI-augmented, customizable templates)
- Fuzzotron (network fuzzer for TCP/UDP)
- Project Discovery nuclei templates for Ruby SAML bypass
- DNSPoison.com (GFW DNS poisoning check tool)
- SideQuest llama.cpp exploit video

### Suggestions and Advices from Hunter
- "When you're doing SAML signature validation, investigate how they're doing XPath selections and see if there's any wiggle room." — Rhynorater
- "If you take the time to set up the software, you'll find so much more because it's not as hardened." — Rhynorater
- "If I'm hitting this wall, every other researcher has also. So if I push through that, it narrows the competition." — Joel Margolis

### AI Takeaway
The Caido 403 Bypasser's hybrid model — natural language → code generation → scan template with visible, verifiable tests — is the ideal pattern for AI-assisted security tooling. The SAML XPath confusion bug type (selection-based signature bypass) is widely applicable beyond SAML to any system that signs/validates selected elements from a document.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Chinese Great Firewall DNS poisoning: ~700 keywords in subdomains cause DNS to resolve to attacker-controllable IPs (including Fastly) → subdomain-takeover-like attacks

#### 2. What you should learn
- Understand **saml signature validation xpath selection is a critical single point of failure — check how nodes are selected and whether unsigned assertions can be smuggled alongside signed ones**
- Understand **dns poisoning via the great firewall of china affects any domain with sensitive subdomain keywords — 700+ known keywords; some poisoned ips host fastly proxies allowing registration → subdomain takeover equivalent**
- Understand **waf bypass technique: mix encodings (html entities + raw characters) to create perception mismatch between waf and server**
- Understand **when auditing saml, check both xpath and xslt (transformations) — two places where parsing mismatches occur**

#### 3. Core concepts explained
**Ruby SAML / GitLab Authentication Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Great Firewall DNS Poisoning**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**XSS WAF Bypass — One Payload for All**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Encoding mismatch WAF bypass**
- Mix HTML entities with raw characters to create parser mismatch between WAF and backend

**SAML assertion smuggling**
- Insert unsigned assertions into SAML response alongside signed ones by exploiting XPath selector order/scope

**Forcing cookie order via path length**
- Cookies ordered by path length then chronologically; set a cookie with very specific path to control position


#### 4. Techniques and tactics
**Encoding mismatch WAF bypass**
- **What it is:** Mix HTML entities with raw characters to create parser mismatch between WAF and backend
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**SAML assertion smuggling**
- **What it is:** Insert unsigned assertions into SAML response alongside signed ones by exploiting XPath selector order/scope
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Forcing cookie order via path length**
- **What it is:** Cookies ordered by path length then chronologically; set a cookie with very specific path to control position
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When you're doing SAML signature validation, investigate how they're doing XPath selections and see if there's any wiggle room."* — **Rhynorater**
- *"If you take the time to set up the software, you'll find so much more because it's not as hardened."* — **Rhynorater**
- *"If I'm hitting this wall, every other researcher has also. So if I push through that, it narrows the competition."* — **Joel Margolis**

#### 6. Mental models
- **When you're doing SAML signature validation, investigate how** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you take the time to set up the software, you'll find so ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If I'm hitting this wall, every other researcher has also. S** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** SAML signature validation XPath selection is a critical single point of failure — check how nodes are selected and whether unsigned assertions can be smuggled alongside signed ones
- **Try this:** DNS poisoning via the Great Firewall of China affects any domain with sensitive subdomain keywords — 700+ known keywords; some poisoned IPs host Fastly proxies allowing registration → subdomain takeover equivalent
- **Try this:** WAF bypass technique: mix encodings (HTML entities + raw characters) to create perception mismatch between WAF and server
- **Try this:** When auditing SAML, check both XPath and XSLT (transformations) — two places where parsing mismatches occur

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Required isolating the library from its consumer (GitLab) for testing
- - Root cause: DNS queries routed through China get poisoned if the subdomain contains any of ~700+ blocked keywords. Resolves to specific IPs, some of which point to Fastly (CDN) — you can register those domains on Fastly and serve content
- - Obstacles & how solved: China-specific attack surface; committed research over months

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **DNS** — Domain Name System — translates domain names to IP addresses
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Ruby SAML / GitLab Authentication Bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Chinese Great Firewall DNS poisoning: ~700 keywords in subdomains cause DNS to r**
2. **SAML signature validation XPath selection is a critical single point of failure **
3. **DNS poisoning via the Great Firewall of China affects any domain with sensitive **
