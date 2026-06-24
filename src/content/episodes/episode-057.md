---
title: "Technical Breakdown from Miami Hacking Event — H1-305"
episode: 57
---


# Episode 57 Technical Breakdown from Miami Hacking Event — H1-305

**Guests:** Justin Gardner (Rhynorater), Joel Margolis (Teknogeek)
**Format:** Full transcript (ASR) — recording from H1-305 Miami live hacking event, target is Capital One

### TL;DR
- Live hacking event debrief from H1-305 Miami (Capital One) — recorded onsite
- Justin had 40 bugs at the time of recording, expects total payouts of 300–400K
- Client-side path traversal predicted as "the new CSRF" — growing bug class driven by browser same-site default changes
- Joel spent 25 hours on a heavily obfuscated mobile app, got past obfuscation but found no further bugs — tracked time for first time, helped decide when to cut losses
- HTML5 spec weirdness: `<image>` tag auto-converts to `<img>` in non-SVG context — useful for WAF bypasses

### Key Takeaways
- Client-side path traversal + open redirect + fetch auto-follows redirects = XSS in even sanitized environments (because response is trusted from the API, not expected to be attacker-controlled)
- Track your time during events — it helps with cutting losses and managing ADHD/focus
- Understand auth flows intimately, especially in merged/acquired company infrastructure — OAuth ATO via first-party consent bypass and third-party application registration
- Third-party widgets/analytics brought into secure environments are frequently not security-reviewed — prime attack surface
- Look at any company re-implementing standard auth (SAML, OAuth) in-house — they likely made implementation errors

### Bugs and Findings

#### Capital One Client-Side CSP-Locked XSS Near-Miss
- **Target/context:** Capital One app — a URL parameter controlled the API host for fetch requests; CSP connect-src was `self` + `*.googleapis.com`
- **Technique / how found:** Parameter injection → dynamically constructed fetch URL → could redirect the API host
- **Obstacles:**
  - CSP connect-src blocked arbitrary hosts
  - `*.googleapis.com` allowed — tried storage.googleapis.com but it doesn't return `Access-Control-Allow-Credentials: true` for credentialed fetch requests
  - Tried data: URI with fetch (works in console, blocked by CSP)
  - Found `storage.googleapis.com` JSON API echoes origin into `Access-Control-Allow-Origin` + returns `Access-Control-Allow-Credentials: true` — but metadata endpoint, not content
  - There's a parameter to return object content instead of metadata — success! Got data into response
  - Sink: `window.location.href` sync after the fetch — but CSP `script-src` blocked execution
  - SessionStorage caching of API host enabled cache poisoning — but sessionStorage cleared on each request
- **Result:** Dead end after 8 hours — could not achieve XSS or data leak

### Techniques and Primitives
- **Client-side path traversal escalation:** Inject into a dynamically-constructed fetch URL → traverse to an open redirect → fetch follows redirect automatically → response injected into DOM from a trusted (but attacker-poisoned) origin
- **Logout via image tag:** Stored image injection with `src` pointing to logout endpoint → user logs out on dashboard load → forced re-auth loop
- **Login CSRF via image:** If no logout CSRF but login CSRF exists, repeatedly log victim into attacker-controlled account → permanent denial of access to own account

### Suggestions and Advices
- **Justin:** "Client-side path traversal is going to be the new CSRF in the near future."
- **Joel:** Tracking time is "good to feel like I'm making progress and not just sitting still."
- **Joel:** "When you do a lot of collaboration, it's really just like sitting around waiting for somebody else to come up with something."
- **Justin:** "Know when to cut your losses. I sunk 8 hours into a bug and it was a mistake."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Live hacking event debrief from H1-305 Miami (Capital One) — recorded onsite

#### 2. What you should learn
- Understand **client-side path traversal + open redirect + fetch auto-follows redirects = xss in even sanitized environments (because response is trusted from the api, not expected to be attacker-controlled)**
- Understand **track your time during events — it helps with cutting losses and managing adhd/focus**
- Understand **understand auth flows intimately, especially in merged/acquired company infrastructure — oauth ato via first-party consent bypass and third-party application registration**
- Understand **third-party widgets/analytics brought into secure environments are frequently not security-reviewed — prime attack surface**
- Understand **look at any company re-implementing standard auth (saml, oauth) in-house — they likely made implementation errors**

#### 3. Core concepts explained
**Capital One Client-Side CSP-Locked XSS Near-Miss**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

****Client**
- A technique discussed in this episode for security research and bug bounty hunting.

**Logout via image tag: Stored image injection with `src` pointing to logout endpoint → user logs out on dashboard load → forced re**
- A technique discussed in this episode for security research and bug bounty hunting.

**Login CSRF via image: If no logout CSRF but login CSRF exists, repeatedly log victim into attacker**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**Client-side path traversal escalation: Inject into a dynamically-constructed fetch URL → traverse to an open redirect → fetch follows redirect automatically → response injected into DOM from a trusted (but attacker-poisoned) origin**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Logout via image tag: Stored image injection with `src` pointing to logout endpoint → user logs out on dashboard load → forced re-auth loop**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Login CSRF via image: If no logout CSRF but login CSRF exists, repeatedly log victim into attacker-controlled account → permanent denial of access to own account**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Justin: "Client-side path traversal is going to be the new CSRF in the near future."*
- *"Joel: Tracking time is "good to feel like I'm making progress and not just sitting still."*
- *"Joel: "When you do a lot of collaboration, it's really just like sitting around waiting for somebody else to come up with something."*
- *"Justin: "Know when to cut your losses. I sunk 8 hours into a bug and it was a mistake."*

#### 6. Mental models
- **Justin: "Client-side path traversal is going to be the new C** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: Tracking time is "good to feel like I'm making progres** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joel: "When you do a lot of collaboration, it's really just ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Client-side path traversal + open redirect + fetch auto-follows redirects = XSS in even sanitized environments (because response is trusted from the API, not expected to be attacker-controlled)
- **Try this:** Track your time during events — it helps with cutting losses and managing ADHD/focus
- **Try this:** Understand auth flows intimately, especially in merged/acquired company infrastructure — OAuth ATO via first-party consent bypass and third-party application registration
- **Try this:** Third-party widgets/analytics brought into secure environments are frequently not security-reviewed — prime attack surface

#### 8. Red flags and pitfalls
- - Obstacles:
- - CSP connect-src blocked arbitrary hosts
- - Tried data: URI with fetch (works in console, blocked by CSP)
- - Sink: `window.location.href` sync after the fetch — but CSP `script-src` blocked execution

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Capital One Client-Side CSP-Locked XSS Near-Miss?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Live hacking event debrief from H1-305 Miami (Capital One) — recorded onsite**
2. **Client-side path traversal + open redirect + fetch auto-follows redirects = XSS **
3. **Track your time during events — it helps with cutting losses and managing ADHD/f**
