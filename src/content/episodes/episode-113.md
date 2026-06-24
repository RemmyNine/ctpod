---
title: "Portswigger Top 10 2024 — Best Technical Takeaways"
episode: 113
---


# Episode 113 Portswigger Top 10 2024 — Best Technical Takeaways

### TL;DR
- Cookie tossing: partial cookie injection via semicolon, set domain+path to hijack session on specific paths
- ChatGPT cache deception via `%2f..%2f` path traversal on `/share/` cached endpoint
- OAuth non-happy path: `response_type=id_token,code` with `prompt=none` — OAuth code lands in fragment
- PDF.js arbitrary JS execution via `new Function()` with font matrix integers → PDF string escaping
- Double-click jacking: `window.open` + `window.moveTo` + mouse events = clickjacking without single-click
- Worst-fit Unicode encoding: full-width double quote (U+FF02), Yen sign (U+00A5), Won sign (U+20A9), full-width backslash all map to ASCII equivalents via best-fit encoding
- HTTP request smuggling T_E_.0: front-end treats CL, back-end treats TE with empty CL
- SQL injection at protocol level: integer overflow in length field → smuggle SQL query in binary protocol
- Orange's confusion attacks: `%3F` in path truncates at query string — rewrite rules don't expect this

### Key Takeaways
- Cookie tossing: partial cookie injection via semicolon in cookie value → `Set-Cookie: session=abc; Domain=.target.com; Path=/specific` — now attacker's cookie is sent first on that specific path
- For OAuth, use `prompt=none` to skip account selection page (user must be logged into Google); combine with `response_type=id_token,code` to put the code in the fragment
- PDF.js font rendering uses `new Function()` with PDF-provided integers; inject PDF string values (with parentheses instead of quotes) to break out
- Double-click jacking: mouseDown on attacker page closes window, mouseUp + second mouseDown lands on victim page's approve button — no mouseMove event means no movement needed
- Worst-fit: `U+FF02` (full-width double quote), `U+00A5` (¥), `U+20A9` (₩), `U+FF3C` (full-width backslash) can all be used to escape strings when encoding doesn't match
- `TE` header with value `,TE` and empty `CL` = front-end ignores CL, back-end processes TE with `0` length body

### Bugs and Findings

#### Cookie Tossing — Partial Cookie Injection to Session Fixation
- **Target/context:** Web apps with client-side cookie setting or reflected cookie values
- **Root cause:** Cookie value from user input injected into `Set-Cookie` without sanitizing semicolons
- **Technique / how found:** Inject `; Domain=.target.com; Path=/specific-path` into a cookie value → attacker controls domain and path attributes → attacker cookie takes priority on specific path
- **Exploitation steps:**
  1. Find reflected/controlled cookie value (query param → `Set-Cookie` header or `document.cookie`)
  2. Inject `; Domain=.target.com; Path=/auth/callback`
  3. Attacker's cookie with fixed session ID is sent first on that path
  4. Victim performs action on that path → attacker sees result in their account
- **Key technical details:** Cookie priority: more specific path > less specific path; domain specificity also affects ordering
- **Impact / severity / bounty:** Data exfiltration, session fixation, self-XSS escalation
- **Obstacles & how solved:** Need a reflection point; can use XSS on subdomain to set cookies with wide domain

#### ChatGPT Cache Deception — Wildcard Cache Deception
- **Target/context:** chat.openai.com `/share/` endpoint
- **Root cause:** `/share/` was cached; `%2f..%2f` path traversal made the URL end in a cacheable extension (`.css`, `.js`) while the backend normalized the path to `/share/chat-uid`
- **Technique / how found:** Request `/share/../share/some-chat-id` or use `%2f..%2f` to make the path appear cacheable — CDN caches the response, next request serves cached data to attacker
- **Key technical details:** Caching server does NOT normalize `%2f`; backend server DOES normalize it. Use `%2f..%2f` so caching server sees a path ending in `.css`, backend sees `/share/chat-uid`
- **Impact / severity / bounty:** $6,500 (shortly after OpenAI bug bounty started)
- **Obstacles & how solved:** Required finding a cached path and a `%2f` parsing discrepancy

#### PDF.js Arbitrary JavaScript Execution
- **Target/context:** Firefox's built-in PDF viewer (pdf.js)
- **Root cause:** pdf.js uses `new Function()` to create font-rendering functions from PDF content; PDF strings are parenthesized, allowing string injection into generated JavaScript
- **Technique / how found:** Create malicious PDF with font matrix containing strings (PDF strings use `(text)` not `"text"`) injected into `new Function()` body → arbitrary JS execution
- **Key technical details:** Runs under `resource://pdf.js` origin — privileged context; can invoke file downloads, access local files. PDF string syntax: `(text)` not `"text"`.
- **Impact / severity / bounty:** CVE, arbitrary code execution in PDF viewer context
- **Obstacles & how solved:** Required understanding PDF syntax (parenthesized strings) and pdf.js internals; new Function() is the "underrated eval"

