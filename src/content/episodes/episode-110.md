---
title: "Oauth Gadget Correlation and Common Attacks"
episode: 110
---


# Episode 110 Oauth Gadget Correlation and Common Attacks

### TL;DR
- DOMPurify 3.2.3 bypass via HTML comment parsing difference (`<!` without `--` triggers mutation XSS)
- OAuth client credentials flow: client secret + client ID = token for the *client* entity, not a user — can leak all tenant users
- Mutable claims attacks in OAuth (Azure AD tenant creation with victim's email)
- Client confusion attack: app trusts token from its own OAuth flow but doesn't validate issuer; attacker presents token from their own app
- Device authorization flow bypasses need for redirect URI — key for OAuth gadget correlation

### Key Takeaways
- When you find an OAuth client secret, use the client credentials flow (`grant_type=client_credentials`) to get a token — that token is for the *client* entity and may have API access to list/manage users
- For client confusion attacks: if an app accepts an `id_token` or `token` directly and doesn't validate the `aud`/`iss` claim, provide a token from your own OAuth app
- Mutable claims: in Azure AD, create your own tenant with a user whose email matches the victim; when the app checks `email` claim instead of `sub`, you get ATO
- Device authorization flow (`urn:ietf:wg:oauth:2.0:oob`) can serve as a universal redirect — no redirect URI needed
- Build OAuth "gadget" lists: endpoints that leak scope, redirect URIs, project IDs, client IDs — correlate them

### Bugs and Findings

#### DOMPurify 3.2.3 Bypass — Mutation XSS
- **Target/context:** DOMPurify default configuration
- **Root cause:** DOMPurify and browser disagree on what constitutes an HTML comment. `<!--` vs `<!` — WHATWG spec accommodates forgetting the `--`, DOMPurify didn't
- **Technique / how found:** Send `<!` to start a comment (browser accepts), DOMPurify doesn't parse as comment → mutation XSS
- **Key technical details:** Using `<!` instead of `<!--` creates parser differential. Combined with liberal template injection sanitization that strips everything inside `<template>`.
- **Impact / severity / bounty:** Bypass of default DOMPurify config — XSS
- **Obstacles & how solved:** Reduced bypass to primitives; reused existing mutation XSS patterns from Yaniv Nizry

#### OAuth Client Credentials Abuse — API Data Leak
- **Target/context:** Mobile apps / SPA clients with embedded client secrets
- **Root cause:** Client secret is extractable (Frida hook on mobile); client credentials flow gives token for the *client*, not a user — with overly permissive scopes
- **Technique / how found:** Extract client secret via Frida; use `grant_type=client_credentials` with `client_id` + `client_secret`; hit API endpoints that list users
- **Exploitation steps:**
  1. Extract client_id and client_secret from mobile app (Frida, decompilation)
  2. POST to token endpoint: `grant_type=client_credentials&client_id=...&client_secret=...`
  3. Use resulting token against API endpoints (e.g., `/api/users`, `/api/tenants`)
- **Key technical details:** Client credentials flow gives a token representing the *application itself*, not an authenticated user; some APIs return all users/tenants
- **Impact / severity / bounty:** Can leak all authenticated users of a tenant
- **Obstacles & how solved:** Need to recognize that client secret ≠ nothing; it has specific permissions

#### Azure AD Mutable Claims ATO
- **Target/context:** Apps using "Login with Microsoft"/"Login with Azure"
- **Root cause:** App checks `email` claim instead of `sub` claim in JWT
- **Technique / how found:** Spin up own Azure tenant; create a user with victim's email (no verification needed); do OAuth flow from that tenant
- **Key technical details:** JWT `sub` claim is immutable and per-tenant; `email` claim is controller by tenant admin. App checking `email` trusts the attacker-controlled email.
- **Impact / severity / bounty:** Full account takeover
- **Obstacles & how solved:** Need to find target that uses email claim for auth

### Techniques and Primitives
- **OAuth gadget correlation** — Build a map of: API keys → project IDs → client IDs → redirect URIs → tokens. Each "gadget" leaks one piece of the puzzle.
- **Device code flow as universal redirect** — `urn:ietf:wg:oauth:2.0:oob` or `urn:ietf:wg:oauth:2.0:oob:auto` works without registered redirect URI
- **Mutable claims attack** — In Azure AD, create tenant → create user with victim email → the `email` claim matches victim
- **Client confusion attack** — Token from App A presented to App B; if B doesn't validate `aud`/`iss`, attacker controls token content

### Tooling and Resources
- Frida (for extracting mobile app client secrets)
- DOMPurify 3.2.3 bypass writeup by nc.zip
- postLogger Chrome Extension (postMessage tracker for Manifest V3)
- DoyanSec OAuth security cheat sheet

### Suggestions and Advices from Hunter
- "Follow the auth flow backwards — search for bearer token strings in HTTP history to trace where they come from"
- "Don't just swap IDs for IDOR — also look at how auth is structured; try removing the password field entirely"
- "Verbose errors are gold — they leak gadget info"
- "Token introspection endpoints can leak scope/permissions"

### AI Takeaway
The OAuth gadget correlation strategy is high-leverage: building a system to log API keys, correlate project IDs to client IDs, and maintain a map of OAuth endpoints transforms scattered recon into a systematic attack surface. The device flow as universal redirect is a particularly useful primitive.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
DOMPurify 3.2.3 bypass via HTML comment parsing difference (`<!` without `--` triggers mutation XSS)

#### 2. What you should learn
- Understand **when you find an oauth client secret, use the client credentials flow (`grant_type=client_credentials`) to get a token — that token is for the *client* entity and may have api access to list/manage users**
- Understand **for client confusion attacks: if an app accepts an `id_token` or `token` directly and doesn't validate the `aud`/`iss` claim, provide a token from your own oauth app**
- Understand **mutable claims: in azure ad, create your own tenant with a user whose email matches the victim; when the app checks `email` claim instead of `sub`, you get ato**
- Understand **device authorization flow (`urn:ietf:wg:oauth:2.0:oob`) can serve as a universal redirect — no redirect uri needed**
- Understand **build oauth "gadget" lists: endpoints that leak scope, redirect uris, project ids, client ids — correlate them**

#### 3. Core concepts explained
**DOMPurify 3.2.3 Bypass — Mutation XSS**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**OAuth Client Credentials Abuse — API Data Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Azure AD Mutable Claims ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**OAuth gadget correlation**
- Build a map of: API keys → project IDs → client IDs → redirect URIs → tokens. Each "gadget" leaks one piece of the puzzle.

**Device code flow as universal redirect**
- `urn:ietf:wg:oauth:2.0:oob` or `urn:ietf:wg:oauth:2.0:oob:auto` works without registered redirect URI

**Mutable claims attack**
- In Azure AD, create tenant → create user with victim email → the `email` claim matches victim


#### 4. Techniques and tactics
**OAuth gadget correlation**
- **What it is:** Build a map of: API keys → project IDs → client IDs → redirect URIs → tokens. Each "gadget" leaks one piece of the puzzle.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Device code flow as universal redirect**
- **What it is:** `urn:ietf:wg:oauth:2.0:oob` or `urn:ietf:wg:oauth:2.0:oob:auto` works without registered redirect URI
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Mutable claims attack**
- **What it is:** In Azure AD, create tenant → create user with victim email → the `email` claim matches victim
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Client confusion attack**
- **What it is:** Token from App A presented to App B; if B doesn't validate `aud`/`iss`, attacker controls token content
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Follow the auth flow backwards"* — **search for bearer token strings in HTTP history to trace where they come from**
- *"Don't just swap IDs for IDOR"* — **also look at how auth is structured; try removing the password field entirely**
- *"Verbose errors are gold"* — **they leak gadget info**
- *"Token introspection endpoints can leak scope/permissions"*

#### 6. Mental models
- **Follow the auth flow backwards — search for bearer token str** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Don't just swap IDs for IDOR — also look at how auth is stru** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Verbose errors are gold — they leak gadget info** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** When you find an OAuth client secret, use the client credentials flow (`grant_type=client_credentials`) to get a token — that token is for the *client* entity and may have API access to list/manage users
- **Try this:** For client confusion attacks: if an app accepts an `id_token` or `token` directly and doesn't validate the `aud`/`iss` claim, provide a token from your own OAuth app
- **Try this:** Mutable claims: in Azure AD, create your own tenant with a user whose email matches the victim; when the app checks `email` claim instead of `sub`, you get ATO
- **Try this:** Device authorization flow (`urn:ietf:wg:oauth:2.0:oob`) can serve as a universal redirect — no redirect URI needed

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Reduced bypass to primitives; reused existing mutation XSS patterns from Yaniv Nizry
- - Obstacles & how solved: Need to recognize that client secret ≠ nothing; it has specific permissions

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **API** — Application Programming Interface — structured endpoints for data exchange
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in DOMPurify 3.2.3 Bypass — Mutation XSS?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **DOMPurify 3.2.3 bypass via HTML comment parsing difference (`<!` without `--` tr**
2. **When you find an OAuth client secret, use the client credentials flow (`grant_ty**
3. **For client confusion attacks: if an app accepts an `id_token` or `token` directl**
