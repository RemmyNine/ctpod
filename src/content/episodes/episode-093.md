---
title: "A Chat with Dr. Bouman — Life as a Hacker and a Doctor"
episode: 93
---


# Episode 93 A Chat with Dr. Bouman — Life as a Hacker and a Doctor

**Guest:** Dr. Jonathan Bouman
**Host:** Justin Gardner (Rhynorater)
**Duration:** 1:41:29
**Transcript source:** feed (full transcript)

### TL;DR
- Dr. Bouman (GP + hacker) has been exclusively hacking Amazon for 6+ years; collab with Zshano is legendary
- FileSender SSTI: 10-year-old template injection leaked S3 keys, exposed via Base64-encoded error messages
- Healthcare hacking: chained IDOR + registration info leak + executable upload in Dutch healthcare systems
- SSTI methodology: custom Burp active scan profile (enable per-code injection, template injection)
- Consistency in payouts is the #1 thing programs can do to retain top researchers

### Key Takeaways
- When you see Base64 in a URL parameter, treat it as "eczema on the skin" — something is off, dig in
- Use Burp's active scanner selectively: disable paths with images/fonts/CSS, enable template/perl/code injections
- Brute-force parameters on endpoints before scanning — discover untouched functionality
- For iOS testing: get a jailbroken iPad (check Palera1n compatibility) and a rooted Pixel for Android (use APK-MITM)
- Have backup devices (2 iPads, 2 Pixels) — jailbreaks can brick devices

### Bugs and Findings

#### FileSender SSTI — S3 Key Leak
- **Target/context:** FileSender (open-source file sharing, widely used in European education/government)
- **Root cause:** Error messages are Base64-encoded in the URL, then passed through a template engine. Template code in error messages gets rendered. config template variables expose server paths, database credentials, S3 keys
- **Technique / how found:** On a fresh black-box test, saw Base64 URL parameters, decoded them, saw template code. Used "Where's the Request" game — searched source code for the error message string, found the template injection point
- **Exploitation steps:**
  1. Download FileSender source from GitHub
  2. `Ctrl+Shift+F` search for the error message string
  3. Identify config template variables (server paths, DB creds)
  4. Inject template code to read `config` variables → get MySQL username/password, S3 access keys
  5. (Bonus) `git blame` revealed the vulnerable code was 10 years old — also exploitable in production
- **Key technical details:** Base64-encoded error message in URL → concatenated into template → rendered. `config` template variable exposes internal configuration. S3 support was added in v3.
- **Impact / severity / bounty:** Full S3 bucket access (read/write), database credentials. Coordinated disclosure with FileSender team.
- **Obstacles & how solved:** The FileSender team was at a conference in Paris; they created a hot patch; the fix was complicated because templating was deeply embedded. Bouman tracked their fix commits via GitHub commit hash scraping (TruffleSec technique).

#### Dutch Healthcare Chain — Ransomware Attack Simulation
- **Target/context:** Dutch healthcare systems (insurance co, complaints mediation portal, EHR systems)
- **Root cause chain:**
  1. **IDOR:** Insurance company portal exposed PDF documents via numeric member ID in URL — replace with another member's ID to view their insurance policy
  2. **Info leak:** Complaints mediation portal returned full account details in the HTTP response on registration (error message included the details even when denying registration)
  3. **Executable upload:** One of 7 EHR systems allowed uploading `.exe` files through patient portal instead of blocking them
- **Technique / how found:** Bouman used his own + his mother's accounts (IDOR tested against self). For the EHR upload, he and a GP buddy tested 7 EHR systems; 1 didn't block executables
- **Exploitation steps:**
  1. Enumerate doctors with high-value insurance policies (via IDOR on insurance portal)
  2. Get their contact details (via info leak on mediation portal)
  3. Upload executable via EHR patient portal to that specific doctor
  4. Doctor clicks executable in Windows desktop app → RCE
- **Key technical details:** Insurance portal: `member_id=NUMERIC_ID` in URL; Mediation portal: registration endpoint returns account details in HTTP response body even on error; EHR: `.exe` upload not blocked
- **Impact / severity / bounty:** Full chain: enumerate → identify → deliver malware → compromise doctor's workstation. "User interaction required but that's about it."
- **Obstacles & how solved:** No bug bounty programs — responsible disclosure; Bouman used his own data to avoid legal issues; his mother was also a customer so he could test IDOR safely

### Techniques and Primitives
- **SSTI via error messages** — Look for Base64-encoded error data in URLs, decode, look for template syntax, use "Where's the Request" (source-code grep for the error string)
- **Active scanner SSTI methodology** — 1) Identify language/framework 2) Enable only relevant injection types (template, perl, code) 3) Exclude static assets (images, CSS, fonts) 4) Set up custom scanner profiles
- **Git commit tracking for fix bypass** — GitHub: even hidden/private forks have commits visible if you know the hash. Scrape commit hashes to monitor vendors applying patches before public disclosure
- **iOS MITM setup** — Jailbroken iPad (Palera1n) + `ios-webkit-debug-proxy` + extracted Safari DevTools frontend = remote debugging from Windows
- **Android MITM setup** — APK-MITM tool (patches APK to disable SSL pinning) or Objection/Frida for custom patching

### Tooling and Resources
- Burp Suite (active scanner with custom profiles, Intruder, Repeater, Param Miner)
- APK-MITM (GitHub) — patches Android APKs to disable SSL pinning
- ios-webkit-debug-proxy (Google) — Safari remote debugging from non-Mac via iPhone
- Palera1n jailbreak tool
- FileSender.org (open source)
- `scroll.am` — Bouman's failed Amazon affiliate project

