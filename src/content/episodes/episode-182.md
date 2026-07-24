---
title: "Partial Auth, Hackbot GraphQL, and AI's #1 Mission"
episode: 182
---



# Episode 182 Partial Auth, Hackbot GraphQL, and AI's #1 Mission

### TL;DR
- WPM (Web Payment Manager / Web Performance Monitoring) integration analysis reveals how historical Wayback Machine data exposes guest Bearer tokens and partial auth bypasses.
- AI-driven Hackbots are transforming GraphQL security testing: discovering hidden introspection endpoints, unlinked mutation fields, and stateful authorization flaws.
- AI's #1 Mission in bug bounty is context enrichment, noise reduction, and state tracking — acting as a force multiplier for hunters rather than a unguided scanner.
- Model Context Protocol (MCP) adoption is standardizing tool interfaces for AI agents, connecting proxies, scanners, and custom scripts into unified execution environments.
- Industry updates highlight YesWeHack's "ChocoPoCs" advisory (trojanised exploits targeting security researchers) and HackerOne's findings on managing AI-driven report volumes.

### Key Takeaways
- [ ] Audit historical Wayback Machine snapshots for leaked Bearer tokens, internal endpoints, and legacy partial-auth mechanisms.
- [ ] Implement Model Context Protocol (MCP) servers for your security tools (Caido, Burp, custom scripts) to enable seamless AI agent orchestration.
- [ ] Use AI Hackbots to discover hidden GraphQL schema paths (e.g., `/graphql-beta`, `/internal/graphql`) and unlinked mutations.
- [ ] Never execute unverified public exploit PoCs on host machines — trojanised payloads ("ChocoPoCs") actively target researchers.
- [ ] Focus AI agent development on context store persistence and signal-to-noise filtering rather than mass unverified scanning.

### Techniques and Primitives
- **Wayback Bearer Token Extraction** — Searching archived HTTP requests and JS bundles for leftover guest tokens or partial auth headers with elevated scope
- **Partial Auth Bypass via Legacy Endpoints** — Replaying guest/onboarding Bearer tokens against modern API endpoints that lack tenant isolation checks
- **GraphQL Hackbot Schema Enumeration** — Automating GraphQL introspection discovery using LLM-guided path fuzzing and query batching
- **Model Context Protocol (MCP) Security Tooling** — Wrapping security proxy interfaces and tools into standardized MCP schemas for direct agent control
- **AI Execution Sandbox Security** — Auditing permission boundaries, prompt boundaries, and tool invocation hooks in autonomous AI security agents

### Bugs and Findings

#### WPM Guest Flow — Partial Auth Token Exposure via Wayback
- **Target/context:** Enterprise E-commerce platform with Web Payment Manager integration
- **Root cause:** Legacy JavaScript bundles archived in Wayback Machine contained hardcoded guest Bearer tokens with elevated API privileges
- **Technique:** Archived asset analysis → extracted Bearer token from legacy client bundle → replayed token against modern backend APIs
- **Key technical details:** The guest Bearer token allowed read/write access to partial user profiles and unfulfilled checkout sessions across multi-tenant stores
- **Impact / severity / bounty:** High — $4,500

#### Enterprise SaaS — Hidden GraphQL Schema Discovered via Hackbot
- **Target/context:** Global SaaS platform with restricted main GraphQL endpoint
- **Root cause:** Introspection disabled on main `/graphql` route, but active on an unlinked `/api/v2/graphql-beta` staging endpoint discovered by an AI Hackbot
- **Technique:** AI Hackbot fuzzed endpoint paths and subdomains → identified active introspection on beta path → auto-generated schema graph and mutation payloads
- **Key technical details:** Introspection revealed unpublished administrative mutations for user role modification and internal billing queries
- **Impact / severity / bounty:** Critical — $10,000

#### Vulnerability Research — Trojanised Exploit PoC (ChocoPoC)
- **Target/context:** Public GitHub repositories offering 0-day / 1-day proof of concept exploit code
- **Root cause:** Threat actors publishing fake vulnerability exploits containing obfuscated reverse shells designed to compromise security researchers
- **Technique:** Static code analysis and sandbox detonation of public PoC scripts revealed hidden payload execution during build/compile phase
- **Key technical details:** Exploit script dropped persistent backdoor upon execution; researchers warned via YesWeHack advisory
- **Impact / severity / bounty:** Critical — Supply chain risk & researcher safety

### Tooling and Resources
- **Caido Skills Framework** — Extension interface and agent skills for Caido proxy (`github.com/caido/skills/pull/22`)
- **AWS Cognito Misconfiguration Guide** — Yassine Aboukir's guide on Cognito security (`yassineaboukir.com/talks/NahamConEU2022.pdf`)
- **X MCP Protocol Integration** — Official MCP documentation for X integration (`docs.x.com/tools/mcp`)
- **HackerOne US South Summer Sessions** — Community hacker event (`h1.community/events/...`)
- **YesWeHack ChocoPoCs Advisory** — Research on trojanised exploits targeting researchers (`yeswehack.com/fr/news/chocopocs...`)

