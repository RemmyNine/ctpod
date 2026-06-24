---
title: "Supply Chain Attack Primer (feat 0xLupin)"
episode: 74
---


# Episode 74 Supply Chain Attack Primer (feat 0xLupin)

**TL;DR**
- Full supply chain attack taxonomy: source → build → package
- Dependency confusion technique: publish a public package with the same name as a private one to hijack internal builds
- Lupin's Depi tool (SaaS, not open source) for enterprise supply chain scanning
- Maintainer attacks via domain takeover (lapsed domains → password reset on NPM)
- Ethical package hosting: create own registry as dependency, hot-swap malicious vs benign packages based on scanner blacklist
- 200,000–400,000 packages internally at large French startups; 1–3 maintainers per package

**Key Takeaways**
- Map scope by collecting `package.json`, `requirements.txt`, `yarn.lock` from open-source repos and web roots
- Check `.map` files in JavaScript bundles to find `sourcesContent` containing full package paths and dependencies
- Git history dumping (tomnomnom's `git-dump`) reveals past packages no longer in use but still pinned
- Many registries don't allow deleting versions — once a vulnerable version is pinned, it's forever
- Domain takeover → NPM password reset is a real, high-impact maintainer attack
- When testing dependency confusion ethically, swapping packages after the first week avoids scanners (SupplyShark technique)
- Exfiltrate over HTTPS rather than DNS to avoid exposure at intermediate DNS servers

**Bugs and Findings**

### Dependency confusion — RCE via package squatting
- **Target/context:** Any organization using a mix of private artifactories and public registries (NPM, PyPI, PIP)
- **Root cause:** The build system pulls the higher-versioned package from whichever registry responds first; public packages with same name + higher version win
- **Technique / how found:** Alex Birsan's 2021 research; Lupin's 50-line bash script scraped JS for packages
- **Exploitation steps:**
  1. Enumerate target's `package.json` / lock files from open-source repos or web roots
  2. Identify packages that don't exist on the public registry
  3. Publish a package with the same name + higher version on NPM/PyPI
  4. Package includes benign code that exfiltrates hostname/path (HTTP or DNS callback)
  5. When the build system pulls it, code executes in the CI/CD pipeline
- **Key technical details:** Exfil over HTTPS preferred; use own registry as dependency with hot-swap logic to avoid scanner detection
- **Impact / severity / bounty:** RCE on build servers — access to secrets, source code, production deployment keys
- **Obstacles & how solved:** Registries now actively ban malicious packages; Lupin's solution uses a private registry as dependency with IP allow-listing

### Maintainer attack via domain takeover
- **Target/context:** NPM/PyPI packages where maintainers use custom domains for their email
- **Root cause:** Domain expires → attacker registers it → uses "forgot password" on the registry → takes over the account
- **Technique / how found:** Research paper on weak links of supply chain; Matthew Bryant (Snap Inc.) demonstrated on Angular dependency
- **Exploitation steps:**
  1. Identify lapsed domains used by package maintainers (check NPM package author email domain)
  2. Register the expired domain
  3. Set up email for the maintainer's address
  4. Trigger password reset on NPM/PyPI
  5. Push malicious update to the package
- **Key technical details:** Even after 2FA enforcement by NPM (2022, >1M weekly downloads), many maintainers don't have it enabled
- **Impact / severity / bounty:** Supply chain compromise affecting all downstream users

**Techniques and Primitives**
- **Package enumeration** — Fuzz web roots for `package.json`, `yarn.lock`, `.map` files; AST-scan minified JS for inline package names
- **Git-dump for historical packages** — Run tomnomnom's `git-dump` on target repos to find packages removed from current `package.json` but still in use elsewhere
- **Ethical backdoor hosting** — Publish a benign package that depends on your private registry; hot-swap responses to deliver payload only to target IPs

**Tooling and Resources**
- `landh.tech/depi` — Depi (SaaS supply chain scanner)
- `arxiv.org/pdf/2112.10165` — Research paper on weak links in supply chain
- `medium.com/alex.birsan/dependency-confusion-4a5d60fec610` — Original Alex Birsan dependency confusion post
- `github.com/tomnomnom/dotfiles/blob/master/scripts/git-dump` — git-dump
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 74 Supply Chain Attack Primer (feat 0xLupin) covers practical bug bounty techniques and security research insights.

#### 2. What you should learn
- Understand the vulnerability classes discussed
- Learn practical exploitation techniques
- Know which tools are useful for this type of research

#### 3. Core concepts explained
**Vulnerability Classes Discussed**
This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.

**Reconnaissance and Discovery**
The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.


#### 4. Techniques and tactics
**Systematic Testing Approach**
- **What it is:** Methodical testing of application features for vulnerability classes
- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses
- **What can go wrong:** Spending too much time on low-probability paths


#### 5. Good Quotes
- *"The best bugs come from persistence and deep understanding of the target"*
- *"Always think about what the worst thing that could happen is"*
- *"Don't be afraid to spend time on a single target"*

#### 6. Mental models
- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?
- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.
- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).

#### 7. Real-world application
- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports
- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques
- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Understand the vulnerability class** — Know how it works and why it matters
2. **Master the exploitation technique** — Practice the specific steps to exploit it
3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets
