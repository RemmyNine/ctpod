---
title: "The Master of Hacker Show&Tell: Inti De Ceukelaire"
episode: 33
---


# Episode 33 The Master of Hacker Show&Tell: Inti De Ceukelaire

**Guests/Hosts:** Justin Gardner, Joel Margolis, Inti De Ceukelaire (Inti / securinti)  
**Date:** 2023-08-24 | **Duration:** 1:22:01

### TL;DR
- Inti is the "master of show & tell" at live hacking events; his presentation skill comes from radio background
- CSS injection turned into a phishing page: reorder elements via CSS, add custom font for password mask, capture credentials
- Ticket trick: GitLab's email-to-ticket feature → sign up for Slack with that email → access GitLab's internal Slack
- Capture-the-flag style password leak: used CSS injection + iframe to display victim's password manager password as a CAPTCHA
- Goal-oriented hacking: set an objective rather than spraying for standard bugs

### Key Takeaways
- CSS injection is more powerful than most think: you can reorder elements, add custom fonts, and change `-webkit-text-security` to turn any field into a password field
- For live hacking events, set a goal (what data you want) and work backward; don't spray for standard vulnerabilities
- Collaboration with the customer: ask "where would you look for a critical?" at happy hour — this is reconnaissance, not social engineering
- Belgium's authorized testing law (with conditions) is now legal — a change Inti helped influence

### Bugs and Findings

