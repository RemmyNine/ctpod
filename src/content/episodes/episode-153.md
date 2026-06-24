---
title: "Hacking Robots with Matt Brown"
episode: 153
---


# Episode 153 Hacking Robots with Matt Brown

### TL;DR
- Hardware hacking methodology: debug interfaces (UART, JTAG, USB/ADB) → firmware extraction → binary reverse engineering → gray-box web hacking
- Matt Brown's IoT Hackbot: Claude Code + skills for picocom, ONVIF camera control → AI-driven hardware exploitation
- Zero-to-Hero hardware hacking guide: start with $20 Goodwill routers, practice UART/SPI extraction, use logic analyzers

### Bugs and Findings

#### Incremental Session Token in Industrial Control System — IDOR
- **Target/context:** Industrial control system remote-view device
- **Root cause:** Server-side session tokens were incremental integers (not Unix timestamps as they appeared)
- **Technique / how found:** Wireshark on device traffic → saw cleartext UDP data with session info; decompiled mobile app, unpinned certs with Frida, found incremental session token; entire fleet shared the same incremental sequence
- **Exploitation steps:**
  1. Monitor device traffic with Wireshark
  2. Unpin mobile app with Frida to see HTTPS traffic
  3. Identify session token that was nearly a Unix timestamp but offset
  4. Initiate session on own device, then walk forward/backward the session ID
  5. Remotely connect to other people's industrial control sessions
- **Impact:** Remote access to any active industrial control session
- **Obstacles & how solved:** Token looked like Unix timestamp but didn't match exact epoch — was incrementing at millisecond/second level with an offset

### Techniques and Primitives
**Hardware Recon** — FCC ID Lookup (fccid.io) for wireless device internals; GROK/Claude for CVE research on known components; open device and photograph all chips → Google part numbers

**Debug Interface Enumeration** — UART for Linux systems; JTAG/SWD for microcontrollers; USB/ADB for Android devices. Use logic analyzer (Saleae or $20 knockoff) to decode inter-chip communication

**Firmware Extraction Flow**:
1. Identify flash chip (EMMC, SPI flash, TSOP-48)
2. Use XGECU programmer with appropriate socket
3. Run `binwalk -e` on the binary
4. If binwalk fails, use UART boot logs to get partition table offsets → `dd` to carve partitions

**IoT Hackbot via Claude Code**:
- Create Claude Skills for tools (picocom, ONVIF fuzzer, binary protocol testers)
- Claude Code gets a root shell on device → can enumerate, craft exploits, and observe stdout/stderr from the target binary
- Provide decompiled source code (from Ghidra/Binary Ninja) as context

### Suggestions and Advices from Hunter
- "Hardware hacking is a means to an end of hacking on software. It turns a black box assessment into a gray box assessment."
- "If you have a debug interface with a shell on a Linux device, you can view running processes, find what's listening on what port, and know exactly where to look in the firmware."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Hardware hacking methodology: debug interfaces (UART, JTAG, USB/ADB) → firmware extraction → binary reverse engineering → gray-box web hacking

#### 2. What you should learn
- Learn about **hardware hacking methodology: debug interfaces (uart, jtag, usb/adb) → firmware extraction → binary reverse engineering → gray-box web hacking**
- Learn about **matt brown's iot hackbot: claude code + skills for picocom, onvif camera control → ai-driven hardware exploitation**
- Learn about **zero-to-hero hardware hacking guide: start with $20 goodwill routers, practice uart/spi extraction, use logic analyzers**

#### 3. Core concepts explained
**Incremental Session Token in Industrial Control System — IDOR**
- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.
- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.
- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.

**Create Claude Skills for tools (picocom, ONVIF fuzzer, binary protocol testers)**
- A technique discussed in this episode for security research and bug bounty hunting.

**Claude Code gets a root shell on device → can enumerate, craft exploits, and observe stdout/stderr from the target binary**
- A technique discussed in this episode for security research and bug bounty hunting.

**Provide decompiled source code (from Ghidra/Binary Ninja) as context**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**Create Claude Skills for tools (picocom, ONVIF fuzzer, binary protocol testers)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Claude Code gets a root shell on device → can enumerate, craft exploits, and observe stdout/stderr from the target binary**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Provide decompiled source code (from Ghidra/Binary Ninja) as context**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Hardware hacking is a means to an end of hacking on software. It turns a black box assessment into a gray box assessment."*
- *"If you have a debug interface with a shell on a Linux device, you can view running processes, find what's listening on what port, and know exactly where to look in the firmware."*

#### 6. Mental models
- **Hardware hacking is a means to an end of hacking on software** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you have a debug interface with a shell on a Linux device** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Token looked like Unix timestamp but didn't match exact epoch — was incrementing at millisecond/second level with an offset

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Incremental Session Token in Industrial Control System — IDOR?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Hardware hacking methodology: debug interfaces (UART, JTAG, USB/ADB) → firmware **
