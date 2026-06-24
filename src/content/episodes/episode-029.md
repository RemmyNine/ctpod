---
title: "Live Episode with Sean Yeoh — Assetnote Engineer"
episode: 29
---


# Episode 29 Live Episode with Sean Yeoh — Assetnote Engineer

**Guests/Hosts:** Justin Gardner, Joel Margolis, Sean Yeoh (Assetnote)  
**Date:** 2023-07-27 | **Duration:** 59:40

### TL;DR
- Sean Yeoh (Assetnote engineer) on building a production-grade recon architecture
- Message brokers (NATS over RabbitMQ), event-driven architecture vs task-based queues
- Optimization: profile first (Go pprof), then optimize bottlenecks; horizontal scaling after vertical optimization
- Database lessons: Postgres > MongoDB for relational recon data; avoid write-hot rows; consider ClickHouse for timeseries

### Key Takeaways
- For personal recon: keep it simple — janky Python scripts beat Kubernetes + event-driven architecture for a single hunter
- For scale: use NATS as message broker (lightweight, good visibility), avoid RabbitMQ (hard to keep alive at scale)
- Kernel optimization for scanning: container networking adds NAT layers that fill conntrack tables; use host networking or raw instances for masscan
- Postgres tips: avoid repeatedly updating the same row (creates bloat); use append-only tables for timeseries; consider ClickHouse for large-scale historical data
- Subdomain vs IP-focused architecture: IP is the lower-level entity; many assets don't have known subdomains

### Techniques and Primitives
- **Profiling-first optimization** — Use Go pprof to find where time is actually spent before optimizing; don't guess
- **Event-driven architecture** — Think "what data do I have?" not "what tasks do I want to run?"; when a domain is discovered, events trigger TLS scan, HTTP title, port scan automatically
- **DNS wildcard detection** — At every update, resolve known-wildcard patterns; hash-map wildcard patterns per domain level for fast matching

### Tooling and Resources
- NATS message broker
- KEDA (Kubernetes Event-Driven Autoscaling)
- Postgres (with indexing + materialized views for complex queries)
- ClickHouse (column-store for timeseries data)
- Go's `pprof` for profiling

### Suggestions and Advices from Hunter
- Sean: "Start from janky Python scripts that automate what you're doing now. Do not start from an event-driven architecture on Kubernetes."
- Sean: "KISS — Keep It Simple, Stupid. 80% of the result with 20% of the effort."
- "Engineering is harder than hacking. Building reliable, consistent systems is the hardest thing I've done."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Sean Yeoh (Assetnote engineer) on building a production-grade recon architecture

#### 2. What you should learn
- Understand **for personal recon: keep it simple — janky python scripts beat kubernetes + event-driven architecture for a single hunter**
- Understand **for scale: use nats as message broker (lightweight, good visibility), avoid rabbitmq (hard to keep alive at scale)**
- Understand **kernel optimization for scanning: container networking adds nat layers that fill conntrack tables; use host networking or raw instances for masscan**
- Understand **postgres tips: avoid repeatedly updating the same row (creates bloat); use append-only tables for timeseries; consider clickhouse for large-scale historical data**
- Understand **subdomain vs ip-focused architecture: ip is the lower-level entity; many assets don't have known subdomains**

#### 3. Core concepts explained
**Profiling-first optimization**
- Use Go pprof to find where time is actually spent before optimizing; don't guess

**Event-driven architecture**
- Think "what data do I have?" not "what tasks do I want to run?"; when a domain is discovered, events trigger TLS scan, HTTP title, port scan automatically

**DNS wildcard detection**
- At every update, resolve known-wildcard patterns; hash-map wildcard patterns per domain level for fast matching


#### 4. Techniques and tactics
**Profiling-first optimization**
- **What it is:** Use Go pprof to find where time is actually spent before optimizing; don't guess
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Event-driven architecture**
- **What it is:** Think "what data do I have?" not "what tasks do I want to run?"; when a domain is discovered, events trigger TLS scan, HTTP title, port scan automatically
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DNS wildcard detection**
- **What it is:** At every update, resolve known-wildcard patterns; hash-map wildcard patterns per domain level for fast matching
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Sean: "Start from janky Python scripts that automate what you're doing now. Do not start from an event-driven architecture on Kubernetes."*
- *"Sean: "KISS"* — **Keep It Simple, Stupid. 80% of the result with 20% of the effort.**
- *"Engineering is harder than hacking. Building reliable, consistent systems is the hardest thing I've done."*

#### 6. Mental models
- **Sean: "Start from janky Python scripts that automate what yo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Sean: "KISS — Keep It Simple, Stupid. 80% of the result with** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Engineering is harder than hacking. Building reliable, consi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** For personal recon: keep it simple — janky Python scripts beat Kubernetes + event-driven architecture for a single hunter
- **Try this:** For scale: use NATS as message broker (lightweight, good visibility), avoid RabbitMQ (hard to keep alive at scale)
- **Try this:** Kernel optimization for scanning: container networking adds NAT layers that fill conntrack tables; use host networking or raw instances for masscan
- **Try this:** Postgres tips: avoid repeatedly updating the same row (creates bloat); use append-only tables for timeseries; consider ClickHouse for large-scale historical data

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **DNS** — Domain Name System — translates domain names to IP addresses
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Sean Yeoh (Assetnote engineer) on building a production-grade recon architecture**
2. **For personal recon: keep it simple — janky Python scripts beat Kubernetes + even**
3. **For scale: use NATS as message broker (lightweight, good visibility), avoid Rabb**
