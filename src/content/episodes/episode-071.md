---
title: "More VDP Chats & AI Bias Bounty Strats with Keith Hoodlet"
episode: 71
---


# Episode 71 More VDP Chats & AI Bias Bounty Strats with Keith Hoodlet

**Guest:** Keith Hoodlet
**Format:** Show notes with timestamps (feed)
**Topics:** VDP debate continued, AI bias bounties, AppSec at scale, government regulation of bug bounty

### TL;DR
- Keith built AppSec at Thermo Fisher from scratch (Fortune 100, 130K employees, 11-person AppSec team at peak)
- VDPs have a place for companies with massive footprints — paying per-bug is unsustainable when you know you have thousands of bugs
- Keith paid occasional bounties to VDP researchers who consistently provided value (5K here, few K there)
- "Security poverty line" (Daniel Miessler) — only FANG/MANGO companies can afford full AppSec staffing
- AI bias bounties: identifying systematic biases in AI chatbots (racial, gender, political) by understanding human heuristics and applying adversarial questioning

### Key Takeaways
- At Thermo Fisher: 11 AppSec people for thousands of developers across 130K employees — "you eat the elephant one bite at a time"
- Variant analysis from VDP findings: one VDP bug taught devs how to hack their own apps via "hack Wednesdays" — the educational value of one finding can prevent hundreds of similar bugs
- Hacker who graduated college bought a car with Thermo Fisher's VDP bounties — selective payment for consistent value
- AI bias bounties require understanding human psychology, not just technical skill — "hacking the training data's human biases"
- Question: Should the government regulate minimum bounty requirements for companies above a certain revenue threshold?

### Techniques and Primitives
- **AI Bias Testing:** Use adversarial prompts to trigger model outputs that reveal systematic prejudice — requires understanding both the training data's biases and the model's guardrails
- **VDP-to-Bounty conversion:** Keep records of researchers who submit high-quality VDP reports → allocate budget for occasional payments to retain talent

### Tooling and Resources
- Daniel Miessler — "The Cybersecurity Skills Gap is Another Instance of Late-Stage Capitalism"
- `securing.dev` — Keith's blog
- Bugcrowd AI Bias Bounty program

### Suggestions and Advices
- **Keith:** "Security is a feature — it needs to be funded, maintained, and continuously tested like any other feature."
- "Companies do not exist to be secure. They exist to sell a product or service. Security allows them to outrun the bear."
- On VDPs: "If a hacker came to us with a VDP and said 'pay me,' I'd say 'I get it, go hack on programs that pay for your work.'"
- **Joel:** "If you're a profit-driven company, you should put money behind your security. 99% of the time, VDPs are inexcusable for companies with significant revenue."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Keith built AppSec at Thermo Fisher from scratch (Fortune 100, 130K employees, 11-person AppSec team at peak)

#### 2. What you should learn
- Understand **at thermo fisher: 11 appsec people for thousands of developers across 130k employees — "you eat the elephant one bite at a time"**
- Understand **variant analysis from vdp findings: one vdp bug taught devs how to hack their own apps via "hack wednesdays" — the educational value of one finding can prevent hundreds of similar bugs**
- Understand **hacker who graduated college bought a car with thermo fisher's vdp bounties — selective payment for consistent value**
- Understand **ai bias bounties require understanding human psychology, not just technical skill — "hacking the training data's human biases"**
- Understand **question: should the government regulate minimum bounty requirements for companies above a certain revenue threshold?**

#### 3. Core concepts explained
**AI Bias Testing: Use adversarial prompts to trigger model outputs that reveal systematic prejudice**
- requires understanding both the training data's biases and the model's guardrails

****VDP**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**AI Bias Testing: Use adversarial prompts to trigger model outputs that reveal systematic prejudice**
- **What it is:** requires understanding both the training data's biases and the model's guardrails
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**VDP-to-Bounty conversion: Keep records of researchers who submit high-quality VDP reports → allocate budget for occasional payments to retain talent**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Keith: "Security is a feature"* — **it needs to be funded, maintained, and continuously tested like any other feature.**
- *"Companies do not exist to be secure. They exist to sell a product or service. Security allows them to outrun the bear."*
- *"On VDPs: "If a hacker came to us with a VDP and said 'pay me,' I'd say 'I get it, go hack on programs that pay for your work.'"*
- *"Joel: "If you're a profit-driven company, you should put money behind your security. 99% of the time, VDPs are inexcusable for companies with significant revenue."*

#### 6. Mental models
- **Keith: "Security is a feature — it needs to be funded, maint** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Companies do not exist to be secure. They exist to sell a pr** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On VDPs: "If a hacker came to us with a VDP and said 'pay me** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** At Thermo Fisher: 11 AppSec people for thousands of developers across 130K employees — "you eat the elephant one bite at a time"
- **Try this:** Variant analysis from VDP findings: one VDP bug taught devs how to hack their own apps via "hack Wednesdays" — the educational value of one finding can prevent hundreds of similar bugs
- **Try this:** Hacker who graduated college bought a car with Thermo Fisher's VDP bounties — selective payment for consistent value
- **Try this:** AI bias bounties require understanding human psychology, not just technical skill — "hacking the training data's human biases"

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.
8. **Reflection:** What would you do differently if you had to redo this testing from scratch?

#### 11. The practical takeaway
1. **Keith built AppSec at Thermo Fisher from scratch (Fortune 100, 130K employees, 1**
2. **At Thermo Fisher: 11 AppSec people for thousands of developers across 130K emplo**
3. **Variant analysis from VDP findings: one VDP bug taught devs how to hack their ow**
