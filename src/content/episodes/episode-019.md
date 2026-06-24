---
title: "Audit Code, Earn Bounties (Part 2) + Zip-Snip, Sitecore, and more!"
episode: 19
---


# Episode 19 Audit Code, Earn Bounties (Part 2) + Zip-Snip, Sitecore, and more!

**Guests/Hosts:** Justin Gardner (Rhynorater), Joel Margolis (Teknogeek)  
**Date:** 2023-05-18 | **Duration:** 53:24

### TL;DR
- New `.zip` TLD creates phishing/social-engineering risk; an invisible space in a `wget` command makes `source-code.zip` resolve as a domain the attacker owns
- AssetNote/Shubs write-up: IIS/Sitecore authentication bypass via email-campaign renderer user, chained with LFD → Telerik deserialization RCE
- Hacklook's 10 tips for crushing bug bounties (fresh programs, focus on strengths, document everything, be persistent)
- Source code review methodology deep-dive: sources vs sinks, config/routing analysis, decompiling .NET DLLs

### Key Takeaways
- When a new TLD matches a file extension (`.zip`, `.mov`, etc.), check for URL-parsing confusion in WAFs, allowlist bypasses, and CI/CD link hijacking
- Start source code review with config files (web.config, app config) to map routes before diving into decompiled code
- Favor starting from sources (ingress points) to understand the app; switch to sinks for RCE hunting
- Read AssetNote blog posts religiously — they model the full attacker mentality

### Bugs and Findings

#### IIS Authorization bypass + LFD → Telerik Deserialization RCE — Auth bypass + LFD + Deserialization
- **Target/context:** Sitecore CMS on IIS
- **Root cause:** The `renderer` user (used for email-campaign subscribers viewing emails) bypasses `this.context.User.Identity.IsAuthenticated` checks. Query params `ec_message_id` and `ec_id` cause the app to set the user to the renderer user.
- **Technique / how found:** Route enumeration via web.config → decompiled Sitecore DLLs (DnSpy) → found preview functionality with a parameter leading to LFD; used LFD to read web.config containing Telerik encryption keys
- **Exploitation steps:**
  1. Subscribe to a mailing list to get a renderer session
  2. Use the `ec_message_id` / `ec_id` params to set the user to renderer
  3. Hit the preview endpoint with a path-traversal parameter → LFD of `web.config`
  4. Extract machineKey / validationKey from web.config
  5. Use known Telerik UI for ASP.NET AUTH deserialization CVE (Operator's 2019 exploit) → RCE
- **Key technical details:** Route: `/api/sitecore/{controller}/{action}` | Parameters: `ec_message_id`, `ec_id` set the auth context | web.config contains Telerik encryption keys
- **Impact / severity / bounty:** Full RCE on the IIS server; high/critical
- **Obstacles & how solved:** Required authenticated access; solved by abusing the email-campaign renderer user to bypass auth

### Techniques and Primitives
- **Source-first code review** — Map ingress points (routes/handlers) and trace data flow; versus sink-first (start at dangerous functions and trace backward)
- **Config-driven recon** — Always read web.config/appsettings first to understand routing, auth schemes, connection strings, encryption keys
- **Decompilation + debugging** — DN Spy / dotPeek for .NET; IntelliJ for Java; Rider for .NET Core; set breakpoints in running processes

### Tooling and Resources
- `DnSpy` (DN Spy) — .NET decompiler/debugger (older but supports live debugging)
- `dotPeek` — Joel's recommended .NET decompiler
- Operator's Telerik UI deserialization exploit (2019)
- AssetNote blog (authored by Dylan Pinder)

### Suggestions and Advices from Hunter
- "If you can get access to the source code, you have a 10x advantage over black-box testers."
- Shubs/AssetNote approach: start with config files, then decompile, then trace routes.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
New `.zip` TLD creates phishing/social-engineering risk; an invisible space in a `wget` command makes `source-code.zip` resolve as a domain the attacker owns

#### 2. What you should learn
- Understand **when a new tld matches a file extension (`.zip`, `.mov`, etc.), check for url-parsing confusion in wafs, allowlist bypasses, and ci/cd link hijacking**
- Understand **start source code review with config files (web.config, app config) to map routes before diving into decompiled code**
- Understand **favor starting from sources (ingress points) to understand the app; switch to sinks for rce hunting**
- Understand **read assetnote blog posts religiously — they model the full attacker mentality**

#### 3. Core concepts explained
**IIS Authorization bypass + LFD → Telerik Deserialization RCE — Auth bypass + LFD + Deserialization**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Source-first code review**
- Map ingress points (routes/handlers) and trace data flow; versus sink-first (start at dangerous functions and trace backward)

**Config-driven recon**
- Always read web.config/appsettings first to understand routing, auth schemes, connection strings, encryption keys

**Decompilation + debugging**
- DN Spy / dotPeek for .NET; IntelliJ for Java; Rider for .NET Core; set breakpoints in running processes


#### 4. Techniques and tactics
**Source-first code review**
- **What it is:** Map ingress points (routes/handlers) and trace data flow; versus sink-first (start at dangerous functions and trace backward)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Config-driven recon**
- **What it is:** Always read web.config/appsettings first to understand routing, auth schemes, connection strings, encryption keys
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Decompilation + debugging**
- **What it is:** DN Spy / dotPeek for .NET; IntelliJ for Java; Rider for .NET Core; set breakpoints in running processes
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you can get access to the source code, you have a 10x advantage over black-box testers."*
- *"Shubs/AssetNote approach: start with config files, then decompile, then trace routes."*

#### 6. Mental models
- **If you can get access to the source code, you have a 10x adv** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Shubs/AssetNote approach: start with config files, then deco** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** When a new TLD matches a file extension (`.zip`, `.mov`, etc.), check for URL-parsing confusion in WAFs, allowlist bypasses, and CI/CD link hijacking
- **Try this:** Start source code review with config files (web.config, app config) to map routes before diving into decompiled code
- **Try this:** Favor starting from sources (ingress points) to understand the app; switch to sinks for RCE hunting
- **Try this:** Read AssetNote blog posts religiously — they model the full attacker mentality

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Required authenticated access; solved by abusing the email-campaign renderer user to bypass auth

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **recon** — Reconnaissance — systematic discovery of target attack surface
- **deserialization** — Converting serialized data back into objects — dangerous if attacker-controlled

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in IIS Authorization bypass + LFD → Telerik Deserialization RCE — Auth bypass + LFD + Deserialization?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **New `.zip` TLD creates phishing/social-engineering risk; an invisible space in a**
2. **When a new TLD matches a file extension (`.zip`, `.mov`, etc.), check for URL-pa**
3. **Start source code review with config files (web.config, app config) to map route**
