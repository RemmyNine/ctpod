---
title: "Rhyno's Hackbot Setup, Sick Bugs, and ZDI Drama"
episode: 175
---


# Episode 175 Rhyno's Hackbot Setup, Sick Bugs, and ZDI Drama

### TL;DR
- Wormable AI exploit: Q-parameter prompt injection → GitHub connector → modify files → auto-deploy → worm spreads via GitHub Pages
- Q-parameter prompt injection: GET parameter that auto-injects as user prompt — bypasses CSRF/redirect protections
- GPT-5.5 vs Claude: GPT-5.5 found 3 P1s in 30 minutes on a fresh Bugcrowd program; `/goal` mode runs overnight until success condition
- Anthropic restricted `-p` (print) mode to separate API credits — workaround: use PTY harness instead
- ZDI drama: Pwn2Own maxed out, Ryotak couldn't register; Orange Tsai got RCE on Edge without memory corruption (4 logic bug chain, $175K)

### Key Takeaways
- [ ] Q-parameter prompt injection: test every AI app for GET parameters that auto-feed the prompt — CSRF/redirect/window.opener can trigger them silently
- [ ] Ambiguous prompting: "go change my website" lets AI figure out the mechanism — more robust than specific instructions
- [ ] Try GPT-5.5 for black-box testing — `/goal` mode runs continuously; symlink Claude.md to Agent.md for Codex compatibility
- [ ] Use PTY harness instead of `-p` for Claude Code to avoid the new API credit restrictions
- [ ] Beautiful POCs matter: v12sec's 192-byte Linux LPE animation — a stunning visual POC helps triage appreciate the finding

### Bugs and Findings

#### Wormable Q-Parameter Prompt Injection → GitHub Auto-Deploy
- **Target/context:** AI app with GitHub connector and Q-parameter injection
- **Root cause:** GET parameter auto-injects into AI prompt as if from the user; AI has GitHub write access
- **Technique:** 1) User visits attacker page 2) Q-parameter injection tells AI: "change my website files" 3) AI lists GitHub repos, finds website repo, modifies files 4) GitHub Pages auto-deploys modified site 5) Modified site contains redirect that triggers same exploit on visitors (wormable)
- **Key technical details:** Q-param = GET parameter auto-fed to prompt; AI uses ambiguous prompting ("change my website") to self-determine repo; window.opener redirect hides processing time
- **Impact / severity / bounty:** Wormable AI exploit — automatic propagation through GitHub Pages CI/CD

#### Mobile CSPT — Second-Order via Link Shortener + Embedded API Key
- **Target/context:** Mobile app with link shortener service
- **Root cause:** Embedded API key in mobile app can create short links with JSON parameter blobs; app resolves short link → processes JSON blob → one action triggers POST request with attacker-controlled path
- **Technique:** 1) Extract embedded API key from mobile app 2) Create custom short link with JSON parameters 3) Victim opens link in app 4) App sends POST request with path containing attacker's traversal payload 5) Truncation via `#`, traversal via `../` → arbitrary POST to victim's API
- **Key technical details:** 27 actions available from JSON parameters; one triggers POST with attacker path; no body control but query params get treated as body by some endpoints
- **Impact / severity / bounty:** Account modification, financial loss, auto-confirm access requests

#### Admin API Key in JS File — Social Media Mega-Crit
- **Target/context:** Fortune 100 brand's social media management
- **Root cause:** API key for social media admin found in JS file — full access to brand's social media account
- **Technique:** JS file enumeration → found API key → full admin access to social media (millions of followers)
- **Impact / severity / bounty:** Could tweet crypto scams, read DMs, delete content

### Techniques and Primitives
- **Q-parameter prompt injection** — GET parameter auto-injected into AI prompt; triggerable via CSRF, redirect, or window.opener
- **Ambiguous prompting** — "Change my website" lets AI enumerate repos, identify website, and modify — more resilient than specific instructions
- **PTY harness for Claude Code** — Write to the pseudo-terminal's PTY instead of using `-p` to avoid API credit restrictions
- **Stop-hook for infinite loop** — Use Claude's stop hook to auto-write "keep going" into the PTY when Claude stops naturally
- **Validator agent with SSH resume** — Triages bugs, writes report, provides SSH command to resume the session with full context

