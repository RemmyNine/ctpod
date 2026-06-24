---
title: "Hacker Loadouts"
episode: 23
---


# Episode 23 Hacker Loadouts

**Guests/Hosts:** Justin Gardner, Joel Margolis  
**Date:** 2023-06-15 | **Duration:** 1:14:34

### TL;DR
- Both hosts discuss their physical hacking setups: desks, monitors, chairs, keyboards, mice, Chromebook for lightweight hacking
- Standing desks (Uplift), multiple monitors, synergy for cross-machine KVM
- Work-life balance and physical health for full-time hackers

### Key Takeaways
- Invest in your workspace: standing desk (Uplift), good chair (Herman Miller Aeron/Embody), quality monitors
- Synergy software KVM — seamless mouse/keyboard across Windows, Mac, Linux
- Chromebook + ZeroTier + Caido remote proxy = lightweight travel hacking setup
- Ergonomic health: change posture every 15 minutes, use standing desk periodically

### Techniques and Primitives
- **Remote proxy setup:** ZeroTier VPN from Chromebook → home PC → Caido/Burp proxy
- **Clamshell dock** — 3D-printed stand holds two laptops vertically; HDMI switch + StreamDeck for input switching

### Tooling and Resources
- Uplift standing desks
- Herman Miller Embody / Aeron chairs
- Synergy KVM software
- Logitech MX Master / G Pro Superlight mice
- Acer Chromebook Spin 713 (R841T series)
- ZeroTier VPN
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Both hosts discuss their physical hacking setups: desks, monitors, chairs, keyboards, mice, Chromebook for lightweight hacking

#### 2. What you should learn
- Understand **invest in your workspace: standing desk (uplift), good chair (herman miller aeron/embody), quality monitors**
- Understand **synergy software kvm — seamless mouse/keyboard across windows, mac, linux**
- Understand **chromebook + zerotier + caido remote proxy = lightweight travel hacking setup**
- Understand **ergonomic health: change posture every 15 minutes, use standing desk periodically**

#### 3. Core concepts explained
**Remote proxy setup: ZeroTier VPN from Chromebook → home PC → Caido/Burp proxy**
- A technique discussed in this episode for security research and bug bounty hunting.

**Clamshell dock**
- 3D-printed stand holds two laptops vertically; HDMI switch + StreamDeck for input switching


#### 4. Techniques and tactics
**Remote proxy setup: ZeroTier VPN from Chromebook → home PC → Caido/Burp proxy**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Clamshell dock**
- **What it is:** 3D-printed stand holds two laptops vertically; HDMI switch + StreamDeck for input switching
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
- **Try this:** Invest in your workspace: standing desk (Uplift), good chair (Herman Miller Aeron/Embody), quality monitors
- **Try this:** Synergy software KVM — seamless mouse/keyboard across Windows, Mac, Linux
- **Try this:** Chromebook + ZeroTier + Caido remote proxy = lightweight travel hacking setup
- **Try this:** Ergonomic health: change posture every 15 minutes, use standing desk periodically

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Burp** — Burp Suite — popular web application security testing proxy

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Both hosts discuss their physical hacking setups: desks, monitors, chairs, keybo**
2. **Invest in your workspace: standing desk (Uplift), good chair (Herman Miller Aero**
3. **Synergy software KVM — seamless mouse/keyboard across Windows, Mac, Linux**
