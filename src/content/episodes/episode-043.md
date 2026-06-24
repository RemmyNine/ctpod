---
title: "Caido — The Up-And-Coming HTTP Proxy"
episode: 43
---


# Episode 43 Caido — The Up-And-Coming HTTP Proxy

### TL;DR
- Interview with Emil (Caido co-founder) — Rust backend, client-server architecture
- Caido features: lightweight intercepting proxy, collections, convert workflows, match-and-replace
- Client-server architecture: run server on VPS/Raspberry Pi, frontend in browser or desktop client
- Converts workflows (node-based system) for text transformation, with planned passive/active workflows

### Key takeaways
- Rust backend provides stability and performance vs Java (Burp); but async Rust is very hard
- Client-server architecture: zero license-per-machine issues, runs on Chromebook/iPad + VPS
- Collections for organizing requests; planned notes/reporting features
- Convert workflows are node-based (similar to Subgraph) — drag, connect, run JS snippets
- No collaborator planned short-term; may integrate with interactsh for DNS callbacks

### Techniques and Primitives
- **Convert workflows** — chain nodes to transform text (base64 encode, URL encode, minify JSON, etc.); can call external programs via shell node
- **Workflows as plugin replacement** — passive workflows (react to events) and active workflows (scanner-like) coming

### Tooling and Resources
- **Caido** — `caido.io`; referral code `CTBBPODCAST` for 10% off
- **Caido Pro free for students**

### Suggestions and Advices from Hunter
- "The goal of Caido as a business: eliminate PDF reports"
- On MVP philosophy: "We try to do an MVP of every new idea, put it out as fast as possible, get feedback, then improve"

### AI Takeaway
The convert workflow system represents a paradigm shift from plugin-dependent extensibility to user-programmable, node-based scripting accessible to non-programmers.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Interview with Emil (Caido co-founder) — Rust backend, client-server architecture

#### 2. What you should learn
- Understand **rust backend provides stability and performance vs java (burp); but async rust is very hard**
- Understand **client-server architecture: zero license-per-machine issues, runs on chromebook/ipad + vps**
- Understand **collections for organizing requests; planned notes/reporting features**
- Understand **convert workflows are node-based (similar to subgraph) — drag, connect, run js snippets**
- Understand **no collaborator planned short-term; may integrate with interactsh for dns callbacks**

#### 3. Core concepts explained
**Convert workflows**
- chain nodes to transform text (base64 encode, URL encode, minify JSON, etc.); can call external programs via shell node

**Workflows as plugin replacement**
- passive workflows (react to events) and active workflows (scanner-like) coming


#### 4. Techniques and tactics
**Convert workflows**
- **What it is:** chain nodes to transform text (base64 encode, URL encode, minify JSON, etc.); can call external programs via shell node
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Workflows as plugin replacement**
- **What it is:** passive workflows (react to events) and active workflows (scanner-like) coming
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The goal of Caido as a business: eliminate PDF reports"*
- *"On MVP philosophy: "We try to do an MVP of every new idea, put it out as fast as possible, get feedback, then improve"*

#### 6. Mental models
- **The goal of Caido as a business: eliminate PDF reports** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On MVP philosophy: "We try to do an MVP of every new idea, p** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Rust backend provides stability and performance vs Java (Burp); but async Rust is very hard
- **Try this:** Client-server architecture: zero license-per-machine issues, runs on Chromebook/iPad + VPS
- **Try this:** Collections for organizing requests; planned notes/reporting features
- **Try this:** Convert workflows are node-based (similar to Subgraph) — drag, connect, run JS snippets

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **DNS** — Domain Name System — translates domain names to IP addresses
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Interview with Emil (Caido co-founder) — Rust backend, client-server architectur**
2. **Rust backend provides stability and performance vs Java (Burp); but async Rust i**
3. **Client-server architecture: zero license-per-machine issues, runs on Chromebook/**
