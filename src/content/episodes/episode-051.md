---
title: "Hacker Stats 2023 & 2024 Goals"
episode: 51
---


# Episode 51 Hacker Stats 2023 & 2024 Goals

### TL;DR
- Franz Rosen's XSS CTF: used JavaScript `String.prototype.replace` with `$&` (match substring) to re-inject a double quote from the matched text
- HackerOne 25K SSRF: blind SSRF in analytics reports via HTML injection in PDF renderer
- Kaido released their search rework with wireshark-esque query language
- PortSwigger released Blind CSS Exfiltration tool (Gareth Hayes) — based on Donut/Pepe Villa's CSS import chain technique
- 2023 hacker stats review and 2024 goal setting

### Key takeaways
- `String.replace()` has special replacement patterns: `$&` (matched substring), `$`` (before match), `$'` (after match) — injecting these into the replacement string can bypass sanitization
- HackerOne crit: a simple HTML `<iframe>` injection in report analytics template -> PDF generator loads -> SSRF to AWS metadata at `169.254.169.254`
- Blind CSS exfiltration: use CSS `@import` chaining with `:has()` and `:not()` selectors to enumerate input field values character by character

### Bugs and Findings
#### Franz Rosen's Regex Replace XSS CTF
- **Target/context:** Google Tag Manager template with escape functions
- **Root cause:** The escape function for regex didn't escape `$` character; `$&` in the payload became the entire matched substring
- **Technique:**
  1. Payload contained `$&` which matched the preceding text (which included a double quote from the HTML attribute)
  2. The double quote was inserted into the replacement, breaking out of the attribute
  3. Allowed injection of arbitrary HTML attributes -> XSS
- **Key technical details:** `$&` in replacement string = the matched substring; `$`` = portion before match; `$'` = portion after match

#### HackerOne 25k Crit SSRF
- **Target:** HackerOne's analytics report functionality
- **Technique:**
  1. Create a new report
  2. In the analytics template, inject HTML `<iframe>` pointing to `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
  3. PDF generator renders the iframe -> SSRF to AWS metadata endpoint
  4. Extract AWS credentials
- **Impact / severity / bounty:** Full AWS account compromise -> $25,000

### Techniques and Primitives
- **Regex replacement injection** — if user input ends up in a `str.replace(regex, replacement)`, injecting `$&`, `$``, `$'` gives control over output
- **Blind CSS exfiltration** — chained `@import` with `:has()` selector: each `@import` polls server with unique URL for each character guess; server responds when character matches

### Tooling and Resources
- **PowerToys** (Windows) — launcher with OCR
- **Flow** — Python-powered launcher
- **Pyperclip** — Python clipboard module
- **Blind CSS Exfiltration** tool (PortSwigger)

### AI Takeaway
The `$&` regex replacement pattern is a reminder that "escaping" functions must cover all special characters in the target context. The fact that `$&`, `$``, and `$'` exist in JavaScript and reference the matched string means any replacement string from user input is code, not data.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Franz Rosen's XSS CTF: used JavaScript `String.prototype.replace` with `$&` (match substring) to re-inject a double quote from the matched text

#### 2. What you should learn
- Understand **`string.replace()` has special replacement patterns: `$&` (matched substring), `$`` (before match), `$'` (after match) — injecting these into the replacement string can bypass sanitization**
- Understand **hackerone crit: a simple html `<iframe>` injection in report analytics template -> pdf generator loads -> ssrf to aws metadata at `169.254.169.254`**
- Understand **blind css exfiltration: use css `@import` chaining with `:has()` and `:not()` selectors to enumerate input field values character by character**

#### 3. Core concepts explained
**Franz Rosen's Regex Replace XSS CTF**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**HackerOne 25k Crit SSRF**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Regex replacement injection**
- if user input ends up in a `str.replace(regex, replacement)`, injecting `$&`, `$``, `$'` gives control over output

**Blind CSS exfiltration**
- chained `@import` with `:has()` selector: each `@import` polls server with unique URL for each character guess; server responds when character matches


#### 4. Techniques and tactics
**Regex replacement injection**
- **What it is:** if user input ends up in a `str.replace(regex, replacement)`, injecting `$&`, `$``, `$'` gives control over output
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Blind CSS exfiltration**
- **What it is:** chained `@import` with `:has()` selector: each `@import` polls server with unique URL for each character guess; server responds when character matches
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
- **Try this:** `String.replace()` has special replacement patterns: `$&` (matched substring), `$`` (before match), `$'` (after match) — injecting these into the replacement string can bypass sanitization
- **Try this:** HackerOne crit: a simple HTML `<iframe>` injection in report analytics template -> PDF generator loads -> SSRF to AWS metadata at `169.254.169.254`
- **Try this:** Blind CSS exfiltration: use CSS `@import` chaining with `:has()` and `:not()` selectors to enumerate input field values character by character

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **AWS metadata** — Cloud instance metadata service at 169.254.169.254 — contains IAM credentials

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Franz Rosen's Regex Replace XSS CTF?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Franz Rosen's XSS CTF: used JavaScript `String.prototype.replace` with `$&` (mat**
2. **`String.replace()` has special replacement patterns: `$&` (matched substring), `**
3. **HackerOne crit: a simple HTML `<iframe>` injection in report analytics template **