### Suggestions and Advices from Hunter
- "Wayback Machine is a goldmine for forgotten authorization headers. Always grep historical JS bundles for guest Bearer tokens." — Security Researcher
- "The true mission of AI in bug bounty is context enrichment and noise reduction — not generating 500 low-quality unverified reports." — Critical Thinking Podcast
- "Never execute public PoCs directly on your host machine. Trojanised exploits (ChocoPoCs) are actively targeting hunters." — YesWeHack Researcher
- "Standardize your tools with Model Context Protocol (MCP). It makes connecting AI agents to your proxy and scanners effortless." — Hunter

---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Historical Wayback data combined with AI-driven GraphQL Hackbots and standardized Model Context Protocol (MCP) tooling are redefining how hunters discover partial auth bypasses and navigate AI security boundaries.

#### 2. What you should learn
- Understand **[ ] extract guest Bearer tokens from historical Wayback JS bundles to test for partial auth bypasses**
- Understand **[ ] build Model Context Protocol (MCP) servers to give AI agents structured control over security proxies**
- Understand **[ ] deploy AI Hackbots to discover unlinked GraphQL introspection endpoints and hidden mutations**
- Understand **[ ] audit public exploit PoCs in isolated sandboxes to protect against trojanised payloads (ChocoPoCs)**
- Understand **[ ] orient AI security tooling toward context persistence and noise reduction as its core mission**

#### 3. Core concepts explained
**Partial Auth Bypass**
- A state where an application grants limited authentication (e.g., guest tokens, checkout tokens, onboarding tokens) but fails to enforce proper authorization checks when those tokens access full API endpoints.

**Wayback Asset Mining**
- Systematic extraction and analysis of historical JavaScript bundles, API definitions, and HTTP requests archived by Wayback Machine to find forgotten endpoints, hardcoded credentials, and legacy token formats.

**Model Context Protocol (MCP) in Security**
- An open standard protocol that allows AI models to interact securely with external tools and data sources. In security context, MCP enables AI agents to query proxies (Caido/Burp), run scanners, and parse response bodies through a uniform API.

**GraphQL Hackbot Schema Mining**
- Using LLM-powered autonomous scripts to fuzz API path structures, detect non-standard GraphQL paths (`/graphql-beta`, `/v2/gql`), extract introspection schemas, and automatically construct valid test queries.

**ChocoPoCs (Trojanised Exploits)**
- Malicious exploit PoCs uploaded to public repositories that pretend to offer zero-day or N-day exploits, but actually execute backdoors or credential stealers against the researcher running them.

#### 4. Techniques and tactics
**Wayback Bearer Token Extraction**
- **What it is:** Searching archived HTTP requests and JS bundles for leftover guest tokens or partial auth headers
- **When to use it:** Target recon on legacy web applications and e-commerce platforms with long version histories
- **What can go wrong:** Extracted tokens may be expired or revoked; verify scope against non-destructive endpoints first

**GraphQL Hackbot Path Fuzzing**
- **What it is:** Automating discovery of secondary GraphQL endpoints where introspection remains enabled
- **When to use it:** When primary `/graphql` endpoint has introspection disabled or rate-limited
- **What can go wrong:** WAF rate limiting; false positives from generic 200 OK responses

**MCP Security Tool Integration**
- **What it is:** Wrapping local proxy APIs (Caido, Burp REST API) in MCP server schemas for LLM agent interaction
- **When to use it:** Building autonomous or semi-autonomous hunting assistants
- **What can go wrong:** Latency in tool calls; agent hallucination of tool parameters if schema is poorly defined

**Exploit Sandbox Detonation**
- **What it is:** Running public PoC code in isolated ephemeral containers with outbound network monitoring
- **When to use it:** Whenever testing third-party exploit code from GitHub or forums
- **What can go wrong:** Sandbox escape vulnerabilities in container runtimes; container environment lacking necessary dependencies

#### 5. Good Quotes
- *"Wayback Machine is a goldmine for forgotten authorization headers. Always grep historical JS bundles for guest Bearer tokens."* — **Security Researcher**
- *"The true mission of AI in bug bounty is context enrichment and noise reduction — not generating 500 low-quality unverified reports."* — **Critical Thinking Podcast**
- *"Never execute public PoCs directly on your host machine. Trojanised exploits (ChocoPoCs) are actively targeting hunters."* — **YesWeHack Researcher**
- *"Standardize your tools with Model Context Protocol (MCP). It makes connecting AI agents to your proxy and scanners effortless."* — **Hunter**

