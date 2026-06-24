---
title: "Alex Chapman — The Man of Many Crits"
episode: 31
---


# Episode 31 Alex Chapman — The Man of Many Crits

**Guests/Hosts:** Justin Gardner, Joel Margolis, Alex Chapman (AJX Chapman)  
**Date:** 2023-08-10 | **Duration:** 1:24:45

### TL;DR
- Alex's career: 16 years in security (Deloitte pen testing → smaller consultancy red team → Yahoo red team → HackerOne TPM → full-time bug bounty since 2019)
- Code review is his primary method: sinks-first (RCE sinks), deep IDE-based analysis
- Binary exploitation for headless Chrome: wrote Chrome renderer RCE exploits from scratch using GitHub Security Lab blog posts
- Perforce RCE: reverse-engineered the binary protocol, built a fake Perforce server in Python that sends `write-file-client` command → arbitrary file write
- Full-time bug bounty: work 3 days/week, strict schedule, GitLab for notes/issues

### Key Takeaways
- Focus on sinks (exec, deserialization, file write) and work backwards to find input paths
- For headless Chrome exploitation: sandbox often disabled → easier RCE; GitHub Security Lab blog is a good starting resource
- Client-server trust boundary: when client connects to attacker's server, the server has increased access; many protocols (Perforce, JDBC, Git) assume client only connects to trusted servers
- JDBC connection string injection: if you control a query parameter in the JDBC URL, you can write arbitrary files or perform SSRF
- Report writing: red team background → very detailed reports (4 hours per report initially); now dialed back but still high quality

### Bugs and Findings

#### Perforce RCE via fake server — RCE
- **Target/context:** Perforce version control client (heavily used in game dev)
- **Root cause:** The Perforce protocol is server-driven: the server tells the client what to do. The `write-file-client` command writes arbitrary files.
- **Technique / how found:** Alex reverse-engineered the binary protocol with Wireshark → built a Python fake Perforce server
- **Exploitation steps:**
  1. Set up a rogue Perforce server
  2. Victim connects (e.g., via DNS poisoning or social engineering)
  3. Server handles auth, then sends `write-file-client` command with arbitrary path/data
  4. File written to victim's system → RCE via webshell/startup folder
- **Key technical details:** Protocol command: `write-file-client` | Auth flow is handled by the fake server | Bounty shared via dupe window at live event
- **Impact / severity / bounty:** Arbitrary file write on connecting client → RCE; critical

#### JDBC connection string injection — File read/write
- **Target/context:** Applications using JDBC connectors
- **Root cause:** If attacker controls query string parameters in the JDBC URL, certain connectors allow arbitrary file operations via logging or other features
- **Key technical details:** JDBC URL parameters like `logger=...` or log file path directives | Recent CVEs for MySQL and PostgreSQL JDBC drivers
- **Technique / how found:** Alex's research focus on JDBC driver file read/write sinks
- **Impact / severity / bounty:** Arbitrary file read/write on the server

### Techniques and Primitives
- **Sink-first code review** — Identify dangerous functions (exec, Runtime.exec, ProcessBuilder, Deserialization.readObject, FileOutputStream) and trace backward to find controllable inputs
- **Protocol reverse engineering** — Use Wireshark to capture traffic; build a minimal fake server that handles auth and sends malicious commands
- **Client-side exploitation of server-driven protocols** — When a client connects to attacker's server, the server has privileged access to send commands (Perforce, some database protocols)

### Tooling and Resources
- IntelliJ IDEA (Java debugging/decompilation)
- JetBrains Rider (.NET debugging)
- GitHub Security Lab blog (Chrome exploitation references)
- Ghidra (binary reverse engineering)

### Suggestions and Advices from Hunter
- "I spend a significant portion of my time hacking in an IDE."
- "All hackers should know how to program, at least basically."
- "If I get one really high-impact bug in a live hacking event, I'm happy."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Alex's career: 16 years in security (Deloitte pen testing → smaller consultancy red team → Yahoo red team → HackerOne TPM → full-time bug bounty since 2019)

#### 2. What you should learn
- Understand **focus on sinks (exec, deserialization, file write) and work backwards to find input paths**
- Understand **for headless chrome exploitation: sandbox often disabled → easier rce; github security lab blog is a good starting resource**
- Understand **client-server trust boundary: when client connects to attacker's server, the server has increased access; many protocols (perforce, jdbc, git) assume client only connects to trusted servers**
- Understand **jdbc connection string injection: if you control a query parameter in the jdbc url, you can write arbitrary files or perform ssrf**
- Understand **report writing: red team background → very detailed reports (4 hours per report initially); now dialed back but still high quality**

#### 3. Core concepts explained
**Perforce RCE via fake server — RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**JDBC connection string injection — File read/write**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Sink-first code review**
- Identify dangerous functions (exec, Runtime.exec, ProcessBuilder, Deserialization.readObject, FileOutputStream) and trace backward to find controllable inputs

**Protocol reverse engineering**
- Use Wireshark to capture traffic; build a minimal fake server that handles auth and sends malicious commands

**Client-side exploitation of server-driven protocols**
- When a client connects to attacker's server, the server has privileged access to send commands (Perforce, some database protocols)


#### 4. Techniques and tactics
**Sink-first code review**
- **What it is:** Identify dangerous functions (exec, Runtime.exec, ProcessBuilder, Deserialization.readObject, FileOutputStream) and trace backward to find controllable inputs
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Protocol reverse engineering**
- **What it is:** Use Wireshark to capture traffic; build a minimal fake server that handles auth and sends malicious commands
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Client-side exploitation of server-driven protocols**
- **What it is:** When a client connects to attacker's server, the server has privileged access to send commands (Perforce, some database protocols)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"I spend a significant portion of my time hacking in an IDE."*
- *"All hackers should know how to program, at least basically."*
- *"If I get one really high-impact bug in a live hacking event, I'm happy."*

#### 6. Mental models
- **I spend a significant portion of my time hacking in an IDE.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **All hackers should know how to program, at least basically.** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If I get one really high-impact bug in a live hacking event,** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Focus on sinks (exec, deserialization, file write) and work backwards to find input paths
- **Try this:** For headless Chrome exploitation: sandbox often disabled → easier RCE; GitHub Security Lab blog is a good starting resource
- **Try this:** Client-server trust boundary: when client connects to attacker's server, the server has increased access; many protocols (Perforce, JDBC, Git) assume client only connects to trusted servers
- **Try this:** JDBC connection string injection: if you control a query parameter in the JDBC URL, you can write arbitrary files or perform SSRF

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **SSRF** — Server-Side Request Forgery — server makes HTTP requests on attacker's behalf
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **deserialization** — Converting serialized data back into objects — dangerous if attacker-controlled

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Perforce RCE via fake server — RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Alex's career: 16 years in security (Deloitte pen testing → smaller consultancy **
2. **Focus on sinks (exec, deserialization, file write) and work backwards to find in**
3. **For headless Chrome exploitation: sandbox often disabled → easier RCE; GitHub Se**
