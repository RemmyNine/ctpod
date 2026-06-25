---
title: "5k Clickjacking, Encryption Oracles, and Cursor for PoCs"
episode: 90
---


# Episode 90 5k Clickjacking, Encryption Oracles, and Cursor for PoCs

**TL;DR**
- Cursor AI for POC development: building realistic exploits with loading bars, cookie modals, multi-step chains
- WhatsUp Gold pre-auth SQL injection → admin password overwrite using encryption oracle
- Content-type research repo: `text/html(...)` — left parenthesis is a valid MIME type delimiter
- Google Docs clickjacking chain: YouTube gadget → path traversal → open redirect → root folder sharing → full Drive access
- Telegram account theft: `t.me` links embed user credentials; changing URL in address bar before page load leaks auth token

**Key Takeaways**
- Cursor is excellent for building polished POCs (loading bars, cookie consent modals for click harvesting) — this directly increases bounty payouts (up to 1.5x)
- For encryption oracles: inject long strings (1000 `A`s) and check if response length increases — indicates your data is being encrypted and reflected
- Content-type `text/html(...)` — the left parenthesis `(` is a valid delimiter in MIME type parsing, allowing XSS even with `text/` prefix requirements
- YouTube → Google open redirect gadget: `youtube.com` embedding feature path traversal → `google.com/amp` → any domain
- Google Drive "root" folder: each user has a root folder ID; sharing that folder shares ALL future Drive content

**Bugs and Findings**

### WhatsUp Gold pre-auth SQLi → admin via encryption oracle
- **Target/context:** WhatsUp Gold (network monitoring software)
- **Root cause:** Vanilla SQL injection in pre-auth endpoint
- **Technique / how found:** SinSinology / Summoning Team
- **Exploitation steps:**
  1. Identify the vanilla SQL injection
  2. Try to overwrite admin password — it's encrypted with a machine-specific key
  3. Use SQLi to read another encrypted field from the database
  4. Set that encrypted value as the admin password
  5. Log in as admin using the known plaintext of the other field
- **Key technical details:** The encryption is deterministic within the same machine; `UPDATE users SET password = (SELECT other_encrypted_field FROM ...) WHERE admin=1`
- **Impact / severity / bounty:** Pre-auth to full admin access

### Google Docs clickjacking → full Drive access ($5,000)
- **Target/context:** Google Docs embedded forms → Google Drive
- **Root cause:** Clickjacking via multi-hop redirect chain; Google Drive root folder sharing
- **Technique / how found:** Rebane writeup; three redirects chained
- **Exploitation steps:**
  1. Embed a Google Form in a Google Doc
  2. When the user clicks Submit, chain: YouTube embed path traversal → www.google.com → via `amp` endpoint → attacker page
  3. The clickjacked button actually authorizes the attacker's Google Drive app
  4. Attacher gains access to victim's "root" Drive folder (which shares all content)
- **Key technical details:** YouTube gadget: `youtube.com` → path traversal in embed → `google.com/amp` open redirect; `root` folder ID obtained from network requests; sharing root = sharing everything
- **Impact / severity / bounty:** Full Google Drive data access; $5,000 from Google VRP

### Content-type `text/html(...)` XSS
- **Target/context:** File uploads with content-type validation regex `^text/`
- **Root cause:** `(` is a valid MIME type delimiter per RFC; `text/html(...)` is parsed as `text/html` by the browser
- **Technique / how found:** Blackfan research repo
- **Exploitation steps:**
  1. Upload file with `Content-Type: text/html(...)` — the regex `^text/` matches `text/`
  2. If the response content-type is set from the upload, browser renders as HTML
  3. XSS
- **Key technical details:** The `(` character is treated as a parameter delimiter; the browser extracts `text/html` as the MIME type
- **Impact / severity / bounty:** Stored XSS from file upload

**Techniques and Primitives**
- **Encryption oracle detection** — Inject 1000 `A`s; if response length increases proportionally, your data is being encrypted and reflected
- **Content-length oracle for injection detection** — Fuzz with oversized inputs and monitor response length changes
- **YouTube → Google Drive redirect chain** — `youtube.com` embed feature → path traversal → `google.com/amp` → any domain
- **Google Drive root folder sharing** — Get the `root` folder ID, share it, and all future uploads are accessible
- **Content-type `(` delimiter bypass** — `text/html(...)` bypasses `^text/` regex checks

**Tooling and Resources**
- `github.com/blackfan/content-type-research` — Content-type XSS research
- `rhynorater.github.io/signin?next=https://accounts.youtube.com/...` — Justin's gadget link
- Rebane's Telegram account theft writeup (`lira.horse`)


### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 90 5k Clickjacking, Encryption Oracles, and Cursor for PoCs covers practical bug bounty techniques and security research insights.

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
