---
title: "Bypassing Cross-Origin Browser Headers"
episode: 107
---


# Episode 107 Bypassing Cross-Origin Browser Headers

**Host:** Justin Gardner (Rhynorater)
**Co-Host:** Joseph Thacker (Rez0)
**Duration:** 1:06:17
**Transcript source:** feed (full transcript)

### TL;DR
- Coop (Cross-Origin Opener Policy) severs window.opener relationships — kills postMessage bugs between cross-origin windows
- Workaround: iframe the Coop-protected page into a page WITHOUT Coop → opener relationship preserved
- Cross-origin headers: Coop, Coep, Corp — part of "cross-origin isolation" (mitigation for Spectre)
- Rez0's AI agent security tweet went viral (118K views) — "AI agent security is a massively slept-on industry"
- Google OAuth login flaw: expired/defunct startup domains allow SSO account takeover
- Gift card hacking: race conditions, IDOR, HTML injection in gift card flows are highly reliable

### Key Takeaways
- Coop header values: `same-origin` (severs all cross-origin opener), `same-origin-allow-popups` (popups keep opener, but not vice versa), `unsafe-none`/missing (default, no restriction)
- If you can get a Coop-protected page iframed into a non-Coop page, you can communicate with it via postMessage through the iframe
- Third-party pivot: XSS on a trusted partner page → redirect Coop-target's iframe on that partner page → postMessage works
- AI agent security: tool invocation chains, untrusted context injection, and sandbox escapes are the key attack surfaces
- Gift card bugs: buy $5 gift card → always find race condition, IDOR, or XSS

### Techniques and Primitives
- **Coop bypass via iframe pivot** — Find a page without Coop that iframes the Coop-protected page. Get XSS on the framing page → communicate with the iframed Coop page via postMessage.
- **Third-party trust chain** — Get XSS on a vendor/support site that the target trusts (framed or embedded on the target page). From there, pivot to the Coop-protected origin.

### Tooling and Resources
- Andrew Lock's "Understanding Cross-Origin Security Headers" (3-part blog series)
- "A Proud Dad's Tale of Two Bug Hunting Daughters" (Dustin Kirkland)
- TruffleSec Google OAuth login flaw writeup
- RAINK (BishopFox) — AI ranking tool for payloads/vulnerable functions
- W2W's Gift Card Security Research
- PortSwigger Top 10 Web Hacking Techniques 2024 voting

### Suggestions and Advices from Hunter
- "If you have a post-message vulnerability that's blocked by Coop, check if there's a way to get the page iframed somewhere." — Justin Gardner
- "Go hack on things you're not supposed to. Find access on third parties." — Justin Gardner (on third-party trust pivots)
- "Taint tracking for AI agents: as soon as untrusted data enters the prompt context, tool invocation should stop." — Joseph Thacker
- "Gift card hacking: always enable out-of-scope logging to catch the checkout finalization request." — W2W

### AI Takeaway
Coop is one of the most frustrating headers for client-side exploitation, but the iframe pivot technique provides a reliable bypass. AI agent security represents a massive underserved niche — the combination of tool invocation, untrusted context injection, and the inability to taint-track properly creates systemic vulnerabilities.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Coop (Cross-Origin Opener Policy) severs window.opener relationships — kills postMessage bugs between cross-origin windows

#### 2. What you should learn
- Understand **coop header values: `same-origin` (severs all cross-origin opener), `same-origin-allow-popups` (popups keep opener, but not vice versa), `unsafe-none`/missing (default, no restriction)**
- Understand **if you can get a coop-protected page iframed into a non-coop page, you can communicate with it via postmessage through the iframe**
- Understand **third-party pivot: xss on a trusted partner page → redirect coop-target's iframe on that partner page → postmessage works**
- Understand **ai agent security: tool invocation chains, untrusted context injection, and sandbox escapes are the key attack surfaces**
- Understand **gift card bugs: buy $5 gift card → always find race condition, idor, or xss**

#### 3. Core concepts explained
**Coop bypass via iframe pivot**
- Find a page without Coop that iframes the Coop-protected page. Get XSS on the framing page → communicate with the iframed Coop page via postMessage.

**Third-party trust chain**
- Get XSS on a vendor/support site that the target trusts (framed or embedded on the target page). From there, pivot to the Coop-protected origin.


#### 4. Techniques and tactics
**Coop bypass via iframe pivot**
- **What it is:** Find a page without Coop that iframes the Coop-protected page. Get XSS on the framing page → communicate with the iframed Coop page via postMessage.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Third-party trust chain**
- **What it is:** Get XSS on a vendor/support site that the target trusts (framed or embedded on the target page). From there, pivot to the Coop-protected origin.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have a post-message vulnerability that's blocked by Coop, check if there's a way to get the page iframed somewhere."* — **Justin Gardner**
- *"Go hack on things you're not supposed to. Find access on third parties."* — **Justin Gardner (on third-party trust pivots)**
- *"Taint tracking for AI agents: as soon as untrusted data enters the prompt context, tool invocation should stop."* — **Joseph Thacker**
- *"Gift card hacking: always enable out-of-scope logging to catch the checkout finalization request."* — **W2W**

#### 6. Mental models
- **If you have a post-message vulnerability that's blocked by C** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Go hack on things you're not supposed to. Find access on thi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Taint tracking for AI agents: as soon as untrusted data ente** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Coop header values: `same-origin` (severs all cross-origin opener), `same-origin-allow-popups` (popups keep opener, but not vice versa), `unsafe-none`/missing (default, no restriction)
- **Try this:** If you can get a Coop-protected page iframed into a non-Coop page, you can communicate with it via postMessage through the iframe
- **Try this:** Third-party pivot: XSS on a trusted partner page → redirect Coop-target's iframe on that partner page → postMessage works
- **Try this:** AI agent security: tool invocation chains, untrusted context injection, and sandbox escapes are the key attack surfaces

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Coop (Cross-Origin Opener Policy) severs window.opener relationships — kills pos**
2. **Coop header values: `same-origin` (severs all cross-origin opener), `same-origin**
3. **If you can get a Coop-protected page iframed into a non-Coop page, you can commu**
