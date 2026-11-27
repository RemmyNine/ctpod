---
title: "Getting Started in Bug Bounty"
episode: 202
date: "2026-11-26"
source: "https://www.criticalthinkingpodcast.io/getting-started-in-bug-bounty/"
description: "Jonathan Dunn and Vitor Falcão discuss how they started in bug bounty, their first bugs, sharing and networking, AI and hackbots, mistakes, and learning the fundamentals before relying on AI."
---

**Guests:** Vitor Falcão

## TL;DR

- Both speakers began with modest, early reports and a developer or hands-on learning background, and they credit a shared recon course and a small, supportive peer chat with helping them get started.
- Sharing work, asking specific questions, and building genuine relationships mattered more than generic requests for mentorship.
- Manual hacking still has an edge over AI agents in multi-step, stateful areas such as authentication, payments, and integrations, where understanding the application and its business logic matters.
- Hacker intuition is presented as experience and pattern recognition built through practice, not a gift, and beginners are advised to learn fundamentals without AI first.

## Chapter notes

### 00:00:00 · Introduction

Jonathan Dunn introduces a special episode prompted by frequent messages asking how he and Vitor started, connected with other hackers, and found their early bugs. Vitor notes that he has appeared on the podcast before and no longer quite feels like a guest, while Jonathan says this is only his second episode hosting and that he still thinks of himself as a guest. Jonathan proposes starting with a bug each of them submitted very early in their careers.

### 00:01:57 · First bugs and starting bug bounty

Vitor says his first reported bug was an enabled GraphQL introspection finding: informational, with no security impact, and closed as a duplicate. He says he would not report it today, but describes it as a step toward hunting real vulnerabilities. He also describes an early stack-trace report and an exposed .git repository that leaked a whole application's source code, found after taking Jason Haddix's recon course and becoming absorbed in directory and file discovery. That report was treated as critical because source code and secrets were exposed; Vitor says reading the code was risky and something he would not do again. Jonathan says he has never found an exposed .git repository himself.

Jonathan says his first reported bug, in January 2023, was a self-XSS on an internal tool, using a script that inserted a link. Vitor says he also found SQL injection early, after deciding to start testing for it. Jonathan says his AI agent has since found more SQL injection than he ever found himself.

On backgrounds, Vitor says he had almost no hacking skills at the start, had done Hack The Box for a few years, and had been a developer, able to pick up languages from documentation and read front-end code, including minified JavaScript, which later helped. Jonathan places their starting and submitting activity around 2022, and Vitor says he was then tired of being a developer and wanted to move into security. Both say Jason Haddix's course was a shared starting point. Through it, Vitor met Ryan, known as Roll for Combat, who invited him into a small chat; Jonathan separately messaged Ryan after the course, was invited into the same chat, and met Vitor there. Both describe the chat as non-judgmental and a place where they could ask basic questions. Vitor says he understood early the power of sharing, and Jonathan agrees that many people in chats do not share, while he tried to contribute. Vitor also describes working on a program alongside another hacker and independently finding the same bug, which convinced him that even more experienced hackers find things through the same process, and that collaborating with someone at a similar skill level was energizing.

### 00:22:04 · Sharing, reaching out to higher tier hackers, and how to network

Vitor advises approaching more advanced hackers with something specific to offer or ask, rather than a generic request for mentorship. He recounts that Justin Gardner had said on the podcast that he would not mentor anyone he did not know in person. Vitor had been active in the podcast community chat, had written a blog, was finding bugs, had quit his job, and needed support with non-technical aspects such as writing, presenting, and making videos. He messaged Justin specifically about help with that work, received a positive reply, and was mentored; Jonathan adds that Justin already thought highly of Vitor's hacking before that.

Jonathan says his own approach was different: he was not deliberately networking, but shared techniques and findings, for example sharing a technique that led to building an API-related project with another hacker, and found that sharing work exposed it but also built relationships. Vitor says he kept a large list of blog posts he could search and share, and wrote his own blog to give back to the community. Both advise sharing even imperfect work, knowing a topic deeply enough to impress people, and treating networking as building genuine relationships rather than extracting help. Near the end of this section, Vitor says his developer background, including debugging minified code, led him into client-side hacking, and that a five-figure client-side bug found mostly with a collaborator reinforced that direction.

### 00:36:20 · AI and hackbots, and hacker intuition