### Tooling and Resources
- GPT-5.5 via Codex — better black-box testing than Claude; `/goal` mode runs to success condition
- v12sec Universal Linux LPE — 192 bytes, read-only page cache overwrite
- Orange Tsai's 4 logic bug chain — $175K, RCE on Edge without memory corruption

### Suggestions and Advices from Hunter
- "When it gets fixed here but works over there, that's a regression. Set Claude to do regression testing for you." — Justin Gardner
- "Beautiful POCs make triagers breathe a breath of fresh air. Give them something beautiful to look at." — Justin Gardner
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Wormable AI exploit: Q-parameter prompt injection → GitHub connector → modify files → auto-deploy → worm spreads via GitHub Pages

#### 2. What you should learn
- Understand **[ ] q-parameter prompt injection: test every ai app for get parameters that auto-feed the prompt — csrf/redirect/window.opener can trigger them silently**
- Understand **[ ] ambiguous prompting: "go change my website" lets ai figure out the mechanism — more robust than specific instructions**
- Understand **[ ] try gpt-5.5 for black-box testing — `/goal` mode runs continuously; symlink claude.md to agent.md for codex compatibility**
- Understand **[ ] use pty harness instead of `-p` for claude code to avoid the new api credit restrictions**
- Understand **[ ] beautiful pocs matter: v12sec's 192-byte linux lpe animation — a stunning visual poc helps triage appreciate the finding**

#### 3. Core concepts explained
**Wormable Q-Parameter Prompt Injection → GitHub Auto-Deploy**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Mobile CSPT — Second-Order via Link Shortener + Embedded API Key**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Admin API Key in JS File — Social Media Mega-Crit**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Q-parameter prompt injection**
- GET parameter auto-injected into AI prompt; triggerable via CSRF, redirect, or window.opener

**Ambiguous prompting**
- "Change my website" lets AI enumerate repos, identify website, and modify — more resilient than specific instructions

**PTY harness for Claude Code**
- Write to the pseudo-terminal's PTY instead of using `-p` to avoid API credit restrictions


#### 4. Techniques and tactics
**Q-parameter prompt injection**
- **What it is:** GET parameter auto-injected into AI prompt; triggerable via CSRF, redirect, or window.opener
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Ambiguous prompting**
- **What it is:** "Change my website" lets AI enumerate repos, identify website, and modify — more resilient than specific instructions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**PTY harness for Claude Code**
- **What it is:** Write to the pseudo-terminal's PTY instead of using `-p` to avoid API credit restrictions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Stop-hook for infinite loop**
- **What it is:** Use Claude's stop hook to auto-write "keep going" into the PTY when Claude stops naturally
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Validator agent with SSH resume**
- **What it is:** Triages bugs, writes report, provides SSH command to resume the session with full context
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When it gets fixed here but works over there, that's a regression. Set Claude to do regression testing for you."* — **Justin Gardner**
- *"Beautiful POCs make triagers breathe a breath of fresh air. Give them something beautiful to look at."* — **Justin Gardner**

#### 6. Mental models
- **When it gets fixed here but works over there, that's a regre** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Beautiful POCs make triagers breathe a breath of fresh air. ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Q-parameter prompt injection: test every AI app for GET parameters that auto-feed the prompt — CSRF/redirect/window.opener can trigger them silently
- **Try this:** [ ] Ambiguous prompting: "go change my website" lets AI figure out the mechanism — more robust than specific instructions
- **Try this:** [ ] Try GPT-5.5 for black-box testing — `/goal` mode runs continuously; symlink Claude.md to Agent.md for Codex compatibility
- **Try this:** [ ] Use PTY harness instead of `-p` for Claude Code to avoid the new API credit restrictions

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **prompt injection** — Tricking an LLM into ignoring its instructions by injecting malicious input
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Wormable Q-Parameter Prompt Injection → GitHub Auto-Deploy?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Wormable AI exploit: Q-parameter prompt injection → GitHub connector → modify fi**
2. **[ ] Q-parameter prompt injection: test every AI app for GET parameters that auto**
3. **[ ] Ambiguous prompting: "go change my website" lets AI figure out the mechanism**
