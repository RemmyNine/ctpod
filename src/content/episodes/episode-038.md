---
title: "Mobile Hacking Maestro — Sergey Toshin (Baggy Pro)"
episode: 38
---


# Episode 38 Mobile Hacking Maestro — Sergey Toshin (Baggy Pro)

### TL;DR
- Sergey Toshin (Baggy Pro) — #1 hacker in Google Play Security Awards, #1 in Samsung program
- Founded Oversecured, a mobile vulnerability scanner for Android and iOS
- Three-year gap between starting bug bounty and first payout
- Published "golden techniques for URL parsing bypasses" on Android — foundational resource

### Key takeaways
- Mobile hacking has far fewer competitors than web (~500 web vs ~5 mobile at the top)
- Use and contribute to Jadx decompiler; report decompilation bugs to keep the flow correct
- Scan with Oversecured, then manually verify in Jadx for tricky conditions
- Old apps + disclosed vulnerability databases are the best way to learn mobile hacking

### Bugs and Findings
#### URL Parsing Bypasses on Android
- **Target/context:** Any Android app parsing URLs
- **Root cause:** Differences between `android.net.uri` and `java.net.URI` — they parse the same URL differently
- **Technique / how found:** Systematic research across Android URI classes; published as "Attack Vectors on the Uri" on Oversecured blog
- **Key technical details:** `Uri.parse()` vs `new URI()` handle user:pass@host, at-signs, backslashes, trailing dots, scheme parsing differently — enabling host validation bypasses
- **Impact / severity / bounty:** Up to account takeover via OAuth redirect manipulation

#### Google Play Security Rewards — 1M in 4-5 months
- **Context:** Google launched program paying $3,000 per vuln in apps with 100M+ installs (500+ apps)
- **Technique:** Scanned all eligible apps with Oversecured
- **Key detail:** Google later dropped rewards to $1,000 after the farming

### Techniques and Primitives
- **Host validation bypass via URI class mismatch** — `android.net.uri` vs `java.net.URI` have different parsing of the `@` sign, backslash, and trailing dot

### Tooling and Resources
- **Oversecured** — mobile vulnerability scanner (Android + iOS)
- **Jadx** — decompiler (Sergey is active contributor)
- **Oversecured blog** — attack vectors on URIs, other mobile research
- **GitHub repositories of disclosed vulnerabilities** — for reproducing and learning

### Suggestions and Advices from Hunter
- "Scan the app with Oversecured, then open it in Jadx for tricky conditions"
- "Hack old apps from disclosed vulnerability databases — reproduce the bugs with your own hands"
- "80% of vulnerability categories intersect between Android and iOS"
- On being #1 in Samsung: "Android devices are completely different from a vulnerability perspective — Pixel vs Samsung vs Xiaomi have device-specific bugs"

### AI Takeaway
The three-year gap between starting bug bounty and first real payout is a critical lesson in persistence. The URI parsing class mismatch between `android.net.uri` and `java.net.URI` is still one of the most lucrative Android bug classes.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Sergey Toshin (Baggy Pro) — #1 hacker in Google Play Security Awards, #1 in Samsung program

#### 2. What you should learn
- Understand **mobile hacking has far fewer competitors than web (~500 web vs ~5 mobile at the top)**
- Understand **use and contribute to jadx decompiler; report decompilation bugs to keep the flow correct**
- Understand **scan with oversecured, then manually verify in jadx for tricky conditions**
- Understand **old apps + disclosed vulnerability databases are the best way to learn mobile hacking**

#### 3. Core concepts explained
**URL Parsing Bypasses on Android**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Google Play Security Rewards — 1M in 4-5 months**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Host validation bypass via URI class mismatch**
- `android.net.uri` vs `java.net.URI` have different parsing of the `@` sign, backslash, and trailing dot


#### 4. Techniques and tactics
**Host validation bypass via URI class mismatch**
- **What it is:** `android.net.uri` vs `java.net.URI` have different parsing of the `@` sign, backslash, and trailing dot
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Scan the app with Oversecured, then open it in Jadx for tricky conditions"*
- *"Hack old apps from disclosed vulnerability databases"* — **reproduce the bugs with your own hands**
- *"80% of vulnerability categories intersect between Android and iOS"*
- *"On being #1 in Samsung: "Android devices are completely different from a vulnerability perspective"* — **Pixel vs Samsung vs Xiaomi have device-specific bugs**

#### 6. Mental models
- **Scan the app with Oversecured, then open it in Jadx for tric** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Hack old apps from disclosed vulnerability databases — repro** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **80% of vulnerability categories intersect between Android an** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Mobile hacking has far fewer competitors than web (~500 web vs ~5 mobile at the top)
- **Try this:** Use and contribute to Jadx decompiler; report decompilation bugs to keep the flow correct
- **Try this:** Scan with Oversecured, then manually verify in Jadx for tricky conditions
- **Try this:** Old apps + disclosed vulnerability databases are the best way to learn mobile hacking

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in URL Parsing Bypasses on Android?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Sergey Toshin (Baggy Pro) — #1 hacker in Google Play Security Awards, #1 in Sams**
2. **Mobile hacking has far fewer competitors than web (~500 web vs ~5 mobile at the **
3. **Use and contribute to Jadx decompiler; report decompilation bugs to keep the flo**
