---
title: "Team 82 Sharon Brizinov — The Live Hacking Polymath"
episode: 98
---


# Episode 98 Team 82 Sharon Brizinov — The Live Hacking Polymath

**Guest:** Sharon Brizinov (Team 82 / Claroty)
**Host:** Justin Gardner (Rhynorater)
**Duration:** 1:43:57
**Transcript source:** feed (full transcript)

### TL;DR
- IoT/SCADA hacking methodology: firmware extraction (vendor website → transition firmware → binary exploitation → desoldering flash chip)
- Device-to-cloud communication is the overlooked attack surface in IoT — impersonating a device to the cloud can lead to device takeover
- Pwn2Own vs HackerOne: ZDI fights for researchers with vendors; Pwn2Own pre-auth RCE only; 3-month prep vs 2-week + 48hr LHE
- Serial+MAC for device identity: MAC is 6 bytes (3 OUI + 3 brute-forceable), serials visible on eBay photos → device impersonation
- Replicate research daily: bot scopes internet for interesting articles → try to replicate → integrate into methodology

### Key Takeaways
- Device-to-cloud communication is often overlooked by developers — impersonate the device to the cloud via brute-forced/buyable identifiers
- For firmware: get previous unencrypted versions first; they contain the decryption key/algorithm for current encrypted firmware
- Emulate firmware in QEMU — patch peripheral reads to return dummy values (e.g., always 98% SpO2)
- Pwn2Own target selection: create metrics matrix (price, firmware extractability, prior CVEs, prior Pwn2Own targeting)
- Reproduce one or two pieces of research daily — integrate new techniques into your methodology

### Bugs and Findings

#### IoT Device-to-Cloud Impersonation — Device Takeover
- **Target/context:** Multiple IoT consumer devices
- **Root cause:** Device identity uses serial number + MAC address. MAC is 6 bytes (3 OUI, 3 brute-forceable). Serial numbers visible on eBay product photos, YouTube unboxings. Some devices have poor randomized identifiers.
- **Technique / how found:** Man-in-the-middle device → cloud communication. Downgrade HTTPS to HTTP by patching binary (change HTTPS→HTTP in config, or inject CA). Collect device identifiers from photos/unboxing videos.
- **Exploitation steps:**
  1. Obtain device identifiers (serial + MAC) from eBay/YouTube
  2. Connect to cloud as that device (identifiers are credentials)
  3. Tell cloud "I belong to attacker's account" → device transfers to attacker
  4. Now attacker can control the victim's device remotely
- **Key technical details:** Serial + MAC as device identity. MAC: first 3 bytes = OUI (vendor), last 3 = brute-forceable (16M possibilities). Some devices use hardware-based identifiers (OTP fuses, secure enclave, private key burned at manufacturing)
- **Impact / severity / bounty:** Full device takeover — control any device from outside the local network, bypass firewalls
- **Obstacles & how solved:** Modern secure devices use private key (2048-bit+) stored in OTP fuses/hardware secure enclave, not guessable

#### Firmware Extraction via Transition Firmware
- **Technique:** Download consecutive firmware versions from vendor site. Find the release where it switched from unencrypted → encrypted. The transition firmware contains the decryption algorithm + key for the encrypted version
- **Alternative methods:** Root the device (find a pre-auth RCE) → dump firmware from running system → extract decryption from binaries. Or desolder the flash chip and read directly.

#### Man-in-the-Middle for IoT Cloud Communication
- **Setup:** Own router fully controlled → device routes through it. Do: HTTPS downgrade (patch binary HTTPS→HTTP), or inject CA into device's trust store, or use DNS + custom CA
- **Tools:** Custom Python scripts, MITMproxy, mitm-ssl (ready-made tools)
- **Protocol:** Mostly HTTPS; also proprietary protocols for specific devices

### Techniques and Primitives
- **Firmware decryption via transition version** — Download old unencrypted firmware → get decryption key/algorithm for current encrypted version
- **Binary patching for emulation** — NOP out peripheral reads (serial bus, RS-485) that return dummy values to make the firmware run in QEMU
- **Documentation tracker** — Scrape release notes, change logs, documentation pages, GitHub repos, product pages for new features/endpoints
- **ReCAPTCHA bypass** — Use UI automation (e.g., UI Vision Chrome extension) to automate mouse clicks on reCAPTCHA elements via CSS selectors; combined with Gmail `+` aliasing for mass account creation
- **Metrics-driven target selection (Pwn2Own)** — Price tag, firmware extractability, prior CVEs, prior Pwn2Own history → matrix to pick 5-6 targets

### Tooling and Resources
- Pwn tools (pwntools) — Python library for binary exploitation
- Ghidra / IDA for binary analysis
- QEMU for firmware emulation
- MITMproxy for TLS interception
- Shodan/Censys for scanning for exposed esoteric protocols (NTP, SNMP, SIP)
- ScanMySMS — Sharon's free anti-phishing service for Israel
- ASMR board from AssetNote

