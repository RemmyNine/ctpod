---
title: "PortSwigger Research Impossible XSS SOLVED"
episode: 183
---



# Episode 183 PortSwigger Research Impossible XSS SOLVED

### TL;DR
- PortSwigger Research's "Unexploitable / Impossible XSS Labs" solved: dissecting complex DOM manipulation, parser differentials, and edge-case execution vectors.
- Demystifying AI security: AI features are just standard web tech features under the hood — analyze them using classic input validation, access control, and state management techniques.
- $15,000 finding breakdown: Client-Side Path Traversal (CSPT) escalated to full Account Takeover (ATO), followed by 2FA bypass via prototype pollution.
- Chrome & Firefox Sanitizer API bypasses: SL Cyber research reveals DOM mutation and parser differential flaws in modern browser sanitizers.
- GitLost vulnerability: how researchers tricked GitHub's AI Agent (Copilot) into leaking private repository code and credentials via cross-repo prompt context injection.
- Chaining Razor SSTI into Remote Code Execution (RCE) via C# reflection (`System.Reflection`) and runtime string concatenation.

### Key Takeaways
- [ ] Treat AI features as standard web tech — audit input boundaries, API payloads, state transitions, and authorization checks.
- [ ] Chain Client-Side Path Traversal (CSPT) with prototype pollution to hijack application state and bypass multi-factor authentication.
- [ ] Test HTML sanitizer implementations against nested elements, custom tags, and browser DOM mutation parser differentials.
- [ ] Audit AI agent context boundaries to prevent prompt injection attacks that exfiltrate private organization repositories (GitLost pattern).
- [ ] Use C# reflection (`System.Type.GetType`, `GetMethod`, `Invoke`) to bypass Razor SSTI filters when direct process execution is blocked.

### Techniques and Primitives
- **CSPT to ATO Chaining** — Using client-side path traversal to fetch attacker-controlled JSON responses, overwrite client state, and steal auth tokens
- **Prototype Chain 2FA Bypass** — Polluting `Object.prototype` properties (e.g., `is_2fa_verified`) to bypass client-side two-factor checks
- **Browser Sanitizer API Bypass** — Exploiting parser differentials and DOM mutations in native browser HTML sanitizers (Chrome/Firefox)
- **AI Agent Context Leakage (GitLost)** — Injecting prompt payloads into public repos to force AI agents to output indexed private code snippets
- **Razor SSTI Reflection RCE** — Constructing C# reflection calls with dynamic string concatenation to bypass Razor template sandbox restrictions

### Bugs and Findings

#### Fintech Web App — $15k CSPT to Account Takeover & 2FA Bypass
- **Target/context:** Major financial management platform with multi-factor authentication
- **Root cause:** Unsanitized URL path parameter allowed Client-Side Path Traversal (CSPT) combined with prototype pollution vulnerability in state parser
- **Technique:** CSPT forced client to fetch attacker payload → payload triggered prototype pollution → overridden `is_2fa_verified` property in JavaScript auth state
- **Key technical details:** Chained 3 distinct client-side vulnerabilities (CSPT, prototype pollution, logic flaw) into a full 2FA bypass and account takeover
- **Impact / severity / bounty:** Critical — $15,000

#### GitHub AI Agent — GitLost Private Repository Exfiltration
- **Target/context:** GitHub AI Agent / Copilot Workspace integration
- **Root cause:** Insufficient context isolation between public repository prompts and indexed private organization repositories
- **Technique:** Prompt injection payload in public repository requested code completion referencing private organization namespace → AI agent returned confidential source code and credentials
- **Key technical details:** Exploited cross-repository context indexing in AI agents that failed to enforce repository-level authorization boundaries
- **Impact / severity / bounty:** Critical — Private code & credential leakage

#### Enterprise .NET Application — Razor SSTI to RCE via Reflection
- **Target/context:** Custom enterprise CMS built on ASP.NET Core Razor Pages
- **Root cause:** User-controlled template input evaluated by Razor engine with restricted execution context
- **Technique:** Used C# reflection (`System.Type.GetType`, `GetMethod`, `Invoke`) to dynamically load `System.Diagnostics.Process` and execute shell commands
- **Key technical details:** Bypassed Razor static analysis filters by building type names dynamically using runtime string concatenation (`"Sys" + "tem.Diag" + ...`)
- **Impact / severity / bounty:** Critical — Remote Code Execution (RCE)

