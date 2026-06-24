---
title: "Crushing Client-Side on Any Scope with MatanBer"
episode: 81
---


# Episode 81 Crushing Client-Side on Any Scope with MatanBer

**TL;DR**
- MatanBer (16-year-old hacker) — competed at H1 LHE events, expert in client-side hacking
- DevTools tips: conditional breakpoints as JS injection points, log points, event listener breakpoints
- Safari file download content-type quirk: `text/xsl` content type allows HTML injection even with Content-Disposition
- Dynamic analysis over static: don't dive into minified JS, use breakpoints and DOM logger instead
- Call stack navigation in DevTools, XHR/fetch breakpoints

**Key Takeaways**
- Use conditional breakpoints to inject code without modifying source files — set a breakpoint, edit it, write `code; false` — the code executes, `false` prevents the break from triggering
- Use "Add log point" (right-click gutter in DevTools) to log variables without stopping execution — useful for debug mode detection bypasses
- For `beforeunload` breakpoints: Sources panel → Event Listener Breakpoints → Load → `beforeunload` — prevents redirects from destroying your debug state
- Override `window.open` with `debugger;` to break on all popup creations
- In Safari: if a file download shows "View" vs "Download" prompt, the content type can allow HTML injection even with Content-Disposition headers — `text/xsl` bypasses the protection
- CSP information is available in DevTools under Application → Frames → (select frame) → CSP — syntax highlighted and broken out

**Techniques and Primitives**
- **Conditional breakpoint as code injector** — Write `payload; false` in the breakpoint condition — the payload runs, `false` prevents the break
- **Log point for stealth observation** — Right-click gutter → Add log point; logs like `console.log()` at that code location without pausing
- **Safari View bug for content-disposition bypass** — Upload file with MIME type that Safari allows "View" for; `text/xsl` works but doesn't execute JS (only HTML injection possible)
- **DevTools frames panel for CSP inspection** — Application tab → Frames → pick frame → CSP section shows fully parsed policy

**Tooling and Resources**
- `aszx87410.github.io/beyond-xss/en/` — Beyond XSS series
- PortSwigger Web Academy DOM XSS labs (underrated, MatanBer recommends)
- PortSwigger Research `css-exfiltration` GitHub repo
- DomLogger++
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Episode Episode 81 Crushing Client-Side on Any Scope with MatanBer covers practical bug bounty techniques and security research insights.

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
