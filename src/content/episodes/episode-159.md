---
title: "Google Cloud VRP with Cote and Darby Hopkins"
episode: 159
---


# Episode 159 Google Cloud VRP with Cote and Darby Hopkins

### TL;DR
- Google Cloud VRP team explains reward structure, panel process, tiers, and how to maximize payouts
- BugSWAT event: 160 reports, $1.6M rewarded; top bugs were service account impersonation chains
- "Privilege escalation delta" is key — clearly state attacker's start vs end privileges
- Avoiding downgrades: follow standard documentation/configuration; call out "User interaction beyond normal usage" vs normal workflow
- 1.2x exceptional report bonus for clear, concise, reproducible reports

### Key Takeaways
- **Tier system**: T1 = high-revenue, wide-attack-surface products (Cloud Storage); T3 = acquisitions, smaller products. But T3 bugs can chain into T1 bugs via interconnectedness
- **Panel process**: 4-6 hours reviewing ~15 reports; leader does deep-dive before panel; all reports get L0 triage → product team → security engineer → panel; appeals go back to same panel
- **Downgrade categories (avoid these):**
  - Prior access: attacker needs more permissions than implied
  - User interaction beyond normal usage (tabs vs normal workflow clicks)
  - Uncommon configuration: using the product in a non-standard setup
  - Exploitability: e.g., time-limited race window, but only if it reduces number of vulnerable customers
- **Report quality bonus (1.2x)**: Short, to-the-point, reproducible. Do NOT write 20-page research papers. Include attack preconditions section. Fix suggestions help. Do NOT use AI to write the full report
- **Exceptional reports**: Clear impact description, attack preconditions, product-understanding explanation, short succint POC
- **Acquisitions**: ~3 years after acquisition, moved from IT3A to higher tier
- **Credentials/credits**: Reach out to Cote/Darby for access to expensive enterprise products; they're working on formal credit programs

### Suggestions and Advices from Hunter
- "If you can point to product documentation about why you believe something isn't working the way it should be, that's one of the best arguments you can make on our panel."
- "Selfishly, it's to our benefit to pay you a little bit of extra time to put some of that extra work into your report so that we can more quickly understand the impact, reproduce, get you a reward faster."
- "Use Terraform, follow our setup documentation — the more closely you match a common customer environment, the more successful you'll be."
- "Feel free to submit your report in your native language whatever you're more comfortable with. We have Google Translate."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Google Cloud VRP team explains reward structure, panel process, tiers, and how to maximize payouts

#### 2. What you should learn
- Understand **tier system**: t1 = high-revenue, wide-attack-surface products (cloud storage); t3 = acquisitions, smaller products. but t3 bugs can chain into t1 bugs via interconnectedness**
- Understand **panel process**: 4-6 hours reviewing ~15 reports; leader does deep-dive before panel; all reports get l0 triage → product team → security engineer → panel; appeals go back to same panel**
- Understand **downgrade categories (avoid these):**
- Understand **prior access: attacker needs more permissions than implied**
- Understand **user interaction beyond normal usage (tabs vs normal workflow clicks)**

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"If you can point to product documentation about why you believe something isn't working the way it should be, that's one of the best arguments you can make on our panel."*
- *"Selfishly, it's to our benefit to pay you a little bit of extra time to put some of that extra work into your report so that we can more quickly understand the impact, reproduce, get you a reward faster."*
- *"Use Terraform, follow our setup documentation"* — **the more closely you match a common customer environment, the more successful you'll be.**
- *"Feel free to submit your report in your native language whatever you're more comfortable with. We have Google Translate."*

#### 6. Mental models
- **If you can point to product documentation about why you beli** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Selfishly, it's to our benefit to pay you a little bit of ex** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use Terraform, follow our setup documentation — the more clo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Tier system**: T1 = high-revenue, wide-attack-surface products (Cloud Storage); T3 = acquisitions, smaller products. But T3 bugs can chain into T1 bugs via interconnectedness
- **Try this:** Panel process**: 4-6 hours reviewing ~15 reports; leader does deep-dive before panel; all reports get L0 triage → product team → security engineer → panel; appeals go back to same panel
- **Try this:** Downgrade categories (avoid these):
- **Try this:** Prior access: attacker needs more permissions than implied

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Google Cloud VRP team explains reward structure, panel process, tiers, and how t**
2. **Tier system**: T1 = high-revenue, wide-attack-surface products (Cloud Storage); **
3. **Panel process**: 4-6 hours reviewing ~15 reports; leader does deep-dive before p**
