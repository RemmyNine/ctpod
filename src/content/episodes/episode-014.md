---
title: "Mobile Hacking Dynamic Analysis w/ Frida + Random Hacker Stuff"
episode: 14
---


# Episode 14 Mobile Hacking Dynamic Analysis w/ Frida + Random Hacker Stuff

### TL;DR
- Frida dynamic analysis for Android: SSL pinning bypass, root detection bypass, function hooking
- Frida setup: download server binary, ADB push to `/data/local/tmp`, chmod +x, disable SELinux (`setenforce 0`), run in daemon mode
- Frida commands: `frida -U` (USB device), `-l script.js` (load script), `-f com.package` (spawn), `-n AppName` (attach)
- Universal SSL unpin script hooks common cert pinning libraries (OkHttp, TrustKit, Android built-in)
- Root AVD tool to root Google Play Store Android emulator images
- scrcpy: display + control physical Android device from desktop over USB

### Key takeaways
- Use ADB `logcat` with PID filter to find root detection/cert pinning error messages
- Custom SSL pinning: find `TLSConfig.setVerifyServer()` — hook it with Frida to return false
- JADX-GUI: right-click function → "Copy as Frida snippet" automatically generates hook boilerplate
- For native library functions, use `setInterval()` + try/catch in Frida to poll until library loads
- Objection (mobile security multi-tool) as a general Swiss Army Knife for Android testing
- `adb reverse tcp:8080 tcp:8080` for proxying over USB (detailed in earlier episode)
- Physical device screen mirroring: `scrcpy` — available via apt/brew

### Bugs and Findings

#### Custom SSL Pinning Bypass + Impersonation Function — ATO (High)
- **Target/context:** Undisclosed care-team app
- **Root cause:** Custom SSL pinning implementation using `TLSConfig.setVerifyServer()` returning boolean; bypass → discovered "impersonate" API function
- **Technique / how found:**
  1. Joel's universal unpin script didn't work — custom pinning
  2. Found `TLSConfig` class in JADX; right-clicked function → "Copy as Frida snippet"
  3. Hover the function to return false → SSL decrypted
  4. Found `impersonate` endpoint taking userID → could impersonate any care-team member
- **Key technical details:** `TLSConfig.setVerifyServer()` boolean return; custom cert pinning
- **Impact / severity / bounty:** High; account takeover of care-team accounts

#### Uber Driver App Jailbreak Detection Bypass (Joel's first bug)
- **Target/context:** Uber driver app at H1-702 2017 (Joel's first live hacking event)
- **Root cause:** Client-side jailbreak detection checks — all hookable with Frida
- **Technique / how found:** Wrote comprehensive Frida script hooking all known root/jailbreak detection methods
- **Impact / severity / bounty:** Medium (program had a specific challenge for bypassing jailbreak detection)

### Techniques and Primitives
- **Frida SSL unpin workflow** — root device → push frida-server → chmod +x → `setenforce 0` → run server `-d` → `frida -U -l ssl-unpin.js -f com.app`
- **Root AVD** — tool to root Google Play images
- **JADX → Frida snippet** — right-click function → "Copy as Frida snippet"
- **Frida native library polling** — `setInterval()` with try/catch until native method resolves
- **scrcpy** — `apt install scrcpy`/`brew install scrcpy`

### Tooling and Resources
- Frida (frida-server + frida-tools via pip)
- Joel's universal SSL unpin script
- Objection (mobile security testing framework)
- Root AVD
- scrcpy (screen copy)
- ADB logcat
- Icos (Icos.blogspot.com) — "Using Frida on Android Without Root"

### Suggestions and Advices from Hunter
- "Most SSL pinning is security-through-obscurity; bypass it and you'll find bugs others miss" — Justin
- "For custom pinning, search for `check`, `verify`, `certificate`, `pinning` in the code" — Joel
- "Use JADX-GUI → right click → 'Copy as Frida snippet' to get hook boilerplate instantly" — Justin
- "scrcpy changes everything for physical device testing" — Joel

### AI Takeaway
The Frida hook generation from JADX-GUI is a game changer for mobile reverse engineering. The combination of static analysis (JADX → find function) + dynamic hooking (right-click → copy Frida snippet → overwrite return value) reduces SSL pinning bypass from hours to minutes. The key insight: custom pinning always ends in a boolean decision somewhere.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Frida dynamic analysis for Android: SSL pinning bypass, root detection bypass, function hooking

#### 2. What you should learn
- Understand **use adb `logcat` with pid filter to find root detection/cert pinning error messages**
- Understand **custom ssl pinning: find `tlsconfig.setverifyserver()` — hook it with frida to return false**
- Understand **jadx-gui: right-click function → "copy as frida snippet" automatically generates hook boilerplate**
- Understand **for native library functions, use `setinterval()` + try/catch in frida to poll until library loads**
- Understand **objection (mobile security multi-tool) as a general swiss army knife for android testing**

#### 3. Core concepts explained
**Custom SSL Pinning Bypass + Impersonation Function — ATO (High)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Uber Driver App Jailbreak Detection Bypass (Joel's first bug)**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Frida SSL unpin workflow**
- root device → push frida-server → chmod +x → `setenforce 0` → run server `-d` → `frida -U -l ssl-unpin.js -f com.app`

**Root AVD**
- tool to root Google Play images

**JADX → Frida snippet**
- right-click function → "Copy as Frida snippet"


#### 4. Techniques and tactics
**Frida SSL unpin workflow**
- **What it is:** root device → push frida-server → chmod +x → `setenforce 0` → run server `-d` → `frida -U -l ssl-unpin.js -f com.app`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Root AVD**
- **What it is:** tool to root Google Play images
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**JADX → Frida snippet**
- **What it is:** right-click function → "Copy as Frida snippet"
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Frida native library polling**
- **What it is:** `setInterval()` with try/catch until native method resolves
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**scrcpy**
- **What it is:** `apt install scrcpy`/`brew install scrcpy`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Most SSL pinning is security-through-obscurity; bypass it and you'll find bugs others miss"* — **Justin**
- *"For custom pinning, search for `check`, `verify`, `certificate`, `pinning` in the code"* — **Joel**
- *"Use JADX-GUI → right click → 'Copy as Frida snippet' to get hook boilerplate instantly"* — **Justin**
- *"scrcpy changes everything for physical device testing"* — **Joel**

#### 6. Mental models
- **Most SSL pinning is security-through-obscurity; bypass it an** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For custom pinning, search for `check`, `verify`, `certifica** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Use JADX-GUI → right click → 'Copy as Frida snippet' to get ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Use ADB `logcat` with PID filter to find root detection/cert pinning error messages
- **Try this:** Custom SSL pinning: find `TLSConfig.setVerifyServer()` — hook it with Frida to return false
- **Try this:** JADX-GUI: right-click function → "Copy as Frida snippet" automatically generates hook boilerplate
- **Try this:** For native library functions, use `setInterval()` + try/catch in Frida to poll until library loads

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Custom SSL Pinning Bypass + Impersonation Function — ATO (High)?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Frida dynamic analysis for Android: SSL pinning bypass, root detection bypass, f**
2. **Use ADB `logcat` with PID filter to find root detection/cert pinning error messa**
3. **Custom SSL pinning: find `TLSConfig.setVerifyServer()` — hook it with Frida to r**
