---
title: "Space Raccoon — From Day Zero to Zero Day"
episode: 120
---


# Episode 120 Space Raccoon — From Day Zero to Zero Day

### TL;DR
- Book "From Day Zero to Zero Day" covers vulnerability research methodology across binaries and source code
- Binary taxonomy: not all binaries require Ghidra — Java/.NET decompile to readable source, Electron apps can be unpacked
- Taint analysis: trace source to sink; academic term for what hunters do intuitively
- Hybrid binary analysis: combine static (Ghidra/IDA) with dynamic (Frida, debuggers) — hook OS-level APIs not just app functions
- Smart weighing machines full chain: UART → shell → firmware extraction → certificate extraction → device-to-cloud MITM → SQLi via version() → WAF bypass

### Key Takeaways
- **Binary taxonomy**: Identify binary type first — Java (.jar) can be decompiled to almost-source, .NET can be decompiled with dnSpy/ILSpy, Electron is just Node.js bundled
- **Dynamic analysis**: Hook OS-level API calls (Windows API, browser APIs) not just app-specific functions — common function names reveal app behavior without deep reversing
- **Fuzzing**: Start with "dumb fuzzing" — throw random inputs without understanding structure; many CVEs are findable with dumb fuzzers
- **Variant analysis**: When you find one pattern, grep for it across the codebase; replicate across similar targets using same libraries
- **Sink-to-source**: In source code, find vulnerable function → trace back to entry point; in binaries, use both directions

### Bugs and Findings

#### Smart Weighing Machines — Full Remote Exploitation
- **Target/context:** IoT smart scales (health devices)
- **Root cause:** Multiple layers of weak security: hardcoded certificates, SQL injection in cloud API, no device-to-cloud authentication verification
- **Technique / how found:**
  1. Physical UART connection → shell access to firmware
  2. Extract certificates from device filesystem
  3. Use certificates to MITM device-to-cloud communication
  4. Found SQLi in cloud API during traffic analysis
  5. Bypassed WAF using `version()` instead of `1=1` — `SELECT * FROM users WHERE id=version()` — `version()` always evaluates to true
- **Exploitation steps:**
  1. Buy scale, open case, connect UART (FT232 required — cheap CP2102 gave garbled data)
  2. Get shell, dump certificate from memory
  3. Set up proxy with certificate → decrypt HTTPS traffic
  4. Find SQL injection in cloud API
  5. WAF blocks `1=1`, use `version()` instead
  6. Dump all user data via SQLi
- **Key technical details:** UART baud rate via logic analyzer/multimeter; FT232 vs CP2102 quality difference; IoT device auth often uses certificates embedded in firmware; `version()` in MySQL evaluates to a positive integer → always true
- **Impact / severity / bounty:** Full remote compromise of all smart scales (PII, health data, remote control)
- **Obstacles & how solved:** Hardware — cheap USB-to-TTL converter caused garbled serial; solved by switching to FT232. WAF — blocked `1=1`, bypassed with `version()`. Bluetooth path considered but deprioritized.

#### Conditional Memory Corruption RCE
- **Target/context:** Large cloud service with load-balanced instances
- **Root cause:** Heap overflow in binary file format parser
- **Technique / how found:**
  1. Traditional heap overflow → info leak + write primitive
  2. Problem: exploit lands on different backend instance for leak vs write
  3. Solution: "conditional corruption" — heap-groom objects with specific pointers
  4. On wrong instance: invalid pointers cause graceful error (crash prevented)
  5. On correct instance: pointers align, overflow continues to code execution
- **Key technical details:** Conditional corruption: heap-groomed objects contain pointers that are valid only on the specific target instance; other instances get invalid pointer → early bailout
- **Impact / severity / bounty:** RCE on cloud backend
- **Obstacles & how solved:** Load-balanced instances — different instance for leak vs overwrite. Solved with conditional corruption (spray-and-pray without availability impact).

### Techniques and Primitives
- **Binary taxonomy first** — Check if it's Java (.jar), .NET (.exe/.dll), Electron, or Go before firing up Ghidra
- **Sink-to-source** — In source code: find vulnerable function, trace back to route/parameter. In binaries: use both directions
- **Conditional corruption** — Heap-groom with target-specific pointers; other instances get invalid pointers → graceful bailout
- **`version()` for SQLi WAF bypass** — `WHERE id=version()` — version() always evaluates to true
- **Auto-generated POC graphs** — Bookmark key lines in VS Code, export vuln pathway for reports
- **Hook OS APIs with Frida** — Not just app functions — hook `CreateFile`, `RegOpenKeyEx`, `send`, `recv` — common names reveal OS interaction

### Tooling and Resources
- "From Day Zero to Zero Day" by Space Raccoon (No Starch Press) — code `ZERODAYDEAL` for 30% off
- CodeQL, Semgrep for automated taint analysis
- Frida, Ghidra, IDA, dnSpy/ILSpy
- AFL, libFuzzer for coverage-guided fuzzing
- Angr for symbolic execution

