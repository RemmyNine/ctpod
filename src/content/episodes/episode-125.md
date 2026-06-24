---
title: "How to Win Live Hacking Events"
episode: 125
---


# Episode 125 How to Win Live Hacking Events

### TL;DR
- Jorian's ultimate double-clickjacking POC: window.moveTo + pop-under + fake Cloudflare CAPTCHA + Flappy Bird game
- Grafana CVE-2025-4123: open redirect via `/\` (slash-backslash) → SSRF via render endpoint → $3,700
- Live hacking event strategy: pick your portion → ignore leaderboard → lock in → attack vector value = (impact × viability) / friction
- Pre-event: preload family time, clear chores, disable notifications
- Don't define identity on event outcome

### Key Takeaways
- **Attack vector value**: `(impact × viability) / friction` — prioritize high-impact, high-viability, low-friction attacks
- **Scope call**: pick what the team wants hacked (impact) but balance with anticipated competition (viability) — tier 0 impact, tier 1 interest
- **Dupe window**: don't collab before dupe window ends; if you do collab, collab with someone less skilled or with different skill set to avoid overlap
- **Ignore leaderboard** — people flexing in Slack are just demoralizing you; stay locked on your portion
- **Take care of biology**: eat, sleep, exercise, go for walks — crits are often solved away from the keyboard
- **Show and tell**: pay attention; also do "show and tell" informally with other hackers — trade bugs and learn
- **Advocate for your bugs**: knock on the war room door with a prepared POC

### Bugs and Findings

#### Ultimate Double-Clickjacking POC (Jorian)
- **Target/context:** Any single-click authorization action
- **Root cause:** Combination of window.moveTo (to align buttons), pop-under (to obscure window), and fake CAPTCHA with double-click trigger
- **Technique / how found:**
  1. Use `window.open` + known target name to create pop-under
  2. Use `window.moveTo` to align victim's approve button with expected click location
  3. Fake Cloudflare CAPTCHA asks visitor to double-click
  4. First click: close pop-under → second click: lands on victim's approve button
- **Key technical details:** Fake CAPTCHA with Flappy Bird game; double-click trigger; `window.moveTo()` works cross-origin
- **Impact / severity / bounty:** Full ATO via one auth click
- **Obstacles & how solved:** Pop-ups need to be enabled; fake CAPTCHA must be convincing

#### Grafana CVE-2025-4123 — Open Redirect to SSRF
- **Target/context:** Grafana instances
- **Root cause:** `/\` (slash + backslash) at start of URL causes browser to interpret it as protocol-relative absolute URL
- **Technique / how found:**
  1. Open redirect via `/\` at path start: `https://grafana.com/\/@attacker.com` → browser redirects to `https://attacker.com`
  2. Chain with Grafana's render endpoint to get SSRF
- **Key technical details:** `/\` = backslash normalized by browser to `/` → protocol-relative URL `//attacker.com`; render endpoint follows redirects
- **Impact / severity / bounty:** $3,700 — open redirect → SSRF
- **Obstacles & how solved:** Requires authenticated user to click (low severity initially); chained with render endpoint for SSRF

### Techniques and Primitives
- **Double-clickjack + moveTo** — `window.moveTo()` to align buttons; fake CAPTCHA to trigger double-click
- **Attack vector value formula** — `(impact × viability) / friction`
- **Scope triage** — Pick tier 0 impact, tier 1 interest (intimidating to others)
- **Show-and-tell trading** — "Show me your bugs and I'll show you mine"
- **Advocate for bugs** — Knock on war room door with prepared POC

### Tooling and Resources
- Jorian's ultimate double-clickjacking POC
- Evan Connelly's "First 100 Bugs" writeup
- Critical Thinking Discord
- HackerNotes by GretMe

