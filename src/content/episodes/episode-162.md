---
title: "HackerOne Training AI on Bug Bounty Data?"
episode: 162
---


# Episode 162 HackerOne Training AI on Bug Bounty Data?

### TL;DR
- Alex Rice (HackerOne CTO/Founder) addresses community concerns about TOS section 3.1 and AI training
- HackerOne is definitively NOT training GenAI models on researcher/customer submissions
- Section 3.1 language is from pre-LLM era covering classic ML (spam classifiers) — an oversight they're correcting
- Agentic PTaaS uses public benchmarks, internal benchmarks, custom vulnerable apps, public CVEs/disclosures, and opt-in sidecar runs — NOT bug bounty reports
- Bounty decrease explained: re-benchmarked from top 1% (Google/Meta tier) to top 80th percentile (high-growth tech); crit definition kept broad (any confidential info exposure)

### Key Findings

#### HackerOne TOS 3.1 Clarification
- **Issue:** "HackerOne may use Confidential Information to develop and/or improve its Services (for example, to identify trends, and to train AI models)"
- **Clarification:** This language dates from before LLMs — covers classic ML like spam classifiers. No GenAI models are trained on submissions. No LLM fine-tuning on report data exists or is planned
- **Anonymized data:** Only used for Hacker-Powered Security Report (aggregate trends). No LLMs involved in that pipeline
- **Bug bounty reports are NOT used in Agentic PTAS.** PTAS trains on: public benchmarks, internal benchmarks, custom vulnerable apps, public CVEs/disclosures, opt-in sidecar runs (pentester + customer consent)
- **IP retention:** Section 8 of community terms: researchers retain all IP; grant limited license to HackerOne for service provision only; customer gets unrestricted license for their own remediation

### Key Takeaways
- **Researcher retains IP** — not transferred to HackerOne or customer (customer gets broad license for remediation)
- **No GenAI training on submissions** — reporting is for spam classifiers and aggregate trends only
- **PTAS Agentic**: uses sidecar runs (opt-in by pentester + customer), public datasets, custom vuln apps, and CVEs. Not bug bounty data
- **Report tip line** being created for suspected data misuse/leaks
- **Bounty decrease**: re-benchmarked from top 1% (cloud hyperscalers) to top 80th percentile (high-growth tech). Biggest cuts in lows/mediums. Crits: $25K→$15K; Highs: $12.5K→$7K. Open to feedback on adding exceptional tiers
- **No pressure** from VCs/PE to monetize data

### Suggestions and Advices from Hunter
- Alex Rice: "This is the oversight on our part, is we have not gone back and made our terms clear in the world of large language models. Large language models are wildly different from classic AI."
- "I would love to see pen testing level up to the level where it actually does what everyone's promising. But put me on the far end of skeptic for full autonomous AI pen testing."
- Joseph: "If you're still in a position where you're not using AI in your bug hunting, you've got to lean in."

# CTBB Episode Analysis: Episodes 163-179
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Alex Rice (HackerOne CTO/Founder) addresses community concerns about TOS section 3.1 and AI training

#### 2. What you should learn
- Understand **researcher retains ip** — not transferred to hackerone or customer (customer gets broad license for remediation)**
- Understand **no genai training on submissions** — reporting is for spam classifiers and aggregate trends only**
- Understand **ptas agentic**: uses sidecar runs (opt-in by pentester + customer), public datasets, custom vuln apps, and cves. not bug bounty data**
- Understand **report tip line** being created for suspected data misuse/leaks**
- Understand **bounty decrease**: re-benchmarked from top 1% (cloud hyperscalers) to top 80th percentile (high-growth tech). biggest cuts in lows/mediums. crits: $25k→$15k; highs: $12.5k→$7k. open to feedback on adding exceptional tiers**

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
- *"Alex Rice: "This is the oversight on our part, is we have not gone back and made our terms clear in the world of large language models. Large language models are wildly different from classic AI."*
- *"I would love to see pen testing level up to the level where it actually does what everyone's promising. But put me on the far end of skeptic for full autonomous AI pen testing."*
- *"Joseph: "If you're still in a position where you're not using AI in your bug hunting, you've got to lean in."*

#### 6. Mental models
- **Alex Rice: "This is the oversight on our part, is we have no** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I would love to see pen testing level up to the level where ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Joseph: "If you're still in a position where you're not usin** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Researcher retains IP** — not transferred to HackerOne or customer (customer gets broad license for remediation)
- **Try this:** No GenAI training on submissions** — reporting is for spam classifiers and aggregate trends only
- **Try this:** PTAS Agentic**: uses sidecar runs (opt-in by pentester + customer), public datasets, custom vuln apps, and CVEs. Not bug bounty data
- **Try this:** Report tip line** being created for suspected data misuse/leaks

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **agent** — AI system that can use tools and make decisions autonomously
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Alex Rice (HackerOne CTO/Founder) addresses community concerns about TOS section**
2. **Researcher retains IP** — not transferred to HackerOne or customer (customer get**
3. **No GenAI training on submissions** — reporting is for spam classifiers and aggre**