#### Worst-Fit Unicode Encoding — Escape Injection
- **Target/context:** Any text encoding conversion at system boundaries
- **Root cause:** When a character is not in the target charset, "best-fit" encoding maps it to the closest ASCII equivalent. Full-width double quote → `"`, Yen/Won signs → `\`, full-width backslash → `\`
- **Technique / how found:** Submit text containing full-width characters; if the application transcodes to a charset that doesn't support them, best-fit mapping converts them to dangerous ASCII equivalents
- **Exploitation steps:**
  1. Identify a charset boundary (e.g., Shift-JIS → UTF-8, or charset conversion on input)
  2. Send `U+FF02` (full-width double quote) instead of `"` — if best-fit maps it to `"`, strings can be escaped
  3. Send `U+00A5` (¥) or `U+20A9` (₩) — best-fit to `\` — escapes quotes
- **Key technical details:** U+FF02 → `"` ; U+00A5 (¥) → `\` ; U+20A9 (₩) → `\` ; U+FF3C (full-width \) → `\`
- **Impact / severity / bounty:** SQL injection, XSS, command injection depending on context
- **Obstacles & how solved:** Need charset conversion boundary; Orange found this across multiple large applications

#### HTTP Request Smuggling T_E_.0
- **Target/context:** HTTP proxies and backends
- **Root cause:** `Transfer-Encoding: ,TE` (with leading junk) exploits parsing differences: front-end ignores malformed TE, reads CL; back-end sees valid `TE`, ignores CL (length 0)
- **Technique / how found:** Send request with `Content-Length: 13` and `Transfer-Encoding:, TE` — front-end uses CL=13 and forwards request + next request's start; back-end uses TE so CL is 0
- **Key technical details:** The specific header `Transfer-Encoding:, TE` causes some parsers to reject it, others to accept. CL=0 + TE → request smuggling.
- **Impact / severity / bounty:** $8,500 from Google
- **Obstacles & how solved:** Testing across different HTTP implementations

#### Protocol-Level SQL Injection via Integer Overflow
- **Target/context:** PostgreSQL, MySQL, MongoDB binary protocols
- **Root cause:** Integer overflow in length field of database binary protocol. Sending ~4GB payload causes length integer to overflow to a small value; data after the truncated length is interpreted as new binary protocol messages
- **Technique / how found:** Send massive payload (~4GB) with GZip compression to bypass web server limits; length field overflows, rest of payload is parsed as protocol messages → smuggle arbitrary SQL queries
- **Exploitation steps:**
  1. Compress payload with GZip to bypass middleware length limits
  2. Send compressed payload to endpoint that passes it to database protocol parser
  3. Length integer overflows → first few bytes of payload are the "real" data, rest is protocol-level messages
  4. Craft the overflow data to include a valid SQL statement
- **Key technical details:** Use compression (GZip) for large payloads; use `multipart/form-data` or alternative body types with larger limits; find server-side string generation to create the large payload internally
- **Impact / severity / bounty:** Stacked-query SQL injection
- **Obstacles & how solved:** Large payload delivery — GZip compression, multipart forms, server-side string generation