### Tooling and Resources
- **CSPT to ATO Writeup** — Full writeup on CSPT escalation to ATO and 2FA bypass (`whoareme.com/blog/cspt-account-takeover-2fa-bypass/`)
- **Chrome Sanitizer API Bypasses** — SL Cyber research paper (`slcyber.io/research-center/two-bypasses-for-chromes-sanitizer-api/`)
- **PortSwigger Unexploitable XSS Labs** — PortSwigger Research documentation (`portswigger.net/research/documenting-the-impossible-unexploitable-xss-labs`)
- **GitLost GitHub AI Agent Leak** — Noma Security vulnerability disclosure (`noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/`)
- **Razor SSTI to RCE Guide** — Reflection techniques in C# Razor SSTI (`phsi.se/posts/chaining-razor-ssti-into-rce-via-reflection-and-runtime-strings/`)
- **YesWeHack LLM Series** — Interviews on LLMs in bug bounty with Aituglo, Rhynorater, and iCare (`yeswehack.com/learn-bug-bounty/`)

### Suggestions and Advices from Hunter
- "Stop treating AI features as magic black boxes. Look at the inputs, outputs, and underlying APIs just like any web feature." — Justin Gardner
- "Client-Side Path Traversal is heavily underrated. When combined with prototype pollution, it consistently turns into account takeover." — Bug Bounty Hunter
- "Always test HTML sanitizer APIs with complex nested tags and DOM mutations — browsers still differ in how they parse edge cases." — SL Cyber Researcher
- "In C# SSTI, reflection is your best friend when direct process invocation (`Process.Start`) is filtered." — Security Researcher

---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Solving PortSwigger's impossible XSS labs, chaining Client-Side Path Traversal into 2FA bypasses, and leaking private repos through AI agents demonstrate that advanced vulnerabilities rely on mastering client-side state and execution primitives.

#### 2. What you should learn
- Understand **[ ] demystify AI features: test them using standard input validation, access control, and API testing techniques**
- Understand **[ ] chain Client-Side Path Traversal (CSPT) with prototype pollution to achieve full 2FA bypass and account takeover**
- Understand **[ ] bypass browser HTML Sanitizer APIs using DOM mutation differentials and nested element parsing bugs**
- Understand **[ ] test AI agents for cross-context data leaks (GitLost pattern) where public prompts extract private workspace data**
- Understand **[ ] construct C# reflection chains to escalate Razor SSTI to full RCE when static string filters are present**

#### 3. Core concepts explained
**Client-Side Path Traversal (CSPT)**
- A vulnerability where user-supplied input alters client-side URL paths in `fetch()` or `XMLHttpRequest` calls, allowing attackers to manipulate API endpoints fetched by the user's browser.

**Prototype Chain Exploitation**
- Modifying `Object.prototype` in JavaScript environments to inject default property values across all objects in application memory, breaking logic checks like `if (user.is_2fa_verified)`.

**Sanitizer API DOM Mutations**
- Browser bugs where native HTML sanitizers parse HTML strings into DOM elements, but re-serialization or DOM insertion causes unexpected mutation, triggering execution of sanitized scripts.

**Cross-Context AI Prompt Exfiltration (GitLost)**
- A flaw in multi-repo AI agent architectures where prompt context from an unprivileged domain causes the agent to pull from index stores belonging to private or restricted repositories.

**Reflection-Based SSTI Escalation**
- Using language introspection capabilities (`System.Reflection` in .NET) to discover and invoke restricted types and methods dynamically, bypassing static code filters in template engines.

#### 4. Techniques and tactics
**CSPT to Account Takeover Chaining**
- **What it is:** Using path traversal in client-side fetch calls to route API requests to attacker-controlled endpoints or unexpected local endpoints
- **When to use it:** When client apps dynamically build API URLs using route parameters or hash fragments
- **What can go wrong:** CORS policies blocking cross-origin fetch; target API validating endpoint paths strictly

**Prototype Pollution 2FA Bypass**
- **What it is:** Polluting `Object.prototype` to set default authorization flags across client-side state models
- **When to use it:** When client JavaScript relies on uninitialized object properties for security checks
- **What can go wrong:** Application crashing due to corrupted object properties; strict property initialization overwriting polluted values

**AI Agent Cross-Repo Context Injection**
- **What it is:** Crafting prompts in public repositories to trick AI agents into referencing private organization data
- **When to use it:** Auditing AI code assistants, automated PR reviewers, and enterprise workspace LLM integrations
- **What can go wrong:** Agent safety filters blocking output; prompt context window truncation

**C# Reflection SSTI Payload Construction**
- **What it is:** Building C# reflection strings dynamically to instantiate `Process` or `Assembly` objects in Razor templates
- **When to use it:** When direct instantiation of `System.Diagnostics.Process` is blocked by WAF or template sandbox
- **What can go wrong:** Medium trust execution environments restricting reflection access; syntax errors in dynamic type resolution

#### 5. Good Quotes
- *"Stop treating AI features as magic black boxes. Look at the inputs, outputs, and underlying APIs just like any web feature."* — **Justin Gardner**
- *"Client-Side Path Traversal is heavily underrated. When combined with prototype pollution, it consistently turns into account takeover."* — **Bug Bounty Hunter**
- *"Always test HTML sanitizer APIs with complex nested tags and DOM mutations — browsers still differ in how they parse edge cases."* — **SL Cyber Researcher**
- *"In C# SSTI, reflection is your best friend when direct process invocation (`Process.Start`) is filtered."* — **Security Researcher**

