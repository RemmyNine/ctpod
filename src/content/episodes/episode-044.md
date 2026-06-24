---
title: "URL Parsing & Auth Bypass Magic"
episode: 44
---


# Episode 44 URL Parsing & Auth Bypass Magic

### TL;DR
- Deep dive into all 9 parts of a URL (scheme, user:pass, domain, port, path, query, fragment, path-parameters)
- XNL Reveal Chrome extension: alerts on reflected query params, shows hidden/disabled elements
- OAuth account takeover via Facebook login — remove email scope, use unverified email trick
- URL parser disagreement on file:// scheme — one parser treats `?` as query, other as path character
- JWT shared secrets across environments, MFA bypass via IDOR on authentication devices

### Key takeaways
- username:password@host can bypass open redirect/host validation checks — backslash (`\`) injected into username bypasses the @ parsing
- Fragment (`#`) is "a comment in a URL" — use it to truncate suffixes appended by the server
- Path-parameters (`;`) — orange's `..;/` trick for path traversal bypass
- Test double-slash `//` for open redirect: `//attacker.com` is an absolute URL, not relative
- Token reuse across environments: if staging and prod share JWT signing secret, register on staging, use same JWT on prod

### Bugs and Findings
#### Facebook OAuth ATO via Email Scope Removal
- **Target/context:** Sites that allow "Login with Facebook"
- **Root cause:** Facebook's OAuth allows logging in without sharing email (scope removal)
- **Technique / how found:** (Jash25):
  1. Log in with Facebook but remove the email scope
  2. Site asks for email manually — enter victim's email
  3. Confirmation link sent to victim's email
  4. Log in again with Facebook, this time sharing your own email
  5. Same email activation link gets sent to the new email
  6. Use the old link to verify the victim's account
- **Impact / severity / bounty:** $16,000 bounty
- **Note:** Tanner Cash (Intigriti) tweeted this exact tip in August 2019 — 4 years earlier

#### Canva URL Parser Disagreement
- **Target/context:** File upload feature using `file://` scheme URLs
- **Root cause:** Two URL parsers disagree on the role of `?` in a `file://` URL
  - Parser 1: treats `?` as query start → trims rest of path
  - Parser 2: treats `?` as part of the path → allows path traversal after it
- **Technique / how found:**
  1. Send `file:///path/to/file?.` (one dot = current dir passes Parser 1 check)
  2. After the `?`, add `../../../../etc/passwd`
  3. Parser 2 resolves the full traversal and reads the file
- **Key technical details:** File scheme URLs can contain `?` — on Linux you can create a file with `?` in its name
- **Impact / severity / bounty:** Arbitrary file read via SVG inclusion

#### Grammarly OAuth ATO (Salt Labs)
- **Technique:** Facebook's implicit grant flow returns an access token directly to the client; the server must call the debug endpoint to verify the token belongs to its own app. If this verification is skipped, an attacker can use a token generated for their own Facebook app to log into Grammarly as any user of their app
- **Key technical detail:** Requires victim to be a user of the attacker's Facebook app

### Techniques and Primitives
- **URL fragment as truncation** — `#` stops server-side processing; use to bypass appended extensions
- **Double-slash open redirect** — `//` is protocol-relative; `//attacker.com` may pass `starts with /` checks
- **Token recipient confusion** — use JWT from one environment/sub-app on a different one that shares the same signing secret

### Suggestions and Advices from Hunter
- "The hash is like a comment in a URL — everything after it is ignored by the server"
- "People that try high-impact attack vectors find high-impact bugs. It's simple."
- On OAuth: "If a website doesn't verify the token is for their own app, they'll accept a token generated for any app"

### AI Takeaway
The URL parser disagreement on `file://` scheme is a perfect example of how spec ambiguity creates exploit opportunities. The fact that `?` is a valid filename character on Linux means treating it as a query delimiter in a `file://` URL is technically a bug.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Deep dive into all 9 parts of a URL (scheme, user:pass, domain, port, path, query, fragment, path-parameters)

#### 2. What you should learn
- Understand **username:password@host can bypass open redirect/host validation checks — backslash (`\`) injected into username bypasses the @ parsing**
- Understand **fragment (`#`) is "a comment in a url" — use it to truncate suffixes appended by the server**
- Understand **path-parameters (`;`) — orange's `..;/` trick for path traversal bypass**
- Understand **test double-slash `//` for open redirect: `//attacker.com` is an absolute url, not relative**
- Understand **token reuse across environments: if staging and prod share jwt signing secret, register on staging, use same jwt on prod**

#### 3. Core concepts explained
**Facebook OAuth ATO via Email Scope Removal**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Canva URL Parser Disagreement**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Grammarly OAuth ATO (Salt Labs)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**URL fragment as truncation**
- `#` stops server-side processing; use to bypass appended extensions

**Double-slash open redirect**
- `//` is protocol-relative; `//attacker.com` may pass `starts with /` checks

**Token recipient confusion**
- use JWT from one environment/sub-app on a different one that shares the same signing secret


#### 4. Techniques and tactics
**URL fragment as truncation**
- **What it is:** `#` stops server-side processing; use to bypass appended extensions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Double-slash open redirect**
- **What it is:** `//` is protocol-relative; `//attacker.com` may pass `starts with /` checks
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Token recipient confusion**
- **What it is:** use JWT from one environment/sub-app on a different one that shares the same signing secret
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The hash is like a comment in a URL"* — **everything after it is ignored by the server**
- *"People that try high-impact attack vectors find high-impact bugs. It's simple."*
- *"On OAuth: "If a website doesn't verify the token is for their own app, they'll accept a token generated for any app"*

#### 6. Mental models
- **The hash is like a comment in a URL — everything after it is** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **People that try high-impact attack vectors find high-impact ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On OAuth: "If a website doesn't verify the token is for thei** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** username:password@host can bypass open redirect/host validation checks — backslash (`\`) injected into username bypasses the @ parsing
- **Try this:** Fragment (`#`) is "a comment in a URL" — use it to truncate suffixes appended by the server
- **Try this:** Path-parameters (`;`) — orange's `..;/` trick for path traversal bypass
- **Try this:** Test double-slash `//` for open redirect: `//attacker.com` is an absolute URL, not relative

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **JWT** — JSON Web Token — compact token format for authentication
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Facebook OAuth ATO via Email Scope Removal?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Deep dive into all 9 parts of a URL (scheme, user:pass, domain, port, path, quer**
2. **username:password@host can bypass open redirect/host validation checks — backsla**
3. **Fragment (`#`) is "a comment in a URL" — use it to truncate suffixes appended by**