### Techniques and Primitives
- **Prompt=None OAuth bypass** — OAuth parameter `prompt=none` skips account selection (Google); user must be logged in, auto-selects primary account
- **Double-response-type OAuth** — `response_type=id_token,code` (comma-separated) — works in Google OAuth; code lands in fragment
- **Worst-fit Unicode characters** — U+FF02 (full-width `"` ), U+00A5 (¥→`\`), U+20A9 (₩→`\`), U+FF3C (full-width \→`\`)
- **Cache path normalization discrepancy** — Use `%2f` (encoded /) vs `/` — caching servers and backend servers may normalize differently
- **TE.,0 smuggling** — `Transfer-Encoding:, TE` with `Content-Length: 0`
- **Symbolic link traversal** — In Apache/HTTPD with `FollowSymLinks` enabled, symlinks can jump out of document root; chain multiple symlinks for deeper access

### Tooling and Resources
- HTTP Garden (`hb.hboeck.de`) — test HTTP parsing differences across implementations
- Orange Tsai's confusion attacks writeup, PS Paul's SQL injection at protocol level
- Portswigger Top 10 Web Hacking Techniques 2024

### Suggestions and Advices from Hunter
- "When looking at a set of payloads/functionality/connection types, make sure you're comprehensive — test all permutations"
- "Google pays 1.5x bounty for 'exceptional reports' with root cause analysis and remediation steps"
- "Use compression to deliver large payloads through HTTP — GZip a 4GB payload down to nearly nothing"
- "For protocol fuzzing, ask AI to render characters through top parsers in different languages — test encoding boundary issues systematically"

### AI Takeaway
The worst-fit Unicode characters (U+FF02, U+00A5, U+20A9, U+FF3C) are the highest-leverage takeaway — test these at every encoding boundary. The cache path normalization discrepancy (`%2f`) is another high-value primitive. Protocol-level integer overflow SQL injection shows that "old" vuln classes are still viable at lower protocol layers.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Cookie tossing: partial cookie injection via semicolon, set domain+path to hijack session on specific paths

#### 2. What you should learn
- Understand **cookie tossing: partial cookie injection via semicolon in cookie value → `set-cookie: session=abc; domain=.target.com; path=/specific` — now attacker's cookie is sent first on that specific path**
- Understand **for oauth, use `prompt=none` to skip account selection page (user must be logged into google); combine with `response_type=id_token,code` to put the code in the fragment**
- Understand **pdf.js font rendering uses `new function()` with pdf-provided integers; inject pdf string values (with parentheses instead of quotes) to break out**
- Understand **double-click jacking: mousedown on attacker page closes window, mouseup + second mousedown lands on victim page's approve button — no mousemove event means no movement needed**
- Understand **worst-fit: `u+ff02` (full-width double quote), `u+00a5` (¥), `u+20a9` (₩), `u+ff3c` (full-width backslash) can all be used to escape strings when encoding doesn't match**

#### 3. Core concepts explained
**Cookie Tossing — Partial Cookie Injection to Session Fixation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**ChatGPT Cache Deception — Wildcard Cache Deception**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**PDF.js Arbitrary JavaScript Execution**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Prompt=None OAuth bypass**
- OAuth parameter `prompt=none` skips account selection (Google); user must be logged in, auto-selects primary account

**Double-response-type OAuth**
- `response_type=id_token,code` (comma-separated) — works in Google OAuth; code lands in fragment

**Worst-fit Unicode characters**
- U+FF02 (full-width `"` ), U+00A5 (¥→`\`), U+20A9 (₩→`\`), U+FF3C (full-width \→`\`)


#### 4. Techniques and tactics
**Prompt=None OAuth bypass**
- **What it is:** OAuth parameter `prompt=none` skips account selection (Google); user must be logged in, auto-selects primary account
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Double-response-type OAuth**
- **What it is:** `response_type=id_token,code` (comma-separated) — works in Google OAuth; code lands in fragment
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Worst-fit Unicode characters**
- **What it is:** U+FF02 (full-width `"` ), U+00A5 (¥→`\`), U+20A9 (₩→`\`), U+FF3C (full-width \→`\`)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cache path normalization discrepancy**
- **What it is:** Use `%2f` (encoded /) vs `/` — caching servers and backend servers may normalize differently
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**TE.,0 smuggling**
- **What it is:** `Transfer-Encoding:, TE` with `Content-Length: 0`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When looking at a set of payloads/functionality/connection types, make sure you're comprehensive"* — **test all permutations**
- *"Google pays 1.5x bounty for 'exceptional reports' with root cause analysis and remediation steps"*
- *"Use compression to deliver large payloads through HTTP"* — **GZip a 4GB payload down to nearly nothing**
- *"For protocol fuzzing, ask AI to render characters through top parsers in different languages"* — **test encoding boundary issues systematically**

#### 6. Mental models
- **When looking at a set of payloads/functionality/connection t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Google pays 1.5x bounty for 'exceptional reports' with root ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use compression to deliver large payloads through HTTP — GZi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Cookie tossing: partial cookie injection via semicolon in cookie value → `Set-Cookie: session=abc; Domain=.target.com; Path=/specific` — now attacker's cookie is sent first on that specific path
- **Try this:** For OAuth, use `prompt=none` to skip account selection page (user must be logged into Google); combine with `response_type=id_token,code` to put the code in the fragment
- **Try this:** PDF.js font rendering uses `new Function()` with PDF-provided integers; inject PDF string values (with parentheses instead of quotes) to break out
- **Try this:** Double-click jacking: mouseDown on attacker page closes window, mouseUp + second mouseDown lands on victim page's approve button — no mouseMove event means no movement needed

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Need a reflection point; can use XSS on subdomain to set cookies with wide domain
- - Obstacles & how solved: Required finding a cached path and a `%2f` parsing discrepancy

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **OAuth** — Open standard for authorization — delegated access without sharing passwords

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Cookie Tossing — Partial Cookie Injection to Session Fixation?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Cookie tossing: partial cookie injection via semicolon, set domain+path to hijac**
2. **Cookie tossing: partial cookie injection via semicolon in cookie value → `Set-Co**
3. **For OAuth, use `prompt=none` to skip account selection page (user must be logged**
