---
title: "The OG Bug Bounty King — Frans Rosen"
episode: 45
---


# Episode 45 The OG Bug Bounty King — Frans Rosen

### TL;DR
- Frans Rosen: OG bug bounty legend, co-founder of Detectify
- Origin of S3 bucket takeover (2014), CloudFront trailing dot takeover
- PostMessage Tracker Chrome extension — only extension of its kind, used daily
- Deep dive on OAuth "dirty dancing" — breaking the state parameter intentionally
- Service workers + CRLF injection + middleware misconfig for persistent XSS

### Key takeaways
- "Automationism" — don't compete on automation speed; go deep manually for high-impact chains
- Take three days to understand a program's taxonomy (casing styles, naming conventions, parameter patterns)
- Error message variations reveal backend components and implementation differences
- Keep a "tips folder" — note every technique, no matter how old; they persist
- Collaboration: 2-person teams are optimal; 50/50 split is simplest

### Bugs and Findings
#### S3 Bucket Takeover
- **Target:** Any website using a CNAME to an S3 bucket the attacker can claim
- **Root cause:** No domain ownership verification when configuring S3 bucket for static website hosting
- **Technique:**
  1. Find subdomain CNAME pointing to `bucket-name.s3.amazonaws.com` that returns 404 NoSuchBucket
  2. Create the bucket in the same region
  3. Upload content — now you control content on that subdomain
- **History:** Discovered 2014; published with 14 affected providers
- **Tool:** S3 Bucket Disclosure (discloses bucket name via error oracles)

#### CloudFront Trailing Dot Takeover
- **Target:** CloudFront distributions
- **Root cause:** Adding a trailing dot (`.`) to a domain makes it a fully qualified domain name; CloudFront didn't require domain ownership validation for trailing-dot variants
- **Technique:**
  1. Create a CloudFront distribution for `target.com.` (with trailing dot)
  2. CloudFront's client-side validation rejected the dot, but intercepting the API request allowed bypass
  3. Serve arbitrary content on `target.com.` — cookies set on `target.com` also sent to `target.com.`
- **Impact:** Cookie theft via email links that include a period at the end of the URL

#### OAuth "Dirty Dancing" — Account Hijacking via State Breaking
- **Target:** Any OAuth flow with a state parameter and a gadget that leaks the URL
- **Root cause:** If the state parameter is broken intentionally (attacker generates state, victim uses it), the OAuth code exchange fails — but the code remains in the URL fragment. If any postMessage listener, tracker (Google Analytics), or error page leaks the URL, the attacker can grab the code and exchange it with their known state
- **Technique:**
  1. Generate OAuth URL with attacker's state parameter
  2. Send victim to that URL
  3. State validation fails, but code is left in the fragment
  4. Leak the code via postMessage listener, GA, or other gadget
  5. Exchange code + attacker's state for access token

### Techniques and Primitives
- **Taxonomy analysis** — extract all words from Burp history, sort unique, compare casing (`intentID` vs `intent_id` signals different developers → inconsistent security)
- **PostMessage port jacking** — messagePort can be shuffled between iframes, leading to cross-origin message interception
- **Service worker + CRLF injection** — inject response headers via CRLF to set Service-Worker-Allowed header; gain control of all pages
- **Stop at the right time** — end a hacking session when you have something promising for tomorrow, not when you're empty; builds motivation

### Tooling and Resources
- **PostMessage Tracker** (Chrome extension)
- **S3 Bucket Disclosure** tool (decloak bucket names)
- **Detectify blog** — all Frans's research

### Suggestions and Advices from Hunter
- On automation: "If your whole idea is to find something you don't know of, you can't really automate it"
- "The bugs I'm proudest of are the ones where I piece together multiple observations into a chain"
- On writing reports: "My reports are sometimes 2000-4000 words. I write them manually — showing step by step how I came to the conclusion"
- "Publish your secrets. It eliminates you from looking at them anymore, and forces you to find new ones"

### AI Takeaway
The OAuth "dirty dancing" technique reframes the state parameter from a CSRF protection into an oracle: by intentionally breaking it, the attacker learns exactly where the OAuth code will be exposed, then uses any URL-leaking gadget to steal it.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Frans Rosen: OG bug bounty legend, co-founder of Detectify

#### 2. What you should learn
- Understand **"automationism" — don't compete on automation speed; go deep manually for high-impact chains**
- Understand **take three days to understand a program's taxonomy (casing styles, naming conventions, parameter patterns)**
- Understand **error message variations reveal backend components and implementation differences**
- Understand **keep a "tips folder" — note every technique, no matter how old; they persist**
- Understand **collaboration: 2-person teams are optimal; 50/50 split is simplest**

#### 3. Core concepts explained
**S3 Bucket Takeover**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CloudFront Trailing Dot Takeover**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**OAuth "Dirty Dancing" — Account Hijacking via State Breaking**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Taxonomy analysis**
- extract all words from Burp history, sort unique, compare casing (`intentID` vs `intent_id` signals different developers → inconsistent security)

**PostMessage port jacking**
- messagePort can be shuffled between iframes, leading to cross-origin message interception

**Service worker + CRLF injection**
- inject response headers via CRLF to set Service-Worker-Allowed header; gain control of all pages


#### 4. Techniques and tactics
**Taxonomy analysis**
- **What it is:** extract all words from Burp history, sort unique, compare casing (`intentID` vs `intent_id` signals different developers → inconsistent security)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**PostMessage port jacking**
- **What it is:** messagePort can be shuffled between iframes, leading to cross-origin message interception
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Service worker + CRLF injection**
- **What it is:** inject response headers via CRLF to set Service-Worker-Allowed header; gain control of all pages
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Stop at the right time**
- **What it is:** end a hacking session when you have something promising for tomorrow, not when you're empty; builds motivation
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"On automation: "If your whole idea is to find something you don't know of, you can't really automate it"*
- *"The bugs I'm proudest of are the ones where I piece together multiple observations into a chain"*
- *"On writing reports: "My reports are sometimes 2000-4000 words. I write them manually"* — **showing step by step how I came to the conclusion**
- *"Publish your secrets. It eliminates you from looking at them anymore, and forces you to find new ones"*

#### 6. Mental models
- **On automation: "If your whole idea is to find something you ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The bugs I'm proudest of are the ones where I piece together** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On writing reports: "My reports are sometimes 2000-4000 word** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** "Automationism" — don't compete on automation speed; go deep manually for high-impact chains
- **Try this:** Take three days to understand a program's taxonomy (casing styles, naming conventions, parameter patterns)
- **Try this:** Error message variations reveal backend components and implementation differences
- **Try this:** Keep a "tips folder" — note every technique, no matter how old; they persist

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in S3 Bucket Takeover?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Frans Rosen: OG bug bounty legend, co-founder of Detectify**
2. **"Automationism" — don't compete on automation speed; go deep manually for high-i**
3. **Take three days to understand a program's taxonomy (casing styles, naming conven**
