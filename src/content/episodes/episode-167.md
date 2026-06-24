---
title: "Stealing Bugs with Valeriy Shevchenko"
episode: 167
---


# Episode 167 Stealing Bugs with Valeriy Shevchenko

### TL;DR
- Valeriy documented everything including screenshot evidence of working credentials — when the server was shut down the next day, the credentials were still active and the report was accepted
- Supplier third-party compromise chain: found a link on the main site pointing to an agency's domain → agency had Symfony debug mode enabled → creds leaked → reused on main domain's WordPress admin → stored XSS/content takeover
- Bug report theft: Valeriy's 3-year-old proprietary research was copy-pasted word-for-word into a submission (including "I did this research")
- HackerOne investigation found 5-10 people using Valeriy's stolen report as a template

### Key Takeaways
- [ ] Document findings with video/screenshots immediately — when a server goes down or creds expire, evidence is all you have
- [ ] Investigate third-party suppliers/agencies linked from the main site — they may have weaker security and reused credentials
- [ ] Consider watermarking reports: invisible Unicode tags, zero-width characters, intentional mistakes unique to you
- [ ] Use your own infrastructure for callbacks (Burp Collab self-hosted) to avoid leaking POC traffic to third-party services
- [ ] Don't over-detail reports — give enough to reproduce but avoid revealing your research methodology

### Bugs and Findings

#### Acquisitions Prep — Node.js Path Traversal → AWS Credentials
- **Target/context:** Company acquired another; Valeriy pre-researched the acquisition target
- **Root cause:** Node.js path traversal on the acquisition target's server leaking environment variables
- **Technique:** 1) Identify upcoming acquisition via news 2) Research target's servers before acquisition legal completion 3) Found NodeJS path traversal leaking env vars with AWS credentials 4) Server shut down on acquisition day but credentials were still active
- **Key technical details:** Screenshot evidence saved; AWS credentials tested via CLI and still valid; server shut down but credentials not rotated
- **Impact / severity / bounty:** $10,500 — AWS access to database etc.

#### Third-Party Supplier → Main Domain WordPress Takeover
- **Target/context:** Large company with third-party content agency
- **Root cause:** Agency domain had Symfony debug mode enabled → PHP info leaked creds; same creds reused on main domain WordPress admin
- **Technique:** 1) Found unexpected third-party domain link in terms & conditions 2) Recon on agency domain → Symfony debug mode → env vars/creds 3) Log files confirmed agency managed content for main domain 4) Creds also worked on main domain's WordPress admin
- **Key technical details:** Symfony debug mode exposes PHP info with credentials; repeated credentials across agency servers and main domain; WordPress admin → stored XSS/content modification
- **Impact / severity / bounty:** Full content takeover of main domain; stored XSS

### Bug Report Theft Case
- Valeriy reported a novel attack vector class (not a single bug) to ~10 programs 3 years prior
- The research was never published publicly
- Full text including "I did this research" was copy-pasted by multiple reporters
- Attributed to leak from: (1) customers with Slack-integrated HackerOne notifications accessible to non-security staff, or (2) duplicate reporters added to the initial report
- HackerOne identified 5-10 users using the stolen template

### Suggestions and Advices from Hunter
- "There is no place where a finding could be legit for a very long period of time. It could be legit as a short term as well." — Valeriy (quoting Jason Haddix)
- "Don't add dupe reporters to your report automatically — insist on accepting or denying access."
- "Put a watermark in your reports — maybe a deliberate mistake that only you know about, or Unicode tags."
- "When triage says 'it doesn't work right now', if it was legit before and credentials were legit, it doesn't matter."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Valeriy documented everything including screenshot evidence of working credentials — when the server was shut down the next day, the credentials were still active and the report was accepted

#### 2. What you should learn
- Understand **[ ] document findings with video/screenshots immediately — when a server goes down or creds expire, evidence is all you have**
- Understand **[ ] investigate third-party suppliers/agencies linked from the main site — they may have weaker security and reused credentials**
- Understand **[ ] consider watermarking reports: invisible unicode tags, zero-width characters, intentional mistakes unique to you**
- Understand **[ ] use your own infrastructure for callbacks (burp collab self-hosted) to avoid leaking poc traffic to third-party services**
- Understand **[ ] don't over-detail reports — give enough to reproduce but avoid revealing your research methodology**

#### 3. Core concepts explained
**Acquisitions Prep — Node.js Path Traversal → AWS Credentials**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Third-Party Supplier → Main Domain WordPress Takeover**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"There is no place where a finding could be legit for a very long period of time. It could be legit as a short term as well."* — **Valeriy (quoting Jason Haddix)**
- *"Don't add dupe reporters to your report automatically"* — **insist on accepting or denying access.**
- *"Put a watermark in your reports"* — **maybe a deliberate mistake that only you know about, or Unicode tags.**
- *"When triage says 'it doesn't work right now', if it was legit before and credentials were legit, it doesn't matter."*

#### 6. Mental models
- **There is no place where a finding could be legit for a very ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Don't add dupe reporters to your report automatically — insi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Put a watermark in your reports — maybe a deliberate mistake** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Document findings with video/screenshots immediately — when a server goes down or creds expire, evidence is all you have
- **Try this:** [ ] Investigate third-party suppliers/agencies linked from the main site — they may have weaker security and reused credentials
- **Try this:** [ ] Consider watermarking reports: invisible Unicode tags, zero-width characters, intentional mistakes unique to you
- **Try this:** [ ] Use your own infrastructure for callbacks (Burp Collab self-hosted) to avoid leaking POC traffic to third-party services

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Acquisitions Prep — Node.js Path Traversal → AWS Credentials?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Valeriy documented everything including screenshot evidence of working credentia**
2. **[ ] Document findings with video/screenshots immediately — when a server goes do**
3. **[ ] Investigate third-party suppliers/agencies linked from the main site — they **
