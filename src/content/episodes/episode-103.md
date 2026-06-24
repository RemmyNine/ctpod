---
title: "Getting ANSI about Unicode Normalization"
episode: 103
---


# Episode 103 Getting ANSI about Unicode Normalization

**Host:** Justin Gardner (Rhynorater)
**Guest Co-Host:** Joseph Thacker (Rez0)
**Duration:** 1:00:30
**Transcript source:** feed (full transcript)

### TL;DR
- Worst Fit (Orange Tsai): Unicode normalization maps YEN SIGN (U+00A5) to backslash → path traversal, command injection, subprocess escape
- `_json` Ruby on Rails quirk: JSON body not starting with `{` gets stored in `params[_json]` key — middleware parsing mismatch
- Cross-site POST without Content-Type: `fetch()` with blob body = no Content-Type header → bypasses CSRF checks that test for `Content-Type != application/json`
- Cookie handling is a minefield: Unicode cookie character can brick Facebook, Instagram, Netflix, Amazon, etc.
- DoubleClickJacking: two-click account takeover via race window between mousedown/mouseup

### Key Takeaways
- Unicode normalization maps YEN SIGN (U+00A5) → backslash, FULLWIDTH SOLIDUS → slash. Add these to path traversal wordlists
- Ruby on Rails: JSON body not starting with `{` → stored in `params[_json]` — middleware parsing mismatch
- `fetch()` with blob body = no Content-Type header → bypasses `if request.contentType != 'application/json' { reject }`
- Unicode cookie character can DOS major websites (Facebook, Instagram, Netflix, Amazon, etc.)
- Safari: `-- value, value --` cookie pattern gets spaces truncated — undocumented behavior

### Bugs and Findings

#### Worst Fit — Unicode Normalization to Backslash
- **Target/context:** curl.exe, wget.exe, SVN, OpenSSL, Windows, IIS, Python subprocess, etc.
- **Root cause:** "Best fit" Unicode mapping in Windows and many libraries maps certain Unicode characters to visually/functionally similar ASCII. YEN SIGN (U+00A5) → backslash (0x5C). FULLWIDTH QUOTATION MARK (U+FF02) → double quote.
- **Key technical details:** YEN SIGN code point U+00A5 maps to `\`. FULLWIDTH REVERSE SOLIDUS → backslash. FULLWIDTH QUOTATION MARK (U+FF02) → `"`. Chinese/Japanese locales on Windows may also map. Python subprocess.run with argument array: fullwidth quotation mark breaks out of argument boundary.
- **Impact / severity / bounty:** Path traversal, command injection, argument injection across a wide range of software.
- **Obstacles & how solved:** Character must be supported by the locale/charset. Some payloads needed double YEN sign for effect.

#### `_json` Juggling Attack
- **Target/context:** Ruby on Rails applications
- **Root cause:** When JSON body doesn't start with `{` (i.e., not an object), Rails stores the data under `params[_json]` key — a hardcoded internal key
- **Impact / severity / bounty:** Middleware/backend parsing mismatch — smuggle payloads past middleware that expects specific JSON structure
- **Key technical details:** `{"key":"value"}` → `params[:key]`. `"string"` or `[1,2,3]` → `params[:_json]`. Rails has test cases for query params that fail parsing → can fingerprint Rails backends.

#### Cross-Site POST Without Content-Type
- **Target/context:** Applications that check `if request.contentType != 'application/json'` for CSRF protection
- **Root cause:** `fetch()` with a Blob body sends NO Content-Type header. The conditional check `if request.contentType and request.contentType != 'application/json'` fails (first condition false) → CSRF check skipped
- **Exploitation:**
  ```javascript
  fetch(url, { method: 'POST', body: new Blob(['{"key":"value"}']) })
  ```
