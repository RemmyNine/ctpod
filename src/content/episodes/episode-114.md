---
title: "Single Page Application Hacking Playbook"
episode: 114
---


# Episode 114 Single Page Application Hacking Playbook

### TL;DR
- BusFactor's CSPT chain: client-side path traversal → file upload (JSON) → `redirect=true` parameter exposes file URL → CloudFront CORS manipulation → scoped self-XSS → $7.5k / $22k
- Common Crawl scanning by Truffle Security: 12,000 live API keys and passwords in DeepSeek's training data
- Pressure-based click exploitation: `window.focus` rarely works, but `window.open('', 'targetname')` focuses via shared browsing context
- SPA hacking methodology: feature flags buried in JS, webpack source maps (.map), application-level 404s, client-side path enumeration (`path:` in JS)
- API swapping: staging/dev backend detection via `window.name` or hostname — different backend = different auth tokens

### Key Takeaways
- For client-side path traversal (CSPT): need one of three escalation paths — open redirect, file upload (JSON response served as JS), or state-changing endpoint (DELETE, PATCH)
- When the file download returns a JSON blob with URL instead of redirecting, check for `?redirect=true` parameter
- If CORS denies cross-origin reads, try caching manipulation: make the request without `Origin` header, cache the response; then let the CSPT make the request with `Origin` header → cached CORS headers serve the data
- Scan Common Crawl for secrets — 400TB of raw HTTP requests/responses; nation-state actors likely already do this
- In SPAs, `path:` in JS files enumerates all client-side routes; these routes can be navigated directly without server requests

### Bugs and Findings

#### BusFactor's CSPT Chain — $7.5k / $22k
- **Target/context:** [Redacted] program
- **Root cause:** Client-side path traversal allowed manipulating fetch URL. File upload stored file on S3. File download endpoint `?redirect=true` returned a redirect instead of JSON URL.
- **Technique / how found:**
  1. Find CSPT → control fetch destination
  2. Upload JSON file containing XSS payload
  3. Discover `?redirect=true` parameter on download endpoint (originally `?tedirect=true` — typo)
  4. Redirect goes to S3 but CORS blocks reading
  5. Bypass CORS: CloudFront cached response from requests without `Origin` header. Let CSPT make the request (it includes `Origin`), response gets proper CORS headers
  6. Scoped self-XSS: set a cookie so the file is only accessible to victim's session
