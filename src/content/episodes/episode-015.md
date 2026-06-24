---
title: "The Israeli Million-Dollar Hacker (n0gl3y Interview)"
episode: 15
---


# Episode 15 The Israeli Million-Dollar Hacker (n0gl3y Interview)

### TL;DR
- n0gl3y (Noam) went from ~$1k earned to million-dollar hacker in ~2 years
- Automation stack: bash scripts, bash loops, cron jobs, Axiom, DigitalOcean, flat TXT files (no database)
- Key automation targets: Log4j scanning, subdomain takeovers, NS takeovers, misconfigured cloud DNS
- Collaboration philosophy: 80% of good bugs come from collaboration or automation
- Bug Bounty Hunters Guild Slack: started with 5-6 top hackers, grew to large community, drove collaboration
- ChatGPT converted all his bash scripts to Python for product reusability

### Key takeaways
- Automation infrastructure: Axiom + DigitalOcean + bash loops + cron + text files (no database needed)
- Number of commits (~20k) backs up recon data every 30 minutes to avoid data loss
- For recon: proprietary wordlists, modified open-source tools, benchmarking against other hackers
- Multi-A DNS rebinding correction: also works on Linux/macOS by targeting `0.0.0.0` instead of `127.0.0.1`
- Twitter digest + email alerts for new nuclei templates
- Live hacking events provide pressure + focus that's hard to replicate alone
- Collaboration phonebook: have different experts for different bug classes (XSS, mobile, etc.)

### Bugs and Findings

#### Web Cache Deception on ChatGPT — JWT Leakage
- **Target/context:** OpenAI ChatGPT (before public bug bounty program)
- **Root cause:** CloudFlare caching configuration — adding `.css` to API endpoint URL cached authenticated response including JWT
- **Technique / how found:**
  1. During preliminary analysis, found API endpoint returning user's JWT
  2. Tried `test.css` extension at end of URL → got cache hit (`cf-cache-status: DYNAMIC` but actually cached)
  3. Victim visits crafted URL → JWT cached → attacker reads JWT from same URL without auth
- **Exploitation steps:**
  1. Craft URL: `https://chat.openai.com/api/auth/session/test.css`
  2. Victim visits URL (authenticated) → CloudFlare caches response
  3. Attacker visits same URL unauthenticated → gets victim's JWT
  4. JWT gives full access to victim's ChatGPT conversations
- **Key technical details:** CloudFlare default cached extensions; authenticated JWT in API response; cache-key collision via extension
- **Impact / severity / bounty:** Reported via email to OpenAI; fixed in 4 minutes; no bounty (pre-program) but high publicity

#### Live Hacking Event SSRF via Burp Active Scan
- **Target/context:** Undisclosed live hacking event target
- **Root cause:** An endpoint concatenated user input into a backend HTTP request without validation
- **Technique / how found:**
  1. Jonathan Bowman showed n0gl3y how to run Burp Active Scan with custom scan profile (focused, not crawling everything)
  2. Active scanner found an external DNS interaction that manually they'd never have discovered
  3. The injected URL was deeply nested in endpoint logic — not obvious
- **Key technical details:** Blind SSRF; payload included full HTTPS URL; JWT (super admin bearer token) leaked in callback request headers
- **Impact / severity / bounty:** Most critical bug of the event

#### Unicode Homoglyph ATO — $28k
- **Target/context:** Large public program (live hacking event)
- **Root cause:** SSO (single sign-on) between subdomains normalized Unicode characters differently; registering with homoglyph "а" (Cyrillic) → SSO normalized to Latin "a" on another subdomain → logged in as admin@company.com
- **Technique / how found:**
  1. Goal: take over any account by email only
  2. Registered as `admin@gmai1.com` using Unicode homoglyph for 'l' (like `ӏ`)
  3. Brute-force tested all subdomains for SSO
  4. On one subdomain, SSO logged in as the actual admin — Unicode normalized during token validation
- **Key technical details:** Unicode homoglyph characters bypass string matching; SSO tokens carry normalized versions
- **Impact / severity / bounty:** $28,000 — full authentication bypass
- **Obstacles & how solved:** Tested all SSO implementations across subdomains manually

### Techniques and Primitives
- **Axiom + bash automation** — VPS fleet orchestrated with Axiom, bash loops, cron for continuous recon
- **Flat file data store** — directory structure: `recon/assets/<domain>/<subdomain>/` — no database needed
- **Burp Active Scan custom profile** — create focused scan profile (no DOM crawling, no heavy JS analysis) for bug bounty speed
- **Unicode homoglyph authentication bypass** — register with visually identical Unicode chars; test across SSO integrations
- **Multi-A rebind correction** — on Linux/macOS, use `0.0.0.0` instead of `127.0.0.1` for DNS rebinding

