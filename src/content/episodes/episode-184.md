---
title: "750+ Bugs in 2026 with 0xMoose (Ads Dawson)"
episode: 184
---



# Episode 184 750+ Bugs in 2026 with 0xMoose (Ads Dawson)

**Guests/Hosts:** Justin Gardner, Joseph Thacker, Ads Dawson (0xMoose)  

### TL;DR
- Special guest Ads Dawson (0xMoose) reveals how he submitted over 750 valid vulnerability reports in 2026 using custom Hackbot automation and agentic workflows.
- Hackbot mechanics & multi-model distribution: routing specific task types to smaller, fast, cost-effective models while reserving frontier models for complex reasoning.
- Using Claude Code for Bug Bounty: finding vulnerability patterns rapidly with LLMs while enforcing strict manual PoC validation to maintain report quality.
- Sitting in the bottleneck: how AI shifts the hunter's primary role from manual scanner to operator, filter, and orchestrator of automated pipelines.
- Meta Bug Bounty's "FBDL Goes Agentic": how Meta uses AI agents to dynamically generate isolated test environments for security researchers.
- "Signal Over Noise": strategies for noise reduction, operator moats, and hill-climbing algorithms in automated vulnerability discovery pipelines.

### Key Takeaways
- [ ] Build modular, specialized Hackbots with multi-model architectures — assign low-cost local models to routine tasks and frontier models to reasoning.
- [ ] Combine Claude Code CLI with proxy tools (Caido/Burp) for rapid traffic analysis, but ALWAYS manually verify PoCs before reporting.
- [ ] Manage Hackbot tech debt aggressively: refactor stale context pipelines, prune outdated rules, and log clean audit trails.
- [ ] Develop an "Operator Moat": your unique target context, custom wordlists, stateful databases, and workflow orchestration that competitors cannot easily copy.
- [ ] Leverage automated environment generation tools (like Meta's FBDL) to reproduce complex multi-tenant vulnerability states quickly.

### Techniques and Primitives
- **Multi-Model Hackbot Load Distribution** — Routing task types (JS parsing, subdomains, endpoint extraction) to cheap models, reserving frontier LLMs for logic bugs
- **Operator Moat Architecture** — Combining custom wordlists, stateful context databases, and proprietary agent prompts into an un-clonable competitive edge
- **Hill-Climbing Payload Mutation** — Using feedback loops from HTTP response status codes and body changes to iteratively refine exploit payloads automatically
- **Claude Code Proxy Integration** — Integrating Claude Code CLI directly with proxy logs (Caido/Burp) for inline traffic analysis and payload generation
- **Agentic Test Environment Provisioning** — Automatically spinning up isolated containerized test environments modeled after target web stacks for safe exploit verification

### Bugs and Findings

#### Multi-Tenant SaaS — Mass Auth Bypass Discovered via 0xMoose Hackbot
- **Target/context:** Global enterprise SaaS platform with hundreds of microservices
- **Root cause:** Inconsistent JWT signature validation across newly deployed internal microservice routing layers
- **Technique:** Hackbot automatically mapped 500+ microservice endpoints → identified 12 endpoints omitting signature verification → generated validated proof of concept
- **Key technical details:** Hackbot ran continuously across newly deployed subdomains, catching authorization regressions within minutes of release
- **Impact / severity / bounty:** Critical — $25,000 across multiple disclosures

#### E-Commerce Giant — Business Logic Price Manipulation via Hackbot State Machine
- **Target/context:** E-commerce platform with complex checkout flow and multi-currency conversion
- **Root cause:** State machine flaw allowed negative quantity parameters in discounted cart items during currency conversion
- **Technique:** Hackbot modeled checkout state machine → systematically fuzzed state transitions → discovered currency rounding & negative item quantity bypass
- **Key technical details:** Discovered by 0xMoose's stateful logic agent after exploring over 10,000 transaction combinations
- **Impact / severity / bounty:** High — $8,500

#### Meta Bug Bounty — Agentic FBDL Environment Exploit Validation
- **Target/context:** Meta GraphQL & Developer Platform APIs
- **Root cause:** Complex permission inheritance flaw in multi-user test organization accounts
- **Technique:** Used Meta's agentic test environment tool to generate complex Org/Team structures → fuzzed permission edges with Claude Code CLI
- **Key technical details:** Reproduced multi-tenant permission bypass in under 15 minutes using automated test environment provisioning
- **Impact / severity / bounty:** Critical — $15,000

### Tooling and Resources
- **0xMoose Substack (Signal Over Noise)** — Deep dive into AI agents and operator moats (`0xmoose.substack.com/p/signal-over-noise-ai-agents-and-the`)
- **Claude Code for Bug Bounty** — YesWeHack guide on using Claude Code CLI in bug bounty (`yeswehack.com/learn-bug-bounty/llm-series-claude`)
- **Meta FBDL Goes Agentic** — Meta Bug Bounty blog on agentic test environment generation (`bugbounty.meta.com/blog/fbdl-goes-agentic/`)
- **Hackbot Multi-Model Framework** — Multi-model orchestrator architecture using Claude Code, Caido, and Python worker swarms

### Suggestions and Advices from Hunter
- "Don't try to make one model do everything. Route cheap tasks to small local models and save frontier models for complex reasoning." — Ads Dawson (0xMoose)
- "The bottleneck isn't finding potential bugs — it's signal over noise. Your moat is how well you filter out false positives." — 0xMoose
- "AI lets you scale your output 10x, but manual validation is what keeps your signal rate high and reputation intact." — Ads Dawson
- "Fix your tech debt in your hackbot before building new features. A clean context pipeline is better than 50 hacky scripts." — Critical Thinking Podcast

---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Ads Dawson (0xMoose) shares how submitting 750+ bugs in 2026 requires multi-model Hackbot architectures, Claude Code integration, and building a defensible operator moat through noise reduction.

#### 2. What you should learn
- Understand **[ ] build multi-model Hackbot architectures: assign small models to routine scans and frontier LLMs to complex reasoning**
- Understand **[ ] use Claude Code CLI alongside proxy tools (Caido/Burp) for rapid traffic analysis and payload generation**
- Understand **[ ] focus on noise reduction and signal quality — manual validation of AI-discovered candidates is critical**
- Understand **[ ] create an Operator Moat: combine proprietary wordlists, stateful context stores, and workflow orchestration**
- Understand **[ ] apply hill-climbing algorithms to iterate exploit payloads based on HTTP response feedback loops**

#### 3. Core concepts explained
**Multi-Model Hackbot Load Distribution**
- An architectural pattern where different AI models handle different pipeline stages based on cost and capability: open-source/small models parse JS and extract endpoints; mid-tier models run initial pattern matches; frontier models (Claude/GPT) perform deep logic analysis.

**The Operator Moat**
- The competitive advantage held by an AI automation operator that cannot be easily replicated by others simply running standard LLMs. Built from proprietary target history, custom wordlists, tailored prompt strategies, stateful databases, and manual validation speed.

**Hill-Climbing Payload Mutation**
- An automated fuzzing technique where an agent sends an initial payload, analyzes the HTTP response (status code, reflection, header changes, body delta), and iteratively modifies the payload in the direction that yields the closest match to exploitation.

**Agentic Test Environment Provisioning**
- Using AI agents to dynamically declare, build, and deploy containerized replica environments of complex web applications (e.g., Meta's FBDL), allowing researchers to test multi-tenant permission bugs without risking live production data.

**Signal Over Noise Bottleneck**
- The reality in modern AI-assisted hunting where generating candidate vulnerabilities is easy, but filtering out false positives and producing clean, reproducible PoCs is the true constraint.

#### 4. Techniques and tactics
**Multi-Model Load Distribution**
- **What it is:** Routing pipeline tasks across a gradient of models (slm/local → mid-tier → frontier LLM)
- **When to use it:** High-volume automated scanning where using frontier models everywhere would be cost-prohibitive
- **What can go wrong:** Lower-tier models dropping subtle candidates; model output schema inconsistencies

**Claude Code Proxy Analysis**
- **What it is:** Feeding proxy logs (Caido/Burp) directly into Claude Code CLI to analyze traffic patterns and suggest payloads
- **When to use it:** Active manual/semi-automated hunting sessions on complex API endpoints
- **What can go wrong:** Exceeding context limits with large HTTP bodies; hallucinations in complex auth flows

**Hill-Climbing Payload Refinement**
- **What it is:** Iteratively mutating payloads based on response feedback (e.g., SQL error changes, WAF bypass clues)
- **When to use it:** WAF bypass, filter evasion, and partial injection vectors
- **What can go wrong:** Getting stuck in local optima; triggering rate limits or WAF IP blocks

**Agentic Replica Environment Generation**
- **What it is:** Automatically instantiating complex multi-role tenant environments using agent tools
- **When to use it:** Testing access control and business logic flaws in complex multi-tenant platforms
- **What can go wrong:** Replica environment mismatching production behavior; setup overhead

#### 5. Good Quotes
- *"Don't try to make one model do everything. Route cheap tasks to small local models and save frontier models for complex reasoning."* — **Ads Dawson (0xMoose)**
- *"The bottleneck isn't finding potential bugs — it's signal over noise. Your moat is how well you filter out false positives."* — **0xMoose**
- *"AI lets you scale your output 10x, but manual validation is what keeps your signal rate high and reputation intact."* — **Ads Dawson**
- *"Fix your tech debt in your hackbot before building new features. A clean context pipeline is better than 50 hacky scripts."* — **Critical Thinking Podcast**

#### 6. Mental models
- **Cost-Gradient Automation** — Cheap compute for volume, expensive compute for intelligence
- **The Human as Validator** — AI proposes candidates at scale; human verifies and formats the signal
- **State > Stateless** — Hackbots that track target state across deployments find 10x more bugs than stateless scanners
- **Refactor before feature addition** — Technical debt in automation pipelines leads to silent failures and missed bugs

#### 7. Real-world application
- **Try this:** [ ] Set up a local small LLM (Ollama/vLLM) to extract endpoints and parameters from JS files before passing to Claude Code
- **Try this:** [ ] Connect Claude Code CLI to your Caido proxy history using custom scripts or Caido Skills
- **Try this:** [ ] Build a simple hill-climbing script that mutates WAF bypass payloads based on HTTP response body changes
- **Try this:** [ ] Create a personal target state database recording subdomains, deployed versions, and tested endpoints

#### 8. Red flags and pitfalls
- **Using frontier models for raw string parsing** — Wastes money and API quota on tasks small local models do faster
- **Submitting unverified AI candidate reports** — Destroys hunter signal rating and leads to program bans
- **Ignoring Hackbot technical debt** — Unmaintained scanner scripts break silently, missing new attack surfaces
- **Relying on stateless scanning** — Missing stateful logic bugs that require multi-step session sequences
- **Failing to build an operator moat** — Using default off-the-shelf scanner prompts means competing with thousands of identical bots

#### 9. Vocabulary
- **Hackbot** — Automated script or AI agent fleet designed to hunt for vulnerabilities continuously
- **Operator Moat** — Defensible competitive advantage in automated security testing (data, prompts, workflow)
- **Hill-Climbing** — Optimization technique that iteratively improves payloads based on response feedback
- **FBDL** — Facebook/Meta Developer Language and environment framework for automated testing
- **Signal-to-Noise Ratio** — Proportion of valid, actionable vulnerability candidates vs false positives

#### 10. Self-test
1. **Recall:** How does 0xMoose distribute workload across different model tiers in his Hackbot?
2. **Application:** Design a 3-tier model distribution architecture for an automated recon and fuzzing pipeline.
3. **Reasoning:** Why is signal-to-noise filtering the primary bottleneck in AI-assisted bug bounty?
4. **Application:** How can you integrate Claude Code CLI with proxy logs for real-time traffic analysis?
5. **Recall:** What is an "Operator Moat" and what four elements compose it?
6. **Reasoning:** Explain how hill-climbing payload mutation works in WAF bypass scenarios.
7. **Application:** Outline a daily routine for managing and refactoring technical debt in your automation tools.
8. **Reflection:** How will the ability to submit 750+ bugs/year change bug bounty program dynamics?

#### 11. The practical takeaway
1. **Submit 750+ bugs by combining automated Hackbots with strict manual PoC verification**
2. **[ ] Implement multi-model load distribution: assign cheap models to scanning and frontier models to reasoning**
3. **[ ] Integrate Claude Code CLI with your proxy workflows (Caido/Burp) for inline traffic analysis**
4. **[ ] Build an Operator Moat through stateful target databases, proprietary wordlists, and custom prompts**
5. **[ ] Focus on signal quality and noise reduction — reputation and signal rating are your primary assets**
---

### 📖 Darsnameh

**Guests:**
- **Ads Dawson** — also appears in [#184](/episodes/184)
- **Joseph Thacker** — also appears in [#184](/episodes/184)

**Bugs & Vulnerabilities:**
- **Agentic FBDL Environment Exploit Validation** — Meta Bug Bounty — Agentic FBDL Environment Exploit Validation ([search](/search?q=Agentic%20FBDL%20Environment%20Exploit%20Validation))
- **Commerce Giant — Business Logic Price Manipulation via Hackbot State Machine** — E-Commerce Giant — Business Logic Price Manipulation via Hackbot State Machine ([search](/search?q=Commerce%20Giant%20—%20Business%20Logic%20Price%20Manipulation%20via%20Hackbot%20State%20Machine))
- **Tenant SaaS — Mass Auth Bypass Discovered via 0xMoose Hackbot** — Multi-Tenant SaaS — Mass Auth Bypass Discovered via 0xMoose Hackbot ([search](/search?q=Tenant%20SaaS%20—%20Mass%20Auth%20Bypass%20Discovered%20via%200xMoose%20Hackbot))
- **test** — 10. Self-test ([search](/search?q=test))
- **world application** — 7. Real-world application ([search](/search?q=world%20application))

**Techniques:**
- **Agentic Test Environment Provisioning** — also in [#184](/episodes/184)
- **Claude Code Proxy Integration** — also in [#184](/episodes/184)
- **Hill-Climbing Payload Mutation** — also in [#184](/episodes/184)
- **Multi-Model Hackbot Load Distribution** — also in [#184](/episodes/184)
- **Operator Moat Architecture** — also in [#184](/episodes/184)

