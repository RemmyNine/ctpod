---
title: "Bug Bounty Mental — Practical Tips for Staying Sharp & Motivated"
episode: 77
---


# Episode 77 Bug Bounty Mental — Practical Tips for Staying Sharp & Motivated

**TL;DR**
- MongoDB NoSQL injection via aggregation pipelines — `$lookup`, `$unionWith`, `$replaceWith`, `$merge` allow cross-collection data extraction
- KakaoTalk 1-click ATO: deep link → open redirect → XSS → auth token sent as header on every request → ATO
- Time-based secrets (ResetTolkien): brute-force password reset tokens based on timestamps using the `Date` header
- iOS URL scheme hijacking: `ASWebAuthenticationSession` + `prompt=none` + custom URL scheme → 30+ apps vulnerable
- ORM injection: string concatenation in ORM queries can lead to injection if the ORM doesn't parameterize

**Key Takeaways**
- For NoSQL injection: look for `$match`, `$lookup` in requests — indicates aggregation pipeline; even if collection is constrained, you can use `$lookup` to read other collections
- For mobile: test if a deep link opens a WebView with JavaScript enabled — any auth token added as a header to every request is game-over if you can redirect
- `ResetTolkien` tool takes a password reset token + email + `Date` response header and tries 6 hash formats with different timestamp offsets to crack it
- iOS `ASWebAuthenticationSession` + `prompt=none` OAuth bypass: malicious app triggers auth flow, redirects to attacker domain, gets the auth code — affects any app using custom URL schemes instead of universal links
- When testing OAuth flows, always try `prompt=none` — skips user confirmation if already authorized

**Bugs and Findings**

### MongoDB NoSQL injection via aggregation pipelines
- **Target/context:** Any MongoDB-backed app where user input flows into queries
- **Root cause:** Aggregation pipeline operators (`$lookup`, `$unionWith`, `$replaceWith`, `$merge`) allow referencing other collections when user can inject into the pipeline array
- **Technique / how found:** Soroush's research; look for `$match` / `$lookup` in JSON request bodies
- **Exploitation steps:**
  1. Identify endpoint that accepts JSON `{"$match": {...}}` or similar MongoDB operators
  2. Inject `$lookup` to join data from a restricted collection:
     `{"$lookup": {"from": "users", "localField": "id", "foreignField": "_id", "as": "user"}}`
  3. Use `$limit` to constrain results and avoid timeout
  4. Use `$unionWith` to merge results from protected collections
- **Key technical details:** Look for JSON arrays describing operations in request bodies; fuzz for `$match`, `$lookup`, `$unionWith`
- **Impact / severity / bounty:** Cross-collection data extraction, privilege escalation

### KakaoTalk 1-click ATO — deep link → open redirect → XSS → ATO
- **Target/context:** KakaoTalk (Korean chat app) — Kakaotalk:// deep link scheme
- **Root cause:** The deep link opened a WebView that set auth token on every request; an open redirect + XSS chain made an attacker-controlled URL load with auth headers
- **Technique / how found:** DSchmidt (stulle123) research
- **Exploitation steps:**
  1. `kakaotalk://buy` opens `buy.kakao.com/<path>` in WebView with JS enabled
  2. Found open redirect at `buy.kakao.com` → any `kakao.com` subdomain
  3. Found DOM XSS at `.shoppinghow.kakao.com`
  4. Victim clicks deep link → open redirect to XSS page → XSS sets `document.location` to attacker URL
  5. Since WebView adds auth header to every request, attacker server receives the victim's auth token
- **Key technical details:** WebView had JavaScript enabled; Retrofit interceptor added auth to ALL requests (not just Kakao domains); deep link uses `kakaotalk://` scheme
- **Impact / severity / bounty:** 1-click ATO; no bounty paid (only Koreans eligible)
- **Obstacles & how solved:** Semi-closed redirect (only kakao.com subdomains) — overcame with a second open redirect + XSS on a different subdomain

### Time-based password reset token cracking — ResetTolkien
- **Target/context:** Any app using `uniqid()`, MongoDB ObjectId, or timestamp-based token generation
- **Root cause:** PHP `uniqid()` is time-based; MongoDB `_id` contains timestamp + process ID + counter
- **Technique / how found:** AethliosIK research; uses the `Date` response header to get server time
- **Exploitation steps:**
  1. Request password reset, capture the reset token from email
  2. Note the `Date` header from the HTTP response
  3. Feed token + email + Date into ResetTolkien tool
  4. Tool tries 6 formats: SHA1/SHA256 of email+timestamp, short hashes, concatenations
- **Key technical details:** The `Date` header is mandatory (RFC 7231) and gives server time; ResetTolkien brute-forces milliseconds forward/backward
- **Impact / severity / bounty:** Account takeover via password reset token prediction

**Techniques and Primitives**
- **Mobile WebView auth leak test** — On Android: install Frida/gadget to globally set WebViews as debuggable; then `document.location = attacker.com` and check if auth headers are sent
- **`prompt=none` OAuth bypass** — Skips user consent if already authorized; try it on every OAuth flow you find
- **ResetTolkien methodology** — Always capture the `Date` header when dealing with reset tokens; run the token through the tool before spending time on other attack paths

**Tooling and Resources**
- `soroush.me/blog/2024/06/mongodb-nosql-injection-with-aggregation-pipelines/` — MongoDB aggregation NoSQL injection
- `stulle123.github.io/posts/kakaotalk-account-takeover/` — KakaoTalk ATO
- `github.com/AethliosIK/reset-tolkien` — ResetTolkien tool
- `elttam.com/blog/plormbing-your-django-orm/` — Django ORM injection
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 77 Bug Bounty Mental — Practical Tips for Staying Sharp & Motivated covers practical bug bounty techniques and security research insights.

#### 2. What you should learn
- Understand the vulnerability classes discussed
- Learn practical exploitation techniques
- Know which tools are useful for this type of research

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
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Understand the vulnerability class** — Know how it works and why it matters
2. **Master the exploitation technique** — Practice the specific steps to exploit it
3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets
