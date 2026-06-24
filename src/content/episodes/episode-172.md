---
title: "Source Code Review Meta Analysis"
episode: 172
---


# Episode 172 Source Code Review Meta Analysis

### TL;DR
- Three root causes of vulns: (1) trace data flow better than dev, (2) know context nuances better than dev, (3) dev forgot security controls
- Increasing complexity of the environment where input lands = higher probability of bug
- Common patterns: parser differentials, chaining, dependency auditing, validate-then-transform ordering, alternative sources
- Key pitfalls: non-global string replacement, bad regex, casing issues, incomplete syntax checks

### Key Takeaways
- [ ] Trace data flow end-to-end: every source to every sink — the developer often didn't realize deep user input was user input
- [ ] When user input enters a "complex environment" (SQL, config files, templates, dynamic code eval), alarm bells should ring
- [ ] Look for validate-then-transform patterns — any transformation after sanitization invalidates it; sanitization must be right before the sink
- [ ] Search for alternative data sources into the same sink (SMS, WebSocket, legacy endpoints, mass import) — they may bypass source-level sanitization
- [ ] Audit path operations in C#: `Path.Combine(SAFE_DIR, userInput)` where `userInput` is absolute — the prefix is silently discarded

### Techniques and Primitives
- **Data flow tracing** — Follow input from entry point through all transformations to final sink; deeper paths are more likely to have missed sanitization
- **Alternative source hunting** — Find all ways data enters the same processing point; one may lack source-level sanitization
- **Non-global replacement** — `string.replace("bad", "")` only replaces first occurrence — always check for `g` flag or recursive replacement
- **Bad regex patterns** — Missing `^`/`$` anchors, unescaped dots in brackets, backslash in character classes acting as literal
- **Dynamic function calling** — PHP string function calls, RPC-like patterns where a string becomes a function name
- **Custom sanitizer fuzzing** — Instrument custom sanitizers and fuzz them; partial bypasses can chain with other gadgets

### Tooling and Resources
- SL Cyber Hyoketsu — scans source code for known open-source libraries/jars
- Ghidra + MCP + Claude — reverse engineering binaries with AI
- AssetNote / SL Cyber write-ups
- YesWeHack Open Source Security Testing Guide

### Suggestions and Advices from Hunter
- "Pay somebody on Fiverr to set up the software on a server for $200 — best money you'll ever spend." — Shubs
- "The more complex the environment where your input lands, the more likely a bug exists." — Justin Gardner
- "Any time I see a `replace()` call on user input, I stare at it for 15 seconds. Something usually jumps out." — Justin Gardner
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Three root causes of vulns: (1) trace data flow better than dev, (2) know context nuances better than dev, (3) dev forgot security controls

#### 2. What you should learn
- Understand **[ ] trace data flow end-to-end: every source to every sink — the developer often didn't realize deep user input was user input**
- Understand **[ ] when user input enters a "complex environment" (sql, config files, templates, dynamic code eval), alarm bells should ring**
- Understand **[ ] look for validate-then-transform patterns — any transformation after sanitization invalidates it; sanitization must be right before the sink**
- Understand **[ ] search for alternative data sources into the same sink (sms, websocket, legacy endpoints, mass import) — they may bypass source-level sanitization**
- Understand **[ ] audit path operations in c#: `path.combine(safe_dir, userinput)` where `userinput` is absolute — the prefix is silently discarded**

#### 3. Core concepts explained
**Data flow tracing**
- Follow input from entry point through all transformations to final sink; deeper paths are more likely to have missed sanitization

**Alternative source hunting**
- Find all ways data enters the same processing point; one may lack source-level sanitization

**Non-global replacement**
- `string.replace("bad", "")` only replaces first occurrence — always check for `g` flag or recursive replacement


#### 4. Techniques and tactics
**Data flow tracing**
- **What it is:** Follow input from entry point through all transformations to final sink; deeper paths are more likely to have missed sanitization
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Alternative source hunting**
- **What it is:** Find all ways data enters the same processing point; one may lack source-level sanitization
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Non-global replacement**
- **What it is:** `string.replace("bad", "")` only replaces first occurrence — always check for `g` flag or recursive replacement
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Bad regex patterns**
- **What it is:** Missing `^`/`$` anchors, unescaped dots in brackets, backslash in character classes acting as literal
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Dynamic function calling**
- **What it is:** PHP string function calls, RPC-like patterns where a string becomes a function name
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Pay somebody on Fiverr to set up the software on a server for $200"* — **best money you'll ever spend." — Shubs**
- *"The more complex the environment where your input lands, the more likely a bug exists."* — **Justin Gardner**
- *"Any time I see a `replace()` call on user input, I stare at it for 15 seconds. Something usually jumps out."* — **Justin Gardner**

#### 6. Mental models
- **Pay somebody on Fiverr to set up the software on a server fo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The more complex the environment where your input lands, the** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Any time I see a `replace()` call on user input, I stare at ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Trace data flow end-to-end: every source to every sink — the developer often didn't realize deep user input was user input
- **Try this:** [ ] When user input enters a "complex environment" (SQL, config files, templates, dynamic code eval), alarm bells should ring
- **Try this:** [ ] Look for validate-then-transform patterns — any transformation after sanitization invalidates it; sanitization must be right before the sink
- **Try this:** [ ] Search for alternative data sources into the same sink (SMS, WebSocket, legacy endpoints, mass import) — they may bypass source-level sanitization

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **fuzzing** — Sending unexpected or malformed data to discover vulnerabilities

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Three root causes of vulns: (1) trace data flow better than dev, (2) know contex**
2. **[ ] Trace data flow end-to-end: every source to every sink — the developer often**
3. **[ ] When user input enters a "complex environment" (SQL, config files, templates**
