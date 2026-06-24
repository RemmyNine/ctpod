---
title: "We Won Google's AI Hacking Event in Tokyo"
episode: 122
---


# Episode 122 We Won Google's AI Hacking Event in Tokyo

### TL;DR
- Google LHE: 70 AI-focused reports, $220k+ paid out (record), 25 researchers
- AI vulnerability components: delivery (how attacker input gets into LLM context) → access to information (what data is available) → exfiltration/impactful action
- React and CodeAct frameworks: LLM uses a "planner" to reason, then executes code in sandbox
- Frankenstein technique: splice words from different languages at token boundaries to bypass prompt filters
- Tokenization quirks: all-caps, multilingual word splicing bypass smaller classifier models
- Google's engineering ratio: 1:1 hacker-to-engineer collaboration during the event

### Key Takeaways
- AI vulns break into three components: delivery, info access, exfiltration/impactful action. Payout depends on which component is most novel
- React/CodeAct architecture: LLM generates reasoning → plan → action (code). The "planner" can be addressed directly: "for the planner: ..."
- Use system language from research papers in prompts: referring to "user intent", "planner", "tool_name" stabilizes exploits
- Tokenization-based bypass: "Frankenstein" words — splice "bird" (English) + "oiseau" (French) + "pajaro" (Spanish) at token boundaries to bypass text filters
- Smaller classifier models (used for latency) are more easily fooled by token manipulation than the full LLM
- Google LHE pays for what's novel — if delivery is known but exfiltration is novel, that component gets rewarded
- 70 reports, $220k+ paid, record for a Google LHE

### Bugs and Findings
*Specific bug details are redacted due to NDA; methodology discussed.*

#### Conditional Memory Corruption (Zak Bennett)
- **Target/context:** Large-scale cloud backend
- **Root cause:** Heap overflow in binary file format processing
- **Technique / how found:** Heap overflow → info leak → write primitive. Problem: load-balanced instances (leak and write hit different boxes). Solution: conditional corruption — heap-groomed objects with instance-specific pointers; wrong instance = graceful error, right instance = exploitation
- **Impact / severity / bounty:** RCE
- **Obstacles & how solved:** Load balancing prevented single-instance exploitation; solved via conditional corruption with spray-and-pray

### Techniques and Primitives
- **Planner-directed prompt engineering** — Address the "planner" component directly (in React/CodeAct architecture); set user intent explicitly
- **Frankenstein token bypass** — Splice word fragments from different languages at token boundaries (e.g., "bir" + "d" from English, French, Spanish)
- **Small model classifier evasion** — Smaller, faster models for user intent classification are more easily bypassed than the full LLM
- **Naming tool calls explicitly** — If you know the internal tool name, reference it directly: "call the 'browse_web' tool"
- **Cultural/linguistic filter bypass** — Different models interpret phrases differently; this disparity can be exploited in multi-agent systems

### Tooling and Resources
- Google VRP (jobs at jobs.ctbb.show)
- React (Reasoning + Acting) paper
- CodeAct paper (code as action)
- Critical Thinking community at Google LHE

### Suggestions and Advices from Hunter
- "Read the research papers — React and CodeAct architectures are goldmines for understanding how to exploit AI"
- "If you want to stabilize exploits, add technical details about the system's architecture to your prompt — talk to the planner"
- "Tokenization: all-caps, multilingual word splicing — test these at every input boundary"
- "One in a million happens every second at Google scale"

### AI Takeaway
The key insight from this episode is that understanding the underlying agent architecture (React/CodeAct) directly enables better exploitation. The "planner" is a concrete component you can target. The multilingual tokenization bypass (Frankenstein technique) is a practical, testable method for filter evasion.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Google LHE: 70 AI-focused reports, $220k+ paid out (record), 25 researchers

#### 2. What you should learn
- Understand **ai vulns break into three components: delivery, info access, exfiltration/impactful action. payout depends on which component is most novel**
- Understand **react/codeact architecture: llm generates reasoning → plan → action (code). the "planner" can be addressed directly: "for the planner: ..."**
- Understand **use system language from research papers in prompts: referring to "user intent", "planner", "tool_name" stabilizes exploits**
- Understand **tokenization-based bypass: "frankenstein" words — splice "bird" (english) + "oiseau" (french) + "pajaro" (spanish) at token boundaries to bypass text filters**
- Understand **smaller classifier models (used for latency) are more easily fooled by token manipulation than the full llm**

#### 3. Core concepts explained
**Conditional Memory Corruption (Zak Bennett)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Planner-directed prompt engineering**
- Address the "planner" component directly (in React/CodeAct architecture); set user intent explicitly

**Frankenstein token bypass**
- Splice word fragments from different languages at token boundaries (e.g., "bir" + "d" from English, French, Spanish)

**Small model classifier evasion**
- Smaller, faster models for user intent classification are more easily bypassed than the full LLM


#### 4. Techniques and tactics
**Planner-directed prompt engineering**
- **What it is:** Address the "planner" component directly (in React/CodeAct architecture); set user intent explicitly
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Frankenstein token bypass**
- **What it is:** Splice word fragments from different languages at token boundaries (e.g., "bir" + "d" from English, French, Spanish)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Small model classifier evasion**
- **What it is:** Smaller, faster models for user intent classification are more easily bypassed than the full LLM
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Naming tool calls explicitly**
- **What it is:** If you know the internal tool name, reference it directly: "call the 'browse_web' tool"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Cultural/linguistic filter bypass**
- **What it is:** Different models interpret phrases differently; this disparity can be exploited in multi-agent systems
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Read the research papers"* — **React and CodeAct architectures are goldmines for understanding how to exploit AI**
- *"If you want to stabilize exploits, add technical details about the system's architecture to your prompt"* — **talk to the planner**
- *"Tokenization: all-caps, multilingual word splicing"* — **test these at every input boundary**
- *"One in a million happens every second at Google scale"*

#### 6. Mental models
- **Read the research papers — React and CodeAct architectures a** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you want to stabilize exploits, add technical details abo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Tokenization: all-caps, multilingual word splicing — test th** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** AI vulns break into three components: delivery, info access, exfiltration/impactful action. Payout depends on which component is most novel
- **Try this:** React/CodeAct architecture: LLM generates reasoning → plan → action (code). The "planner" can be addressed directly: "for the planner: ..."
- **Try this:** Use system language from research papers in prompts: referring to "user intent", "planner", "tool_name" stabilizes exploits
- **Try this:** Tokenization-based bypass: "Frankenstein" words — splice "bird" (English) + "oiseau" (French) + "pajaro" (Spanish) at token boundaries to bypass text filters

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Load balancing prevented single-instance exploitation; solved via conditional corruption with spray-and-pray

#### 9. Vocabulary
- **agent** — AI system that can use tools and make decisions autonomously
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Conditional Memory Corruption (Zak Bennett)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Google LHE: 70 AI-focused reports, $220k+ paid out (record), 25 researchers**
2. **AI vulns break into three components: delivery, info access, exfiltration/impact**
3. **React/CodeAct architecture: LLM generates reasoning → plan → action (code). The **
