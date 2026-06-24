---
title: "New Research in Blind SSRF and Self-XSS, and How to Architect Source-code Review AI Bots"
episode: 128
---


# Episode 128 New Research in Blind SSRF and Self-XSS, and How to Architect Source-code Review AI Bots

**Source:** Full ASR transcript.

### TL;DR
- Slonser's research: credentialless iframes are same-origin with regular iframes.
- FetchLater API: delayed requests extended via 307 redirect loops to ~1.5 hours.
- Shubs & AssetNote: blind SSRF escalation via 30+ redirect chains.
- Hrishi (Southbridge AI) reverse-engineered Claude Code using AI.
- Chrome intent to prototype: frame busting intervention may remove cross-origin iframe top navigation.

### Key takeaways
- [ ] Credentialless iframe + login CSRF: credentialless iframe (no cookies) + fetch to cookie jar = login CSRF without logout.
- [ ] FetchLater + redirect loop: POST via FetchLater with 300s timeout, 20x 307 redirects = ~1.5h delay until victim re-auths.
- [ ] Blind SSRF → full SSRF: chain 5+ redirects; after 5th, app error handling changes, returning full response for 500 errors.
- [ ] For code review AI: Gemini 2.5 Pro (1M context) for sub-agents, Opus 4 as orchestrator.
- [ ] Frame busting may be removed soon — test cross-origin iframe top navigation now.

### Bugs and Findings

#### Credentialless iframe same-origin — Login CSRF enabler
- **Target/context:** Sites using credentialless iframes.
- **Root cause:** Credentialless iframes are same-origin with regular iframes (opaque origin not implemented).
- **Key technical details:** `credentialless` attribute → no cookies sent, but still same-origin with authenticated iframes on same page.
- **Impact / severity / bounty:** Enables login CSRF without logout.

#### FetchLater + Redirect Loop — Stored XSS-style persistence
- **Target/context:** Chrome (FetchLater API).
- **Root cause:** FetchLater sends request after page close; extended via 307 redirect loop with 300s per hop.
- **Technique / how found:** Justin: register FetchLater with 300s timeout → attacker stalls → 307 redirect → loop 20x = ~1.5h. Attacker logs out, victim re-auths → stale FetchLater fires with victim's cookies.
- **Key technical details:** `fetchLater(url, {timeout: 300_000})`; 20 redirects × 300s = ~100 minutes; POST + 307 for body preservation.
- **Impact / severity / bounty:** Persistence in browser.

#### Blind SSRF → Full SSRF via Redirect Chain — SSRF escalation
- **Target/context:** Apps with blind SSRF.
- **Root cause:** After 5+ redirects, LibCurl max-redirect crossed → app handles error differently, returning full response for 500 status codes.
- **Technique / how found:** Shubs/AssetNote: chain 301→302→303→… incrementally; responses from status 305+ returned fully; 500 errors leak full HTTP response.
- **Key technical details:** Python script iterates status codes; 500 status codes from final target leak body; 200s remain blind.
- **Impact / severity / bounty:** Blind SSRF → full SSRF on 500-returning endpoints.

### Techniques and Primitives
- **Credentialless iframe login CSRF** — Same-origin bridge for login CSRF without logout.
- **FetchLater persistence** — Delayed request extended with redirect loops.
- **Blind SSRF via redirect exhaustion** — Push past libcurl redirect limit → different error handling.
- **Sub-agent architecture** — Gemini 2.5 Pro as sub-agents, Opus 4 as orchestrator.
- **Mandork** — CLI tool printing codebase with line numbers wrapped in XML for LLM ingestion.

### Tooling and Resources
- Slonser — credentialless iframes, FetchLater research
- Shubs / AssetNote — blind SSRF escalation
- Hrishi (Southbridge AI) — Claude Code reverse engineering, Mandork, Luminthus
- Google Blink intent-to-prototype

