---
title: "Zendesk Fiasco & the CTBB Naughty List"
episode: 94
---


# Episode 94 Zendesk Fiasco & the CTBB Naughty List

**Hosts:** Justin Gardner (Rhynorater), Joel Margolis (Teknogeek)
**Duration:** 49:29
**Transcript source:** feed (full transcript)

### TL;DR
- Zendesk email spoofing bug closed as "Informative" by H1 triage; researcher disclosed to affected customers → Zendesk crisis; community split on ethics
- AuthzAI (Ron Chan's open-source authorization audit tool) launched
- Ophion Security research: live chat HMAC authentication bypass via `_svpt` cookie value manipulation
- Debate over hacker "naughty list" vs platform-level accountability

### Key Takeaways
- Email spoofing bugs require extra scrutiny on Zendesk (history of impactful email bugs)
- Live chat/third-party integrations are often the weakest link — HMAC-based auth that trusts client-provided identifiers is a common pattern
- When a program says "informative", you're still bound by their disclosure terms — but there's a gray area when the bug is valid but rejected
- Best approach: make a public statement acknowledging the mistake, pay the bounty, move on

### Bugs and Findings

#### Zendesk Email-Based Helpdesk Ticket Leak
- **Target/context:** Zendesk helpdesk platform
- **Root cause:** Email spoofing allows sending emails that appear to come from Zendesk; email security headers misconfiguration leaks ticket contents
- **Technique / how found:** Researcher Hackermondev (15 years old) found a way to leak contents of any helpdesk ticket via email spoofing
- **Key technical details:** Email security headers/spoofing; HackerOne triage closed as "Informative" saying email spoofing is not a valid bug; mediation confirmed the decision
- **Impact / severity / bounty:** Eventually led to ~$50K across multiple affected companies after disclosure. Zendesk initially: Informative/NA.
- **Obstacles & how solved:** H1 triager + mediation both misclassified. Researcher disclosed to affected companies. Zendesk responded by saying researcher violated program terms. Community outrage.

#### Ophion Security — Live Chat HMAC Auth Bypass
- **Target/context:** Live chat systems (HelpShift and others)
- **Root cause:** HMAC digest generated client-side using user identifiers and secret key; `_svpt` cookie with email address value used to authenticate → dumping the auth token was trivial
- **Technique / how found:** Rogan (Ophion Security) analyzed the integration flow: website → generates HMAC using user identifiers → passes to live chat service as authentication
- **Key technical details:** `_svpt` cookie contains email address → server dumps back auth token. The entire authentication relies on client-side data.
- **Impact / severity / bounty:** Access to other users' live chat messages/conversations
- **Obstacles & how solved:** Trend across multiple live chat services using similar patterns

### Techniques and Primitives
- **Third-party integration assessment** — The glue between your app and third-party services is often the weakest point. Check auth handoff, cookie sharing, and trust assumptions.
- **Program accountability tracking** — The episode sparked debate about a community-maintained "naughty list" of programs that mistreat researchers (ultimately rejected as too close to blackmail/extortion)

### Tooling and Resources
- AuthzAI (https://authzai.com) — Ron Chan's open-source authorization audit tool
- Ophion Security research blog
- Hackermondev Zendesk disclosure gist

### Suggestions and Advices from Hunter
- "Triage services at scale face a systemic problem: putting a generic puzzle piece into a complex solution tends to fail." — Joel Margolis
- "If you're getting a lot of pushback about something, give it a little manual look." — Joel Margolis (to programs)
- "Email bugs: 99% are informative. But when you look deeper, this one was valid." — Rhynorater

### AI Takeaway
The Zendesk incident demonstrates that generic triage at scale cannot handle per-program nuance. The `_svpt` cookie auth pattern is a great SSO/handoff vulnerability class to check across live chat, support, and integration systems — any place where authentication credentials are derived from client-supplied identifiers.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Zendesk email spoofing bug closed as "Informative" by H1 triage; researcher disclosed to affected customers → Zendesk crisis; community split on ethics

#### 2. What you should learn
- Understand **email spoofing bugs require extra scrutiny on zendesk (history of impactful email bugs)**
- Understand **live chat/third-party integrations are often the weakest link — hmac-based auth that trusts client-provided identifiers is a common pattern**
- Understand **when a program says "informative", you're still bound by their disclosure terms — but there's a gray area when the bug is valid but rejected**
- Understand **best approach: make a public statement acknowledging the mistake, pay the bounty, move on**

#### 3. Core concepts explained
**Zendesk Email-Based Helpdesk Ticket Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Ophion Security — Live Chat HMAC Auth Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Third-party integration assessment**
- The glue between your app and third-party services is often the weakest point. Check auth handoff, cookie sharing, and trust assumptions.

**Program accountability tracking**
- The episode sparked debate about a community-maintained "naughty list" of programs that mistreat researchers (ultimately rejected as too close to blackmail/extortion)


#### 4. Techniques and tactics
**Third-party integration assessment**
- **What it is:** The glue between your app and third-party services is often the weakest point. Check auth handoff, cookie sharing, and trust assumptions.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Program accountability tracking**
- **What it is:** The episode sparked debate about a community-maintained "naughty list" of programs that mistreat researchers (ultimately rejected as too close to blackmail/extortion)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Triage services at scale face a systemic problem: putting a generic puzzle piece into a complex solution tends to fail."* — **Joel Margolis**
- *"If you're getting a lot of pushback about something, give it a little manual look."* — **Joel Margolis (to programs)**
- *"Email bugs: 99% are informative. But when you look deeper, this one was valid."* — **Rhynorater**

#### 6. Mental models
- **Triage services at scale face a systemic problem: putting a ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you're getting a lot of pushback about something, give it** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Email bugs: 99% are informative. But when you look deeper, t** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Email spoofing bugs require extra scrutiny on Zendesk (history of impactful email bugs)
- **Try this:** Live chat/third-party integrations are often the weakest link — HMAC-based auth that trusts client-provided identifiers is a common pattern
- **Try this:** When a program says "informative", you're still bound by their disclosure terms — but there's a gray area when the bug is valid but rejected
- **Try this:** Best approach: make a public statement acknowledging the mistake, pay the bounty, move on

#### 8. Red flags and pitfalls
- - Obstacles & how solved: H1 triager + mediation both misclassified. Researcher disclosed to affected companies. Zendesk responded by saying researcher violated program terms. Community outrage.
- - Obstacles & how solved: Trend across multiple live chat services using similar patterns

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Zendesk Email-Based Helpdesk Ticket Leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Zendesk email spoofing bug closed as "Informative" by H1 triage; researcher disc**
2. **Email spoofing bugs require extra scrutiny on Zendesk (history of impactful emai**
3. **Live chat/third-party integrations are often the weakest link — HMAC-based auth **