### Tooling and Resources
- Axiom (interactsh/ProjectDiscovery)
- Bash, cron, DigitalOcean
- Burp Suite Active Scanner (custom profiles)
- ChatGPT (for bash→Python conversion)
- shockwave.security (n0gl3y's startup)

### Suggestions and Advices from Hunter
- "80% of good bugs come from automation or collaboration" — n0gl3y
- "I can't focus manually on programs outside of live hacking events" — n0gl3y on manual vs automation hacking
- "Have a 'phonebook' of experts — different people for different bug classes" — n0gl3y
- "Twitter digest + email alerts for new nuclei templates keeps me current" — n0gl3y

### AI Takeaway
n0gl3y's rise validates that automation-first recon (bash + Axiom + flat files) combined with targeted collab is a viable path to seven figures. The cloudflare cache extension trick for ChatGPT was simple but devastating. The Unicode homoglyph technique is a must-test for any SSO implementation.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
n0gl3y (Noam) went from ~$1k earned to million-dollar hacker in ~2 years

#### 2. What you should learn
- Understand **automation infrastructure: axiom + digitalocean + bash loops + cron + text files (no database needed)**
- Understand **number of commits (~20k) backs up recon data every 30 minutes to avoid data loss**
- Understand **for recon: proprietary wordlists, modified open-source tools, benchmarking against other hackers**
- Understand **multi-a dns rebinding correction: also works on linux/macos by targeting `0.0.0.0` instead of `127.0.0.1`**
- Understand **twitter digest + email alerts for new nuclei templates**

#### 3. Core concepts explained
**Web Cache Deception on ChatGPT — JWT Leakage**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Live Hacking Event SSRF via Burp Active Scan**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Unicode Homoglyph ATO — $28k**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Axiom + bash automation**
- VPS fleet orchestrated with Axiom, bash loops, cron for continuous recon

**Flat file data store**
- directory structure: `recon/assets/<domain>/<subdomain>/` — no database needed

**Burp Active Scan custom profile**
- create focused scan profile (no DOM crawling, no heavy JS analysis) for bug bounty speed


#### 4. Techniques and tactics
**Axiom + bash automation**
- **What it is:** VPS fleet orchestrated with Axiom, bash loops, cron for continuous recon
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Flat file data store**
- **What it is:** directory structure: `recon/assets/<domain>/<subdomain>/` — no database needed
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Burp Active Scan custom profile**
- **What it is:** create focused scan profile (no DOM crawling, no heavy JS analysis) for bug bounty speed
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Unicode homoglyph authentication bypass**
- **What it is:** register with visually identical Unicode chars; test across SSO integrations
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Multi-A rebind correction**
- **What it is:** on Linux/macOS, use `0.0.0.0` instead of `127.0.0.1` for DNS rebinding
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"80% of good bugs come from automation or collaboration"* — **n0gl3y**
- *"I can't focus manually on programs outside of live hacking events"* — **n0gl3y on manual vs automation hacking**
- *"Have a 'phonebook' of experts"* — **different people for different bug classes" — n0gl3y**
- *"Twitter digest + email alerts for new nuclei templates keeps me current"* — **n0gl3y**

#### 6. Mental models
- **80% of good bugs come from automation or collaboration" — n0** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I can't focus manually on programs outside of live hacking e** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Have a 'phonebook' of experts — different people for differe** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Automation infrastructure: Axiom + DigitalOcean + bash loops + cron + text files (no database needed)
- **Try this:** Number of commits (~20k) backs up recon data every 30 minutes to avoid data loss
- **Try this:** For recon: proprietary wordlists, modified open-source tools, benchmarking against other hackers
- **Try this:** Multi-A DNS rebinding correction: also works on Linux/macOS by targeting `0.0.0.0` instead of `127.0.0.1`

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **DNS** — Domain Name System — translates domain names to IP addresses
- **Burp** — Burp Suite — popular web application security testing proxy
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Web Cache Deception on ChatGPT — JWT Leakage?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **n0gl3y (Noam) went from ~$1k earned to million-dollar hacker in ~2 years**
2. **Automation infrastructure: Axiom + DigitalOcean + bash loops + cron + text files**
3. **Number of commits (~20k) backs up recon data every 30 minutes to avoid data loss**