#### CSS Injection → Credential Harvesting — Phishing via CSS
- **Target/context:** Collaboration platform (Inti couldn't pop XSS, only CSS injection)
- **Root cause:** Stored CSS injection allowed full control over element positioning and styling, including `-webkit-text-security` font property
- **Technique / how found:** Inti analyzed the CSS injection scope: he could inject a custom font via `@font-face` and reorder page elements
- **Exploitation steps:**
  1. Send victim a collaboration invite with CSS injection
  2. CSS repositions elements to mimic the login page
  3. A text input on the page is re-styled as a password field (custom font with dots)
  4. Victim types their password → value sent via form submission to attacker's server
- **Key technical details:** `@font-face` with custom font rendering dots | CSS repositions elements via position/absolute/z-index
- **Impact / severity / bounty:** Credential theft; paid (five-figure range for similar follow-up CSSi bugs)

#### Ticket Trick — Slack takeover via email-to-ticket
- **Target/context:** GitLab + Slack
- **Root cause:** GitLab's email-to-ticket feature created tickets from emails sent to `[hash]@incoming.gitlab.com`. Anyone with a `@gitlab.com` email could sign up for Slack.
- **Technique / how found:** Inti observed GitLab used Slack heavily; signed up for Slack using the `@incoming.gitlab.com` email from a ticket
- **Exploitation steps:**
  1. Create a support ticket on GitLab (receives a unique `@incoming.gitlab.com` email)
  2. Go to GitLab's Slack signup page, enter that email
  3. Slack sends verification to the email → it appears as a ticket comment
  4. Click the verification link → logged into GitLab's internal Slack
- **Key technical details:** Mail-to-ticket flow: any email to `@incoming.gitlab.com` creates a ticket | Slack allowed signup with any `@gitlab.com` email
- **Impact / severity / bounty:** Full access to GitLab's internal Slack (still VDP at the time, CEO personally paid $100)

#### CAPTCHA-style Password Theft — Credential theft
- **Target/context:** Password manager web app
- **Root cause:** The password manager displayed passwords in an iframe embeddable on any page; attacker could display but not read cross-origin
- **Technique / how found:** Inti realized he could iframe the password, but couldn't read it. Instead, he applied CSS filters and clipping to make the password look like a CAPTCHA challenge.
- **Exploitation steps:**
  1. Create a page that iframes the password manager showing the user's Facebook password
  2. Apply CSS filters, rotation, clipping to each letter to look like a distorted CAPTCHA
  3. Display "Please type the text above to prove you're human"
  4. Victim reads their own password and types it → attacker receives it
- **Key technical details:** `iframe` + CSS `filter` distortions | Each letter clipped and rotated independently
- **Impact / severity / bounty:** Plaintext password theft; critical

### Techniques and Primitives
- **CSS injection → phishing** — With CSS injection, you can load custom fonts (`@font-face`), reposition elements, change `-webkit-text-security`, and modify `content` properties to fake a login page
- **Email-to-ticket hijacking** — Find apps that auto-create tickets from inbound emails; use that email to register on third-party services (Slack, Zendesk, etc.)
- **PostMessage for client-side auth** — Applications using iframe + postMessage for auth can be abused if the origin check is missing or weak

### Tooling and Resources
- Inti's blog: `securinti.be`
- Live hacking events (Integrity/HackerOne/Bugcrowd)

### Suggestions and Advices from Hunter
- "It's not about the bug per se — a CSS injection must be low, right? But it resulted in plaintext passwords."
- "Set a goal. What kind of data do I want? Then look for the most exotic ways to get there, not the standard ways."
- "If you can't pop XSS, what else can you do with CSS injection? It's more powerful than you think."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Inti is the "master of show & tell" at live hacking events; his presentation skill comes from radio background

#### 2. What you should learn
- Understand **css injection is more powerful than most think: you can reorder elements, add custom fonts, and change `-webkit-text-security` to turn any field into a password field**
- Understand **for live hacking events, set a goal (what data you want) and work backward; don't spray for standard vulnerabilities**
- Understand **collaboration with the customer: ask "where would you look for a critical?" at happy hour — this is reconnaissance, not social engineering**
- Understand **belgium's authorized testing law (with conditions) is now legal — a change inti helped influence**

#### 3. Core concepts explained
**CSS Injection → Credential Harvesting — Phishing via CSS**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Ticket Trick — Slack takeover via email-to-ticket**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CAPTCHA-style Password Theft — Credential theft**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**CSS injection → phishing**
- With CSS injection, you can load custom fonts (`@font-face`), reposition elements, change `-webkit-text-security`, and modify `content` properties to fake a login page

**Email-to-ticket hijacking**
- Find apps that auto-create tickets from inbound emails; use that email to register on third-party services (Slack, Zendesk, etc.)

**PostMessage for client-side auth**
- Applications using iframe + postMessage for auth can be abused if the origin check is missing or weak


#### 4. Techniques and tactics
**CSS injection → phishing**
- **What it is:** With CSS injection, you can load custom fonts (`@font-face`), reposition elements, change `-webkit-text-security`, and modify `content` properties to fake a login page
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Email-to-ticket hijacking**
- **What it is:** Find apps that auto-create tickets from inbound emails; use that email to register on third-party services (Slack, Zendesk, etc.)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**PostMessage for client-side auth**
- **What it is:** Applications using iframe + postMessage for auth can be abused if the origin check is missing or weak
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"It's not about the bug per se"* — **a CSS injection must be low, right? But it resulted in plaintext passwords.**
- *"Set a goal. What kind of data do I want? Then look for the most exotic ways to get there, not the standard ways."*
- *"If you can't pop XSS, what else can you do with CSS injection? It's more powerful than you think."*

#### 6. Mental models
- **It's not about the bug per se — a CSS injection must be low,** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Set a goal. What kind of data do I want? Then look for the m** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you can't pop XSS, what else can you do with CSS injectio** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** CSS injection is more powerful than most think: you can reorder elements, add custom fonts, and change `-webkit-text-security` to turn any field into a password field
- **Try this:** For live hacking events, set a goal (what data you want) and work backward; don't spray for standard vulnerabilities
- **Try this:** Collaboration with the customer: ask "where would you look for a critical?" at happy hour — this is reconnaissance, not social engineering
- **Try this:** Belgium's authorized testing law (with conditions) is now legal — a change Inti helped influence

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **recon** — Reconnaissance — systematic discovery of target attack surface

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in CSS Injection → Credential Harvesting — Phishing via CSS?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Inti is the "master of show & tell" at live hacking events; his presentation ski**
2. **CSS injection is more powerful than most think: you can reorder elements, add cu**
3. **For live hacking events, set a goal (what data you want) and work backward; don'**