### Suggestions and Advices from Hunter
- "Create a habit of reading one or two articles daily and trying to replicate them in your own work. This is how you stay current." — Sharon Brizinov
- "For bug bounty, think about attack surfaces others aren't looking at: DB-to-host escape, external scanning (non-HTTP protocols like NTP, SNMP, SIP)." — Sharon Brizinov
- "The key to bug bounty at scale is to be first. The way to do that is get a notification the second there's a new version." — Sharon Brizinov
- "Pwn2Own: ZDI fights for you with the vendor. That's something HackerOne doesn't provide at the same level." — Sharon Brizinov
- "Replicate one or two pieces of research daily — take new methods and implement them in your work." — Sharon Brizinov

### AI Takeaway
The device-to-cloud impersonation attack surface is massive and overlooked. The documentation tracker (automated scraping of changelogs, release notes, GitHub) is the highest-ROI recon investment — being first to a new version is everything. The metrics-driven Pwn2Own target selection methodology is applicable to any competitive hacking.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
IoT/SCADA hacking methodology: firmware extraction (vendor website → transition firmware → binary exploitation → desoldering flash chip)

#### 2. What you should learn
- Understand **device-to-cloud communication is often overlooked by developers — impersonate the device to the cloud via brute-forced/buyable identifiers**
- Understand **for firmware: get previous unencrypted versions first; they contain the decryption key/algorithm for current encrypted firmware**
- Understand **emulate firmware in qemu — patch peripheral reads to return dummy values (e.g., always 98% spo2)**
- Understand **pwn2own target selection: create metrics matrix (price, firmware extractability, prior cves, prior pwn2own targeting)**
- Understand **reproduce one or two pieces of research daily — integrate new techniques into your methodology**

#### 3. Core concepts explained
**IoT Device-to-Cloud Impersonation — Device Takeover**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Firmware Extraction via Transition Firmware**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Man-in-the-Middle for IoT Cloud Communication**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Firmware decryption via transition version**
- Download old unencrypted firmware → get decryption key/algorithm for current encrypted version

**Binary patching for emulation**
- NOP out peripheral reads (serial bus, RS-485) that return dummy values to make the firmware run in QEMU

**Documentation tracker**
- Scrape release notes, change logs, documentation pages, GitHub repos, product pages for new features/endpoints


#### 4. Techniques and tactics
**Firmware decryption via transition version**
- **What it is:** Download old unencrypted firmware → get decryption key/algorithm for current encrypted version
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Binary patching for emulation**
- **What it is:** NOP out peripheral reads (serial bus, RS-485) that return dummy values to make the firmware run in QEMU
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Documentation tracker**
- **What it is:** Scrape release notes, change logs, documentation pages, GitHub repos, product pages for new features/endpoints
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**ReCAPTCHA bypass**
- **What it is:** Use UI automation (e.g., UI Vision Chrome extension) to automate mouse clicks on reCAPTCHA elements via CSS selectors; combined with Gmail `+` aliasing for mass account creation
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Metrics-driven target selection (Pwn2Own)**
- **What it is:** Price tag, firmware extractability, prior CVEs, prior Pwn2Own history → matrix to pick 5-6 targets
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Create a habit of reading one or two articles daily and trying to replicate them in your own work. This is how you stay current."* — **Sharon Brizinov**
- *"For bug bounty, think about attack surfaces others aren't looking at: DB-to-host escape, external scanning (non-HTTP protocols like NTP, SNMP, SIP)."* — **Sharon Brizinov**
- *"The key to bug bounty at scale is to be first. The way to do that is get a notification the second there's a new version."* — **Sharon Brizinov**
- *"Pwn2Own: ZDI fights for you with the vendor. That's something HackerOne doesn't provide at the same level."* — **Sharon Brizinov**
- *"Replicate one or two pieces of research daily"* — **take new methods and implement them in your work." — Sharon Brizinov**

#### 6. Mental models
- **Create a habit of reading one or two articles daily and tryi** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For bug bounty, think about attack surfaces others aren't lo** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **The key to bug bounty at scale is to be first. The way to do** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Device-to-cloud communication is often overlooked by developers — impersonate the device to the cloud via brute-forced/buyable identifiers
- **Try this:** For firmware: get previous unencrypted versions first; they contain the decryption key/algorithm for current encrypted firmware
- **Try this:** Emulate firmware in QEMU — patch peripheral reads to return dummy values (e.g., always 98% SpO2)
- **Try this:** Pwn2Own target selection: create metrics matrix (price, firmware extractability, prior CVEs, prior Pwn2Own targeting)

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Modern secure devices use private key (2048-bit+) stored in OTP fuses/hardware secure enclave, not guessable

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in IoT Device-to-Cloud Impersonation — Device Takeover?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **IoT/SCADA hacking methodology: firmware extraction (vendor website → transition **
2. **Device-to-cloud communication is often overlooked by developers — impersonate th**
3. **For firmware: get previous unencrypted versions first; they contain the decrypti**
