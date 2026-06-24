---
title: "Chill Chat with Legendary DoD Hacker Corben Leo"
episode: 21
---


# Episode 21 Chill Chat with Legendary DoD Hacker Corben Leo

**Guests/Hosts:** Justin Gardner, Corben Leo (hacker_ / corben)  
**Date:** 2023-06-01 | **Duration:** 1:13:50

### TL;DR
- Corben's journey: started hacking in high school (freshman), found bug bounty via Tommy DeVoss tweet, 10 months to first bounty on DoD programs
- Recon methodology: virtual host enumeration, load balancer analysis, ingress endpoint fuzzing
- Writing/storytelling as a key skill: simplify without dumbing down, reach broader audience
- Copywriting applied to bug reports: clear summary + detailed CVSS metric justification

### Key Takeaways
- Load balancer identification: look at response headers (Kong, AWS ELB in SNI), try host-header fuzzing, check default 404 responses
- Map domains to IPs — build host-to-IP resolution into your recon pipeline; the same IP can serve different domains via virtual hosting
- For reports: write the summary in clear, non-technical language; in the impact section, list every CVSS metric and justify why you chose it — forces the program to engage
- DoD VDP is a valid training ground due to wide scope and variety of stacks; but expect 10 months+ for first paid bounty

### Bugs and Findings
*(No specific named bugs in this episode beyond general methodology)*

### Techniques and Primitives
- **Virtual-host brute force** — Send requests with different `Host:` headers to the same IP; varying responses indicate multiple apps behind one IP
- **Ingress endpoint cycling** — Identify load balancers (AWS ELB, Kong, etc.) and fuzz hostnames against different backends
- **Directory brute force on JS directories** — Found `/javascript/` directories, brute-force for JS files inside them to discover hidden endpoints like `upload.aspx`
- **Copywriting for reports** — Use Sam Parr's "Copy That" course principles: simplify, captivate, then deliver technical detail

### Tooling and Resources
- Archangel D Day's "100 very short bug bounty rules" tweet
- Sam Parr's Copy That copywriting course
- Hakluke's tooling / methodology

### Suggestions and Advices from Hunter
- "The whole point of recon is to find more applications to hack."
- "I make all these talks about recon to help you find more apps to hack. Do your recon until you find an interesting app, then hack that app." — jhaddix
- Corben: "Was it an intern who wrote this? I got so much flack for simplifying. But I wasn't writing for them — I was writing for people who need to understand."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Corben's journey: started hacking in high school (freshman), found bug bounty via Tommy DeVoss tweet, 10 months to first bounty on DoD programs

#### 2. What you should learn
- Understand **load balancer identification: look at response headers (kong, aws elb in sni), try host-header fuzzing, check default 404 responses**
- Understand **map domains to ips — build host-to-ip resolution into your recon pipeline; the same ip can serve different domains via virtual hosting**
- Understand **for reports: write the summary in clear, non-technical language; in the impact section, list every cvss metric and justify why you chose it — forces the program to engage**
- Understand **dod vdp is a valid training ground due to wide scope and variety of stacks; but expect 10 months+ for first paid bounty**

#### 3. Core concepts explained
**Virtual-host brute force**
- Send requests with different `Host:` headers to the same IP; varying responses indicate multiple apps behind one IP

**Ingress endpoint cycling**
- Identify load balancers (AWS ELB, Kong, etc.) and fuzz hostnames against different backends

**Directory brute force on JS directories**
- Found `/javascript/` directories, brute-force for JS files inside them to discover hidden endpoints like `upload.aspx`


#### 4. Techniques and tactics
**Virtual-host brute force**
- **What it is:** Send requests with different `Host:` headers to the same IP; varying responses indicate multiple apps behind one IP
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Ingress endpoint cycling**
- **What it is:** Identify load balancers (AWS ELB, Kong, etc.) and fuzz hostnames against different backends
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Directory brute force on JS directories**
- **What it is:** Found `/javascript/` directories, brute-force for JS files inside them to discover hidden endpoints like `upload.aspx`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Copywriting for reports**
- **What it is:** Use Sam Parr's "Copy That" course principles: simplify, captivate, then deliver technical detail
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The whole point of recon is to find more applications to hack."*
- *"I make all these talks about recon to help you find more apps to hack. Do your recon until you find an interesting app, then hack that app."* — **jhaddix**
- *"Corben: "Was it an intern who wrote this? I got so much flack for simplifying. But I wasn't writing for them"* — **I was writing for people who need to understand.**

#### 6. Mental models
- **The whole point of recon is to find more applications to hac** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **I make all these talks about recon to help you find more app** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Corben: "Was it an intern who wrote this? I got so much flac** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Load balancer identification: look at response headers (Kong, AWS ELB in SNI), try host-header fuzzing, check default 404 responses
- **Try this:** Map domains to IPs — build host-to-IP resolution into your recon pipeline; the same IP can serve different domains via virtual hosting
- **Try this:** For reports: write the summary in clear, non-technical language; in the impact section, list every CVSS metric and justify why you chose it — forces the program to engage
- **Try this:** DoD VDP is a valid training ground due to wide scope and variety of stacks; but expect 10 months+ for first paid bounty

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **recon** — Reconnaissance — systematic discovery of target attack surface
- **fuzzing** — Sending unexpected or malformed data to discover vulnerabilities

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Corben's journey: started hacking in high school (freshman), found bug bounty vi**
2. **Load balancer identification: look at response headers (Kong, AWS ELB in SNI), t**
3. **Map domains to IPs — build host-to-IP resolution into your recon pipeline; the s**
