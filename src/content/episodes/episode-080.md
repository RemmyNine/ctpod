---
title: "Pwn2Own VS H1 Live Hacking Event (feat SinSinology)"
episode: 80
---


# Episode 80 Pwn2Own VS H1 Live Hacking Event (feat SinSinology)

**TL;DR**
- Sina Kheirkhah (SinSinology) journey from web dev to binary exploitation to Pwn2Own
- IoT hacking methodology: UART/JTAG for initial shell, glitching for console bypass, firmware extraction via chip desoldering
- Debugger is essential: JDWP for Java, Dnspy/DnspyEx for .NET, GDB for embedded
- .NET optimization issue: breakpoints won't hit until you de-optimize with `.ini` file
- Pwn2Own focus on full-chain RCE vs H1 LHE focus on web bugs

**Key Takeaways**
- When you can't get .NET debugger breakpoints to hit, create a `<executable>.ini` file next to the image with optimization disabled
- Java debugging: find the start command (`.sh` file), add JDWP arguments to expose a debug port, connect remotely
- For IoT: try to get a shell via UART before attempting chip extraction; if UART is password-protected, try glitching
- The process of reproducing other researchers' exploits (especially Stephen Sealey's) is the single best way to learn binary exploitation
- When choosing between volume (many mediums) and impact (few crits), deep expertise on one application beats spraying

**Bugs and Findings**
(No specific disclosed bugs; this is a methodology episode.)

**Techniques and Primitives**
- **.NET debugger de-optimization** — Create `MyApp.exe.ini` with `[.NET Framework Debugging Control]` + `AllowOptimize=0` to enable breakpoints on optimized assemblies
- **JDWP for remote Java debugging** — Add `-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005` to the Java start command, expose the port
- **IoT initial shell via UART** — Identify UART pins on the PCB (4 pins: VCC, GND, TX, RX), connect with USB-UART adapter at common baud rates (115200, 57600)

**Tooling and Resources**
- `dnspyex.github.io` — DnspyEx (.NET debugger maintained by electrokill, age 19-20)
- `github.com/aapooksman/certmitm` — certmitm tool
- Sina's .NET exploitation training (August 2024, 25 seats filled)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 80 Pwn2Own VS H1 Live Hacking Event (feat SinSinology) covers practical bug bounty techniques and security research insights.

#### 2. What you should learn
- Understand the vulnerability classes discussed
- Learn practical exploitation techniques
- Know which tools are useful for this type of research

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


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
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Understand the vulnerability class** — Know how it works and why it matters
2. **Master the exploitation technique** — Practice the specific steps to exploit it
3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets
