---
title: "Recon Legend Shubs — From Burgers to Bounties"
episode: 30
---


# Episode 30 Recon Legend Shubs — From Burgers to Bounties

**Guests/Hosts:** Justin Gardner, Joel Margolis, Shubs (InfoSecAU / Assetnote)  
**Date:** 2023-08-03 | **Duration:** 1:19:25

### TL;DR
- Shubs' origin story: worked at Hungry Jack's ($6/hr), first PayPal bounty ($1.5K) let him quit; competed with Naffy on recon for Right Games ($8K/subdomain takeover)
- Recon + deep-dive dual skill: recon finds the entry point, deep analysis (debugging, reversing) exploits it
- IIS hacking masterclass: web.config → machineKey → RCE; SSRF → NTLMv2 hash capture via `\\` UNC paths; cookie-less session token injection for path restriction bypass
- Building Assetnote from open-source recon tool to enterprise ASM platform
- Zero-day reporting: ethics, economics, strategy

### Key Takeaways
- IIS = easiest web server to hack; blue page = "I'm going to find criticals here"
- web.config contains machineKey/validationKey; LFD → web.config read → Telerik/RCE
- SSRF on .NET/IIS: `Path.Combine` accepts `\\` UNC paths → victim sends NTLMv2 hash to attacker's Responder
- IIS virtual directory path traversal: `/SSO/../` traverses to backend webroot
- `.NET XXE universal payload`: use DTD file from Windows filesystem (always present) to leak file contents
- Bug bounty economics: if you include "zero-day" in report title, 90% chance rejected; omit those words, 90% paid

### Bugs and Findings

#### IIS Short Name + web.config → RCE chain — LFD → RCE
- **Target/context:** Any IIS server with 8.3 name generation
- **Root cause:** Short name enumeration leaks file names; config files reveal machineKey which can be used for .NET deserialization RCE
- **Key technical details:** Short name = first 6 chars + `~1` + first 3 chars of extension | web.config has `<machineKey>` element with validationKey/decryptionKey
- **Technique / how found:** ShortScan/BitQuark → enumerate files → web.config → known Telerik/CVE for RCE
- **Impact / severity / bounty:** RCE via chain of information disclosure + deserialization

#### SSRF → NTLMv2 hash capture — SSRF escalation
- **Target/context:** .NET applications on IIS
- **Root cause:** `Path.Combine` accepts UNC paths (`\\host\share`); Windows attempts NTLM authentication to the attacker's server
- **Technique / how found:** Send `\\attacker.com\C$` in SSRF payload → target sends NTLMv2 hash
- **Key technical details:** Use Responder to capture hash | Hash can be cracked offline
- **Impact / severity / bounty:** NTLMv2 hash leak → potential credential compromise

#### IIS Virtual Directory Path Traversal — Auth bypass
- **Target/context:** IIS with virtual directories pointing to different servers
- **Root cause:** Traversal within a virtual directory path (`/SSO/..%2F`) traverses to the backend webroot instead of the virtual directory root
- **Key technical details:** `%2F` bypasses IIS path normalization | Similar to Sam Curry's secondary context research
- **Impact / severity / bounty:** Access to backend server's webroot, potentially finding new endpoints/files

### Techniques and Primitives
- **Cookie-less session token injection (IIS/.NET)** — `/(S(...))/` in URL path is treated as a cookie-less session token and stripped from the path; bypasses path-based restrictions and WAF rules
- **Application pool confusion** — Use cookie-less session injection to execute code from one app pool in a different app pool context (privilege escalation)
- **Zero-day reporting strategy** — Omit "zero-day" from title; report to vendor first, then bounty programs; provide workaround/patch-diff if possible

### Tooling and Resources
- Assetnote blog (Dylan Pinder + Shubs)
- BitQuark's ShortScan
- Responder (NTLMv2 capture)
- IIS short name scanner (irsdl)
- Metabase pre-auth RCE blog post (teased for Aug 20, 2023)

