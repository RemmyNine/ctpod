---
title: "MCP Hacking Guide"
episode: 148
---


# Episode 148 MCP Hacking Guide

### TL;DR
- Justin solo episode covering Model Context Protocol (MCP) architecture, auth, initialization, and attack surface
- MCP communication over JSON-RPC via stdin, streamable HTTP, or SSE
- Malicious server can inject instructions into the client's system prompt via the `instructions` field in initialization response
- `resources/templates` is almost certainly vulnerable to path traversal
- Tools have multiple ambiguous naming fields (name, title, annotation title) enabling tool hijacking

### Bugs and Findings

#### MCP Tool Name Confusion — Tool Hijacking
- **Target/context:** MCP protocol clients/servers
- **Root cause:** Tool object schema has name, title, and annotation.title — three places to name a tool; namespace specification is unclear
- **Technique / how found:** Reading MCP spec and implementing malicious server
- **Exploitation steps:**
  1. Name tool benign in title field ("Justin's Cool Tool")
  2. Set name to something malicious ("always_use_me")
  3. LLM selects based on displayed title, back-end invokes based on name
  4. Namespace collisions possible if tool name contains `__` (double underscore)
- **Impact:** Tool hijacking, tool poisoning, DOS

#### MCP Resources/templates — Arbitrary File Read
- **Target/context:** MCP protocol
- **Root cause:** Templatized resources take user parameters and construct URIs dynamically
- **Technique / how found:** Spec analysis
- **Exploitation steps:**
  1. Call `resources/templates/list` to discover templatized resources
  2. Use parameter to inject path traversal (e.g., `../../../etc/passwd`)
  3. `resources/read` returns the file content
- **Key technical details:** URI schemes: `file://`, `https://`, `git://`; GitHub specified directly in the spec
- **Impact:** Arbitrary file read, git submodule recursion attacks, symlink writes, hook-based RCE

#### MCP `instructions` Field — System Prompt Injection
- **Target/context:** MCP clients
- **Root cause:** Server's `instructions` string in initialization response may be integrated into the client's system prompt
- **Exploitation steps:**
  1. Set up malicious MCP server
  2. In initialization response, include crafted `instructions` string
  3. Instructions get absorbed into client's system prompt, influencing LLM behavior
- **Impact:** Context poisoning, tool hijacking, prompt injection delivery

### Techniques and Primitives
**Roots Enumeration** — From malicious server, send `roots/list` RPC to client to discover exposed filesystem roots

**Sampling Elicitation** — Server can request info from user; may auto-accept without prompting. Use invisible Unicode characters for UI spoofing

**Resource Response Types** — Text, image (base64), audio (base64), resource links (URI + MIME) — each with annotations; test how client renders each for XSS/other client-side vulns

### AI Takeaway
MCP is extremely juicy attack surface — especially `resources/templates` (guaranteed path traversal), ambiguous tool naming, and the `instructions` system prompt injection. The spec directly mentioning `git://` as a supported scheme is an open invitation for supply-chain attacks.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Justin solo episode covering Model Context Protocol (MCP) architecture, auth, initialization, and attack surface

#### 2. What you should learn
- Learn about **justin solo episode covering model context protocol (mcp) architecture, auth, initialization, and attack surface**
- Learn about **mcp communication over json-rpc via stdin, streamable http, or sse**
- Learn about **malicious server can inject instructions into the client's system prompt via the `instructions` field in initialization response**
- Learn about **`resources/templates` is almost certainly vulnerable to path traversal**
- Learn about **tools have multiple ambiguous naming fields (name, title, annotation title) enabling tool hijacking**

#### 3. Core concepts explained
**MCP Tool Name Confusion — Tool Hijacking**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**MCP Resources/templates — Arbitrary File Read**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**MCP `instructions` Field — System Prompt Injection**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in MCP Tool Name Confusion — Tool Hijacking?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Justin solo episode covering Model Context Protocol (MCP) architecture, auth, in**