#### 6. Mental models
- **AI features are web features** — Strip away the "AI" hype and analyze endpoints, inputs, outputs, and auth tokens
- **Primitives compound exponentially** — CSPT alone = Low/Medium; CSPT + Prototype Pollution = Critical ATO
- **Parsers lie, serializers mutate** — Sanitizing HTML string → DOM tree → serialized string often introduces execution windows
- **Reflection bypasses static filters** — If you can't type a class name directly, construct it at runtime character by character

#### 7. Real-world application
- **Try this:** [ ] Intercept client-side API requests and test if URL path parameters permit `../` traversal to alter destination endpoints
- **Try this:** [ ] Audit JavaScript libraries for prototype pollution entry points using query params, URL fragments, or JSON inputs
- **Try this:** [ ] Test AI code assistants by creating public repos that prompt for internal organization code structures and secret key formats
- **Try this:** [ ] Practice building dynamic C# reflection strings in local Razor template environments to bypass string filters

#### 8. Red flags and pitfalls
- **Ignoring client-side path parameters** — Assuming fetch path parameters can't be manipulated because they are client-side
- **Treating prototype pollution as theoretical** — Failing to check if polluted properties flow into auth logic or state checkers
- **Relying solely on native sanitizer APIs** — Assuming browser `Sanitizer()` is immune to parser differential bugs
- **Overlooking cross-repo AI indexing** — Assuming AI agents enforce organization repository permissions in context retrieval
- **Using hardcoded type names in SSTI PoCs** — Easily blocked by WAFs; use reflection and string concatenation instead

#### 9. Vocabulary
- **CSPT** — Client-Side Path Traversal: manipulating client-side fetch paths via user input
- **Prototype Pollution** — Injecting properties into `Object.prototype` in JavaScript environments
- **GitLost** — Vulnerability pattern where AI agents leak private repository code via public prompts
- **Razor SSTI** — Server-Side Template Injection in ASP.NET Razor template engine
- **Reflection** — Programming capability to inspect and invoke types, methods, and properties at runtime

#### 10. Self-test
1. **Recall:** What is Client-Side Path Traversal (CSPT) and how does it differ from Server-Side Path Traversal?
2. **Application:** How can prototype pollution be leveraged to bypass a client-side 2FA check?
3. **Reasoning:** Why do native browser Sanitizer APIs still suffer from XSS bypasses?
4. **Application:** Write a conceptual prompt injection payload designed to test if an AI agent has access to private repo context.
5. **Recall:** What C# reflection methods are used to instantiate objects dynamically in Razor SSTI?
6. **Reasoning:** Why is treating AI features as standard web features an effective testing strategy?
7. **Application:** Outline the steps to chain CSPT + Prototype Pollution into a full account takeover.
8. **Reflection:** What client-side vulnerability primitives are currently most neglected in your testing routine?

#### 11. The practical takeaway
1. **Treat AI integration points as standard web features — test inputs, APIs, and access boundaries**
2. **[ ] Audit client-side fetch calls for CSPT and pair with prototype pollution for account takeover impact**
3. **[ ] Test browser Sanitizer APIs with nested HTML and DOM mutations for parser differential bypasses**
4. **[ ] Audit AI agent context bounds to prevent prompt injection leaks of private organization code (GitLost)**
5. **[ ] Use C# reflection and runtime string building to escalate Razor SSTI to RCE when filters exist**
---

### 📖 Darsnameh

**Bugs & Vulnerabilities:**
- **$15k CSPT to Account Takeover & 2FA Bypass** — Fintech Web App — $15k CSPT to Account Takeover & 2FA Bypass ([search](/search?q=$15k%20CSPT%20to%20Account%20Takeover%20&%202FA%20Bypass))
- **GitLost Private Repository Exfiltration** — GitHub AI Agent — GitLost Private Repository Exfiltration ([search](/search?q=GitLost%20Private%20Repository%20Exfiltration))
- **Razor SSTI to RCE via Reflection** — Enterprise .NET Application — Razor SSTI to RCE via Reflection ([search](/search?q=Razor%20SSTI%20to%20RCE%20via%20Reflection))
- **test** — 10. Self-test ([search](/search?q=test))
- **world application** — 7. Real-world application ([search](/search?q=world%20application))

**Techniques:**
- **AI Agent Context Leakage (GitLost)** — also in [#183](/episodes/183)
- **Browser Sanitizer API Bypass** — also in [#183](/episodes/183)
- **CSPT to ATO Chaining** — also in [#183](/episodes/183)
- **Prototype Chain 2FA Bypass** — also in [#183](/episodes/183)
- **Razor SSTI Reflection RCE** — also in [#183](/episodes/183)

