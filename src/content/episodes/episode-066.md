---
title: "CDN-CGI Research, Intent To Ship, and Louis Vuitton"
episode: 66
---


# Episode 66 CDN-CGI Research, Intent To Ship, and Louis Vuitton

**Guests:** Justin Gardner, Joel Margolis
**Format:** Full transcript (ASR)
**Topics:** Louis Vuitton live hacking event, Google intent-to-ship feeds, Cloudflare CDN-CGI deep-dive, browser market share analysis, OAuth `@` sign bypass

### TL;DR
- Justin found an OAuth redirect_uri bypass using `?` + `@` in the username part — `https://target.com?@evil.com` bypasses host checks when `?` terminates the domain parsing before the `@`
- Cloudflare `/cdn-cgi/` image endpoint can be used for subdomain-only 307 redirect via `onerror=redirect` parameter
- Browser market share: Safari 18.5% total (8% desktop, 24% mobile) — Firefox <3% total
- Google Blink-dev "Intent to Ship" mailing list is the best source for finding new browser features before they land — useful for CSP bypass gadget discovery
- Louis Vuitton live hacking event: lower bounties than HackerOne events (1/5 to 1/10 typical), but swag was exceptional; Team Spain dominated the leaderboard

### Key Takeaways
- OAuth redirect_uri host check bypass: `https://target.com?@evil.com` — the `?` makes everything after part of query string, `@` is not parsed as user/auth separator. Many OAuth libraries only validate the host before `@` and after `://`
- Cloudflare `/cdn-cgi/image/onerror=redirect&url=https://subdomain.evil.com` → 307 redirect to any subdomain of the same TLD — useful for SSRF and CSRF chains
- Intents-to-ship (blink-dev Google Group) should be monitored for new event handlers that could enable CSP bypasses and XSS gadgets
- Host restrictions in mobile intent filters can be bypassed using `googlechrome://navigate?url=` if any URL scheme is allowed
- Using live hacking event data: top earners made significantly less at the Louis Vuitton event vs typical HackerOne LHEs — budget transparency is improving with HackerOne's new bounty stats

### Tooling and Resources
- Blink-dev Google Group — Intent to Ship posts
- Google BigQuery HTTP Archive — for large-scale endpoint enumeration
- Bright Data residential proxies (for bypassing IP-based blocking)
- `history.pushState` for hiding XSS payloads in URL bar
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Justin found an OAuth redirect_uri bypass using `?` + `@` in the username part — `https://target.com?@evil.com` bypasses host checks when `?` terminates the domain parsing before the `@`

#### 2. What you should learn
- Understand **oauth redirect_uri host check bypass: `https://target.com?@evil.com` — the `?` makes everything after part of query string, `@` is not parsed as user/auth separator. many oauth libraries only validate the host before `@` and after `://`**
- Understand **cloudflare `/cdn-cgi/image/onerror=redirect&url=https://subdomain.evil.com` → 307 redirect to any subdomain of the same tld — useful for ssrf and csrf chains**
- Understand **intents-to-ship (blink-dev google group) should be monitored for new event handlers that could enable csp bypasses and xss gadgets**
- Understand **host restrictions in mobile intent filters can be bypassed using `googlechrome://navigate?url=` if any url scheme is allowed**
- Understand **using live hacking event data: top earners made significantly less at the louis vuitton event vs typical hackerone lhes — budget transparency is improving with hackerone's new bounty stats**

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** OAuth redirect_uri host check bypass: `https://target.com?@evil.com` — the `?` makes everything after part of query string, `@` is not parsed as user/auth separator. Many OAuth libraries only validate the host before `@` and after `://`
- **Try this:** Cloudflare `/cdn-cgi/image/onerror=redirect&url=https://subdomain.evil.com` → 307 redirect to any subdomain of the same TLD — useful for SSRF and CSRF chains
- **Try this:** Intents-to-ship (blink-dev Google Group) should be monitored for new event handlers that could enable CSP bypasses and XSS gadgets
- **Try this:** Host restrictions in mobile intent filters can be bypassed using `googlechrome://navigate?url=` if any URL scheme is allowed

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Justin found an OAuth redirect_uri bypass using `?` + `@` in the username part —**
2. **OAuth redirect_uri host check bypass: `https://target.com?@evil.com` — the `?` m**
3. **Cloudflare `/cdn-cgi/image/onerror=redirect&url=https://subdomain.evil.com` → 30**
