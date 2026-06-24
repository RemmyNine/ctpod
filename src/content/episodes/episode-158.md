---
title: "10hr Marathon Hack-Along Recap"
episode: 158
---


# Episode 158 10hr Marathon Hack-Along Recap

### TL;DR
- Charity hackalong recap: postMessage race condition, partial auth states, permission delegation to iframes
- InsertScript's `event.source = null` technique explained
- Meta Conversion API Gateway XSS ($300K in bugs)
- Claude Code security bypasses by Ryotak (Flat Security): 8 ways to escape allowed command lists
- Trail of Bits Claude Skills release

### Bugs and Findings

#### PostMessage Race Condition via Window Open + Dimensions
- **Target/context:** SaaS platform (hackalong target)
- **Root cause:** Race condition between legitimate postMessage init and attacker postMessage — window throttling prevented reliable timing
- **Technique / how solved:** Used `window.open(url, '_blank', 'width=500,height=500')` to create a visible popup → browser doesn't throttle JS execution → postMessages fire reliably
- **Code pattern found:** `if (event.source === allowedFrame || event.secret === expectedSecret)` — when secret not yet set, it's `undefined`; sending without secret bypasses the check

#### Camera/Microphone Permission Delegation to Attacker Iframe
- **Target/context:** Any website with permanent camera/mic permissions + iframes with `allow` attribute
- **Root cause:** Chrome delegates hardware permissions to iframes with `allow="camera; microphone"` when the top-level page has permanent permission
- **Exploitation steps:**
  1. Find a page where user has granted permanent camera/mic access
  2. Embed attacker-controlled iframe with `allow="camera; microphone"`
  3. Permission is delegated to attacker iframe
  4. Record audio/video without further prompts
- **Impact:** Unauthorized camera/mic access; legacy behavior unlikely to be fixed

#### Meta Conversion API Gateway XSS Chain
- **Target/context:** Meta (Facebook) Conversion API Gateway
- **Root cause:** PostMessage listener without origin check set a localStorage key → used to load a JS file
- **Technique / how found:** Open-source code review of the gateway; found string-concatenation JSON generation in decompiled JAR from ECR
- **Exploitation steps:**
  1. PostMessage without origin check → write localStorage key
  2. Bypass CSP using a page with relaxed CSP (more third-parties allowed)
  3. Bypass COOP using Facebook Android WebView quirk: `window.name = "test"` + `window.open("test")` → keeps opener reference
  4. Pwn third-party server (full RCE) to hijack iframe
  5. Host JS on compromised third-party, load on Meta's domain → XSS
- **Key technical details:** IDOR in gateway allows configuring rules for any pixel; string concatenation in dynamic JS generation; COOP bypass via Android WebView window.name trick
- **Impact:** $65K + $250K bugs; arbitrary JS execution on Meta domains

#### Claude Code 8 Bypasses (Ryotak/Flat Security)
- **Target/context:** Claude Code's allowed-commands list
- **Root cause:** Whitelist implemented via regex — multiple bypasses found
- **Bypass techniques:**
  1. `man --html=touch /tmp/poned` — man's `--html` flag specifies custom renderer
  2. `sort --compress-program=id` — sort's compression program flag
  3. `history -a; history -s 'id'` — history command options
  4. Git argument abbreviation: `git ls-remote --upload-pack` abbreviated to `--upload-pa` (Git auto-completes)
  5. `sed -i 's/foo/bar/g' -e '!id'` — sed's `-e` flag with shell execution
  6. `xargs -t touch echo id` — `-t` is boolean, so `touch` becomes the next command to execute
  7. `rg -z id` — ripgrep with gzip flag
  8. `bash -c 'echo ${x@P}'` — `${var@P}` modifier parses value as prompt string → `$()` in prompt becomes command substitution
- **Impact:** Full RCE bypassing Claude Code permission system

### Techniques and Primitives
**CRLF in Location Header on 302** — If you control the full Location header and can start it with `\r\n`, the 302 redirect page renders HTML allowing XSS (even on 302)

**iframe Permission Inheritance** — Iframes with `allow="camera; microphone"` on a page with permanent camera/mic permissions get delegated access

### Suggestions and Advices from Hunter
- Justin's quote from Yousef's write-up: "When JavaScript is shared across projects, domains and customers, it becomes a part of the platform's trusted computing base. At that point, origin validation, strict CSP design and safe code generation are no longer optional. They are existential requirements."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Charity hackalong recap: postMessage race condition, partial auth states, permission delegation to iframes

#### 2. What you should learn
- Learn about **charity hackalong recap: postmessage race condition, partial auth states, permission delegation to iframes**
- Learn about **insertscript's `event.source = null` technique explained**
- Learn about **meta conversion api gateway xss ($300k in bugs)**
- Learn about **claude code security bypasses by ryotak (flat security): 8 ways to escape allowed command lists**
- Learn about **trail of bits claude skills release**

#### 3. Core concepts explained
**PostMessage Race Condition via Window Open + Dimensions**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Camera/Microphone Permission Delegation to Attacker Iframe**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Meta Conversion API Gateway XSS Chain**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Justin's quote from Yousef's write-up: "When JavaScript is shared across projects, domains and customers, it becomes a part of the platform's trusted computing base. At that point, origin validation, strict CSP design and safe code generation are no longer optional. They are existential requirements."*

#### 6. Mental models
- **Justin's quote from Yousef's write-up: "When JavaScript is s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- - Technique / how solved: Used `window.open(url, '_blank', 'width=500,height=500')` to create a visible popup → browser doesn't throttle JS execution → postMessages fire reliably

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in PostMessage Race Condition via Window Open + Dimensions?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Charity hackalong recap: postMessage race condition, partial auth states, permis**