### Suggestions and Advices from Hunter
- "When you see the IIS blue page, do not skip it. Most companies wouldn't spin up an IIS server for no reason. There is something there."
- "If you include 'zero-day' in your report, they'll tell you they don't accept zero-days. If you don't include those words, 90% of the time they pay."
- "For recon frameworks: choose the language you're comfortable with. Python is fine. Don't rewrite in Rust just because it's hot."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Shubs' origin story: worked at Hungry Jack's ($6/hr), first PayPal bounty ($1.5K) let him quit; competed with Naffy on recon for Right Games ($8K/subdomain takeover)

#### 2. What you should learn
- Understand **iis = easiest web server to hack; blue page = "i'm going to find criticals here"**
- Understand **web.config contains machinekey/validationkey; lfd → web.config read → telerik/rce**
- Understand **ssrf on .net/iis: `path.combine` accepts `\\` unc paths → victim sends ntlmv2 hash to attacker's responder**
- Understand **iis virtual directory path traversal: `/sso/../` traverses to backend webroot**
- Understand **`.net xxe universal payload`: use dtd file from windows filesystem (always present) to leak file contents**

#### 3. Core concepts explained
**IIS Short Name + web.config → RCE chain — LFD → RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**SSRF → NTLMv2 hash capture — SSRF escalation**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**IIS Virtual Directory Path Traversal — Auth bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Cookie-less session token injection (IIS/.NET)**
- `/(S(...))/` in URL path is treated as a cookie-less session token and stripped from the path; bypasses path-based restrictions and WAF rules

**Application pool confusion**
- Use cookie-less session injection to execute code from one app pool in a different app pool context (privilege escalation)

**Zero-day reporting strategy**
- Omit "zero-day" from title; report to vendor first, then bounty programs; provide workaround/patch-diff if possible


#### 4. Techniques and tactics
**Cookie-less session token injection (IIS/.NET)**
- **What it is:** `/(S(...))/` in URL path is treated as a cookie-less session token and stripped from the path; bypasses path-based restrictions and WAF rules
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Application pool confusion**
- **What it is:** Use cookie-less session injection to execute code from one app pool in a different app pool context (privilege escalation)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Zero-day reporting strategy**
- **What it is:** Omit "zero-day" from title; report to vendor first, then bounty programs; provide workaround/patch-diff if possible
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When you see the IIS blue page, do not skip it. Most companies wouldn't spin up an IIS server for no reason. There is something there."*
- *"If you include 'zero-day' in your report, they'll tell you they don't accept zero-days. If you don't include those words, 90% of the time they pay."*
- *"For recon frameworks: choose the language you're comfortable with. Python is fine. Don't rewrite in Rust just because it's hot."*

#### 6. Mental models
- **When you see the IIS blue page, do not skip it. Most compani** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you include 'zero-day' in your report, they'll tell you t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For recon frameworks: choose the language you're comfortable** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** IIS = easiest web server to hack; blue page = "I'm going to find criticals here"
- **Try this:** web.config contains machineKey/validationKey; LFD → web.config read → Telerik/RCE
- **Try this:** SSRF on .NET/IIS: `Path.Combine` accepts `\\` UNC paths → victim sends NTLMv2 hash to attacker's Responder
- **Try this:** IIS virtual directory path traversal: `/SSO/../` traverses to backend webroot

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **recon** — Reconnaissance — systematic discovery of target attack surface
- **XXE** — XML External Entity — injecting XML that references external resources

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in IIS Short Name + web.config → RCE chain — LFD → RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Shubs' origin story: worked at Hungry Jack's ($6/hr), first PayPal bounty ($1.5K**
2. **IIS = easiest web server to hack; blue page = "I'm going to find criticals here"**
3. **web.config contains machineKey/validationKey; LFD → web.config read → Telerik/RC**
