---
title: "Our Take on PortSwigger's Top 10 Web Hacking Techniques of 2023"
episode: 60
---


# Episode 60 Our Take on PortSwigger's Top 10 Web Hacking Techniques of 2023

**Guests:** Justin Gardner, Joel Margolis
**Format:** Show notes with timestamps (feed)
**Topics:** Smashing the state machine (#1), From Akamai to F5 to NTLM (#8), SMTP smuggling (#3), PHP filter chains (#4), HTTP parsers inconsistencies (#5), HTTP request splitting (#6), How I Hacked Microsoft Teams (#7), Cookie Crumbles (#9), EPP server takeover (#10)

### TL;DR
- James Kettle's "Smashing the state machine" (#1) — send last byte of multiple HTTP/2 requests in a single TCP packet so they arrive simultaneously at the server, enabling sub-millisecond race conditions
- Akamai → F5 BigIP → NTLM hash theft (#8): HTTP request smuggling through Akamai edge servers → cache poison BigIP → redirect to trigger NTLM auth → capture hashes via Responder
- PHP filter chains (#4): chain PHP filters (UTF-8, rot13, dechunk, iconv encodings) to create an error-based oracle reading arbitrary files byte-by-byte with no echo sink — only needs a `file()` call
- Microsoft Teams Electron RCE at Pwn2Own (#7): bypassed `contextIsolation=true` and `nodeIntegration=false` by exploiting XSS + preload script gadgets
- HTTP parsers inconsistencies (#5): Nginx + backend language mismatches — backslash XA0 bypasses Nginx rules but gets stripped by Node's trim()

### Key Takeaways
- For race conditions: HTTP/2 single-packet attack = group requests, withhold final byte + END_STREAM flag, send all at once
- PHP filter chain generator is available — from LFI with no upload, read arbitrary files byte-by-byte via error oracle
- Detection method for request splitting: `space X` → non-400 error vs `space H` → 400 (Nginx interprets H as start of HTTP version)
- For HTTP smuggling detection: `space HTTP/13.37\r\n` → 505 error from backend
- Electron RCE checklist: check `nodeIntegration`, `contextIsolation`, `sandbox` in BrowserWindow instantiation — bypass preload script restrictions via prototype pollution or gadget chains in `contextBridge`

### Bugs and Findings

#### Microsoft Teams Electron RCE (Pwn2Own 2023 — Masato Kinugawa)
- **Target/context:** Microsoft Teams desktop app (Electron)
- **Root cause:** XSS in the app + preload script with `postMessage` listener that did `location.href = msg.url` → open redirect gadget
- **Obstacles:**
  - `nodeIntegration: false` — require() not available from renderer
  - `contextIsolation: true` — preload script runs in isolated context
  - `sandbox: true` (likely) — further restricted
  - Found a preload script with `postMessage` listener setting `location.href` to a message origin → open redirect
- **Exploitation steps:**
  1. Pop XSS in the renderer
  2. Send postMessage to trigger `location.href = attackerURL`
  3. Redirect to `file:///` or a custom protocol handler (provided the redirect target is controlled)
  4. Chain with additional gadgets to escape the preload context → full RCE
- **Bounty:** $150,000 (Pwn2Own)

### Tooling and Resources
- Burp "send in parallel" feature for HTTP/2 single-packet race conditions
- PHP filter chain generator (by Synactiv — "PHP filter chains: file read from error-based oracle")
- ConfuserEx (for renaming .NET function names to bypass AV/EDR)
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
James Kettle's "Smashing the state machine" (#1) — send last byte of multiple HTTP/2 requests in a single TCP packet so they arrive simultaneously at the server, enabling sub-millisecond race conditions

#### 2. What you should learn
- Understand **for race conditions: http/2 single-packet attack = group requests, withhold final byte + end_stream flag, send all at once**
- Understand **php filter chain generator is available — from lfi with no upload, read arbitrary files byte-by-byte via error oracle**
- Understand **detection method for request splitting: `space x` → non-400 error vs `space h` → 400 (nginx interprets h as start of http version)**
- Understand **for http smuggling detection: `space http/13.37\r\n` → 505 error from backend**
- Understand **electron rce checklist: check `nodeintegration`, `contextisolation`, `sandbox` in browserwindow instantiation — bypass preload script restrictions via prototype pollution or gadget chains in `contextbridge`**

#### 3. Core concepts explained
**Microsoft Teams Electron RCE (Pwn2Own 2023 — Masato Kinugawa)**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.


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
- **Try this:** For race conditions: HTTP/2 single-packet attack = group requests, withhold final byte + END_STREAM flag, send all at once
- **Try this:** PHP filter chain generator is available — from LFI with no upload, read arbitrary files byte-by-byte via error oracle
- **Try this:** Detection method for request splitting: `space X` → non-400 error vs `space H` → 400 (Nginx interprets H as start of HTTP version)
- **Try this:** For HTTP smuggling detection: `space HTTP/13.37\r\n` → 505 error from backend

#### 8. Red flags and pitfalls
- - Obstacles:

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Microsoft Teams Electron RCE (Pwn2Own 2023 — Masato Kinugawa)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **James Kettle's "Smashing the state machine" (#1) — send last byte of multiple HT**
2. **For race conditions: HTTP/2 single-packet attack = group requests, withhold fina**
3. **PHP filter chain generator is available — from LFI with no upload, read arbitrar**