### Suggestions and Advices from Hunter
- "Binaries are not binary — some are just Node.js apps bundled into Electron, you can unpack and read the source"
- "Start fuzzing with dumb fuzzing — throw random inputs without understanding structure. Many CVEs are findable this way."
- "When doing source code review, understand how input propagates through the system. Hooks in WordPress are a great example."
- "If you're stuck on hardware, ask a friend for sanity check — my CP2102 was faulty, switching to FT232 fixed it"
- "Variant analysis: when you find one CVE pattern, replicate it across all similar functions and targets"

### AI Takeaway
The `version()` SQLi WAF bypass is a simple but effective primitive worth testing everywhere. The conditional corruption technique for load-balanced environments is a sophisticated solution to a common availability problem in exploit development.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Book "From Day Zero to Zero Day" covers vulnerability research methodology across binaries and source code

#### 2. What you should learn
- Understand **binary taxonomy**: identify binary type first — java (.jar) can be decompiled to almost-source, .net can be decompiled with dnspy/ilspy, electron is just node.js bundled**
- Understand **dynamic analysis**: hook os-level api calls (windows api, browser apis) not just app-specific functions — common function names reveal app behavior without deep reversing**
- Understand **fuzzing**: start with "dumb fuzzing" — throw random inputs without understanding structure; many cves are findable with dumb fuzzers**
- Understand **variant analysis**: when you find one pattern, grep for it across the codebase; replicate across similar targets using same libraries**
- Understand **sink-to-source**: in source code, find vulnerable function → trace back to entry point; in binaries, use both directions**

#### 3. Core concepts explained
**Smart Weighing Machines — Full Remote Exploitation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Conditional Memory Corruption RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Binary taxonomy first**
- Check if it's Java (.jar), .NET (.exe/.dll), Electron, or Go before firing up Ghidra

**Sink-to-source**
- In source code: find vulnerable function, trace back to route/parameter. In binaries: use both directions

**Conditional corruption**
- Heap-groom with target-specific pointers; other instances get invalid pointers → graceful bailout


#### 4. Techniques and tactics
**Binary taxonomy first**
- **What it is:** Check if it's Java (.jar), .NET (.exe/.dll), Electron, or Go before firing up Ghidra
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Sink-to-source**
- **What it is:** In source code: find vulnerable function, trace back to route/parameter. In binaries: use both directions
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Conditional corruption**
- **What it is:** Heap-groom with target-specific pointers; other instances get invalid pointers → graceful bailout
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`version()` for SQLi WAF bypass**
- **What it is:** `WHERE id=version()` — version() always evaluates to true
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Auto-generated POC graphs**
- **What it is:** Bookmark key lines in VS Code, export vuln pathway for reports
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Binaries are not binary"* — **some are just Node.js apps bundled into Electron, you can unpack and read the source**
- *"Start fuzzing with dumb fuzzing"* — **throw random inputs without understanding structure. Many CVEs are findable this way.**
- *"When doing source code review, understand how input propagates through the system. Hooks in WordPress are a great example."*
- *"If you're stuck on hardware, ask a friend for sanity check"* — **my CP2102 was faulty, switching to FT232 fixed it**
- *"Variant analysis: when you find one CVE pattern, replicate it across all similar functions and targets"*

#### 6. Mental models
- **Binaries are not binary — some are just Node.js apps bundled** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Start fuzzing with dumb fuzzing — throw random inputs withou** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **When doing source code review, understand how input propagat** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Binary taxonomy**: Identify binary type first — Java (.jar) can be decompiled to almost-source, .NET can be decompiled with dnSpy/ILSpy, Electron is just Node.js bundled
- **Try this:** Dynamic analysis**: Hook OS-level API calls (Windows API, browser APIs) not just app-specific functions — common function names reveal app behavior without deep reversing
- **Try this:** Fuzzing**: Start with "dumb fuzzing" — throw random inputs without understanding structure; many CVEs are findable with dumb fuzzers
- **Try this:** Variant analysis**: When you find one pattern, grep for it across the codebase; replicate across similar targets using same libraries

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Hardware — cheap USB-to-TTL converter caused garbled serial; solved by switching to FT232. WAF — blocked `1=1`, bypassed with `version()`. Bluetooth path considered but deprioritized.
- - Obstacles & how solved: Load-balanced instances — different instance for leak vs overwrite. Solved with conditional corruption (spray-and-pray without availability impact).

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **SQLi** — SQL Injection — inserting SQL queries through user input
- **API** — Application Programming Interface — structured endpoints for data exchange
- **DNS** — Domain Name System — translates domain names to IP addresses
- **WAF** — Web Application Firewall — filters and monitors HTTP traffic
- **fuzzing** — Sending unexpected or malformed data to discover vulnerabilities

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Smart Weighing Machines — Full Remote Exploitation?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Book "From Day Zero to Zero Day" covers vulnerability research methodology acros**
2. **Binary taxonomy**: Identify binary type first — Java (.jar) can be decompiled to**
3. **Dynamic analysis**: Hook OS-level API calls (Windows API, browser APIs) not just**
