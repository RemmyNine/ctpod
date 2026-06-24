---
title: "Claude Code + Tmux, Websockets, and Other Korea LHE Takeaways"
episode: 170
---


# Episode 170 Claude Code + Tmux, Websockets, and Other Korea LHE Takeaways

### TL;DR
- Claude Code + tmux reverse shell: pipe commands via `tmux send-keys` into an nc reverse shell pane
- Google LHE: zero-click AI bugs are becoming more deterministic; POC quality and social engineering context are critical
- OAuth grant scope expansion: AI agents/MCP servers performing actions beyond what the user authorized in the grant
- Regression testing on AI features: adding new rendering or preview features can re-enable old exfiltration bugs
- Human tokens concept: advocating for your bugs with triage — prepare hit lists, lock in severity commitments

### Key Takeaways
- [ ] Use `tmux send-keys` to give Claude Code control of a reverse shell — works perfectly, no escaping issues
- [ ] Record video POCs immediately when you find a bug (or even before, if you suspect one) — AI can't forge a talking-head video
- [ ] Test for OAuth grant scope expansion: does the AI agent perform actions beyond what the OAuth grant authorized?
- [ ] Write concise reports for Google VRP — AI-written slop gets closed; ensure POC video shows clear attacker→victim narrative
- [ ] Hone your VRP reporting agent with explicit instructions: concise, technical, no fluff, attacker-victim language

### Bugs and Findings

#### Google OAuth Grant Scope Expansion
- **Target/context:** Google AI/MCP servers using OAuth grants
- **Root cause:** OAuth grant token was used for feature authorization, but the AI's actual permissions were different/broader
- **Technique:** 1) Complete OAuth grant with specific scopes 2) Observe AI actions exceeding granted scopes
- **Impact / severity / bounty:** Unauthorized data access; privilege escalation

### Techniques and Primitives
- **tmux + Claude Code for reverse shell control** — `tmux send-keys -t <pane> "<command>"` lets Claude send arbitrary commands into an nc reverse shell
- **Protoscope for binary Protobuf** — CLI tool to decode/encode binary Protobuf; pipe through base64 for Kaido workflow
- **Regression testing against old AI exfiltration bugs** — Companies add new rendering/preview features that re-enable old exfiltration vectors
- **Human tokens / mouth tokens** — Advocate for your bugs: prepare a hit list, elevator pitch each bug, end with "we agree this is a [severity]", DM that commitment to the triager

### Tooling and Resources
- Protoscope — binary Protobuf CLI tool
- Kaido WebSocket Repeater (upcoming)
- tmux
- Burp Suite for WebSocket replay (current workaround)

### Suggestions and Advices from Hunter
- "Record a video immediately when you discover a bug — even if you don't write the report that moment." — Justin Gardner
- "Handwrite your reports unless you've really honed your AI report writer." — Justin Gardner
- "Have a hit list when meeting with triage. Boom boom boom — elevator pitch, lock in severity, notate it." — Justin Gardner
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Claude Code + tmux reverse shell: pipe commands via `tmux send-keys` into an nc reverse shell pane

#### 2. What you should learn
- Understand **[ ] use `tmux send-keys` to give claude code control of a reverse shell — works perfectly, no escaping issues**
- Understand **[ ] record video pocs immediately when you find a bug (or even before, if you suspect one) — ai can't forge a talking-head video**
- Understand **[ ] test for oauth grant scope expansion: does the ai agent perform actions beyond what the oauth grant authorized?**
- Understand **[ ] write concise reports for google vrp — ai-written slop gets closed; ensure poc video shows clear attacker→victim narrative**
- Understand **[ ] hone your vrp reporting agent with explicit instructions: concise, technical, no fluff, attacker-victim language**

#### 3. Core concepts explained
**Google OAuth Grant Scope Expansion**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**tmux + Claude Code for reverse shell control**
- `tmux send-keys -t <pane> "<command>"` lets Claude send arbitrary commands into an nc reverse shell

**Protoscope for binary Protobuf**
- CLI tool to decode/encode binary Protobuf; pipe through base64 for Kaido workflow

**Regression testing against old AI exfiltration bugs**
- Companies add new rendering/preview features that re-enable old exfiltration vectors


#### 4. Techniques and tactics
**tmux + Claude Code for reverse shell control**
- **What it is:** `tmux send-keys -t <pane> "<command>"` lets Claude send arbitrary commands into an nc reverse shell
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Protoscope for binary Protobuf**
- **What it is:** CLI tool to decode/encode binary Protobuf; pipe through base64 for Kaido workflow
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Regression testing against old AI exfiltration bugs**
- **What it is:** Companies add new rendering/preview features that re-enable old exfiltration vectors
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Human tokens / mouth tokens**
- **What it is:** Advocate for your bugs: prepare a hit list, elevator pitch each bug, end with "we agree this is a [severity]", DM that commitment to the triager
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Record a video immediately when you discover a bug"* — **even if you don't write the report that moment." — Justin Gardner**
- *"Handwrite your reports unless you've really honed your AI report writer."* — **Justin Gardner**
- *"Have a hit list when meeting with triage. Boom boom boom"* — **elevator pitch, lock in severity, notate it." — Justin Gardner**

#### 6. Mental models
- **Record a video immediately when you discover a bug — even if** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Handwrite your reports unless you've really honed your AI re** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Have a hit list when meeting with triage. Boom boom boom — e** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Use `tmux send-keys` to give Claude Code control of a reverse shell — works perfectly, no escaping issues
- **Try this:** [ ] Record video POCs immediately when you find a bug (or even before, if you suspect one) — AI can't forge a talking-head video
- **Try this:** [ ] Test for OAuth grant scope expansion: does the AI agent perform actions beyond what the OAuth grant authorized?
- **Try this:** [ ] Write concise reports for Google VRP — AI-written slop gets closed; ensure POC video shows clear attacker→victim narrative

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **API** — Application Programming Interface — structured endpoints for data exchange
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Google OAuth Grant Scope Expansion?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Claude Code + tmux reverse shell: pipe commands via `tmux send-keys` into an nc **
2. **[ ] Use `tmux send-keys` to give Claude Code control of a reverse shell — works **
3. **[ ] Record video POCs immediately when you find a bug (or even before, if you su**
