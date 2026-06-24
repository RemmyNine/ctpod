---
title: "Bug Bounty Lifestyle = Less Hacking Time?"
episode: 124
---


# Episode 124 Bug Bounty Lifestyle = Less Hacking Time?

### TL;DR
- Supabase API URL operators: `?column=eq.value` can use `gt.`/`lt.` operators on UUID columns — UUIDs processed as numeric entity
- Click detection in cross-origin iframes via `navigator.userActivation.isActive` on 0ms interval
- Clipboard hijacking via embedded page: Ctrl+A → Ctrl+C on victim page → forced focus to attacker's textarea → Ctrl+V leaks selection
- Full-time bug bounty lifestyle discussion: flexibility is the real win, not necessarily more hacking

### Key Takeaways
- Supabase REST API uses `?column=eq.value` format; try `?column=gt.00000000-0000-0000-0000-000000000000` or `?column=lt.ffffffff-ffff-ffff-ffff-ffffffffffff` to bypass row-level security
- Cross-origin click detection: poll `navigator.userActivation.isActive` on 0ms interval; when true, consume with `window.open('')` → close → repeat
- Clipboard hijacking: embed victim page, force Ctrl+A → Ctrl+C (select all + copy on victim), then focus attacker's textarea, victim presses Ctrl+V → attacker gets content
- Full-time bug bounty: the real value is flexibility to pursue ideas, not just hacking more hours

### Bugs and Findings

#### Supabase API UUID IDOR via GT/LT Operators
- **Target/context:** Supabase-backed applications (common in AI startups)
- **Root cause:** Supabase REST API format `?column=eq.value` also supports `gt.` (greater than) and `lt.` (less than) operators; UUIDs are compared as numeric entities when using these operators
- **Technique / how found:** Change `?id=eq.a1b2c3d4-...` to `?id=gt.00000000-0000-0000-0000-000000000000` — the UUID column is compared numerically, returning all objects greater than the zero UUID
- **Key technical details:** Format: `?column=gt.value`; works even with UUID column types; bypasses row-level security when RLS is misconfigured or when non-UUID comparison logic is unexpected
- **Impact / severity / bounty:** IDOR — read all objects in collection
- **Obstacles & how solved:** Most Supabase implementations have RLS; but where RLS is disabled or the comparison is unexpected, this bypasses column-level access

#### Cross-Origin Iframe Click Detection via userActivation
- **Target/context:** Any page that can embed iframes
- **Root cause:** `navigator.userActivation.isActive` returns true when a user activation (click, keypress) is active, even if it originated in a cross-origin iframe
- **Technique / how found:** Poll in 0ms interval: `setInterval(() => { if (navigator.userActivation.isActive) { /* consume */ window.open(''); window.close(); } }, 0)`
- **Key technical details:** `userActivation.isActive` is cross-origin accessible; consuming the activation (`window.open`) resets it, allowing repeated detection
- **Impact / severity / bounty:** Enables reliable clickjacking with multiple clicks; clipboard data theft
- **Obstacles & how solved:** Requires user to have pop-ups allowed or existing pop-up context

#### Clipboard Hijacking via Embedded Page
- **Target/context:** Any page with sensitive data in DOM
- **Root cause:** By embedding a victim page and detecting user activations, attacker can force focus to their own textarea when the user presses Ctrl+V
- **Technique / how found:**
  1. Embed victim page in iframe
  2. Detect user activation (copy/select via keyboard)
  3. When Ctrl+A/Ctrl+C is pressed on victim content, force focus to attacker's textarea
  4. User presses Ctrl+V → content pasted into attacker's textarea → exfiltrated
- **Key technical details:** Cross-origin iframe; keyboard shortcuts are user activations; `window.focus()` on attacker's element redirects paste
- **Impact / severity / bounty:** Theft of any data user can select and copy
- **Obstacles & how solved:** Requires user to use keyboard shortcuts (Ctrl+A, Ctrl+C, Ctrl+V)

### Techniques and Primitives
- **Supabase UUID GT/LT** — `?column=gt.00000000-0000-0000-0000-000000000000` for IDOR bypass
- **userActivation click detection** — `navigator.userActivation.isActive` + 0ms interval polling
- **Clipboard hijacking** — Embed victim → detect Ctrl+A/C → force focus to attacker textarea → victim Ctrl+V leaks selection
- **URL as window reference fallback** — `URL` in inline onload handler = `document.URL` (not the constructor)

