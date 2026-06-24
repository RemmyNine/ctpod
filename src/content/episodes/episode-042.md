---
title: "Renniepak Interview & Intigriti LHE Recap"
episode: 42
---


# Episode 42 Renniepak Interview & Intigriti LHE Recap

### TL;DR
- Renee (Renniepak) — top 11 on Intigriti, full-time bounty hunter for 1.5 years
- Found XSS in NFT platforms by minting own NFTs with malicious metadata — bypasses platform input validation
- Emphasis on postMessage XSS as underexplored territory
- Live hacking event in Portugal with Intigriti; discussion of sponsored vs self-sponsored attendance

### Key takeaways
- Web3/Web2 bridge: mint your own NFT with XSS payloads in metadata fields; platforms that accept ERC-721 metadata blindly re-render it
- postMessage is critically underexplored — origin checks are often missing or use bad regex (unescaped dots)
- Custom browser extensions for monitoring reflected XSS in query params and postMessage listeners
- Collaboration: having a fresh set of eyes on a bug breaks assumptions

### Bugs and Findings
#### XSS via ERC-721 NFT Metadata
- **Target/context:** NFT marketplaces/platforms that accept ERC-721 tokens
- **Root cause:** Platforms trust metadata from user-minted NFTs; they don't re-validate input
- **Technique / how found:**
  1. Mint own NFT directly on Ethereum (bypass platform's input validation)
  2. Embed XSS payloads in every metadata field (name, description, image URL, etc.)
  3. When platform renders the NFT, payload executes
- **Key technical details:** Uses ERC-721 standard; Ethereum blockchain is permissionless — anyone can mint
- **Impact / severity / bounty:** XSS in the platform's primary UI, can lead to wallet/account compromise

### Techniques and Primitives
- **postMessage origin regex bypass** — unescaped dots in origin regex (`/.*attacker.com/` matches `Xattacker.com`)
- **Reflected XSS via browser extension** — custom extension injects a harmless payload into every query param and pops an alert if reflected

### Tooling and Resources
- **PostMessage Tracker** (by Frans Rosen) — Chrome extension to monitor postMessage listeners
- **Custom browser extension** for monitoring reflected parameters
- **Hacker Hideout** (.xyz) — Dutch hackers' community/co-working initiative

### Suggestions and Advices from Hunter
- "I'm really into XSS. In the Web3 ecosphere, it's much more critical because there is no server-side stuff"
- On full-time bounty: "The most challenging part is working alone" — solved by co-working space
- "Give yourself a fixed salary and keep a buffer — it removes the stress of month-to-month volatility"

### AI Takeaway
The NFT metadata XSS is a perfect example of platform trust assumptions breaking down: anyone can mint an ERC-721 token, and the platform blindly trusts the metadata. The "mint your own token" bypass applies to any system that ingests user-controlled blockchain data.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Renee (Renniepak) — top 11 on Intigriti, full-time bounty hunter for 1.5 years

#### 2. What you should learn
- Understand **web3/web2 bridge: mint your own nft with xss payloads in metadata fields; platforms that accept erc-721 metadata blindly re-render it**
- Understand **postmessage is critically underexplored — origin checks are often missing or use bad regex (unescaped dots)**
- Understand **custom browser extensions for monitoring reflected xss in query params and postmessage listeners**
- Understand **collaboration: having a fresh set of eyes on a bug breaks assumptions**

#### 3. Core concepts explained
**XSS via ERC-721 NFT Metadata**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

**postMessage origin regex bypass**
- unescaped dots in origin regex (`/.*attacker.com/` matches `Xattacker.com`)

**Reflected XSS via browser extension**
- custom extension injects a harmless payload into every query param and pops an alert if reflected


#### 4. Techniques and tactics
**postMessage origin regex bypass**
- **What it is:** unescaped dots in origin regex (`/.*attacker.com/` matches `Xattacker.com`)
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Reflected XSS via browser extension**
- **What it is:** custom extension injects a harmless payload into every query param and pops an alert if reflected
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"I'm really into XSS. In the Web3 ecosphere, it's much more critical because there is no server-side stuff"*
- *"On full-time bounty: "The most challenging part is working alone"* — **solved by co-working space**
- *"Give yourself a fixed salary and keep a buffer"* — **it removes the stress of month-to-month volatility**

#### 6. Mental models
- **I'm really into XSS. In the Web3 ecosphere, it's much more c** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **On full-time bounty: "The most challenging part is working a** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Give yourself a fixed salary and keep a buffer — it removes ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Web3/Web2 bridge: mint your own NFT with XSS payloads in metadata fields; platforms that accept ERC-721 metadata blindly re-render it
- **Try this:** postMessage is critically underexplored — origin checks are often missing or use bad regex (unescaped dots)
- **Try this:** Custom browser extensions for monitoring reflected XSS in query params and postMessage listeners
- **Try this:** Collaboration: having a fresh set of eyes on a bug breaks assumptions

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in XSS via ERC-721 NFT Metadata?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Renee (Renniepak) — top 11 on Intigriti, full-time bounty hunter for 1.5 years**
2. **Web3/Web2 bridge: mint your own NFT with XSS payloads in metadata fields; platfo**
3. **postMessage is critically underexplored — origin checks are often missing or use**
