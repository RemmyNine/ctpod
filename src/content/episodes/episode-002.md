---
title: "Exploit Writing & Automation / Do you need to know how to program to hack?"
episode: 2
---


# Episode 2 Exploit Writing & Automation / Do you need to know how to program to hack?

### TL;DR
- Justin found an arbitrary account takeover via MD5-hashed password reset tokens (email+Unix timestamp concatenated then MD5'd)
- IoT device teardown: heat gun + EMMC adapter → firmware dump → Android app reverse engineering
- Brute-forcing a 4-digit PIN (9000 possibilities, 10 attempts per session) on an IoT casting protocol by replicating the crypto handshake in Python/Java
- ADB forward/reverse for mobile proxying, Chromium DevTools Protocol (port 9222) for headless browser exploitation
- Python scripts vs Bash for rapid prototyping; Shubs advice: prototype fast, scale horizontally

### Key takeaways
- Always check password reset token hashes: if MD5, try concatenating email + timestamp format and brute-force recent timestamps
- Use `adb reverse tcp:8080 tcp:8080` to proxy Android traffic through Burp over USB
- For IoT: remove EMMC chip with heat gun (300°C), use EMMC-to-SD adapter, dump partitions, mount and extract filesystem
- For Android crypto reversing: if it's Java, just run the decompiled Java on your local JVM
- When brute-forcing things with rate limits, calculate odds: 9000 possibilities, 10 tries per session = 1:900 per session
- Prototype fast, don't over-engineer; scale horizontally when needed

### Bugs and Findings

#### Password Reset Token Hash Predictable — Account Takeover (High)
- **Target/context:** Undisclosed web application
- **Root cause:** Password reset token = MD5(email + Unix timestamp of submission)
- **Technique / how found:** Noticed the reset token was an MD5 hash; wrote a Python script that generated hashes for ~15 formats (email+timestamp variants) across recent timestamps
- **Exploitation steps:**
  1. Trigger password reset for victim
  2. Run script that generates MD5 hashes of email+timestamp for last ~15 seconds of Unix timestamps
  3. Submit each hash as the reset token
  4. Token matched → arbitrary account takeover
- **Key technical details:** `MD5(user_email + unix_timestamp)` as reset token; token predictable within seconds of submission
- **Impact / severity / bounty:** Rated High (not Critical) by program; Justin argued it should be Critical
- **Obstacles & how solved:** Needed to guess timestamp within ~15 seconds; solved by rapid iteration

#### IoT Device 4-Digit PIN Brute Force — Full Device Takeover
- **Target/context:** Undisclosed Android-based IoT tablet with custom casting/pairing protocol
- **Root cause:** 4-digit PIN (1000–9999 = 9000 possibilities), 10 attempts per session before reset, but sessions could be restarted infinitely with no rate limiting
- **Technique / how found:** Hardware dumped firmware via EMMC chip removal; reversed Android apps; found custom crypto handshake protocol on port 8009; re-implemented the protocol in Python (then Java) to brute force the PIN
- **Exploitation steps:**
  1. Joel removed EMMC chip with heat gun + flux paste, used EMMC-to-SD adapter, dumped and mounted partitions
  2. Extracted and reversed Android APKs
  3. Found custom casting protocol on port 8009 with 4-char PIN and crypto handshake
  4. Spent days replicating the crypto flow in Python, switched to Java (same language as server) for interoperability
  5. Brute forced PIN: 10 tries/session, restart session after 10 failures, ~30 seconds average to hit correct PIN
  6. Once paired with the device, gained persistence (key cached)
- **Key technical details:** Port 8009; 4-char PIN between 1000-9999; custom pairing protocol with crypto handshake; rolling key exchange
- **Impact / severity / bounty:** Full device takeover + persistence; bounty amount undisclosed
- **Obstacles & how solved:** Crypto handshake was complex to replicate; solved by switching to Java (same language as the Android app) for library compatibility; brute force optimization

### Techniques and Primitives
- **EMMC firmware extraction** — heat gun to desolder BGA chip → EMMC-to-SD adapter → `dd` dump → mount partitions → extract filesystem
- **MD5 token prediction** — if reset token is MD5, try email+timestamp concatenation with recent timestamps
- **Crypto protocol replication in same language** — when reversing crypto, use the same language the target uses (Java→Java, not Python)
- **Horizontal scaling over optimization** — Shubs: "prototype fast, scale horizontally"
- **307 redirect for POST preservation** — for CSRF/XSS chains requiring POST

### Tooling and Resources
- Heat gun (300°C), flux paste, EMMC-to-SD adapter
- APKTool, JADX
- Flipper Zero (RogueMaster firmware mentioned)
- curlconverter.com (convert curl to Python/JS/Go/etc.)
- CyberChef (drag-and-drop data transformation)
- Caido (Burp alternative)
- VSCode

### Suggestions and Advices from Hunter
- "If you're trying to reverse crypto stuff, use the language and the library that you know in the same language of the server" — Justin
- "Just take Java and just run it on your computer. Copy paste the code and get all the Android specific stuff out of there and just run it locally" — Joel
- "Scale when it needs to scale and do it the fastest way" — Joel on automation
- "Your first version of your product isn't embarrassing, then you've launched too late" — Reid Hoffman quote via Justin

### AI Takeaway
The IoT PIN brute force is a textbook example of combining hardware extraction, firmware reversing, protocol analysis, and cryptographic replication into one exploitation chain. The key lesson: when dealing with Android Java code, just run it directly on a JVM rather than trying to reimplement it.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Justin found an arbitrary account takeover via MD5-hashed password reset tokens (email+Unix timestamp concatenated then MD5'd)

#### 2. What you should learn
- Understand **always check password reset token hashes: if md5, try concatenating email + timestamp format and brute-force recent timestamps**
- Understand **use `adb reverse tcp:8080 tcp:8080` to proxy android traffic through burp over usb**
- Understand **for iot: remove emmc chip with heat gun (300°c), use emmc-to-sd adapter, dump partitions, mount and extract filesystem**
- Understand **for android crypto reversing: if it's java, just run the decompiled java on your local jvm**
- Understand **when brute-forcing things with rate limits, calculate odds: 9000 possibilities, 10 tries per session = 1:900 per session**

#### 3. Core concepts explained
**Password Reset Token Hash Predictable — Account Takeover (High)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**IoT Device 4-Digit PIN Brute Force — Full Device Takeover**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**EMMC firmware extraction**
- heat gun to desolder BGA chip → EMMC-to-SD adapter → `dd` dump → mount partitions → extract filesystem

**MD5 token prediction**
- if reset token is MD5, try email+timestamp concatenation with recent timestamps

**Crypto protocol replication in same language**
- when reversing crypto, use the same language the target uses (Java→Java, not Python)


#### 4. Techniques and tactics
**EMMC firmware extraction**
- **What it is:** heat gun to desolder BGA chip → EMMC-to-SD adapter → `dd` dump → mount partitions → extract filesystem
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**MD5 token prediction**
- **What it is:** if reset token is MD5, try email+timestamp concatenation with recent timestamps
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Crypto protocol replication in same language**
- **What it is:** when reversing crypto, use the same language the target uses (Java→Java, not Python)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Horizontal scaling over optimization**
- **What it is:** Shubs: "prototype fast, scale horizontally"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**307 redirect for POST preservation**
- **What it is:** for CSRF/XSS chains requiring POST
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you're trying to reverse crypto stuff, use the language and the library that you know in the same language of the server"* — **Justin**
- *"Just take Java and just run it on your computer. Copy paste the code and get all the Android specific stuff out of there and just run it locally"* — **Joel**
- *"Scale when it needs to scale and do it the fastest way"* — **Joel on automation**
- *"Your first version of your product isn't embarrassing, then you've launched too late"* — **Reid Hoffman quote via Justin**

#### 6. Mental models
- **If you're trying to reverse crypto stuff, use the language a** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Just take Java and just run it on your computer. Copy paste ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Scale when it needs to scale and do it the fastest way" — Jo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Always check password reset token hashes: if MD5, try concatenating email + timestamp format and brute-force recent timestamps
- **Try this:** Use `adb reverse tcp:8080 tcp:8080` to proxy Android traffic through Burp over USB
- **Try this:** For IoT: remove EMMC chip with heat gun (300°C), use EMMC-to-SD adapter, dump partitions, mount and extract filesystem
- **Try this:** For Android crypto reversing: if it's Java, just run the decompiled Java on your local JVM

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Needed to guess timestamp within ~15 seconds; solved by rapid iteration
- - Obstacles & how solved: Crypto handshake was complex to replicate; solved by switching to Java (same language as the Android app) for library compatibility; brute force optimization

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Password Reset Token Hash Predictable — Account Takeover (High)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Justin found an arbitrary account takeover via MD5-hashed password reset tokens **
2. **Always check password reset token hashes: if MD5, try concatenating email + time**
3. **Use `adb reverse tcp:8080 tcp:8080` to proxy Android traffic through Burp over U**
