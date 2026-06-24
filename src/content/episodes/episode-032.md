---
title: "The Great Write-up Low-down"
episode: 32
---


# Episode 32 The Great Write-up Low-down

**Guests/Hosts:** Justin Gardner (solo — Joel had con flu)  
**Date:** 2023-08-17 | **Duration:** 1:01:05

### TL;DR
- Solo episode covering major write-ups and research from DefCon season
- James Kettle's "Smashing the State Machine" — HTTP/2 single-packet attack for sub-millisecond race condition sync
- Sirush's cookie-less session token injection in IIS (.NET) — path restriction bypass
- Ophion Security's Shopify store account takeover via unverified email + disabled-but-accessible Shop Pay OAuth
- Sam Curry's points.com hack: secondary context exploitation, weak JWT secret (`"secret"`), leaking 22M records
- Lupin/Holmes' sandwich attack: UUIDv1 predictable tokens for ATO

### Key Takeaways
- **Single-packet attack**: Send all HTTP/2 request headers except the last byte + omit END_STREAM flag; all requests arrive in one TCP packet → sub-ms synchronization for race conditions
- **IIS cookie-less session injection**: `/(S(X))/` in path is stripped by .NET `RemoveAppPathModifier` → bypasses all path-based restrictions
- **ChatGPT for IIS short name guessing**: Use OpenAI API to predict full names from 6-char short names (~35 lines of code)
- **Sam Curry's secondary context hacking**: When an API concatenates user input into a backend request URL, try adding `#`, `?`, `../` to leak backend paths and hit unintended endpoints

### Bugs and Findings

#### GitLab email race condition — Race condition
- **Target/context:** GitLab
- **Root cause:** When changing email, a function is async-called with the new email as parameter. Inside, the `confirmation_token` is fetched from the DB at render time. A race condition between two email changes can swap the tokens.
- **Technique / how found:** James Kettle's race condition research; single-packet attack for timing
- **Exploitation steps:**
  1. Send ChangeEmail request 1 to `test1@attacker.com`
  2. Simultaneously send ChangeEmail request 2 to `test2@attacker.com`
  3. Email body is generated with confirmation_token from request 2's DB state but sent to `test1@attacker.com`
- **Key technical details:** Token fetched from DB during template rendering, not passed as parameter

#### Points.com mass data leak via secondary context — IDOR
- **Target/context:** Points.com rewards platform (Delta, United, Marriott, etc.)
- **Root cause:** The `lpId` parameter is concatenated into backend API URLs without sanitization; `mvpPayload` accepts arbitrary POST parameters
- **Technique / how found:** Sam Curry's team used wayback machine, JS analysis, paid for miles to trace auth flow → found membership auth token leak in response headers
- **Exploitation steps:**
  1. Send miles: response includes victim's `membershipAuthorizationToken`
  2. Use `#`, `../` in `lpId` to traverse backend URL to different API endpoints
  3. Fuzz `mvpPayload` → found it accepts arbitrary query params → added `q=` parameter to search endpoint → 22M records dumped
- **Key technical details:** `lpId=UUID#$../` backend request becomes `GET /api/v1/search/orders?q=[payload]` | Static JWT secret `"secret"` on console.points.com
- **Impact / severity / bounty:** 22M transaction records leaked; ATO on multiple airline/hotel accounts

#### Points.com JWT secret `"secret"` — Weak crypto
- **Target/context:** Points.com console admin panel
- **Root cause:** JWT signing key = literally the word `"secret"`
- **Technique / how found:** Brute-forced via CookieMonster tool
- **Impact / severity / bounty:** Arbitrary session forging → full admin access to all rewards programs

#### UUIDv1 Sandwich Attack — ATO
- **Target/context:** Application using UUIDv1 for password reset tokens
- **Root cause:** UUIDv1 encodes timestamp; tokens are predictable if you can create two reference tokens around the target's token
- **Technique / how found:** Lupin/Holmes
- **Exploitation steps:**
  1. Request password reset for your own account (bottom bread)
  2. Request password reset for victim account (meat)
  3. Request password reset for your account again (top bread)
  4. Compute timestamp range from bottom/top UUIDs
  5. Brute-force all UUIDs in that range to find victim's token
- **Key technical details:** UUIDv1: version digit = `1` in 3rd segment | Timestamp in milliseconds; 1000 possibilities per second | Thin sandwich = faster brute force

