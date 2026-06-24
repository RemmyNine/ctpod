---
title: "Protobuf Hacking, AI-Powered Bug Hunting, and Self-Improving Claude Workflows"
episode: 165
---


# Episode 165 Protobuf Hacking, AI-Powered Bug Hunting, and Self-Improving Claude Workflows

### TL;DR
- Protobuf decoding in Google: many parameters are base64-encoded binary Protobuf — often unsigned and modifiable
- Claude Code is very good at reversing Protobuf structures and computing checksums
- Bug hunters should build skills/Claude.md files for target-specific knowledge and tool access (Kaido, custom servers)
- Self-improving Claude via Claude.md "applied learning" section — whenever Claude struggles, document the fix for next time

### Key Takeaways
- [ ] Decode base64-encoded Protobuf strings in requests — even without field names, you can identify IDs, strings, and structures; Claude can reverse and re-encode them
- [ ] For Google hacking: Protobuf fields have wire type (3 bits), field number (4 bits), continuation bit — understanding this helps decode binary Protobuf
- [ ] Add an "applied learning" section to your Claude.md — every time Claude fails or gets frustrated, document the solution
- [ ] Permission delegation via iframe `allow` attribute — check if third-party iframes inherit microphone/camera permissions
- [ ] Login CSRF + audio recording CSRF = microphone spying chain

### Bugs and Findings

#### Mic Recording CSRF Chain (Login CSRF + Audio CSRF)
- **Target/context:** Web app with microphone permission and recording feature
- **Root cause:** Domain-locked permissions (mic) vs account-locked authorization; once user grants mic permission to site, CSRF can trigger recording without interaction
- **Technique:** 1) Login CSRF into attacker's account 2) CSRF the "start recording" endpoint 3) Recording is uploaded to attacker's account after timeout
- **Key technical details:** Requires user to have previously clicked "Allow" on microphone permission; login CSRF to attacker's controlled account; recording transcribed and saved to attacker's account
- **Impact / severity / bounty:** Microphone surveillance — spy on victim remotely

#### Permission Delegation via iframe `allow` Attribute
- **Target/context:** Sites embedding third-party iframes with `allow` attribute
- **Technique:** Check if iframe has `allow="microphone"` or `allow="camera"` — top-level frame delegates permissions to iframe; attacker-controlled iframe can abuse
- **Key technical details:** HTML iframe `allow` property specifies permissions policy
- **Impact / severity / bounty:** Unauthorized sensor access via third-party iframe

### Techniques and Primitives
- **Protobuf binary injection via base64** — Decode, tweak, re-encode with Protoscope; Claude can infer field structure and checksums
- **Self-improving Claude.md** — When Claude fails, document the fix in an "applied learning" section; it improves over time
- **Kaido + Claude integration** — Use Kaido mode skill so Claude can read/edit HTTP history, replay requests, and add findings

### Tooling and Resources
- Protoscope — binary Protobuf decode/encode CLI
- BBscope (sweetlie) — scope dumping tool for HackerOne
- H1Brain MCP by PatrikFehrenbach — search HackerOne reports
- Caido skills repo: github.com/caido/skills
- Matt Brown (nmatt0) — IoT/hardware hacking YouTube channel
- OriginalSickSec — HackerOne MCP client

### Suggestions and Advices from Hunter
- "If you have three accounts on Claude.ai and turn training data off on each, that's three times the tokens." — Joseph Thacker (joking)
- "What you're really doing is lending all your technical expertise to make the AI work. Claude can do the hosting too now." — Justin Gardner
- "Play whack-a-mole with false positives — go back, look at them, and incorporate why they were wrong into the prompt." — Joseph Thacker
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Protobuf decoding in Google: many parameters are base64-encoded binary Protobuf — often unsigned and modifiable

#### 2. What you should learn
- Understand **[ ] decode base64-encoded protobuf strings in requests — even without field names, you can identify ids, strings, and structures; claude can reverse and re-encode them**
- Understand **[ ] for google hacking: protobuf fields have wire type (3 bits), field number (4 bits), continuation bit — understanding this helps decode binary protobuf**
- Understand **[ ] add an "applied learning" section to your claude.md — every time claude fails or gets frustrated, document the solution**
- Understand **[ ] permission delegation via iframe `allow` attribute — check if third-party iframes inherit microphone/camera permissions**
- Understand **[ ] login csrf + audio recording csrf = microphone spying chain**

#### 3. Core concepts explained
**Mic Recording CSRF Chain (Login CSRF + Audio CSRF)**
- **What it is:** Cross-Site Request Forgery — tricking a victim's browser into making unwanted requests to a site where they're authenticated.
- **Why it matters:** CSRF can change email, password, or perform actions on behalf of the victim.
- **Common mistake:** Only testing GET-based CSRF — POST and PUT endpoints with CSRF tokens may still be vulnerable if tokens are predictable.

**Permission Delegation via iframe `allow` Attribute**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Protobuf binary injection via base64**
- Decode, tweak, re-encode with Protoscope; Claude can infer field structure and checksums

**Self-improving Claude.md**
- When Claude fails, document the fix in an "applied learning" section; it improves over time

**Kaido + Claude integration**
- Use Kaido mode skill so Claude can read/edit HTTP history, replay requests, and add findings


#### 4. Techniques and tactics
**Protobuf binary injection via base64**
- **What it is:** Decode, tweak, re-encode with Protoscope; Claude can infer field structure and checksums
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Self-improving Claude.md**
- **What it is:** When Claude fails, document the fix in an "applied learning" section; it improves over time
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Kaido + Claude integration**
- **What it is:** Use Kaido mode skill so Claude can read/edit HTTP history, replay requests, and add findings
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have three accounts on Claude.ai and turn training data off on each, that's three times the tokens."* — **Joseph Thacker (joking)**
- *"What you're really doing is lending all your technical expertise to make the AI work. Claude can do the hosting too now."* — **Justin Gardner**
- *"Play whack-a-mole with false positives"* — **go back, look at them, and incorporate why they were wrong into the prompt." — Joseph Thacker**

#### 6. Mental models
- **If you have three accounts on Claude.ai and turn training da** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **What you're really doing is lending all your technical exper** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Play whack-a-mole with false positives — go back, look at th** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Decode base64-encoded Protobuf strings in requests — even without field names, you can identify IDs, strings, and structures; Claude can reverse and re-encode them
- **Try this:** [ ] For Google hacking: Protobuf fields have wire type (3 bits), field number (4 bits), continuation bit — understanding this helps decode binary Protobuf
- **Try this:** [ ] Add an "applied learning" section to your Claude.md — every time Claude fails or gets frustrated, document the solution
- **Try this:** [ ] Permission delegation via iframe `allow` attribute — check if third-party iframes inherit microphone/camera permissions

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Mic Recording CSRF Chain (Login CSRF + Audio CSRF)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Protobuf decoding in Google: many parameters are base64-encoded binary Protobuf **
2. **[ ] Decode base64-encoded Protobuf strings in requests — even without field name**
3. **[ ] For Google hacking: Protobuf fields have wire type (3 bits), field number (4**