### Suggestions and Advices from Hunter
- "Summarization is lossy — avoid it for code understanding."
- "Opus 4 is best at writing prompts for other models."
- "Build your own agent framework with REST APIs, not LangChain."
- "I need to be more comfortable with the abstract and take educated guesses." (Justin)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Slonser's research: credentialless iframes are same-origin with regular iframes.

#### 2. What you should learn
- Understand **[ ] credentialless iframe + login csrf: credentialless iframe (no cookies) + fetch to cookie jar = login csrf without logout**
- Understand **[ ] fetchlater + redirect loop: post via fetchlater with 300s timeout, 20x 307 redirects = ~1.5h delay until victim re-auths**
- Understand **[ ] blind ssrf → full ssrf: chain 5+ redirects; after 5th, app error handling changes, returning full response for 500 errors**
- Understand **[ ] for code review ai: gemini 2.5 pro (1m context) for sub-agents, opus 4 as orchestrator**
- Understand **[ ] frame busting may be removed soon — test cross-origin iframe top navigation now**

#### 3. Core concepts explained
**Credentialless iframe same-origin — Login CSRF enabler**
- **What it is:** Cross-Site Request Forgery — tricking a victim's browser into making unwanted requests to a site where they're authenticated.
- **Why it matters:** CSRF can change email, password, or perform actions on behalf of the victim.
- **Common mistake:** Only testing GET-based CSRF — POST and PUT endpoints with CSRF tokens may still be vulnerable if tokens are predictable.

**FetchLater + Redirect Loop — Stored XSS-style persistence**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Blind SSRF → Full SSRF via Redirect Chain — SSRF escalation**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Credentialless iframe login CSRF**
- Same-origin bridge for login CSRF without logout.

**FetchLater persistence**
- Delayed request extended with redirect loops.

**Blind SSRF via redirect exhaustion**
- Push past libcurl redirect limit → different error handling.


#### 4. Techniques and tactics
**Credentialless iframe login CSRF**
- **What it is:** Same-origin bridge for login CSRF without logout.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**FetchLater persistence**
- **What it is:** Delayed request extended with redirect loops.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Blind SSRF via redirect exhaustion**
- **What it is:** Push past libcurl redirect limit → different error handling.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Sub-agent architecture**
- **What it is:** Gemini 2.5 Pro as sub-agents, Opus 4 as orchestrator.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Mandork**
- **What it is:** CLI tool printing codebase with line numbers wrapped in XML for LLM ingestion.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Summarization is lossy"* — **avoid it for code understanding.**
- *"Opus 4 is best at writing prompts for other models."*
- *"Build your own agent framework with REST APIs, not LangChain."*
- *"I need to be more comfortable with the abstract and take educated guesses." (Justin)"*

#### 6. Mental models
- **Summarization is lossy — avoid it for code understanding.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Opus 4 is best at writing prompts for other models.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Build your own agent framework with REST APIs, not LangChain** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Credentialless iframe + login CSRF: credentialless iframe (no cookies) + fetch to cookie jar = login CSRF without logout.
- **Try this:** [ ] FetchLater + redirect loop: POST via FetchLater with 300s timeout, 20x 307 redirects = ~1.5h delay until victim re-auths.
- **Try this:** [ ] Blind SSRF → full SSRF: chain 5+ redirects; after 5th, app error handling changes, returning full response for 500 errors.
- **Try this:** [ ] For code review AI: Gemini 2.5 Pro (1M context) for sub-agents, Opus 4 as orchestrator.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **API** — Application Programming Interface — structured endpoints for data exchange
- **agent** — AI system that can use tools and make decisions autonomously
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Credentialless iframe same-origin — Login CSRF enabler?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Slonser's research: credentialless iframes are same-origin with regular iframes.**
2. **[ ] Credentialless iframe + login CSRF: credentialless iframe (no cookies) + fet**
3. **[ ] FetchLater + redirect loop: POST via FetchLater with 300s timeout, 20x 307 r**