- **Key technical details:** Blob body → no Content-Type header. Combined with SameSite=None cookies required (fetch can't do top-level navigation). Niche but powerful when SameSite=None is required.

#### Unicode Cookie — DOS on Major Sites
- **Target/context:** Facebook, Instagram, Netflix, Amazon, AWS, Apple Support, Best Buy, eBay, Home Depot, Okta, WhatsApp, etc.
- **Root cause:** Setting a cookie with a Unicode/emoji character in the name or value causes different parser behaviors across frameworks: some return 400, some 500, some partially work with broken links
- **Key technical details:** Amazon: mostly works but links broken. Various: 400, 500 errors.
- **Impact / severity / bounty:** DOS via cookie bombing if you have a cookie injection primitive (client-side or XSS)

### Techniques and Primitives
- **Unicode normalization payloads** — Add YEN SIGN (U+00A5), FULLWIDTH REVERSE SOLIDUS, FULLWIDTH QUOTATION MARK (U+FF02) to path traversal and injection wordlists
- **`_json` param smuggling** — Send JSON arrays/strings instead of objects to exploit Rails' `_json` internal parameter key
- **Blob body CSRF bypass** — `fetch(url, {method:'POST', body: new Blob([data])})` → no Content-Type → bypasses `contentType != 'application/json'` checks
- **Unicode cookie bomb** — Set a cookie with any Unicode/emoji character → DOS on Facebook, Instagram, Netflix, Amazon, etc.

### Tooling and Resources
- worst.fit (Orange Tsai's research site)
- Backslash Powered Scanner (PortSwigger) — now has normalization detection
- Handling Cookies is a Minefield (Gray Duck research)
- Terminal DiLLMa (Johann Rehberger) — ANSI escape code injection via LLMs
- DoubleClickJacking: A New Era of UI Redressing (Paulos Yibelo)
- CTFd 0day — cross-site leak via 200/404 history visit + requestAnimationFrame timing

### Suggestions and Advices from Hunter
- "When Orange Tsai releases research, add those characters to your payloads immediately." — Justin Gardner
- "Hackers' brains tingle at little stuff like Safari cookie truncation — that's where bugs hide." — Justin Gardner
- "Unicode cookie bombs: you need a single cookie value injection, not arbitrary cookie set — much easier to find." — Justin Gardner

### AI Takeaway
Orange Tsai's Worst Fit research is one of the most impactful vulnerability discoveries of the year — Unicode normalization to ASCII equivalents is embedded in Windows, curl, OpenSSL, Python, and countless libraries. Every penetration tester should add YEN SIGN and FULLWIDTH variants to their path traversal and injection wordlists.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Worst Fit (Orange Tsai): Unicode normalization maps YEN SIGN (U+00A5) to backslash → path traversal, command injection, subprocess escape

#### 2. What you should learn
- Understand **unicode normalization maps yen sign (u+00a5) → backslash, fullwidth solidus → slash. add these to path traversal wordlists**
- Understand **ruby on rails: json body not starting with `{` → stored in `params[_json]` — middleware parsing mismatch**
- Understand **`fetch()` with blob body = no content-type header → bypasses `if request.contenttype != 'application/json' { reject }`**
- Understand **unicode cookie character can dos major websites (facebook, instagram, netflix, amazon, etc.)**
- Understand **safari: `-- value, value --` cookie pattern gets spaces truncated — undocumented behavior**

#### 3. Core concepts explained
**Worst Fit — Unicode Normalization to Backslash**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**`_json` Juggling Attack**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Cross-Site POST Without Content-Type**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Unicode normalization payloads**
- Add YEN SIGN (U+00A5), FULLWIDTH REVERSE SOLIDUS, FULLWIDTH QUOTATION MARK (U+FF02) to path traversal and injection wordlists

**`_json` param smuggling**
- Send JSON arrays/strings instead of objects to exploit Rails' `_json` internal parameter key

**Blob body CSRF bypass**
- `fetch(url, {method:'POST', body: new Blob([data])})` → no Content-Type → bypasses `contentType != 'application/json'` checks


#### 4. Techniques and tactics
**Unicode normalization payloads**
- **What it is:** Add YEN SIGN (U+00A5), FULLWIDTH REVERSE SOLIDUS, FULLWIDTH QUOTATION MARK (U+FF02) to path traversal and injection wordlists
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`_json` param smuggling**
- **What it is:** Send JSON arrays/strings instead of objects to exploit Rails' `_json` internal parameter key
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Blob body CSRF bypass**
- **What it is:** `fetch(url, {method:'POST', body: new Blob([data])})` → no Content-Type → bypasses `contentType != 'application/json'` checks
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Unicode cookie bomb**
- **What it is:** Set a cookie with any Unicode/emoji character → DOS on Facebook, Instagram, Netflix, Amazon, etc.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When Orange Tsai releases research, add those characters to your payloads immediately."* — **Justin Gardner**
- *"Hackers' brains tingle at little stuff like Safari cookie truncation"* — **that's where bugs hide." — Justin Gardner**
- *"Unicode cookie bombs: you need a single cookie value injection, not arbitrary cookie set"* — **much easier to find." — Justin Gardner**

#### 6. Mental models
- **When Orange Tsai releases research, add those characters to ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Hackers' brains tingle at little stuff like Safari cookie tr** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Unicode cookie bombs: you need a single cookie value injecti** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Unicode normalization maps YEN SIGN (U+00A5) → backslash, FULLWIDTH SOLIDUS → slash. Add these to path traversal wordlists
- **Try this:** Ruby on Rails: JSON body not starting with `{` → stored in `params[_json]` — middleware parsing mismatch
- **Try this:** `fetch()` with blob body = no Content-Type header → bypasses `if request.contentType != 'application/json' { reject }`
- **Try this:** Unicode cookie character can DOS major websites (Facebook, Instagram, Netflix, Amazon, etc.)

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Character must be supported by the locale/charset. Some payloads needed double YEN sign for effect.

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Worst Fit — Unicode Normalization to Backslash?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Worst Fit (Orange Tsai): Unicode normalization maps YEN SIGN (U+00A5) to backsla**
2. **Unicode normalization maps YEN SIGN (U+00A5) → backslash, FULLWIDTH SOLIDUS → sl**
3. **Ruby on Rails: JSON body not starting with `{` → stored in `params[_json]` — mid**
