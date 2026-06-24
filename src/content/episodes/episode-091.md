---
title: "Zero to LHE in 9 Months (feat gr3pme)"
episode: 91
---


# Episode 91 Zero to LHE in 9 Months (feat gr3pme)

**Guest:** Brandyn Murtagh (gr3pme)
**Hosts:** Justin Gardner (Rhynorater)
**Duration:** 1:22:50
**Transcript source:** feed (show notes + partial transcript)

### TL;DR
- Journey from 0 bug bounty experience to Live Hacking Event performer in ~10 months via mentorship
- Ecosystem hacking — focusing on interconnected apps/APIs rather than single targets
- Attack vector ideation (massive preloaded checklist) as the #1 underrated skill
- Emotional regulation and self-care as force multipliers
- Live hacking events provide instant feedback you can't get anywhere else

### Key Takeaways
- Build a preloaded "attack vector ideation" document before starting any target — list every possible attack vector no matter how improbable
- Use the products you already pay for as bug bounty targets — you already have access, familiarity, and legitimate reason to probe
- Pick targets with geographic/paywall friction to reduce dupe competition
- Take collaboration leads seriously even when your spidey sense says "not sketchy"
- Prioritize gym, eating, and breaks even at LHEs — brute force leads to burnout

### Bugs and Findings

#### FinTech Bank ATO — Stored XSS via Payment Reference
- **Target/context:** EU FinTech bank using Open Banking API
- **Root cause:** International payment reference fields accept arbitrary character sets (emojis, Unicode) that get rendered unsanitized in the recipient's web banking interface
- **Technique / how found:** Created 7–8 real bank accounts across different payment providers; mapped which character sets each allows; sent 1-penny payments with XSS payloads in the reference field
- **Exploitation steps:**
  1. Create bank accounts with multiple payment providers to understand character set allowances
  2. Study Open Banking API spec vs implementation to find discrepancies
  3. Send international payment (inter-bank) with XSS payload in the reference/emoji message field
  4. When recipient opens the payment notification, stored XSS fires → ATO
- **Key technical details:** Open Banking API is an EU standard for bank-to-bank communication; cross-border payments inherit local character sets; emoji support in payment references was the conduit
- **Impact / severity / bounty:** Critical, first HackerOne bug (paid crit)
- **Obstacles & how solved:** Bank fraud teams flagged the activity ("Who are you? Why are you sending 1 penny with nonsensical strings?"); needed 7+ real accounts

#### Zero Interaction ATO via Object State Endpoints
- **Target/context:** Redacted Live Hacking Event target
- **Root cause:** Endpoints that expose object properties change their response based on object state (invited, active, banned, deleted). Same endpoint, different state → different data leaked
- **Technique / how found:** Mapped every endpoint that references a user object and documented which properties each endpoint exposes. Found that endpoints accessible to all users leak invitation tokens when object is in specific states
- **Key technical details:** Object states: active, inactive, deleted, invited, revoked, banned; same endpoint + different state = invitation token disclosure
- **Impact / severity / bounty:** Zero-interaction account takeover chain
- **Obstacles & how solved:** Required deep understanding of the full ecosystem, not just one app

#### SSRF via OAuth Redirect URI Abuse
- **Target/context:** Ecosystem target with developer sandbox + OAuth
- **Root cause:** OAuth response type parameter accepts arbitrary values → when invalid, redirect happens anyway → open redirect. Combined with host-based allowlists that trust the same host used for developer sandbox apps
- **Technique / how found:** Was blocked by host-based SSRF validation. Found that developer sandbox allows registering redirect URIs on the same hostnames trusted by production. OAuth's `response_type` param (set to nonsensical value) triggers redirect to whitelisted redirect URI bypassing validation
- **Exploitation steps:**
  1. Register as developer on target ecosystem
  2. Create a test app with a redirect URI on the same hostname trusted by production
  3. Attack SSRF endpoint with that hostname
  4. Use OAuth flow with invalid `response_type` to force redirect to your controlled URI
- **Key technical details:** OAuth `response_type` parameter; setting it to nonsense values triggers redirect to the registered `redirect_uri` — weaponized as open redirect
- **Impact / severity / bounty:** Multiple SSRFs unlocked; characterized as inherent design flaw between teams not coordinating
- **Obstacles & how solved:** Two different architectural teams didn't communicate; developer sandbox was on same hostnames as production

### Techniques and Primitives
- **Attack vector ideation document** — Preload a living document with every possible attack vector for a target, check them off as tested, add new ones as understanding deepens. Critical for part-time hunters who context-switch
- **Ecosystem hacking** — Focus on the interconnected apps/APIs rather than one app; discrepancies in access control across technologies are gold
- **Object property enumeration by state** — Map which endpoints expose which properties of an object, then iterate the object through different states (invited, active, banned, etc.) — same endpoint + different state = different information disclosed
- **OAuth response_type abuse** — Invalid `response_type` values trigger fallback redirect; combined with developer sandbox on same hostname, bypasses SSRF host restrictions

