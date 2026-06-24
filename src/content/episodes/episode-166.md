---
title: "Rez0's Top Claude Skill Secrets"
episode: 166
---


# Episode 166 Rez0's Top Claude Skill Secrets

### TL;DR
- Claude Code skills: markdown files with frontmatter (title, description) that get loaded into context — the `description` field determines when the skill is invoked
- Skills are best for: things Claude doesn't know natively, custom setups (VPS creds, file structures), secret techniques not in training data
- Three-tier architecture: skill file → primitives (JS/Python CLI) → direct GraphQL — fallback chain when a method fails
- Claude.md should define note structure: notes → leads → gadgets/primitives → findings → reports
- Use folder-based `.claude` configs to scope skills to specific targets

### Key Takeaways
- [ ] Build skills for custom workflows (Kaido integration, target-specific gadgets) — Claude won't know these natively
- [ ] Structure hacking notes in a funnel: notes (everything) → leads (interesting items) → gadgets/primitives (reusable) → findings (confirmed bugs) → reports (written)
- [ ] Use folder-based Claude.md: run `claude` from a target-specific folder with target info in that folder's `.claude/Claude.md`
- [ ] In skill frontmatter, put invocation rules in the `description` field — Claude uses this (not skill body) to decide when to invoke
- [ ] Limit subagents to 2-3 when running autonomously overnight to avoid compaction issues
- [ ] Contribute false-positive learnings back to your skills/Claude.md to improve signal

### Techniques and Primitives
- **Fallback skill architecture** — Try skill → fall back to primitives → fall back to direct API/GraphQL when higher-level methods fail
- **Session search skill** — CLI wrapper for ripgrep across all Claude session logs (up to 4GB); find tokens, commands, findings from past sessions
- **Validator agent** — Separate agent that reviews findings for false positives; uses severity guidelines, real examples, and skepticism
- **Subagent limiting for overnight runs** — Cap at 2-3 subagents to prevent context compaction deadlocks

### Tooling and Resources
- H1Brain MCP (Patrick) — pulls policy page, scope, and disclosed reports
- Kaido Mode Skill — integrates Claude with Kaido proxy/Replay
- BBscope — scope/report dumping
- Zero-Day Research skill (XSS Doctor) — trained on Eugene's content for zero-day hunting in source code and binaries
- Report Writer skill — example reports, fields template

### Suggestions and Advices from Hunter
- "Create a skill that says: 'When I ask you to do something, invoke the skill. But if it fails or isn't comprehensive enough, don't stop there — use your own exploration.'" — Joseph Thacker
- "Tokens are cheap and subsidized right now. Always do both: hardcode your methodology AND let Claude free-roam, then compare." — Joseph Thacker
- "Don't say 'I trained my ChatGPT' — you gave it context and a prompt, not fine-tuning." — Joseph Thacker
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Claude Code skills: markdown files with frontmatter (title, description) that get loaded into context — the `description` field determines when the skill is invoked

#### 2. What you should learn
- Understand **[ ] build skills for custom workflows (kaido integration, target-specific gadgets) — claude won't know these natively**
- Understand **[ ] structure hacking notes in a funnel: notes (everything) → leads (interesting items) → gadgets/primitives (reusable) → findings (confirmed bugs) → reports (written)**
- Understand **[ ] use folder-based claude.md: run `claude` from a target-specific folder with target info in that folder's `.claude/claude.md`**
- Understand **[ ] in skill frontmatter, put invocation rules in the `description` field — claude uses this (not skill body) to decide when to invoke**
- Understand **[ ] limit subagents to 2-3 when running autonomously overnight to avoid compaction issues**

#### 3. Core concepts explained
**Fallback skill architecture**
- Try skill → fall back to primitives → fall back to direct API/GraphQL when higher-level methods fail

**Session search skill**
- CLI wrapper for ripgrep across all Claude session logs (up to 4GB); find tokens, commands, findings from past sessions

**Validator agent**
- Separate agent that reviews findings for false positives; uses severity guidelines, real examples, and skepticism


#### 4. Techniques and tactics
**Fallback skill architecture**
- **What it is:** Try skill → fall back to primitives → fall back to direct API/GraphQL when higher-level methods fail
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Session search skill**
- **What it is:** CLI wrapper for ripgrep across all Claude session logs (up to 4GB); find tokens, commands, findings from past sessions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Validator agent**
- **What it is:** Separate agent that reviews findings for false positives; uses severity guidelines, real examples, and skepticism
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Subagent limiting for overnight runs**
- **What it is:** Cap at 2-3 subagents to prevent context compaction deadlocks
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Create a skill that says: 'When I ask you to do something, invoke the skill. But if it fails or isn't comprehensive enough, don't stop there"* — **use your own exploration.'" — Joseph Thacker**
- *"Tokens are cheap and subsidized right now. Always do both: hardcode your methodology AND let Claude free-roam, then compare."* — **Joseph Thacker**
- *"Don't say 'I trained my ChatGPT'"* — **you gave it context and a prompt, not fine-tuning." — Joseph Thacker**

#### 6. Mental models
- **Create a skill that says: 'When I ask you to do something, i** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Tokens are cheap and subsidized right now. Always do both: h** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Don't say 'I trained my ChatGPT' — you gave it context and a** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Build skills for custom workflows (Kaido integration, target-specific gadgets) — Claude won't know these natively
- **Try this:** [ ] Structure hacking notes in a funnel: notes (everything) → leads (interesting items) → gadgets/primitives (reusable) → findings (confirmed bugs) → reports (written)
- **Try this:** [ ] Use folder-based Claude.md: run `claude` from a target-specific folder with target info in that folder's `.claude/Claude.md`
- **Try this:** [ ] In skill frontmatter, put invocation rules in the `description` field — Claude uses this (not skill body) to decide when to invoke

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Claude Code skills: markdown files with frontmatter (title, description) that ge**
2. **[ ] Build skills for custom workflows (Kaido integration, target-specific gadget**
3. **[ ] Structure hacking notes in a funnel: notes (everything) → leads (interesting**
