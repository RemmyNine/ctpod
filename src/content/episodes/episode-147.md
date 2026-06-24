---
title: "Stupid Simple Hacking Workflow Tips"
episode: 147
---


# Episode 147 Stupid Simple Hacking Workflow Tips

### TL;DR
- Kaido EvenBetter plugin command palette PR adds convert workflows (Ctrl+K base64, URL, etc.)
- Chrome DevTools "Edit as HTML" for copying non-downloadable content (Google Docs), debugging AI, testing HTML encoding
- ffuf `-request` flag for post-auth fuzzing; interactive filtering (Enter → AFS to add filter size); color with `-c`
- JX Scout + Cursor for JS file analysis with AI
- Conditional breakpoints in DevTools to run arbitrary JS (e.g., force feature flags on)

### Key Takeaways
- Use **Kaido Command Palette** (via EvenBetter PR) for quick encodings: highlight text → `Ctrl+K base64` → Enter
- **Chrome DevTools "Edit as HTML"** — right-click node → copy all HTML for AI context; also use to check if `<` is HTML-encoded
- **Quick Tricks toolkit**: personal web server with scripts for window.open (null origin), iframe with sandbox properties, redirect scripts; test.html with CodeMirror + iframe for dynamic JS/DOM testing
- **CyberChef** for URL-encoding AI prompts/query params; parsing JSON-escaped responses
- **Raycast custom scripts**: clipboard transformations — `mr` (match/replace), URL-encode-all, JWT→jwt.io, HTTP request cookie redaction; text transforms via muscle-memory strings (qq=double URL encode, qqw=URL×2+URL decode, qqwa=URL×2+URL decode+base64 encode)
- **ffuf `-request` flag**: paste raw HTTP request with cookies/auth token; save as `req.txt`, use bash alias; interactive mode: hit Enter to pause, `AFS` to add filter size, `FS` to filter by size, then Enter to resume
- **JX Scout** (Kaido plugin): watches request history, downloads/beautifies JS, resolves source maps; pair with Cursor for AI-assisted route/parameter analysis
- **Conditional breakpoints**: right-click breakpoint → edit → add expression like `(console.log("data"), false)` to run JS without breaking; useful for feature flag manipulation
- **Mac system-wide proxy**: WiFi settings → Details → Proxies; useful for desktop apps
- **Terminal Notifier**: ping when AI code-agent finishes

### Tooling and Resources
- Kaido EvenBetter plugin
- ffuf with `-request` flag, `-c` for color, interactive mode (Enter → AFS/FS → Enter)
- JX Scout (Kaido plugin + CLI + VSCode extension)
- Raycast with custom scripts (mr, text transforms, quick links)
- CyberChef
- Chrome DevTools Edit as HTML
- Terminal Notifier (macOS)

### AI Takeaway
Episode is a goldmine of workflow optimizations. The Raycast clipboard-as-object approach (transform in place via muscle-memory strings) and the ffuf interactive filtering are the highest-leverage tips.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Kaido EvenBetter plugin command palette PR adds convert workflows (Ctrl+K base64, URL, etc.)

#### 2. What you should learn
- Understand **use kaido command palette (via evenbetter pr) for quick encodings: highlight text → `ctrl+k base64` → enter**
- Understand **chrome devtools "edit as html"** — right-click node → copy all html for ai context; also use to check if `<` is html-encoded**
- Understand **quick tricks toolkit**: personal web server with scripts for window.open (null origin), iframe with sandbox properties, redirect scripts; test.html with codemirror + iframe for dynamic js/dom testing**
- Understand **cyberchef** for url-encoding ai prompts/query params; parsing json-escaped responses**
- Understand **raycast custom scripts**: clipboard transformations — `mr` (match/replace), url-encode-all, jwt→jwt.io, http request cookie redaction; text transforms via muscle-memory strings (qq=double url encode, qqw=url×2+url decode, qqwa=url×2+url decode+base64 encode)**

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
- **Try this:** Use Kaido Command Palette (via EvenBetter PR) for quick encodings: highlight text → `Ctrl+K base64` → Enter
- **Try this:** Chrome DevTools "Edit as HTML"** — right-click node → copy all HTML for AI context; also use to check if `<` is HTML-encoded
- **Try this:** Quick Tricks toolkit**: personal web server with scripts for window.open (null origin), iframe with sandbox properties, redirect scripts; test.html with CodeMirror + iframe for dynamic JS/DOM testing
- **Try this:** CyberChef** for URL-encoding AI prompts/query params; parsing JSON-escaped responses

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **JWT** — JSON Web Token — compact token format for authentication
- **fuzzing** — Sending unexpected or malformed data to discover vulnerabilities
- **agent** — AI system that can use tools and make decisions autonomously

#### 10. Self-test
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Kaido EvenBetter plugin command palette PR adds convert workflows (Ctrl+K base64**
2. **Use Kaido Command Palette (via EvenBetter PR) for quick encodings: highlight tex**
3. **Chrome DevTools "Edit as HTML"** — right-click node → copy all HTML for AI conte**
