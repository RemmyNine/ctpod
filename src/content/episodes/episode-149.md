---
title: "DEFCON Debrief"
episode: 149
---


# Episode 149 DEFCON Debrief

### TL;DR
- Justin and Joseph recap their favorite DEFCON 33 talks
- Expo team's Prompt→Scan→Exploit talk: scoring targets, deduplication via embeddings, model-switching strategy, diminishing returns per vuln class
- Breaking into thousands of cloud VPNs with one bug — SAML bypasses, pre-auth config leaks in Zscaler/Netscope
- DOM Clobbering at scale — TheHulk tool found ~500 bugs in webpack/rspack/Vite/Astro
- Passkeys — shim navigator.credentials via malicious extension for ATO

### Bugs and Findings

#### Unicode Surrogates → Wildcard in Databases
- **Target/context:** Elasticsearch / Solar
- **Root cause:** Unicode code point DC2A normalizes to `?`, which is a wildcard character in Elasticsearch/Solar
- **Technique / how found:** Crit Research Lab submission
- **Key technical details:** Code point U+DC2A (a surrogate) → `?` → wildcard in databases
- **Impact:** Potential for authentication bypass, data leakage via wildcard matching

#### Expo Team Scoring & Deduplication
- **Target/context:** Hackbot / AI vulnerability scanning
- **Key technical details:**
  - 80-attribute scoring: does it have GraphQL? Forms? API? Password reset? → AI rates each host
  - Cut 45% of targets (low-scoring ones)
  - Dedup via text content + embeddings (cosine similarity) instead of visual/DOM hashing
  - Model rotation: switch models every rotation cycle — different models bring different perspectives, increasing efficacy
  - Diminishing returns: per vulnerability class, find optimal rotation count (e.g., XSS peaks at 8 rotations) then stop

#### DOM Clobbering at Scale — TheHulk
- **Target/context:** Webpack, Rspack, Vite, Astro, Google API client library
- **Root cause:** Bundler runtime code vulnerable to DOM clobbering
- **Technique / how found:** Formalized DOM clobbering — taint analysis → AST → HTML structure → auto-payload generation
- **Key technical details:** ~500 zero-days/bugs found; tool called "TheHulk" on GitHub; requires HTML injection primitive
- **Impact:** XSS via DOM clobbering on major bundlers
- **Tool:** DOM Clobbering Collection by Jack from East

#### Passkey Shim via Malicious Extension — ATO
- **Target/context:** WebAuthn / passkeys
- **Root cause:** Browser extensions can shim `navigator.credentials` calls
- **Exploitation steps:**
  1. Malicious extension inserts content script
  2. Shim `navigator.credentials.get()` / `.create()`
  3. On registration: link attacker's passkey to victim's account
  4. On login: intercept auth material and use for ATO
- **Impact:** Full account takeover including passkey-protected accounts

### Techniques and Primitives
**Pre-auth Config Enumeration (SaaS/Appliances)** — Find endpoints like `/.git/mobile/user/pack?orgKey=<key>` that leak org config (routes, internal/external hosts, keys); works on Netscope and other appliances

**Bad SAML Testing** — Create your own tenant/org, sign your own SAML assertions, test cross-org access; check if signature validation is just checking "valid signature" vs "signature valid for this specific tenant"; check field validation within signed assertions

**AI Agent Model Rotation** — Rotate models each agent cycle to avoid stagnation; different internal structures yield different approaches

### Suggestions and Advices from Hunter
- Joseph on gadget research: "Anytime there's like a gadget that slows something down to get a race condition through, it feels like that's just peak hacking."
- On prompt injection delivery: Use the app's own suggested prompts (e.g., "summarize my day") for more realistic PoC
- "Mirror the model's language in your prompt injection payload"
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Justin and Joseph recap their favorite DEFCON 33 talks

#### 2. What you should learn
- Learn about **justin and joseph recap their favorite defcon 33 talks**
- Learn about **expo team's prompt→scan→exploit talk: scoring targets, deduplication via embeddings, model-switching strategy, diminishing returns per vuln class**
- Learn about **breaking into thousands of cloud vpns with one bug — saml bypasses, pre-auth config leaks in zscaler/netscope**
- Learn about **dom clobbering at scale — thehulk tool found ~500 bugs in webpack/rspack/vite/astro**
- Learn about **passkeys — shim navigator.credentials via malicious extension for ato**

#### 3. Core concepts explained
**Unicode Surrogates → Wildcard in Databases**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Expo Team Scoring & Deduplication**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**DOM Clobbering at Scale — TheHulk**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Joseph on gadget research: "Anytime there's like a gadget that slows something down to get a race condition through, it feels like that's just peak hacking."*
- *"On prompt injection delivery: Use the app's own suggested prompts (e.g., "summarize my day") for more realistic PoC"*
- *"Mirror the model's language in your prompt injection payload"*

#### 6. Mental models
- **Joseph on gadget research: "Anytime there's like a gadget th** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On prompt injection delivery: Use the app's own suggested pr** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Mirror the model's language in your prompt injection payload** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **embeddings** — Mathematical representations of text for similarity search

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Unicode Surrogates → Wildcard in Databases?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Justin and Joseph recap their favorite DEFCON 33 talks**
