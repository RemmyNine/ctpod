---
title: "The Hacker's Toolkit"
episode: 16
---


# Episode 16 The Hacker's Toolkit

### TL;DR
- Every tool in The Hacker's Toolkit: FeroxBuster, FFUF, Caido, Burp, HTTPx, Go Witness, JQ, ripgrep, fzf, VIM tricks
- Automation infrastructure: zero-tier VPN for NFS sharing across home server + cloud VPS + laptop
- VIM life hacks: `:w !sudo tee %` to write read-only files; `:x` to save and quit
- Storing recon data: NFS mount shared across devices via zero-tier; folder structure: `/targets/<name>/`, `/tools/<category>/`
- Burp/Kaito workflow: Caido for daily web, Burp for mobile/legacy needs
- source code review: VSCode + extensions (Todo Highlight) for code flow analysis

### Key takeaways
- FeroxBuster: Rust-based, recursive, fast; FFUF for complex fuzzing (cookie/header placement)
- HTTPx: pipe `gau` output to HTTPx for quick status code/content-type filtering
- Go Witness: screenshot masses of URLs; dedupe by MD5 hash of screenshot to find unique pages
- `:w !sudo tee %` in VIM: saves read-only file by piping buffer through sudo tee
- `:x` in VIM: saves and quits (write only if modified)
- `dd` in VIM: delete current line; `yy` yank; `p` paste; `.` repeat last change
- Control+P in VSCode: file switcher; Control+Shift+P: command palette
- Todo Highlight extension for VSCode: marks TODO comments, shows in tree sidebar

### Bugs and Findings

#### DNS Shell via DNSchef — Establishing Reliable C2 in VDI Environment
- **Target/context:** Client's VDI environment with strict HTTP/HTTPS allowlist
- **Root cause:** DNS outbound was not filtered — could be abused as C2 channel
- **Technique / how found:**
  1. Used DNSchef as DNS server on own infrastructure
  2. Hooked into TXT record handling in DNSchef's code
  3. Wrote Python client that sends DNS TXT queries to attacker server → hex-encoded response → execute locally
- **Key technical details:** DNS TXT record as C2 channel; DNSchef framework; hex encoding for binary data
- **Impact / severity / bounty:** Established reliable shell out of VDI (reward for completing the challenge)

### Techniques and Primitives
- **Zero-tier VPN + NFS** — share recon data across devices via zero-tier private network; mount NFS on all devices
- **Burp → Caido transition** — Caido for web, Burp for mobile (Android proxying)
- **VIM `:w !sudo tee %`** — write read-only files by piping buffer through sudo
- **VSCode Todo Highlight** — mark steps in code analysis with TODO: comments, navigate via tree
- **DNS C2 via DNSchef** — hook TXT record handler; encode commands in DNS queries
- **Wildcard cert on POC domain** — `*.poc.runerator.com` for hosting POC payloads with valid TLS

### Tooling and Resources
- FeroxBuster (Rust content discovery)
- FFUF (Go fuzzer)
- Caido (Rust Burp alternative)
- HTTPx (Go HTTP toolkit by ProjectDiscovery)
- Go Witness (Go screenshot utility)
- JQ (JSON processor), ripgrep (rg)
- fzf (fuzzy finder)
- Zero-tier (VPN alternative) / Tailscale
- DNSchef
- VSCode + Todo Highlight extension

### Suggestions and Advices from Hunter
- "If the same task takes you 5+ minutes and you do it regularly, automate it" — Justin
- "Caido + Burp is my combo: Caido is catching up fast, plugin system coming" — Justin
- "Zero-tier for NFS: mount your VPS drives on your laptop, no more SCP" — Joel
- "Learn VIM properly; the buffer piping (`:w !sudo tee %`) alone is worth it" — Joel

### AI Takeaway
The VIM `:w !sudo tee %` technique and the VSCode `:x` shortcut are tiny changes with outsized impact on workflow speed. The GOWitness + MD5 dedup methodology for large-scale recon is a practical approach to filtering thousands of screenshots.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Every tool in The Hacker's Toolkit: FeroxBuster, FFUF, Caido, Burp, HTTPx, Go Witness, JQ, ripgrep, fzf, VIM tricks

#### 2. What you should learn
- Understand **feroxbuster: rust-based, recursive, fast; ffuf for complex fuzzing (cookie/header placement)**
- Understand **httpx: pipe `gau` output to httpx for quick status code/content-type filtering**
- Understand **go witness: screenshot masses of urls; dedupe by md5 hash of screenshot to find unique pages**
- Understand **`:w !sudo tee %` in vim: saves read-only file by piping buffer through sudo tee**
- Understand **`:x` in vim: saves and quits (write only if modified)**

#### 3. Core concepts explained
**DNS Shell via DNSchef — Establishing Reliable C2 in VDI Environment**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Zero-tier VPN + NFS**
- share recon data across devices via zero-tier private network; mount NFS on all devices

**Burp → Caido transition**
- Caido for web, Burp for mobile (Android proxying)

**VIM `:w !sudo tee %`**
- write read-only files by piping buffer through sudo


#### 4. Techniques and tactics
**Zero-tier VPN + NFS**
- **What it is:** share recon data across devices via zero-tier private network; mount NFS on all devices
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Burp → Caido transition**
- **What it is:** Caido for web, Burp for mobile (Android proxying)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**VIM `:w !sudo tee %`**
- **What it is:** write read-only files by piping buffer through sudo
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**VSCode Todo Highlight**
- **What it is:** mark steps in code analysis with TODO: comments, navigate via tree
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**DNS C2 via DNSchef**
- **What it is:** hook TXT record handler; encode commands in DNS queries
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If the same task takes you 5+ minutes and you do it regularly, automate it"* — **Justin**
- *"Caido + Burp is my combo: Caido is catching up fast, plugin system coming"* — **Justin**
- *"Zero-tier for NFS: mount your VPS drives on your laptop, no more SCP"* — **Joel**
- *"Learn VIM properly; the buffer piping (`:w !sudo tee %`) alone is worth it"* — **Joel**

#### 6. Mental models
- **If the same task takes you 5+ minutes and you do it regularl** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Caido + Burp is my combo: Caido is catching up fast, plugin ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Zero-tier for NFS: mount your VPS drives on your laptop, no ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** FeroxBuster: Rust-based, recursive, fast; FFUF for complex fuzzing (cookie/header placement)
- **Try this:** HTTPx: pipe `gau` output to HTTPx for quick status code/content-type filtering
- **Try this:** Go Witness: screenshot masses of URLs; dedupe by MD5 hash of screenshot to find unique pages
- **Try this:** `:w !sudo tee %` in VIM: saves read-only file by piping buffer through sudo tee

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **DNS** — Domain Name System — translates domain names to IP addresses
- **Burp** — Burp Suite — popular web application security testing proxy
- **recon** — Reconnaissance — systematic discovery of target attack surface
- **fuzzing** — Sending unexpected or malformed data to discover vulnerabilities

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in DNS Shell via DNSchef — Establishing Reliable C2 in VDI Environment?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Every tool in The Hacker's Toolkit: FeroxBuster, FFUF, Caido, Burp, HTTPx, Go Wi**
2. **FeroxBuster: Rust-based, recursive, fast; FFUF for complex fuzzing (cookie/heade**
3. **HTTPx: pipe `gau` output to HTTPx for quick status code/content-type filtering**