#### 6. Mental models
- **Legacy code never truly dies** — If an endpoint or token format existed in 2021, backend microservices may still honor it today
- **AI as Context Manager > AI as Scanner** — AI excels at holding context across 1,000 requests, not at firing blind payloads
- **Trust zero public PoCs** — Threat actors view security researchers as high-value targets; treat external code as hostile
- **Standardized interfaces beat custom glue code** — Adopting MCP saves hundreds of hours of custom API integration code

#### 7. Real-world application
- **Try this:** [ ] Pull historical JS URLs for your target using `waybackurls`, download bundles, and grep for `Bearer `, `token=`, and `api_key`
- **Try this:** [ ] Fuzz for hidden GraphQL paths using wordlists containing `graphql-beta`, `v1/gql`, `admin/graphql`, and `internal/graphql`
- **Try this:** [ ] Set up a local MCP server wrapping Caido or Burp REST API to let your LLM query proxy history programmatically
- **Try this:** [ ] Create a Docker container template for safely executing untrusted Python/Node PoC scripts from GitHub

#### 8. Red flags and pitfalls
- **Testing public PoCs on host workstation** — Direct execution of untrusted scripts can compromise your entire system
- **Assuming disabled introspection is universal** — Microservices often expose introspection on secondary paths or staging routes
- **Overlooking guest session permissions** — Guest tokens often bypass checks intended for fully authenticated users
- **Building un-abstracted AI tooling** — Hardcoding API calls instead of using standard schemas like MCP causes maintenance headaches

#### 9. Vocabulary
- **Partial Auth** — Session state with restricted privileges (e.g., unverified user, guest checkout, onboarding flow)
- **Wayback Mining** — Gathering intelligence and sensitive data from archived web pages and static assets
- **MCP (Model Context Protocol)** — Standardized protocol for connecting AI models to external tools and data stores
- **ChocoPoC** — Trojanised vulnerability exploit designed to compromise the security researcher running it
- **GraphQL Introspection** — Feature of GraphQL that allows querying the schema to discover all types, queries, and mutations

#### 10. Self-test
1. **Recall:** What is partial authentication and why does it frequently lead to authorization bypasses?
2. **Application:** Write a command pipeline using `waybackurls` and `grep` to extract auth headers from historical JS bundles.
3. **Reasoning:** Why is context enrichment a better mission for AI security tooling than mass unverified scanning?
4. **Application:** Describe how to isolate public exploit PoCs to prevent ChocoPoC compromise.
5. **Recall:** What role does Model Context Protocol (MCP) play in building AI bug bounty agents?
6. **Reasoning:** Why might an enterprise disable GraphQL introspection on `/graphql` but leave it active on `/api/v2/graphql-beta`?
7. **Application:** Outline a testing procedure for verifying if a guest Bearer token has elevated API access.
8. **Reflection:** How has the availability of historical web archives changed your target recon workflow?

#### 11. The practical takeaway
1. **Mine historical Wayback assets for leaked guest Bearer tokens and deprecated endpoints**
2. **[ ] Adopt Model Context Protocol (MCP) to standardize AI agent interaction with your proxy and security tools**
3. **[ ] Fuzz for secondary GraphQL introspection endpoints when the main path is restricted**
4. **[ ] Detonate public exploit PoCs inside isolated containers to prevent ChocoPoC backdoor execution**
5. **[ ] Focus AI development on context tracking and noise reduction to maximize signal quality**
---

### 📖 Darsnameh

**Bugs & Vulnerabilities:**
- **Hidden GraphQL Schema Discovered via Hackbot** — Enterprise SaaS — Hidden GraphQL Schema Discovered via Hackbot ([search](/search?q=Hidden%20GraphQL%20Schema%20Discovered%20via%20Hackbot))
- **Partial Auth Token Exposure via Wayback** — WPM Guest Flow — Partial Auth Token Exposure via Wayback ([search](/search?q=Partial%20Auth%20Token%20Exposure%20via%20Wayback))
- **Trojanised Exploit PoC (ChocoPoC)** — Vulnerability Research — Trojanised Exploit PoC (ChocoPoC) ([search](/search?q=Trojanised%20Exploit%20PoC%20(ChocoPoC)))
- **test** — 10. Self-test ([search](/search?q=test))
- **world application** — 7. Real-world application ([search](/search?q=world%20application))

**Techniques:**
- **AI Execution Sandbox Security** — also in [#182](/episodes/182)
- **GraphQL Hackbot Schema Enumeration** — also in [#182](/episodes/182)
- **Model Context Protocol (MCP) Security Tooling** — also in [#182](/episodes/182)
- **Partial Auth Bypass via Legacy Endpoints** — also in [#182](/episodes/182)
- **Wayback Bearer Token Extraction** — also in [#182](/episodes/182)