### Techniques and Primitives
- **Single-packet attack (HTTP/2)** — Send all full HTTP/2 frames except last byte + no END_STREAM flag; all arrive in same TCP packet → sub-ms sync | Implementation: use h2 library, set END_STREAM=false, omit last byte
- **Secondary context exploitation** — Insert `#`, `../`, `?` into path params to manipulate backend URL resolution; detect via 400 vs 200 responses
- **Content discovery with Chat GPT** — For IIS short names: feed partial name to GPT-3/3.5 API → get predicted full names

### Tooling and Resources
- James Kettle's "Smashing the State Machine" paper
- PortSwigger's single-packet attack implementation (Burp)
- Sirush's blog: `sirush.me` — IIS cookie-less session techniques
- ShortNameGuesser (Monke's tool using GPT-3)
- CookieMonster (Ian Carroll) — JWT secret brute-forcer
- CVSS Advisor (cvssadvisor.com) — community tool for CVSS escalation advice

### Suggestions and Advices from Hunter
- James Kettle: "The whole concept for this single-packet attack is sending the full body except the last byte" → abusing Nagel's algorithm
- Sam Curry method: "Always pay the money. If you see a place where you could pay money and it's reasonable, get excited — that's ROI."
- "Learn secondary context attacks. Sam Curry's presentation is mandatory reading."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Solo episode covering major write-ups and research from DefCon season

#### 2. What you should learn
- Understand **single-packet attack**: send all http/2 request headers except the last byte + omit end_stream flag; all requests arrive in one tcp packet → sub-ms synchronization for race conditions**
- Understand **iis cookie-less session injection**: `/(s(x))/` in path is stripped by .net `removeapppathmodifier` → bypasses all path-based restrictions**
- Understand **chatgpt for iis short name guessing**: use openai api to predict full names from 6-char short names (~35 lines of code)**
- Understand **sam curry's secondary context hacking**: when an api concatenates user input into a backend request url, try adding `#`, `?`, `../` to leak backend paths and hit unintended endpoints**

#### 3. Core concepts explained
**GitLab email race condition — Race condition**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Points.com mass data leak via secondary context — IDOR**
- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.
- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.
- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.

**Points.com JWT secret `"secret"` — Weak crypto**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Single-packet attack (HTTP/2)**
- Send all full HTTP/2 frames except last byte + no END_STREAM flag; all arrive in same TCP packet → sub-ms sync | Implementation: use h2 library, set END_STREAM=false, omit last byte

**Secondary context exploitation**
- Insert `#`, `../`, `?` into path params to manipulate backend URL resolution; detect via 400 vs 200 responses

**Content discovery with Chat GPT**
- For IIS short names: feed partial name to GPT-3/3.5 API → get predicted full names


#### 4. Techniques and tactics
**Single-packet attack (HTTP/2)**
- **What it is:** Send all full HTTP/2 frames except last byte + no END_STREAM flag; all arrive in same TCP packet → sub-ms sync | Implementation: use h2 library, set END_STREAM=false, omit last byte
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Secondary context exploitation**
- **What it is:** Insert `#`, `../`, `?` into path params to manipulate backend URL resolution; detect via 400 vs 200 responses
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Content discovery with Chat GPT**
- **What it is:** For IIS short names: feed partial name to GPT-3/3.5 API → get predicted full names
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"James Kettle: "The whole concept for this single-packet attack is sending the full body except the last byte" → abusing Nagel's algorithm"*
- *"Sam Curry method: "Always pay the money. If you see a place where you could pay money and it's reasonable, get excited"* — **that's ROI.**
- *"Learn secondary context attacks. Sam Curry's presentation is mandatory reading."*

#### 6. Mental models
- **James Kettle: "The whole concept for this single-packet atta** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Sam Curry method: "Always pay the money. If you see a place ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Learn secondary context attacks. Sam Curry's presentation is** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Single-packet attack**: Send all HTTP/2 request headers except the last byte + omit END_STREAM flag; all requests arrive in one TCP packet → sub-ms synchronization for race conditions
- **Try this:** IIS cookie-less session injection**: `/(S(X))/` in path is stripped by .NET `RemoveAppPathModifier` → bypasses all path-based restrictions
- **Try this:** ChatGPT for IIS short name guessing**: Use OpenAI API to predict full names from 6-char short names (~35 lines of code)
- **Try this:** Sam Curry's secondary context hacking**: When an API concatenates user input into a backend request URL, try adding `#`, `?`, `../` to leak backend paths and hit unintended endpoints

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **JWT** — JSON Web Token — compact token format for authentication
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GitLab email race condition — Race condition?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Solo episode covering major write-ups and research from DefCon season**
2. **Single-packet attack**: Send all HTTP/2 request headers except the last byte + o**
3. **IIS cookie-less session injection**: `/(S(X))/` in path is stripped by .NET `Rem**
