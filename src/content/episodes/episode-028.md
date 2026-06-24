---
title: "Surfin' with CSRFs"
episode: 28
---


# Episode 28 Surfin' with CSRFs

**Guests/Hosts:** Justin Gardner, Joel Margolis  
**Date:** 2023-07-20 | **Duration:** 1:18:05

### TL;DR
- CSRF is not dead — SameSite=Lax changed the game but did not eliminate it
- Modern CSRF conditions: GET or POST, top-level navigation, content-type `text/plain`/`form-urlencoded`/`multipart`
- SameSite=Lax bypass via "lax+post" two-minute window: force re-login (GET) to reset cookie timer, then POST
- Rails HEAD method quirk: HEAD routes to same handler as GET; if code has `if request.get? ... else ... end`, HEAD hits the `else` branch
- Custom referrer policy via `<meta name="referrer" content="unsafe-url">` to send full URL (bypassing referrer checks)

### Key Takeaways
- SameSite=Lax (implicit, without explicit attribute) IS subject to the lax+post accommodation; SameSite=Lax (explicitly set) IS NOT — check this before reporting
- Rails HEAD method goes to the GET route; `if request.get?` + `else` catches HEAD → potential CSRF
- Method override params (e.g., `_method=POST`) may allow GET requests to be replayed as POST — worth checking
- Referrer-based CSRF protection is bypassable: use `<meta name="referrer" content="unsafe-url">` on your attacker page to send the full URL, including path

### Bugs and Findings

#### GitHub OAuth CSRF via HEAD method — CSRF
- **Target/context:** GitHub OAuth flow (Rails-based)
- **Root cause:** Rails routes defined as `match ... via: [:get, :post]`. HEAD is routed to the same handler as GET. Code had `if request.get?` (grant) vs `else` (authorize). HEAD hit the `else` (authorize) branch despite being a "read" method.
- **Technique / how found:** Teddy Katz (blog post: "Bypassing GitHub's OAuth flow")
- **Exploitation steps:**
  1. Send a HEAD request to the OAuth authorize endpoint
  2. Rails routes HEAD to the GET handler
  3. `if request.get?` is false (it's HEAD), so the `else` branch runs → authorization is granted
- **Key technical details:** Rails implicit HEAD routing | `if request.get?` guard | Bounty: $25,000
- **Impact / severity / bounty:** OAuth bypass → account takeover; $25K

#### Mobile CSRF via QR code / WebView (CARRF) — Cross-app request forgery
- **Target/context:** TikTok (2019)
- **Root cause:** QR code scanner in app opens arbitrary URLs in internal WebView → JavaScript bridge accessible via `isSafeHost()` check using `.endsWith()` (not `.equals()`) → `notTikTok.com` passes the check
- **Technique / how found:** Joel scanned QR codes → WebView → JS bridge interaction
- **Exploitation steps:**
  1. Encode a URL to `http://notTikTok.com/exploit.html` as QR code
  2. Victim scans QR code inside TikTok app → WebView opens attacker URL
  3. `.endsWith("tikTok.com")` check passes for `notTikTok.com`
  4. JS bridge commands: create popups, install APKs, exfiltrate user info
- **Key technical details:** `.endsWith()` not `.equals()` | Bought domain `notTikTok.com` for $5
- **Impact / severity / bounty:** Full access to JS bridge → data exfiltration, APK install; high

### Techniques and Primitives
- **Force re-login for CSRF** — Open `window.open('https://target.com/login')` to reset cookie → then top-level POST within 2 minutes (lax+post window)
- **Referrer policy bypass** — `<meta name="referrer" content="unsafe-url">` forces the browser to send the full URL (including path) in the `Referer` header
- **Double-click action** — Use form submit + button onclick in same click: `onclick="window.open(...)"` and form submits simultaneously

### Tooling and Resources
- Teddy Katz's "Bypassing GitHub's OAuth flow" blog post
- "The Great SameSite Confusion" by jub0bs
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
CSRF is not dead — SameSite=Lax changed the game but did not eliminate it

#### 2. What you should learn
- Understand **samesite=lax (implicit, without explicit attribute) is subject to the lax+post accommodation; samesite=lax (explicitly set) is not — check this before reporting**
- Understand **rails head method goes to the get route; `if request.get?` + `else` catches head → potential csrf**
- Understand **method override params (e.g., `_method=post`) may allow get requests to be replayed as post — worth checking**
- Understand **referrer-based csrf protection is bypassable: use `<meta name="referrer" content="unsafe-url">` on your attacker page to send the full url, including path**

#### 3. Core concepts explained
**GitHub OAuth CSRF via HEAD method — CSRF**
- **What it is:** Cross-Site Request Forgery — tricking a victim's browser into making unwanted requests to a site where they're authenticated.
- **Why it matters:** CSRF can change email, password, or perform actions on behalf of the victim.
- **Common mistake:** Only testing GET-based CSRF — POST and PUT endpoints with CSRF tokens may still be vulnerable if tokens are predictable.

**Mobile CSRF via QR code / WebView (CARRF) — Cross-app request forgery**
- **What it is:** Cross-Site Request Forgery — tricking a victim's browser into making unwanted requests to a site where they're authenticated.
- **Why it matters:** CSRF can change email, password, or perform actions on behalf of the victim.
- **Common mistake:** Only testing GET-based CSRF — POST and PUT endpoints with CSRF tokens may still be vulnerable if tokens are predictable.

**Force re-login for CSRF**
- Open `window.open('https://target.com/login')` to reset cookie → then top-level POST within 2 minutes (lax+post window)

**Referrer policy bypass**
- `<meta name="referrer" content="unsafe-url">` forces the browser to send the full URL (including path) in the `Referer` header

**Double-click action**
- Use form submit + button onclick in same click: `onclick="window.open(...)"` and form submits simultaneously


#### 4. Techniques and tactics
**Force re-login for CSRF**
- **What it is:** Open `window.open('https://target.com/login')` to reset cookie → then top-level POST within 2 minutes (lax+post window)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Referrer policy bypass**
- **What it is:** `<meta name="referrer" content="unsafe-url">` forces the browser to send the full URL (including path) in the `Referer` header
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Double-click action**
- **What it is:** Use form submit + button onclick in same click: `onclick="window.open(...)"` and form submits simultaneously
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
- **Try this:** SameSite=Lax (implicit, without explicit attribute) IS subject to the lax+post accommodation; SameSite=Lax (explicitly set) IS NOT — check this before reporting
- **Try this:** Rails HEAD method goes to the GET route; `if request.get?` + `else` catches HEAD → potential CSRF
- **Try this:** Method override params (e.g., `_method=POST`) may allow GET requests to be replayed as POST — worth checking
- **Try this:** Referrer-based CSRF protection is bypassable: use `<meta name="referrer" content="unsafe-url">` on your attacker page to send the full URL, including path

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GitHub OAuth CSRF via HEAD method — CSRF?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **CSRF is not dead — SameSite=Lax changed the game but did not eliminate it**
2. **SameSite=Lax (implicit, without explicit attribute) IS subject to the lax+post a**
3. **Rails HEAD method goes to the GET route; `if request.get?` + `else` catches HEAD**