### Tooling and Resources
- Open Banking API spec (open standard for EU bank-to-bank)
- Burp Suite (notes, files, Repeater)
- Franz Rosen (mentioned as top performer at LHEs)

### Suggestions and Advices from Hunter
- "The purpose of recon is to find more apps to hack." — Jason Haddix (quoted)
- "Client side can really be useful in informing the way you make assumptions about the server side." — Rhynorater
- "Spending time on a wider ecosystem and understanding all the components can be incredibly useful." — gr3pme
- "If you aren't full-time hunting and don't have much time... putting in that investment to go through signup/configuration will pay off about 90% of the time." — gr3pme

### AI Takeaway
Attack vector ideation — the practice of preloading a massive document of possible attack vectors before deep-diving — is the highest-leverage underrated skill. The OAuth response_type → open redirect trick is broadly applicable across the many OAuth implementations in modern apps.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Journey from 0 bug bounty experience to Live Hacking Event performer in ~10 months via mentorship

#### 2. What you should learn
- Understand **build a preloaded "attack vector ideation" document before starting any target — list every possible attack vector no matter how improbable**
- Understand **use the products you already pay for as bug bounty targets — you already have access, familiarity, and legitimate reason to probe**
- Understand **pick targets with geographic/paywall friction to reduce dupe competition**
- Understand **take collaboration leads seriously even when your spidey sense says "not sketchy"**
- Understand **prioritize gym, eating, and breaks even at lhes — brute force leads to burnout**

#### 3. Core concepts explained
**FinTech Bank ATO — Stored XSS via Payment Reference**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**Zero Interaction ATO via Object State Endpoints**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SSRF via OAuth Redirect URI Abuse**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Attack vector ideation document**
- Preload a living document with every possible attack vector for a target, check them off as tested, add new ones as understanding deepens. Critical for part-time hunters who context-switch

**Ecosystem hacking**
- Focus on the interconnected apps/APIs rather than one app; discrepancies in access control across technologies are gold

**Object property enumeration by state**
- Map which endpoints expose which properties of an object, then iterate the object through different states (invited, active, banned, etc.) — same endpoint + different state = different information disclosed


#### 4. Techniques and tactics
**Attack vector ideation document**
- **What it is:** Preload a living document with every possible attack vector for a target, check them off as tested, add new ones as understanding deepens. Critical for part-time hunters who context-switch
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Ecosystem hacking**
- **What it is:** Focus on the interconnected apps/APIs rather than one app; discrepancies in access control across technologies are gold
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Object property enumeration by state**
- **What it is:** Map which endpoints expose which properties of an object, then iterate the object through different states (invited, active, banned, etc.) — same endpoint + different state = different information disclosed
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**OAuth response_type abuse**
- **What it is:** Invalid `response_type` values trigger fallback redirect; combined with developer sandbox on same hostname, bypasses SSRF host restrictions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The purpose of recon is to find more apps to hack."* — **Jason Haddix (quoted)**
- *"Client side can really be useful in informing the way you make assumptions about the server side."* — **Rhynorater**
- *"Spending time on a wider ecosystem and understanding all the components can be incredibly useful."* — **gr3pme**
- *"If you aren't full-time hunting and don't have much time... putting in that investment to go through signup/configuration will pay off about 90% of the time."* — **gr3pme**

#### 6. Mental models
- **The purpose of recon is to find more apps to hack." — Jason ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Client side can really be useful in informing the way you ma** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Spending time on a wider ecosystem and understanding all the** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Build a preloaded "attack vector ideation" document before starting any target — list every possible attack vector no matter how improbable
- **Try this:** Use the products you already pay for as bug bounty targets — you already have access, familiarity, and legitimate reason to probe
- **Try this:** Pick targets with geographic/paywall friction to reduce dupe competition
- **Try this:** Take collaboration leads seriously even when your spidey sense says "not sketchy"

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Bank fraud teams flagged the activity ("Who are you? Why are you sending 1 penny with nonsensical strings?"); needed 7+ real accounts
- - Obstacles & how solved: Required deep understanding of the full ecosystem, not just one app

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in FinTech Bank ATO — Stored XSS via Payment Reference?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Journey from 0 bug bounty experience to Live Hacking Event performer in ~10 mont**
2. **Build a preloaded "attack vector ideation" document before starting any target —**
3. **Use the products you already pay for as bug bounty targets — you already have ac**
