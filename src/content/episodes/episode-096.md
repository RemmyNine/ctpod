---
title: "Cookies & Caching with MatanBer"
episode: 96
---


# Episode 96 Cookies & Caching with MatanBer

**Guest:** MatanBer
**Host:** Justin Gardner (Rhynorater)
**Duration:** 49:09
**Transcript source:** feed (full transcript)

### TL;DR
- Cookie quoting: Java/Python environments use double-quoted cookie values — `key="value"` allows semicolons and special chars in value
- Safari-specific bug: closing curly bracket `}` in cookie attributes comments out the rest of the Set-Cookie header
- Force-cache fetch attack: prime cache with `<img>` (sends SameSite=None cookies, can't read response), then read from cache via `fetch(url, {cache: "force-cache"})` (can't send creds but can read cached)
- Cache API poisoning: `caches.open()` with the same identifier as the service worker to add malicious responses

### Key Takeaways
- Cookie ordering: path length descending, then chronological (last set wins). Set very specific paths to control order
- Safari: closing curly bracket `}` in cookie attribute value discards all subsequent attributes — useful for cookie tossing when you have partial injection
- Force-cache fetch: `<img src="https://target.com/secret">` sends cookies and caches response; `fetch("https://target.com/secret", {cache: "force-cache"})` reads from cache without sending credentials but bypasses CORS
- Cache API (`caches.open("cacheName")`) is shared per-origin between pages and service workers — usable for service worker cache poisoning from an XSS

### Bugs and Findings

#### Cookie Quoting — Partial to Full Cookie Injection
- **Target/context:** Java/Python web apps (CherryPy, web.py, aiohttp, etc.)
- **Root cause:** Some servers parse `"` as a cookie value delimiter — `x="value; with; semicolons"` is valid. A cookie value starting with `"` comments out all subsequent cookies until matching `"`
- **Technique:** Set a cookie whose value starts with `"` to quote (comment out) all cookies that follow it. Use path ordering to control position.
- **Key technical details:** Java, CherryPy, web.py, aiohttp support quoted cookie values. Setting `malicious="` as first cookie will make everything after it part of its value
- **Obstacles & how solved:** Cookie order determined by path length (longer path = earlier) and chronological (newest = later). Need to get your `"` cookie after the target cookie.

#### Safari Cookie Attribute Comment-Out
- **Target/context:** Safari browser
- **Root cause:** Safari's cookie parser treats `}` as a cookie-attribute terminator — everything after `}` in a Set-Cookie header is ignored
- **Technique / how found:** Collaboration between MatanBer and Justin — needed to remove trailing cookie attributes when they had partial cookie injection
- **Key technical details:** Inject `; }` or similar after your cookie value in Set-Cookie header → Safari ignores all remaining attributes (Path, Domain, Secure, etc.)
- **Obstacles & how solved:** Only works in Safari; helps for cookie tossing when original Set-Cookie has restrictive attributes