Vitor says he has been mapping areas hackbots avoid, arguing that manual hackers should go to authentication, payments, and integrations — for example, a platform that connects to Google Drive to act on files — where bots struggle with multi-step flows, state, and business logic, and where understanding the application matters. He reports finding eight or nine bugs in the previous week by manually hacking in such areas. Both agree AI is weak at business-logic flaws and do not expect it to close that gap imminently.

On intuition, Vitor argues it is not magic: it is experience and pattern matching built by doing the work, including asking what a feature is supposed to do, what could go wrong, and where a security boundary can be broken, especially in multi-step chains. Jonathan notes chains of three steps, and often five to ten steps. Jonathan distinguishes technical intuition, knowing how things work under the hood, from persistence — not stopping at a wall until the bug appears — and from pattern recognition in client-side and server-side behaviour. Both say intuition only comes from hands-on experience, not just reading; Jonathan says making his own small labs helped, and Vitor cites building features himself as an example of learning by building.

### 00:47:11 · Mistakes, regrets, and bugs that changed you

Vitor says his main regret is giving up repeatedly and remaining a developer longer than necessary, partly because of marketing that promised a workflow or automation setup would produce a bug within 24 hours. He says he spent too much time building automation and tools that were sold, rather than hunting. Jonathan regrets jumping from program to program in his first year instead of staying with one program long enough to learn it deeply. Vitor agrees, and says Justin advised him to spend a set period focused on one program, advice he credits with helping his progress.

Bugs that changed them include live-hacking-event finds and long transformation chains that changed how they map an application. Jonathan describes a chain he found that taught him about chaining: cookie smuggling, then XSS via cookie smuggling combined with login and logout CSRF, then persistent XSS on a main domain via a localStorage parameter, culminating in account takeover. He also says hacking with rez0, Joseph Thacker, on a hackbot changed his approach: rez0 thinks big-picture while Jonathan works in details, and Jonathan learned how to communicate with triagers and to collaborate with an automated agent rather than only compete with it. Vitor adds that collaboration, even with a hackbot, opens up thinking, and that he moved from chasing only non-duplicate, hard bugs to accepting that some reported bugs may duplicate. He also describes a recent find involving many connected services that reminded him, after years of experience, to test everything. Jonathan notes hackbot findings he does not yet understand, including a case requiring a victim to paste something into developer tools.

### 01:01:54 · Learning

For beginners, Vitor advises learning without AI first: do capture-the-flag exercises on a time limit — he suggests about two hours — without AI, then use AI for help on what remains, so the fundamentals are actually learned. Using a gym analogy, he says the struggle is the training. He warns that asking AI to teach a topic from zero, such as heap exploitation, can produce poor teaching because the learner cannot judge it, and stresses prompting AI well so it teaches rather than just answers.

Jonathan says he recently started learning heap exploitation, that AI helped him get past the assembly hurdle where he would otherwise have quit halfway, and that Vitor's stronger assembly background helped him relearn memory layout. Jonathan says he uses AI constantly as an audio learner, valuing tools that cite sources he can check, and that he re-used Jason Haddix's course material for a current engagement. He describes treating AI as a knowledgeable person he can consult.

## Key takeaways

- Start by reporting and learning from small findings, and treat early informational or duplicate reports as steps toward real vulnerabilities rather than as the goal.
- Build relationships by sharing specific work and asking specific questions; generic mentorship requests and extracting help without contributing are less effective.
- Focus manual effort where automation struggles: multi-step flows, state, authentication, payments, integrations, and business logic, and learn the application deeply before testing it.
- Learn fundamentals hands-on first, including through time-limited exercises and small labs, and use AI to support learning and verification rather than as a substitute for understanding.

## Reference concepts

- **GraphQL introspection**: A GraphQL feature that exposes a schema describing available queries and types; leaving it enabled can reveal application structure even when it has no direct security impact on its own.
- **Self-XSS**: Cross-site scripting that requires the victim's own action, such as pasting or running code themselves, which limits its impact compared with XSS that an attacker can trigger for another user.
- **Business-logic flaw**: A weakness in how an application enforces its intended workflow, state, or permissions, which often requires understanding the feature rather than only testing individual inputs.
- **Hacker intuition**: Pattern recognition built through hands-on experience, including asking what a feature should do, what could go wrong, and where a security boundary can be broken across a chain of steps.

## Source

[Critical Thinking Bug Bounty Podcast: Episode 202, show notes and transcript](https://www.criticalthinkingpodcast.io/getting-started-in-bug-bounty/)