### Suggestions and Advices from Hunter
- "Transparency is trust." — Jobert (quoted by Bouman)
- "Third-party code or enterprise software should not be out of scope. If you do that, you lose big talent." — Dr. Bouman
- "For heavy targets, write a documentation tracker — scrape documentation, release notes, GitHub repos. Be first." — Dr. Bouman
- "Consistency is the key thing programs need to achieve. Be predictable, take feedback from researchers." — Dr. Bouman
- "If you feel like something doesn't feel comfortable, bring it up and say, hey, what do you think about that? Communication." — Dr. Bouman

### AI Takeaway
The documentation tracker approach — automated scraping of release notes, changelogs, GitHub, and JS files to detect new features/endpoints — is the highest-ROI automation for bug bounty. Being first to a new endpoint trumps nearly every other advantage.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Dr. Bouman (GP + hacker) has been exclusively hacking Amazon for 6+ years; collab with Zshano is legendary

#### 2. What you should learn
- Understand **when you see base64 in a url parameter, treat it as "eczema on the skin" — something is off, dig in**
- Understand **use burp's active scanner selectively: disable paths with images/fonts/css, enable template/perl/code injections**
- Understand **brute-force parameters on endpoints before scanning — discover untouched functionality**
- Understand **for ios testing: get a jailbroken ipad (check palera1n compatibility) and a rooted pixel for android (use apk-mitm)**
- Understand **have backup devices (2 ipads, 2 pixels) — jailbreaks can brick devices**

#### 3. Core concepts explained
**FileSender SSTI — S3 Key Leak**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Dutch Healthcare Chain — Ransomware Attack Simulation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**SSTI via error messages**
- Look for Base64-encoded error data in URLs, decode, look for template syntax, use "Where's the Request" (source-code grep for the error string)

**Active scanner SSTI methodology**
- 1) Identify language/framework 2) Enable only relevant injection types (template, perl, code) 3) Exclude static assets (images, CSS, fonts) 4) Set up custom scanner profiles

**Git commit tracking for fix bypass**
- GitHub: even hidden/private forks have commits visible if you know the hash. Scrape commit hashes to monitor vendors applying patches before public disclosure


#### 4. Techniques and tactics
**SSTI via error messages**
- **What it is:** Look for Base64-encoded error data in URLs, decode, look for template syntax, use "Where's the Request" (source-code grep for the error string)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Active scanner SSTI methodology**
- **What it is:** 1) Identify language/framework 2) Enable only relevant injection types (template, perl, code) 3) Exclude static assets (images, CSS, fonts) 4) Set up custom scanner profiles
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Git commit tracking for fix bypass**
- **What it is:** GitHub: even hidden/private forks have commits visible if you know the hash. Scrape commit hashes to monitor vendors applying patches before public disclosure
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**iOS MITM setup**
- **What it is:** Jailbroken iPad (Palera1n) + `ios-webkit-debug-proxy` + extracted Safari DevTools frontend = remote debugging from Windows
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Android MITM setup**
- **What it is:** APK-MITM tool (patches APK to disable SSL pinning) or Objection/Frida for custom patching
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Transparency is trust."* — **Jobert (quoted by Bouman)**
- *"Third-party code or enterprise software should not be out of scope. If you do that, you lose big talent."* — **Dr. Bouman**
- *"For heavy targets, write a documentation tracker"* — **scrape documentation, release notes, GitHub repos. Be first." — Dr. Bouman**
- *"Consistency is the key thing programs need to achieve. Be predictable, take feedback from researchers."* — **Dr. Bouman**
- *"If you feel like something doesn't feel comfortable, bring it up and say, hey, what do you think about that? Communication."* — **Dr. Bouman**

#### 6. Mental models
- **Transparency is trust." — Jobert (quoted by Bouman)** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Third-party code or enterprise software should not be out of** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **For heavy targets, write a documentation tracker — scrape do** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** When you see Base64 in a URL parameter, treat it as "eczema on the skin" — something is off, dig in
- **Try this:** Use Burp's active scanner selectively: disable paths with images/fonts/CSS, enable template/perl/code injections
- **Try this:** Brute-force parameters on endpoints before scanning — discover untouched functionality
- **Try this:** For iOS testing: get a jailbroken iPad (check Palera1n compatibility) and a rooted Pixel for Android (use APK-MITM)

#### 8. Red flags and pitfalls
- - Obstacles & how solved: The FileSender team was at a conference in Paris; they created a hot patch; the fix was complicated because templating was deeply embedded. Bouman tracked their fix commits via GitHub commit hash scraping (TruffleSec technique).
- - Key technical details: Insurance portal: `member_id=NUMERIC_ID` in URL; Mediation portal: registration endpoint returns account details in HTTP response body even on error; EHR: `.exe` upload not blocked
- - Obstacles & how solved: No bug bounty programs — responsible disclosure; Bouman used his own data to avoid legal issues; his mother was also a customer so he could test IDOR safely

#### 9. Vocabulary
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **Burp** — Burp Suite — popular web application security testing proxy
- **SSTI** — Server-Side Template Injection — injecting template syntax that executes on server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in FileSender SSTI — S3 Key Leak?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Dr. Bouman (GP + hacker) has been exclusively hacking Amazon for 6+ years; colla**
2. **When you see Base64 in a URL parameter, treat it as "eczema on the skin" — somet**
3. **Use Burp's active scanner selectively: disable paths with images/fonts/CSS, enab**