### Tooling and Resources
- Jorian's writeups (clickjacking, clipboard)
- Supabase REST API docs
- YesWeHack: Louis Vuitton, OpenPGP.js CVE

### Suggestions and Advices from Hunter
- "Desire is a contract you make with yourself to be unhappy until you get what you want"
- "Full-time bug bounty: the real win is the flexibility to pursue ideas, not just hacking more hours"
- "Sit in your wins — don't constantly move the goalpost"

### AI Takeaway
The Supabase GT/LT operator technique is directly applicable to the many AI apps built on Supabase. Combined with the `navigator.userActivation` cross-origin click detection, these are two high-value client-side primitives.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Supabase API URL operators: `?column=eq.value` can use `gt.`/`lt.` operators on UUID columns — UUIDs processed as numeric entity

#### 2. What you should learn
- Understand **supabase rest api uses `?column=eq.value` format; try `?column=gt.00000000-0000-0000-0000-000000000000` or `?column=lt.ffffffff-ffff-ffff-ffff-ffffffffffff` to bypass row-level security**
- Understand **cross-origin click detection: poll `navigator.useractivation.isactive` on 0ms interval; when true, consume with `window.open('')` → close → repeat**
- Understand **clipboard hijacking: embed victim page, force ctrl+a → ctrl+c (select all + copy on victim), then focus attacker's textarea, victim presses ctrl+v → attacker gets content**
- Understand **full-time bug bounty: the real value is flexibility to pursue ideas, not just hacking more hours**

#### 3. Core concepts explained
**Supabase API UUID IDOR via GT/LT Operators**
- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.
- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.
- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.

**Cross-Origin Iframe Click Detection via userActivation**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Clipboard Hijacking via Embedded Page**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Supabase UUID GT/LT**
- `?column=gt.00000000-0000-0000-0000-000000000000` for IDOR bypass

**userActivation click detection**
- `navigator.userActivation.isActive` + 0ms interval polling

**Clipboard hijacking**
- Embed victim → detect Ctrl+A/C → force focus to attacker textarea → victim Ctrl+V leaks selection


#### 4. Techniques and tactics
**Supabase UUID GT/LT**
- **What it is:** `?column=gt.00000000-0000-0000-0000-000000000000` for IDOR bypass
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**userActivation click detection**
- **What it is:** `navigator.userActivation.isActive` + 0ms interval polling
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Clipboard hijacking**
- **What it is:** Embed victim → detect Ctrl+A/C → force focus to attacker textarea → victim Ctrl+V leaks selection
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**URL as window reference fallback**
- **What it is:** `URL` in inline onload handler = `document.URL` (not the constructor)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Desire is a contract you make with yourself to be unhappy until you get what you want"*
- *"Full-time bug bounty: the real win is the flexibility to pursue ideas, not just hacking more hours"*
- *"Sit in your wins"* — **don't constantly move the goalpost**

#### 6. Mental models
- **Desire is a contract you make with yourself to be unhappy un** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Full-time bug bounty: the real win is the flexibility to pur** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Sit in your wins — don't constantly move the goalpost** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Supabase REST API uses `?column=eq.value` format; try `?column=gt.00000000-0000-0000-0000-000000000000` or `?column=lt.ffffffff-ffff-ffff-ffff-ffffffffffff` to bypass row-level security
- **Try this:** Cross-origin click detection: poll `navigator.userActivation.isActive` on 0ms interval; when true, consume with `window.open('')` → close → repeat
- **Try this:** Clipboard hijacking: embed victim page, force Ctrl+A → Ctrl+C (select all + copy on victim), then focus attacker's textarea, victim presses Ctrl+V → attacker gets content
- **Try this:** Full-time bug bounty: the real value is flexibility to pursue ideas, not just hacking more hours

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Most Supabase implementations have RLS; but where RLS is disabled or the comparison is unexpected, this bypasses column-level access
- - Obstacles & how solved: Requires user to have pop-ups allowed or existing pop-up context

#### 9. Vocabulary
- **IDOR** — Insecure Direct Object Reference — accessing resources by manipulating identifiers
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **API** — Application Programming Interface — structured endpoints for data exchange

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Supabase API UUID IDOR via GT/LT Operators?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Supabase API URL operators: `?column=eq.value` can use `gt.`/`lt.` operators on **
2. **Supabase REST API uses `?column=eq.value` format; try `?column=gt.00000000-0000-**
3. **Cross-origin click detection: poll `navigator.userActivation.isActive` on 0ms in**