- **Key technical details:** CloudFront caching; `Origin` header determines CORS headers; CSPT adds `Origin` automatically; `?redirect=true` triggers HTTP redirect; scoped self-XSS via cookie fixation
- **Impact / severity / bounty:** $7,500 (first target), $22,000 (better-protected target)
- **Obstacles & how solved:** CORS blocked cross-origin reads; solved by letting CSPT add the `Origin` header (top-level navigation doesn't include it)

#### Common Crawl Secret Scanning — 12,000 Live API Keys
- **Target/context:** Common Crawl dataset (400TB+ of web data)
- **Root cause:** Raw HTTP responses in Common Crawl include headers, query parameters, and body — secrets embedded in API calls
- **Technique / how found:** Run secret scanners (like TruffleHog) across the entire Common Crawl dataset
- **Key technical details:** Common Crawl includes full request and response data (URLs, headers, body); used as training data for many AI models; 12,000 live secrets found; verification required checking each key individually
- **Impact / severity / bounty:** [inferred] Very high — exposed credentials for thousands of services
- **Obstacles & how solved:** Scale — 400TB dataset requires significant compute; verification required implementing auth checks for hundreds of services

#### Double-Click Jacking — Pop-Under and Window Focus
- **Target/context:** Any page with a single-click authorization action
- **Root cause:** `window.focus()` rarely works; `window.open('', 'known-name')` focuses via shared browsing context. Pop-under + `moveTo` enables reliable double-click hijacking.
- **Technique / how found:**
  1. `window.open(victim-url, 'some_name')` — opens victim in named window
  2. `window.open('', 'some_name')` — re-focuses that window by name (no page reload)
  3. Combine with `moveTo()` to align victim's approve button under user's cursor
- **Key technical details:** `window.open('', target)` with existing target name focuses the window without navigation; works cross-origin; `window.moveTo()` works cross-origin on popup windows
- **Impact / severity / bounty:** Depends on the single-click action — can be ATO
- **Obstacles & how solved:** Pop-ups are often blocked; user must allow pop-ups or use existing pop-under

### Techniques and Primitives
- **CSPT + ?redirect param** — File download endpoints with ?redirect=true can turn JSON response into actual redirect
- **CORS bypass via cache** — Request without `Origin` header gets cached without CORS headers; request with `Origin` later gets proper CORS (if cache serves stale)
- **Application-level 404 vs server-level 404** — 404 from the app (JSON `{"error":"not found"}`) vs HTTP 404 — differential reveals hidden endpoints
- **API backend swapping** — `window.name = 'dev'` or similar triggers different API backend; staging tokens often work in prod (same signing key)
- **JWT email vs sub claim test** — Change email in profile → make API calls before confirming → see if auth uses email or sub
- **`text/plain` + JSON body** — Send `Content-Type: text/plain` with JSON body; some backends accept it, enabling CSRF where `application/json` is blocked

### Tooling and Resources
- BusFactor + XSSDoctor write-up
- Truffle Security — Common Crawl secret scan
- Hackadvisor.io — bug bounty program ratings
- p-prettier (parallel-prettier) — multi-threaded JS beautifier
- Caido/Shift for API backend swapping

### Suggestions and Advices from Hunter
- "For SPAs, download all JS, grep for `path:` to enumerate client-side routes — these routes can be exploited without server-side changes"
- "Application-level 404s (not HTTP 404) indicate a valid endpoint returning a 'not found' message — that's a gadget for IDOR"
- "When an API uses cookie-based auth, try sending `Content-Type: text/plain` with JSON body — some backends accept it"
- "Don't fuzz APIs recursively — fuzz at the known path level. Finding one hidden endpoint can lead to three IDORs"

### AI Takeaway
The `?redirect=true` parameter discovery is a great reminder to test every parameter variation. The CORS + caching bypass technique (request without `Origin` gets cached, serves CORS headers later) is broadly applicable — test this whenever S3/CloudFront serves files with conditional CORS.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
BusFactor's CSPT chain: client-side path traversal → file upload (JSON) → `redirect=true` parameter exposes file URL → CloudFront CORS manipulation → scoped self-XSS → $7.5k / $22k

#### 2. What you should learn
- Understand **for client-side path traversal (cspt): need one of three escalation paths — open redirect, file upload (json response served as js), or state-changing endpoint (delete, patch)**
- Understand **when the file download returns a json blob with url instead of redirecting, check for `?redirect=true` parameter**
- Understand **if cors denies cross-origin reads, try caching manipulation: make the request without `origin` header, cache the response; then let the cspt make the request with `origin` header → cached cors headers serve the data**
- Understand **scan common crawl for secrets — 400tb of raw http requests/responses; nation-state actors likely already do this**
- Understand **in spas, `path:` in js files enumerates all client-side routes; these routes can be navigated directly without server requests**

#### 3. Core concepts explained
**BusFactor's CSPT Chain — $7.5k / $22k**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Common Crawl Secret Scanning — 12,000 Live API Keys**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Double-Click Jacking — Pop-Under and Window Focus**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CSPT + ?redirect param**
- File download endpoints with ?redirect=true can turn JSON response into actual redirect

**CORS bypass via cache**
- Request without `Origin` header gets cached without CORS headers; request with `Origin` later gets proper CORS (if cache serves stale)

**Application-level 404 vs server-level 404**
- 404 from the app (JSON `{"error":"not found"}`) vs HTTP 404 — differential reveals hidden endpoints


#### 4. Techniques and tactics
**CSPT + ?redirect param**
- **What it is:** File download endpoints with ?redirect=true can turn JSON response into actual redirect
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CORS bypass via cache**
- **What it is:** Request without `Origin` header gets cached without CORS headers; request with `Origin` later gets proper CORS (if cache serves stale)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Application-level 404 vs server-level 404**
- **What it is:** 404 from the app (JSON `{"error":"not found"}`) vs HTTP 404 — differential reveals hidden endpoints
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**API backend swapping**
- **What it is:** `window.name = 'dev'` or similar triggers different API backend; staging tokens often work in prod (same signing key)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**JWT email vs sub claim test**
- **What it is:** Change email in profile → make API calls before confirming → see if auth uses email or sub
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"For SPAs, download all JS, grep for `path:` to enumerate client-side routes"* — **these routes can be exploited without server-side changes**
- *"Application-level 404s (not HTTP 404) indicate a valid endpoint returning a 'not found' message"* — **that's a gadget for IDOR**
- *"When an API uses cookie-based auth, try sending `Content-Type: text/plain` with JSON body"* — **some backends accept it**
- *"Don't fuzz APIs recursively"* — **fuzz at the known path level. Finding one hidden endpoint can lead to three IDORs**

#### 6. Mental models
- **For SPAs, download all JS, grep for `path:` to enumerate cli** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Application-level 404s (not HTTP 404) indicate a valid endpo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **When an API uses cookie-based auth, try sending `Content-Typ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** For client-side path traversal (CSPT): need one of three escalation paths — open redirect, file upload (JSON response served as JS), or state-changing endpoint (DELETE, PATCH)
- **Try this:** When the file download returns a JSON blob with URL instead of redirecting, check for `?redirect=true` parameter
- **Try this:** If CORS denies cross-origin reads, try caching manipulation: make the request without `Origin` header, cache the response; then let the CSPT make the request with `Origin` header → cached CORS headers serve the data
- **Try this:** Scan Common Crawl for secrets — 400TB of raw HTTP requests/responses; nation-state actors likely already do this

#### 8. Red flags and pitfalls
- - Obstacles & how solved: CORS blocked cross-origin reads; solved by letting CSPT add the `Origin` header (top-level navigation doesn't include it)
- - Obstacles & how solved: Scale — 400TB dataset requires significant compute; verification required implementing auth checks for hundreds of services

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **JWT** — JSON Web Token — compact token format for authentication
- **CORS** — Cross-Origin Resource Sharing — browser mechanism for cross-domain requests

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in BusFactor's CSPT Chain — $7.5k / $22k?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **BusFactor's CSPT chain: client-side path traversal → file upload (JSON) → `redir**
2. **For client-side path traversal (CSPT): need one of three escalation paths — open**
3. **When the file download returns a JSON blob with URL instead of redirecting, chec**
