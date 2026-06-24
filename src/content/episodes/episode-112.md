---
title: "Interview with Ciarán Cotter (MonkeHack)"
episode: 112
---


# Episode 112 Interview with Ciarán Cotter (MonkeHack)

### TL;DR
- Three bugs presented: complex postMessage ATO chain via OAuth fixation + iframe hop + double URL-encoded hash fragment; unauthenticated CSTI with frame ancestors bypass via DOM purging; server-side classpath resource enumeration via error differentiation
- WebSocket research: sending HTTP request body with WebSocket upgrade request causes server to interpret body as WebSocket frame — pipeline frames enable frame smuggling
- Server-side: URL parameter that accepted relative paths → `jar:` protocol check → error differentiation reveals file existence
- AI hacking: invisible text in templates for prompt injection; cross-site leaks via iframe counting

### Key Takeaways
- In complex client-side chains, `window.open()` to victim page gives a window reference; if that page has `Cross-Origin-Opener-Policy` (COOP), postMessage is blocked — use OAuth state fixation to bypass COOP by jumping to a different flow step
- Double URL-encode a hash fragment: on first redirect it decodes once, on second redirect to victim page it decodes again — the OAuth code lands in the hash and is not consumed
- For CSTI in unauthenticated context: frame the vulnerable page in an iframe, purge its DOM (same-origin so you can), then create a new iframe to the authenticated page — frame ancestors check passes because the top frame is the same origin, but the redirect code is gone
- For web socket smuggling: send `Transfer-Encoding: chunked` in the upgrade request body — HTTP stack reads it as a second request, but server interprets it as a WebSocket frame, smuggling frame content
- Server-side classpath enumeration: if a URL parameter returns "jar protocol not allowed" for existing files and "classpath resource does not exist" for missing files, you have an oracle to enumerate the classpath

### Bugs and Findings

#### Bug 1: PostMessage ATO Chain via OAuth Fixation
- **Target/context:** Public program with chat widget in iframe
- **Root cause:** Chat widget accepted postMessage with URL to render in iframe src — `javascript:` protocol worked (XSS in widget context). Widget had origin check that allowed custom domains. OAuth flow had COOP on `/authorize` but not on subsequent step.
- **Technique / how found:**
  1. Host JS on allowed custom domain → `window.open(victim)` → send postMessage (from allowed origin)
  2. OAuth state fixation: generate state, fixate it in victim (state not tied to session)
  3. Double URL-encode hash fragment so OAuth code lands in hash (unconsumed)
  4. postMessage to chat widget iframe → iframe hop (same-origin between frames) → trigger logging → leak parent href containing OAuth code
- **Key technical details:** COOP blocks postMessage from popup to opener; state fixation bypasses COOP by jumping to next flow step; double URL-encoded `#` in the redirect chain puts code in fragment
- **Impact / severity / bounty:** High bounty (exact amount not stated but described as "high")
- **Obstacles & how solved:** Took a week with collaborator; wrote automated POC that generates fresh state from server

#### Bug 2: Unauthenticated CSTI to ATO via DOM Purging
- **Target/context:** App with Angular CSTI on unauthenticated page, separate authenticated origin
- **Root cause:** CSTI exists only on unauthenticated page. Authenticated page has postMessage listener that sends credentials to parent, but checks `frame-ancestors`.
- **Technique / how found:**
  1. Frame the CSTI page (same-origin as itself)
  2. Purge the DOM of the framed CSTI page (same-origin → `document.write('')` or remove all nodes)
  3. In the purged frame, create an iframe to the authenticated page
  4. `frame-ancestors` check passes because the top frame is the CSTI origin (same-origin)
  5. PostMessage from authenticated iframe sends creds to parent (the purged frame) → exfiltrate
- **Key technical details:** Same-origin iframes can manipulate each other's DOM; purging DOM removes redirect JavaScript but retains frame ancestry; `frame-ancestors` whitelisted the CSTI page
- **Impact / severity / bounty:** Account takeover without being logged in
- **Obstacles & how solved:** Required CSTI on an unauthenticated page; needed the authenticated page's frame-ancestors to include the CSTI page

