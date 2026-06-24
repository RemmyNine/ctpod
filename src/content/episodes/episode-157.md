---
title: "Kernel Driver Exploits with Hypr"
episode: 157
---


# Episode 157 Kernel Driver Exploits with Hypr

### TL;DR
- Hypr (Enrique) discusses MediaTek kernel driver heap overflow (CVE-2025-27422) and broader kernel exploitation
- Found MediaTek driver source code leaked in Netgear GPL package
- Exploited ioctl handler reachable without authentication → heap overflow → free list pointer corruption → modprobe path overwrite → LPE → shell
- No debugger available — blind exploitation via trial-and-error with 10,000+ reboots
- pwn2own vs HackerOne ecosystem comparison

### Bugs and Findings

#### MediaTek Kernel Driver Heap Overflow (CVE-2025-27422) — LPE
- **Target/context:** MediaTek Wi-Fi drivers on Netgear routers (and many other devices including Starlink)
- **Root cause:** ioctl handler copies data from userland structure to kernel structure using a `char`-type size field (max 255) without bounds checking
- **Technique / how found:** Source code review — found MediaTek SDK source in Netgear's GPL package; iwpriv utility exposes ioctl handlers; fuzzed ioctl codes with `0x0000` to `0xFFFF`
- **Exploitation steps:**
  1. ioctl handler reachable without authentication
  2. Heap overflow → corrupt free list pointer in slab allocator
  3. Arbitrary allocation at controlled address
  4. Overwrite `modprobe_path` kernel variable (string path to modprobe binary)
  5. Create fake non-ELF binary → kernel tries to execute it → invokes modprobe → runs attacker's binary
  6. Shell as root
- **Key technical details:** `char` size field → max 255 bytes overflow; no authentication check on ioctl handler; modprobe_path overwrite for privilege escalation; kernel oops doesn't always fully reboot (sometimes recovers)
- **Impact:** Full LPE from unprivileged user on affected devices; remotely exploitable via WAPD daemon's ioctl interfaces
- **Obstacles:** No debugger (no JTAG, couldn't compile custom kernel); ~10,000 reboots during exploit dev; exploited blind via trial and error

#### Pwn2Own vs HackerOne Ecosystems
- **Key comparison:** HackerOne bug bounty had adversarial interactions with MediaTek (downgrades, budget exhaustion, dishonesty); Pwn2Own more prestigious but riskier (need to travel, patches can drop days before)
- **MediaTek experience:** 20 bugs submitted → bug bounty budget was "exhausted" → program closed for that chipset; reports downgraded with "AI-like" obtuse responses; HackerOne mediation unresponsive; received code of conduct violation for calling them liars
- **Pwn2Own:** Sina (Summoning Team) reached out for collaboration; exploits were ~80% working but ASLR made them probabilistic (loop and guess); only 3 attempts at competition; patches can drop last-minute destroying months of work

### Techniques and Primitives
**ioctl Scanning** — Write a simple fuzzer that iterates ioctl codes from `0x0000` to `0xFFFF` with a buffer of `A`s; Hypr found multiple bugs this way. ioctl numbers are command codes (integers), each handler defines its own structure

**Source-to-Sink Code Review for Kernel** — Index on `memcpy` operations; identify where external data influences size parameters; check for bounds validation on size fields before memory operations

**Kernel-Utils Repo** — `github.com/mellow-hype/kernel-utils`: scripts to automate kernel build + Debian root filesystem (via debootstrap) for KVM-based kernel exploitation dev

**modprobe_path Overwrite** — Classic kernel LPE technique: overwrite the string path to modprobe binary → trigger execution of a non-ELF file → kernel invokes the overwritten path → attacker's binary runs as root

### Suggestions and Advices from Hunter
- "Pwn2Own: biggest stress is the 3-4 days leading up to the competition where vendors push last-minute patches."
- "The reason I like memory corruption bugs: find the potential bug first, then determine whether the data can be controlled."
- On MediaTek: "It was not about the money for me. I do this stuff for fun... throughout the whole experience, it feels like you're being disrespected."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Hypr (Enrique) discusses MediaTek kernel driver heap overflow (CVE-2025-27422) and broader kernel exploitation

#### 2. What you should learn
- Learn about **hypr (enrique) discusses mediatek kernel driver heap overflow (cve-2025-27422) and broader kernel exploitation**
- Learn about **found mediatek driver source code leaked in netgear gpl package**
- Learn about **exploited ioctl handler reachable without authentication → heap overflow → free list pointer corruption → modprobe path overwrite → lpe → shell**
- Learn about **no debugger available — blind exploitation via trial-and-error with 10,000+ reboots**
- Learn about **pwn2own vs hackerone ecosystem comparison**

#### 3. Core concepts explained
**MediaTek Kernel Driver Heap Overflow (CVE-2025-27422) — LPE**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Pwn2Own vs HackerOne Ecosystems**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"Pwn2Own: biggest stress is the 3-4 days leading up to the competition where vendors push last-minute patches."*
- *"The reason I like memory corruption bugs: find the potential bug first, then determine whether the data can be controlled."*
- *"On MediaTek: "It was not about the money for me. I do this stuff for fun... throughout the whole experience, it feels like you're being disrespected."*

#### 6. Mental models
- **Pwn2Own: biggest stress is the 3-4 days leading up to the co** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The reason I like memory corruption bugs: find the potential** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On MediaTek: "It was not about the money for me. I do this s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- - Obstacles: No debugger (no JTAG, couldn't compile custom kernel); ~10,000 reboots during exploit dev; exploited blind via trial and error

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in MediaTek Kernel Driver Heap Overflow (CVE-2025-27422) — LPE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Hypr (Enrique) discusses MediaTek kernel driver heap overflow (CVE-2025-27422) a**
