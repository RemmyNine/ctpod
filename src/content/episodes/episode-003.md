---
title: "H1-407 Event Madness & Takeaways Part 1"
episode: 3
---


# Episode 3 H1-407 Event Madness & Takeaways Part 1

### TL;DR
- DLL hijacking on Windows executables as exploitation technique (not always a valid vuln)
- Binary decompilation tools: ILSpy, dotPeek (.NET/C#); JD-GUI/JADX (Java); PyInstaller Extractor + Uncompyle6 (Python)
- Enumerate Windows URI handlers via PowerShell for attack surface on native apps
- SameSite cookie bypass via Lax+POST (2-minute window for top-level POST requests)
- GraphQL error-based enumeration (schema-less brute force via error messages)
- Caido public beta released

### Key takeaways
- Use ILSpy or dotPeek to decompile .NET/C# binaries back to source code
- For Python binaries: PyInstaller Extractor → .pyc → Uncompyle6 → .py
- Run `strings` or `objdump` on binaries to identify language (Python, .NET, C#, etc.)
- Enumerate Windows URI handlers: PowerShell script that checks registry keys for URL protocol associations
- Error messages can leak information via Boolean logic or direct ID disclosure
- SameSite cookies: Lax+POST gives a 2-minute window for top-level POST CSRF
- GraphQL: error messages often reveal valid inputs, field names, or schema
- Caido went public beta; distributed architecture (server + thin client)

### Bugs and Findings

#### [Implied] DLL Hijacking on Windows Binary
- **Target/context:** Windows executable in H1-407 scope
- **Root cause:** Missing DLLs found via Process Monitor (Procmon); binary loads DLLs from adjacent folder
- **Technique / how found:** Opened Procmon, noticed "Name Not Found" DLLs; compiled malicious DLL, placed in path, got calc.exe
- **Impact / severity / bounty:** Not a valid vulnerability per H1-407 triage — considered an exploitation technique, not a remediable vuln for the program

### Techniques and Primitives
- **Binary language identification** — `strings`/`objdump` to detect Python, .NET, C# references
- **Decompilation pipeline per language** — .NET: dotPeek/ILSpy; Java: JADX/JD-GUI; Python: PyInstaller Extractor → Uncompyle6
- **Windows URI handler enumeration** — check registry `HKCR\*\shell\*\command` for protocol handlers
- **GraphQL field enumeration via error messages** — send invalid input, error often reveals allowed values
- **SameSite Lax+POST timer reset** — CSRF login/logout resets the 2-min timer for top-level POST requests

### Tooling and Resources
- ILSpy, dotPeek (JetBrains) — .NET/C# decompilers
- JADX GUI — Java/Android decompiler
- JD-GUI — Java decompiler
- Jsmoot — EXE→JAR converter
- PyInstaller Extractor — extract .pyc from PyInstaller binaries
- Uncompyle6 — .pyc → .py decompiler
- Procmon (Process Monitor) for Windows DLL enumeration
- Caido (public beta at caido.io) — Rust-based Burp alternative
- Franz Rosen's research on S3 signed URL authorization paths
- Juubobs' "SameSite Confusion" blog post

### Suggestions and Advices from Hunter
- "If you have a Windows native app, enumerate the Windows URI handlers" — Justin
- "Beware of capitalization in GraphQL — try different case on inputs" — Joel

### AI Takeaway
The decompilation pipeline mapping (.NET→dotPeek, Python→Uncompyle6, Java→JADX) is essential for anyone approaching compiled binaries in scope. The Windows URI handler attack surface is underutilized.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
DLL hijacking on Windows executables as exploitation technique (not always a valid vuln)

#### 2. What you should learn
- Understand **use ilspy or dotpeek to decompile .net/c# binaries back to source code**
- Understand **for python binaries: pyinstaller extractor → .pyc → uncompyle6 → .py**
- Understand **run `strings` or `objdump` on binaries to identify language (python, .net, c#, etc.)**
- Understand **enumerate windows uri handlers: powershell script that checks registry keys for url protocol associations**
- Understand **error messages can leak information via boolean logic or direct id disclosure**

#### 3. Core concepts explained
**[Implied] DLL Hijacking on Windows Binary**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Binary language identification**
- `strings`/`objdump` to detect Python, .NET, C# references

**Decompilation pipeline per language**
- .NET: dotPeek/ILSpy; Java: JADX/JD-GUI; Python: PyInstaller Extractor → Uncompyle6

**Windows URI handler enumeration**
- check registry `HKCR\*\shell\*\command` for protocol handlers


#### 4. Techniques and tactics
**Binary language identification**
- **What it is:** `strings`/`objdump` to detect Python, .NET, C# references
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Decompilation pipeline per language**
- **What it is:** .NET: dotPeek/ILSpy; Java: JADX/JD-GUI; Python: PyInstaller Extractor → Uncompyle6
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Windows URI handler enumeration**
- **What it is:** check registry `HKCR\*\shell\*\command` for protocol handlers
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**GraphQL field enumeration via error messages**
- **What it is:** send invalid input, error often reveals allowed values
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**SameSite Lax+POST timer reset**
- **What it is:** CSRF login/logout resets the 2-min timer for top-level POST requests
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you have a Windows native app, enumerate the Windows URI handlers"* — **Justin**
- *"Beware of capitalization in GraphQL"* — **try different case on inputs" — Joel**

#### 6. Mental models
- **If you have a Windows native app, enumerate the Windows URI ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Beware of capitalization in GraphQL — try different case on ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Use ILSpy or dotPeek to decompile .NET/C# binaries back to source code
- **Try this:** For Python binaries: PyInstaller Extractor → .pyc → Uncompyle6 → .py
- **Try this:** Run `strings` or `objdump` on binaries to identify language (Python, .NET, C#, etc.)
- **Try this:** Enumerate Windows URI handlers: PowerShell script that checks registry keys for URL protocol associations

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in [Implied] DLL Hijacking on Windows Binary?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **DLL hijacking on Windows executables as exploitation technique (not always a val**
2. **Use ILSpy or dotPeek to decompile .NET/C# binaries back to source code**
3. **For Python binaries: PyInstaller Extractor → .pyc → Uncompyle6 → .py**
