---
title: "White Box Formulas — Vulnerable Coding Patterns"
episode: 54
---


# Episode 54 White Box Formulas — Vulnerable Coding Patterns

### TL;DR
- Joel's HackerOne data scraping: top 10 programs pay 50% of all bounties; 75% of programs pay <10K total (accounting for 10% of bounties)
- HackerNotes launched — podcast companion with 5-bullet TLDR + elaboration
- GitLab CVE-2023-7028: account takeover by passing array of emails in password reset (`user[email][]=victim@example.com&user[email][]=attacker@example.com`)
- Invisible prompt injection using Unicode tag characters (invisible text that LLMs can read)
- Vulnerable code pattern analysis: sanitize-then-modify, auth check inside if statement, bad regex, replace-as-sanitizer

### Key takeaways
- 75% of programs pay <$10K total over 90 days = lots of uncrowded programs with budget
- GitLab ATO: passing an array instead of a single email caused password reset to be sent to both addresses
- Unicode tag characters (U+E0000-U+E007F) are invisible but LLMs parse them — can embed hidden prompt injections in visible text
- Code patterns to look for in code review: sanitize + modify, auth inside if, bad regex with dots not escaped, replace() as sanitizer

### Bugs and Findings
#### GitLab CVE-2023-7028 — Account Takeover
- **Target:** Self-hosted and GitLab.com
- **Root cause:** Password reset endpoint accepted array parameter for email
- **Technique:**
  ```
  POST /users/password
  user[email][]=victim@example.com&user[email][]=attacker@example.com
  ```
- **Key technical details:** Both emails received the password reset link; attacker could reset victim's password
- **Impact / severity / bounty:** Critical — unauthenticated account takeover; CVSS 10.0
- **Fix:** Validate `email` parameter is a string, not an array

### Techniques and Primitives
- **Array parameter injection** — when a parameter expects a scalar, try passing an array (`param[]=a&param[]=b`) to trigger unexpected behavior
- **Unicode tag character prompt injection** — characters `U+E0000` to `U+E007F` represent letters but are invisible; copy-paste them into an LLM prompt and it reads the hidden instruction
- **Vulnerable code patterns:**
  1. Sanitize then modify data (e.g., `strip_tags()` then `urldecode()`) — the second call undoes the first
  2. Auth check inside an if-block without proper control flow — missing `exit`/`return`/`die` after auth failure
  3. Bad regex: unescaped dots (`.` matches any char, allowing domain confusion)
  4. `str_replace()` as sanitizer — single-pass replace can be bypassed with nested payloads

### Suggestions and Advices from Hunter
- On code review patterns: "When I turn these into formulas in my brain, it makes the code easier to see — less intuition-based, more principle-based"
- "If you find a bug and they don't rotate the credential, the fix is incomplete"
- On data scraping: "Top 10 programs pay 50% of all bounties, but 75% of programs pay <10K total — those are uncrowded"

### AI Takeaway
The GitLab ATO is one of the simplest yet most impactful bugs: a single parameter type confusion (`email` string vs `email[]` array) in a password reset flow. The invisible Unicode tag character attack is a foundational LLM injection vector — the characters are invisible to humans but fully readable by models, making prompt injection undetectable.


### 📘 Episode Booklet

#### 1. Episode in one sentence
Joel's HackerOne data scraping: top 10 programs pay 50% of all bounties; 75% of programs pay <10K total (accounting for 10% of bounties)

#### 2. What you should learn
- Understand **75% of programs pay <$10k total over 90 days = lots of uncrowded programs with budget**
- Understand **gitlab ato: passing an array instead of a single email caused password reset to be sent to both addresses**
- Understand **unicode tag characters (u+e0000-u+e007f) are invisible but llms parse them — can embed hidden prompt injections in visible text**
- Understand **code patterns to look for in code review: sanitize + modify, auth inside if, bad regex with dots not escaped, replace() as sanitizer**

#### 3. Core concepts explained
**GitLab CVE-2023-7028 — Account Takeover**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Array parameter injection**
- when a parameter expects a scalar, try passing an array (`param[]=a&param[]=b`) to trigger unexpected behavior

**Unicode tag character prompt injection**
- characters `U+E0000` to `U+E007F` represent letters but are invisible; copy-paste them into an LLM prompt and it reads the hidden instruction

**Vulnerable code patterns:**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**Array parameter injection**
- **What it is:** when a parameter expects a scalar, try passing an array (`param[]=a&param[]=b`) to trigger unexpected behavior
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Unicode tag character prompt injection**
- **What it is:** characters `U+E0000` to `U+E007F` represent letters but are invisible; copy-paste them into an LLM prompt and it reads the hidden instruction
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Vulnerable code patterns:**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"On code review patterns: "When I turn these into formulas in my brain, it makes the code easier to see"* — **less intuition-based, more principle-based**
- *"If you find a bug and they don't rotate the credential, the fix is incomplete"*
- *"On data scraping: "Top 10 programs pay 50% of all bounties, but 75% of programs pay <10K total"* — **those are uncrowded**

#### 6. Mental models
- **On code review patterns: "When I turn these into formulas in** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you find a bug and they don't rotate the credential, the ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On data scraping: "Top 10 programs pay 50% of all bounties, ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** 75% of programs pay <$10K total over 90 days = lots of uncrowded programs with budget
- **Try this:** GitLab ATO: passing an array instead of a single email caused password reset to be sent to both addresses
- **Try this:** Unicode tag characters (U+E0000-U+E007F) are invisible but LLMs parse them — can embed hidden prompt injections in visible text
- **Try this:** Code patterns to look for in code review: sanitize + modify, auth inside if, bad regex with dots not escaped, replace() as sanitizer

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **prompt injection** — Tricking an LLM into ignoring its instructions by injecting malicious input
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in GitLab CVE-2023-7028 — Account Takeover?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Joel's HackerOne data scraping: top 10 programs pay 50% of all bounties; 75% of **
2. **75% of programs pay <$10K total over 90 days = lots of uncrowded programs with b**
3. **GitLab ATO: passing an array instead of a single email caused password reset to **
