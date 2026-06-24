---
title: "Attacking OAuth 2.1"
episode: 169
---


# Episode 169 Attacking OAuth 2.1

### TL;DR
- OAuth 2.1 changes: PKCE mandatory, implicit and password credential flows removed, exact redirect URI matching, bearer tokens prohibited in URIs
- Client Identity Metadata Document (CIMD) introduces new SSRF surface — server MUST fetch and validate multiple URIs (client manifest, JWKS, logo)
- Token exchange RFC 8693 aims to fix agent-to-agent delegation but introduces confused deputy risks
- PKCE downgrade attacks occur when servers accept code exchange without a code challenge

### Key Takeaways
- [ ] OAuth 2.1 PKCE is mandatory — test PKCE downgrade by stripping `code_challenge` from authorization request; if server still accepts token exchange, it's a vulnerability
- [ ] CIMD flow: attacker supplies `client_manifest_uri`, server fetches it — SSRF on the metadata verification service; also check `logo_uri` and `jwks_uri` inside the client.json
- [ ] Check for mutable OIDC claims being used as account UID — `preferred_username` is often mutable and not globally unique
- [ ] Test refresh tokens for deactivated users — can a deactivated user's refresh token still fetch new access tokens?
- [ ] Look for transition gaps when frameworks move 2.0→2.1 — compatibility shims often introduce bugs

### Bugs and Findings

#### PKCE Bypass in Cloudflare Workers (CVE-2025-4144)
- **Target/context:** Cloudflare Workers OAuth provider
- **Root cause:** `handleTokenRequest` accepted a `code_verifier` even when the initial authorization request omitted `code_challenge`
- **Technique:** 1) Send authorization request without `code_challenge` 2) Intercept the auth code 3) Exchange it without a valid verifier
- **Key technical details:** MCP specification requires OAuth 2.0; server failed to enforce PKCE on the authorization request
- **Impact / severity / bounty:** Auth code interception; account takeover

#### Django-OAuth Account Takeover (ZeroPath)
- **Target/context:** Django-allauth library (2M monthly downloads)
- **Root cause:** Used `preferred_username` from OAuth response as account UID — this claim is mutable on many providers (Okta, NetIQ)
- **Technique:** Attacker sets their `preferred_username` to victim's username → logs in as victim via OAuth
- **Key technical details:** 7 vulnerabilities found total; mutability of `preferred_username` on Okta and NetIQ; tokens for deactivated users could be refreshed indefinitely
- **Impact / severity / bounty:** Full account takeover

#### OAuth2-Proxy Auth Bypass (CVE-2025-54576)
- **Target/context:** OAuth2-Proxy (Kubernetes gateway)
- **Root cause:** Regex pattern for path-based auth bypass matched against the entire request URI including query parameters
- **Technique:** `/protected-endpoint?skip_auth_regex_pattern` — the regex match succeeds on the query parameter value, not the actual path
- **Key technical details:** Regex matched on `request.URL.String()` which includes query string
- **Impact / severity / bounty:** Complete auth bypass for protected endpoints

### Techniques and Primitives
- **PKCE downgrade attack** — Omit `code_challenge` from auth request; if token exchange still works without verifier, PKCE is bypassed
- **CIMD SSRF** — Supply `client_manifest_uri` pointing to internal/metadata endpoints; also test `logo_uri`, `jwks_uri` inside the client manifest for nested SSRF
- **Token passthrough → confused deputy** — Check if AI agents pass full-privilege tokens to downstream tools instead of scoped tokens
- **Mutable claim abuse** — Test if `preferred_username`, `email`, or other claims can be overwritten on the provider and used as identity

### Tooling and Resources
- zeropath.com — Django-allauth audit, OAuth2-Proxy CVE
- Github advisory GHSA-qgp8-v765-qxx9 — CF Workers PKCE bypass
- RFC 8693 — Token Exchange
- MCP Authorization Spec
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
OAuth 2.1 changes: PKCE mandatory, implicit and password credential flows removed, exact redirect URI matching, bearer tokens prohibited in URIs

#### 2. What you should learn
- Understand **[ ] oauth 2.1 pkce is mandatory — test pkce downgrade by stripping `code_challenge` from authorization request; if server still accepts token exchange, it's a vulnerability**
- Understand **[ ] cimd flow: attacker supplies `client_manifest_uri`, server fetches it — ssrf on the metadata verification service; also check `logo_uri` and `jwks_uri` inside the client.json**
- Understand **[ ] check for mutable oidc claims being used as account uid — `preferred_username` is often mutable and not globally unique**
- Understand **[ ] test refresh tokens for deactivated users — can a deactivated user's refresh token still fetch new access tokens?**
- Understand **[ ] look for transition gaps when frameworks move 2.0→2.1 — compatibility shims often introduce bugs**

#### 3. Core concepts explained
**PKCE Bypass in Cloudflare Workers (CVE-2025-4144)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Django-OAuth Account Takeover (ZeroPath)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**OAuth2-Proxy Auth Bypass (CVE-2025-54576)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**PKCE downgrade attack**
- Omit `code_challenge` from auth request; if token exchange still works without verifier, PKCE is bypassed

**CIMD SSRF**
- Supply `client_manifest_uri` pointing to internal/metadata endpoints; also test `logo_uri`, `jwks_uri` inside the client manifest for nested SSRF

**Token passthrough → confused deputy**
- Check if AI agents pass full-privilege tokens to downstream tools instead of scoped tokens


#### 4. Techniques and tactics
**PKCE downgrade attack**
- **What it is:** Omit `code_challenge` from auth request; if token exchange still works without verifier, PKCE is bypassed
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CIMD SSRF**
- **What it is:** Supply `client_manifest_uri` pointing to internal/metadata endpoints; also test `logo_uri`, `jwks_uri` inside the client manifest for nested SSRF
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Token passthrough → confused deputy**
- **What it is:** Check if AI agents pass full-privilege tokens to downstream tools instead of scoped tokens
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Mutable claim abuse**
- **What it is:** Test if `preferred_username`, `email`, or other claims can be overwritten on the provider and used as identity
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** [ ] OAuth 2.1 PKCE is mandatory — test PKCE downgrade by stripping `code_challenge` from authorization request; if server still accepts token exchange, it's a vulnerability
- **Try this:** [ ] CIMD flow: attacker supplies `client_manifest_uri`, server fetches it — SSRF on the metadata verification service; also check `logo_uri` and `jwks_uri` inside the client.json
- **Try this:** [ ] Check for mutable OIDC claims being used as account UID — `preferred_username` is often mutable and not globally unique
- **Try this:** [ ] Test refresh tokens for deactivated users — can a deactivated user's refresh token still fetch new access tokens?

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in PKCE Bypass in Cloudflare Workers (CVE-2025-4144)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **OAuth 2.1 changes: PKCE mandatory, implicit and password credential flows remove**
2. **[ ] OAuth 2.1 PKCE is mandatory — test PKCE downgrade by stripping `code_challen**
3. **[ ] CIMD flow: attacker supplies `client_manifest_uri`, server fetches it — SSRF**
