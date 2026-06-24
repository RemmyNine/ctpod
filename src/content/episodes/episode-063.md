---
title: "JHaddix Returns"
episode: 63
---


# Episode 63 JHaddix Returns

**Guest:** Jason Haddix
**Format:** Show notes with timestamps (feed)
**Topics:** Updates to Bug Hunter's Methodology, red teaming, dark web credentials, FIS hunting, new recon techniques, AI integrations

### TL;DR
- JHaddix started Arcanum Information Security (consultancy) — the name comes from The Name of the Wind
- Updated Bug Hunter's Methodology with heavy JavaScript analysis section — lazy loading, minification, framework-specific cheat sheets
- Dark web credential hunting: Stealer logs (RedLine) sold on Telegram — buy fresh creds for $10+; use companies like Flare for indexing at scale
- FIS target recon: aggressive Akamai blocking forced residential proxies (Bright Data) — geo-locked regional domains required localized proxies
- New recon technique: "Reverse the d-mark" — finding apex domains nobody else has by going the extra 10-15%

### Key Takeaways
- RedLine stealer malware steals cookies AND creds — if you find a cred on a forum, the cookie is likely there too → inject cookie → bypass 2FA
- Five out of six recent red team engagements succeeded via credentials bought from Telegram/Discord threat actor channels
- Bright Data residential proxy network = request goes through real home IPs → bypass VPS blacklisting
- Developer programs, reseller programs, KYC-required functions = greenfield attack surface most hunters skip
- Heat-mapping: integration points (webhooks, API connectors) are where input validation is weakest — focus there

### Techniques and Primitives
- **Threat-Intel-as-Vulnerability:** Buy stealer log samples from Telegram → parse for target domain credentials → submit as P1 with working POC (cookie injection). 50/50 acceptance rate by programs
- **Geolocation-restricted recon:** Use localized VPS or residential proxies (Bright Data) to access region-locked subdomains (e.g., fis.jp, fis.uk)
- **Heat-mapping for input validation gaps:** Integration features (webhooks, third-party connectors) routinely bypass standard sanitization — "people just don't do it"

### Tooling and Resources
- Flare.io — dark web credential intelligence
- Dehashed.com — breach data search (level 1, often stale)
- Bright Data — residential proxy network
- Fragga — by SensePost, for indexing breach data
- `csprecon` by edoardottt — CSP endpoint discovery

### Suggestions and Advices
- **JHaddix:** "Going deep" means: paid account access, geo-located access, KYC acceptance, developer programs — anything that raises the barrier for other hunters
- "The extra 10-15% that nobody else will do" — that's where the greenfield targets are
- On credential reporting: "If you find a cred and you're on a VPN login to Azure/M365, most programs will pay for that"
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
JHaddix started Arcanum Information Security (consultancy) — the name comes from The Name of the Wind

#### 2. What you should learn
- Understand **redline stealer malware steals cookies and creds — if you find a cred on a forum, the cookie is likely there too → inject cookie → bypass 2fa**
- Understand **five out of six recent red team engagements succeeded via credentials bought from telegram/discord threat actor channels**
- Understand **bright data residential proxy network = request goes through real home ips → bypass vps blacklisting**
- Understand **developer programs, reseller programs, kyc-required functions = greenfield attack surface most hunters skip**
- Understand **heat-mapping: integration points (webhooks, api connectors) are where input validation is weakest — focus there**

#### 3. Core concepts explained
****Threat**
- A technique discussed in this episode for security research and bug bounty hunting.

****Geolocation**
- A technique discussed in this episode for security research and bug bounty hunting.

**Heat-mapping for input validation gaps: Integration features (webhooks, third-party connectors) routinely bypass standard sanitization**
- "people just don't do it"


#### 4. Techniques and tactics
**Threat-Intel-as-Vulnerability: Buy stealer log samples from Telegram → parse for target domain credentials → submit as P1 with working POC (cookie injection). 50/50 acceptance rate by programs**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Geolocation-restricted recon: Use localized VPS or residential proxies (Bright Data) to access region-locked subdomains (e.g., fis.jp, fis.uk)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Heat-mapping for input validation gaps: Integration features (webhooks, third-party connectors) routinely bypass standard sanitization**
- **What it is:** "people just don't do it"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"JHaddix: "Going deep" means: paid account access, geo-located access, KYC acceptance, developer programs"* — **anything that raises the barrier for other hunters**
- *"The extra 10-15% that nobody else will do"* — **that's where the greenfield targets are**
- *"On credential reporting: "If you find a cred and you're on a VPN login to Azure/M365, most programs will pay for that"*

#### 6. Mental models
- **JHaddix: "Going deep" means: paid account access, geo-locate** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The extra 10-15% that nobody else will do" — that's where th** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On credential reporting: "If you find a cred and you're on a** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** RedLine stealer malware steals cookies AND creds — if you find a cred on a forum, the cookie is likely there too → inject cookie → bypass 2FA
- **Try this:** Five out of six recent red team engagements succeeded via credentials bought from Telegram/Discord threat actor channels
- **Try this:** Bright Data residential proxy network = request goes through real home IPs → bypass VPS blacklisting
- **Try this:** Developer programs, reseller programs, KYC-required functions = greenfield attack surface most hunters skip

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **JHaddix started Arcanum Information Security (consultancy) — the name comes from**
2. **RedLine stealer malware steals cookies AND creds — if you find a cred on a forum**
3. **Five out of six recent red team engagements succeeded via credentials bought fro**