### Suggestions and Advices from Hunter
- "Pick your portion of the scope, lock in, and find a shit ton of bugs. Ignore leaders who are flexing in Slack."
- "Take time away from the screen. I've popped multiple crits while sitting in the hot tub or on a walk."
- "Don't define your identity on the outcome of a live hacking event — it's too volatile."
- "If you find yourself comparing, redirect to positive: 'Hell yeah, my boy just popped a crit! Let's go!'"

### AI Takeaway
The attack vector value formula `(impact × viability) / friction` is a useful mental model for any hacking, not just live events. The advice about pre-loading family time and doing deep scope commitment applies to any concentrated hacking effort.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Jorian's ultimate double-clickjacking POC: window.moveTo + pop-under + fake Cloudflare CAPTCHA + Flappy Bird game

#### 2. What you should learn
- Understand **attack vector value**: `(impact × viability) / friction` — prioritize high-impact, high-viability, low-friction attacks**
- Understand **scope call**: pick what the team wants hacked (impact) but balance with anticipated competition (viability) — tier 0 impact, tier 1 interest**
- Understand **dupe window**: don't collab before dupe window ends; if you do collab, collab with someone less skilled or with different skill set to avoid overlap**
- Understand **ignore leaderboard** — people flexing in slack are just demoralizing you; stay locked on your portion**
- Understand **take care of biology**: eat, sleep, exercise, go for walks — crits are often solved away from the keyboard**

#### 3. Core concepts explained
**Ultimate Double-Clickjacking POC (Jorian)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Grafana CVE-2025-4123 — Open Redirect to SSRF**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Double-clickjack + moveTo**
- `window.moveTo()` to align buttons; fake CAPTCHA to trigger double-click

**Attack vector value formula**
- `(impact × viability) / friction`

**Scope triage**
- Pick tier 0 impact, tier 1 interest (intimidating to others)


#### 4. Techniques and tactics
**Double-clickjack + moveTo**
- **What it is:** `window.moveTo()` to align buttons; fake CAPTCHA to trigger double-click
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Attack vector value formula**
- **What it is:** `(impact × viability) / friction`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Scope triage**
- **What it is:** Pick tier 0 impact, tier 1 interest (intimidating to others)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Show-and-tell trading**
- **What it is:** "Show me your bugs and I'll show you mine"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Advocate for bugs**
- **What it is:** Knock on war room door with prepared POC
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Pick your portion of the scope, lock in, and find a shit ton of bugs. Ignore leaders who are flexing in Slack."*
- *"Take time away from the screen. I've popped multiple crits while sitting in the hot tub or on a walk."*
- *"Don't define your identity on the outcome of a live hacking event"* — **it's too volatile.**
- *"If you find yourself comparing, redirect to positive: 'Hell yeah, my boy just popped a crit! Let's go!'"*

#### 6. Mental models
- **Pick your portion of the scope, lock in, and find a shit ton** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Take time away from the screen. I've popped multiple crits w** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Don't define your identity on the outcome of a live hacking ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Attack vector value**: `(impact × viability) / friction` — prioritize high-impact, high-viability, low-friction attacks
- **Try this:** Scope call**: pick what the team wants hacked (impact) but balance with anticipated competition (viability) — tier 0 impact, tier 1 interest
- **Try this:** Dupe window**: don't collab before dupe window ends; if you do collab, collab with someone less skilled or with different skill set to avoid overlap
- **Try this:** Ignore leaderboard** — people flexing in Slack are just demoralizing you; stay locked on your portion

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Pop-ups need to be enabled; fake CAPTCHA must be convincing
- - Obstacles & how solved: Requires authenticated user to click (low severity initially); chained with render endpoint for SSRF

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Ultimate Double-Clickjacking POC (Jorian)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Jorian's ultimate double-clickjacking POC: window.moveTo + pop-under + fake Clou**
2. **Attack vector value**: `(impact × viability) / friction` — prioritize high-impac**
3. **Scope call**: pick what the team wants hacked (impact) but balance with anticipa**