#### Bug 3: Classpath Resource Enumeration via Error Differentiation
- **Target/context:** Proxy API with URL parameter
- **Root cause:** Parameter accepted relative paths. When given a relative path like `/`, returned "jar protocol not allowed" vs "classpath resource does not exist" based on file existence.
- **Technique / how found:** Try `/` → error contains "classpath resource does not exist". Try `/META-INF` → "jar protocol not allowed" (file exists but jar: blocked). Use this oracle to fuzz the entire classpath.
- **Key technical details:** Spring classpath protocol; "jar protocol not allowed" = file exists, "classpath resource does not exist" = file missing
- **Impact / severity / bounty:** Low (information disclosure — file name enumeration)
- **Obstacles & how solved:** Needed Spring expert (PM.H) to identify the classpath protocol

#### WebSocket Frame Smuggling via HTTP Pipelining
- **Target/context:** Apps using WebSockets
- **Root cause:** Sending HTTP request body *with* the WebSocket upgrade request causes the server to interpret the body as the first WebSocket frame. `Transfer-Encoding: chunked` enables smuggling frames via HTTP pipelining.
- **Technique / how found:** Send upgrade request + body; server sees upgrade (101), then interprets body bytes as WebSocket frame — attacker controls opcodes and payload of the first frame
- **Key technical details:** WebSocket frames have opcodes (text, binary, close, ping, pong) + payload; normally user only controls message content. With pipeline smuggling, attacker controls frame headers too. `Transfer-Encoding: chunked` enables this across multiple implementations.
- **Impact / severity / bounty:** Potential request smuggling — smuggle WebSocket frames between users
- **Obstacles & how solved:** Found by testing implementations against spec; cross-implementation behavior suggests systemic issue

### Techniques and Primitives
- **Iframe hop (same-origin frame navigation)** — Two iframes from same origin in different documents can still access each other if the parent pages share an opener relationship
- **DOM purging for frame-ancestors bypass** — Purge an iframe's DOM to remove redirect/security code while retaining frame ancestry
- **WebSocket pipeline frame smuggling** — `Transfer-Encoding: chunked` with WebSocket upgrade; body bytes interpreted as raw WebSocket frame
- **Classpath oracle via error messages** — "protocol not allowed" = exists; "resource not found" = missing
- **Double URL-encoded hash fragment** — `%23` → `#` after second decode — OAuth code lands in fragment, unconsumed

### Tooling and Resources
- HackerOne Ambassador program
- Critical Thinking Research Lab
- Douglas Day (Archangel), Lupin, HakuPiku, Fonson — collaborators

### Suggestions and Advices from Hunter
- "When creating gadgets of any kind, you want to know the individual pieces — you can't solve the puzzle without knowing what your puzzle pieces are"
- "WebSockets are very underappreciated — they're a whole other protocol, susceptible to the same bugs (IDOR, auth bypass)"
- "If you don't understand how components interact, your brain can't work out the attack in the shower"
- "Frame ancestors whitelisted the CSTI page — by purging the DOM I didn't trigger the code that would redirect and break everything"

### AI Takeaway
The WebSocket frame smuggling primitive is potentially high-impact: if `TE: chunked` is accepted in WebSocket upgrade requests across multiple implementations, there may be a systematic vulnerability class. Testing this across popular WebSocket libraries could yield CVEs or bounty-worthy bugs.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Three bugs presented: complex postMessage ATO chain via OAuth fixation + iframe hop + double URL-encoded hash fragment; unauthenticated CSTI with frame ancestors bypass via DOM purging; server-side classpath resource enumeration via error differentiation