#### Medium Cache-Cache — Force-Cache Fetch Leak
- **Target/context:** HeroCTF v6 challenge (Mizu.re writeup)
- **Root cause:** Browser cache keyed by (top-level site, current site, resource URL). `<img>` can load a resource with credentials (SameSite=None) but cannot read response. `fetch()` with `cache: "force-cache"` can read from cache but cannot send credentials to `Access-Control-Allow-Origin: *` endpoints
- **Exploitation steps:**
  1. `<img src="https://target.com/secret?q=flag">` → loads with cookies, caches response
  2. `fetch("https://target.com/secret?q=flag", {cache: "force-cache"})` → reads cached response (CORS-allowed because it's from cache)
- **Key technical details:** Cache keys: (top-level ETLD+1, current ETLD+1, full URL). SameSite cookies flow through `<img>`. `force-cache` bypasses CORS restriction for credentialed requests.
- **Impact:** Cross-site read of responses cached with credentials
- **Obstacles & how solved:** Requires SameSite=None cookies (or lax, with top-level navigation); requires XSS on same-site subdomain to exploit

#### Cache API Poisoning — Service Worker Hijack
- **Target/context:** Sites using service workers with Cache API
- **Root cause:** `caches.open("cacheName")` is shared per-origin between all pages and the service worker
- **Technique / how found:** From an XSS on the origin, call `caches.open("service-worker-cache-name")` → get reference to same cache → add malicious response (HTML payload) → match against future requests
- **Impact:** Persistent XSS — every time the service worker matches the poisoned request, it returns your malicious payload
- **Obstacles & how solved:** Need to know the cache identifier used by the service worker; `cache.add()` won't send POST requests

### Techniques and Primitives
- **Cookie quoting to reorder/comment** — Set cookie value starting with `"` to comment out subsequent cookies (Java/Python environments). Combine with path ordering to position your cookie.
- **Safari cookie `}` truncation** — Injects `}` to discard remaining Set-Cookie attributes. Unique to Safari.
- **Force-cache cross-site leak** — Prime cache via `<img>` (sends creds), read via `fetch(url, {cache: "force-cache"})` (reads cached response without CORS issues).
- **Cache API for XSS persistence** — `caches.open()` from page context shares same cache as service worker → add malicious responses.

### Tooling and Resources
- Cookie Bugs research: Ankur Sundara's blog on cookie smuggling/injection
- ios-webkit-debug-proxy (Google) — Safari remote debugging from non-Mac via iPhone
- Mizu.re HeroCTF v6 writeups
- Medium article: Cookie ordering by path + chronological

### Suggestions and Advices from Hunter
- "For Safari debugging without a Mac: connect an iPhone, install iTunes, enable debugging, use ios-webkit-debug-proxy + extracted Safari DevTools frontend." — MatanBer
- "Have two iPads and two Pixels for mobile testing — one will inevitably brick." — Dr. Bouman (referenced)
- "The Cache API is shared per-origin. If the service worker uses it, you can access it from any page on that origin." — MatanBer

### AI Takeaway
The force-cache fetch technique is a powerful new cross-site leak primitive. The fact that `caches.open()` returns the same cache regardless of whether the caller is a page or service worker is a fundamental design issue that provides XSS persistence in many contexts.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Cookie quoting: Java/Python environments use double-quoted cookie values — `key="value"` allows semicolons and special chars in value

#### 2. What you should learn
- Understand **cookie ordering: path length descending, then chronological (last set wins). set very specific paths to control order**
- Understand **safari: closing curly bracket `}` in cookie attribute value discards all subsequent attributes — useful for cookie tossing when you have partial injection**
- Understand **force-cache fetch: `<img src="https://target.com/secret">` sends cookies and caches response; `fetch("https://target.com/secret", {cache: "force-cache"})` reads from cache without sending credentials but bypasses cors**
- Understand **cache api (`caches.open("cachename")`) is shared per-origin between pages and service workers — usable for service worker cache poisoning from an xss**

#### 3. Core concepts explained
**Cookie Quoting — Partial to Full Cookie Injection**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Safari Cookie Attribute Comment-Out**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Medium Cache-Cache — Force-Cache Fetch Leak**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Cookie quoting to reorder/comment**
- Set cookie value starting with `"` to comment out subsequent cookies (Java/Python environments). Combine with path ordering to position your cookie.

**Safari cookie `}` truncation**
- Injects `}` to discard remaining Set-Cookie attributes. Unique to Safari.

**Force-cache cross-site leak**
- Prime cache via `<img>` (sends creds), read via `fetch(url, {cache: "force-cache"})` (reads cached response without CORS issues).


#### 4. Techniques and tactics
**Cookie quoting to reorder/comment**
- **What it is:** Set cookie value starting with `"` to comment out subsequent cookies (Java/Python environments). Combine with path ordering to position your cookie.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Safari cookie `}` truncation**
- **What it is:** Injects `}` to discard remaining Set-Cookie attributes. Unique to Safari.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Force-cache cross-site leak**
- **What it is:** Prime cache via `<img>` (sends creds), read via `fetch(url, {cache: "force-cache"})` (reads cached response without CORS issues).
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cache API for XSS persistence**
- **What it is:** `caches.open()` from page context shares same cache as service worker → add malicious responses.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"For Safari debugging without a Mac: connect an iPhone, install iTunes, enable debugging, use ios-webkit-debug-proxy + extracted Safari DevTools frontend."* — **MatanBer**
- *"Have two iPads and two Pixels for mobile testing"* — **one will inevitably brick." — Dr. Bouman (referenced)**
- *"The Cache API is shared per-origin. If the service worker uses it, you can access it from any page on that origin."* — **MatanBer**

#### 6. Mental models
- **For Safari debugging without a Mac: connect an iPhone, insta** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Have two iPads and two Pixels for mobile testing — one will ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The Cache API is shared per-origin. If the service worker us** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Cookie ordering: path length descending, then chronological (last set wins). Set very specific paths to control order
- **Try this:** Safari: closing curly bracket `}` in cookie attribute value discards all subsequent attributes — useful for cookie tossing when you have partial injection
- **Try this:** Force-cache fetch: `<img src="https://target.com/secret">` sends cookies and caches response; `fetch("https://target.com/secret", {cache: "force-cache"})` reads from cache without sending credentials but bypasses CORS
- **Try this:** Cache API (`caches.open("cacheName")`) is shared per-origin between pages and service workers — usable for service worker cache poisoning from an XSS

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Cookie order determined by path length (longer path = earlier) and chronological (newest = later). Need to get your `"` cookie after the target cookie.
- - Obstacles & how solved: Only works in Safari; helps for cookie tossing when original Set-Cookie has restrictive attributes

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **CORS** — Cross-Origin Resource Sharing — browser mechanism for cross-domain requests

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Cookie Quoting — Partial to Full Cookie Injection?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Cookie quoting: Java/Python environments use double-quoted cookie values — `key=**
2. **Cookie ordering: path length descending, then chronological (last set wins). Set**
3. **Safari: closing curly bracket `}` in cookie attribute value discards all subsequ**