#### 2. What you should learn
- Understand **in complex client-side chains, `window.open()` to victim page gives a window reference; if that page has `cross-origin-opener-policy` (coop), postmessage is blocked — use oauth state fixation to bypass coop by jumping to a different flow step**
- Understand **double url-encode a hash fragment: on first redirect it decodes once, on second redirect to victim page it decodes again — the oauth code lands in the hash and is not consumed**
- Understand **for csti in unauthenticated context: frame the vulnerable page in an iframe, purge its dom (same-origin so you can), then create a new iframe to the authenticated page — frame ancestors check passes because the top frame is the same origin, but the redirect code is gone**
- Understand **for web socket smuggling: send `transfer-encoding: chunked` in the upgrade request body — http stack reads it as a second request, but server interprets it as a websocket frame, smuggling frame content**
- Understand **server-side classpath enumeration: if a url parameter returns "jar protocol not allowed" for existing files and "classpath resource does not exist" for missing files, you have an oracle to enumerate the classpath**

#### 3. Core concepts explained
**Bug 1: PostMessage ATO Chain via OAuth Fixation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Bug 2: Unauthenticated CSTI to ATO via DOM Purging**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Bug 3: Classpath Resource Enumeration via Error Differentiation**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Iframe hop (same-origin frame navigation)**
- Two iframes from same origin in different documents can still access each other if the parent pages share an opener relationship

**DOM purging for frame-ancestors bypass**
- Purge an iframe's DOM to remove redirect/security code while retaining frame ancestry

**WebSocket pipeline frame smuggling**
- `Transfer-Encoding: chunked` with WebSocket upgrade; body bytes interpreted as raw WebSocket frame


#### 4. Techniques and tactics
**Iframe hop (same-origin frame navigation)**
- **What it is:** Two iframes from same origin in different documents can still access each other if the parent pages share an opener relationship
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DOM purging for frame-ancestors bypass**
- **What it is:** Purge an iframe's DOM to remove redirect/security code while retaining frame ancestry
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WebSocket pipeline frame smuggling**
- **What it is:** `Transfer-Encoding: chunked` with WebSocket upgrade; body bytes interpreted as raw WebSocket frame
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Classpath oracle via error messages**
- **What it is:** "protocol not allowed" = exists; "resource not found" = missing
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Double URL-encoded hash fragment**
- **What it is:** `%23` → `#` after second decode — OAuth code lands in fragment, unconsumed
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"When creating gadgets of any kind, you want to know the individual pieces"* — **you can't solve the puzzle without knowing what your puzzle pieces are**
- *"WebSockets are very underappreciated"* — **they're a whole other protocol, susceptible to the same bugs (IDOR, auth bypass)**
- *"If you don't understand how components interact, your brain can't work out the attack in the shower"*
- *"Frame ancestors whitelisted the CSTI page"* — **by purging the DOM I didn't trigger the code that would redirect and break everything**

#### 6. Mental models
- **When creating gadgets of any kind, you want to know the indi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **WebSockets are very underappreciated — they're a whole other** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you don't understand how components interact, your brain ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** In complex client-side chains, `window.open()` to victim page gives a window reference; if that page has `Cross-Origin-Opener-Policy` (COOP), postMessage is blocked — use OAuth state fixation to bypass COOP by jumping to a different flow step
- **Try this:** Double URL-encode a hash fragment: on first redirect it decodes once, on second redirect to victim page it decodes again — the OAuth code lands in the hash and is not consumed
- **Try this:** For CSTI in unauthenticated context: frame the vulnerable page in an iframe, purge its DOM (same-origin so you can), then create a new iframe to the authenticated page — frame ancestors check passes because the top frame is the same origin, but the redirect code is gone
- **Try this:** For web socket smuggling: send `Transfer-Encoding: chunked` in the upgrade request body — HTTP stack reads it as a second request, but server interprets it as a WebSocket frame, smuggling frame content

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Took a week with collaborator; wrote automated POC that generates fresh state from server
- - Obstacles & how solved: Required CSTI on an unauthenticated page; needed the authenticated page's frame-ancestors to include the CSTI page

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **OAuth** — Open standard for authorization — delegated access without sharing passwords
- **prompt injection** — Tricking an LLM into ignoring its instructions by injecting malicious input
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Bug 1: PostMessage ATO Chain via OAuth Fixation?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Three bugs presented: complex postMessage ATO chain via OAuth fixation + iframe **
2. **In complex client-side chains, `window.open()` to victim page gives a window ref**
3. **Double URL-encode a hash fragment: on first redirect it decodes once, on second **
