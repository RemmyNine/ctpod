---
title: "Harley & Ariel - Your Guide to Bug Bounty Village 2026"
episode: 185
date: "2026-07-30"
source: "https://www.criticalthinkingpodcast.io/harley-ariel-your-guide-to-bug-bounty-village-2026/"
description: "Harley Kimball and Ariel Garcia preview Bug Bounty Village 2026, from its hands-on CTF and packed agenda to responsible AI-assisted research and reporting."
---

**Guests:** Harley Kimball, Ariel Garcia

## TL;DR

- Harley and Ariel share contrasting stories about serious account and transaction-authorization flaws, emphasizing how impact depends on the full context.
- Bug Bounty Village 2026 will feature a realistic AI-themed CTF, in-person and remote participation, and feedback on report quality.
- The expanded village layout is designed to support talks, collaboration, and community activities, alongside a busy agenda focused heavily on AI and security research.
- Harley describes scaling AI-assisted research while stressing that researchers remain responsible for their agents’ actions and scope.

## Chapter notes

### 00:04:39 · Podcast ATO & ATM Hacks

Harley recounts finding a serious account-access issue in podcasting software, illustrating how separate application flows can combine into substantial impact. Ariel describes an authorized assessment of an ATM cash-withdrawal feature that revealed a transaction-authorization weakness.

### 00:17:12 · Bug Bounty Village Preview

Harley and Ariel preview the village’s events, including a CTF built around a fictional AI company with multiple connected components. The challenge will welcome remote and in-person participants and provide triager feedback intended to help improve vulnerability reports.

### 00:31:02 · BBV Room Layout and Swag

The organizers describe a larger space with seating for talks and a lounge for researchers to meet and collaborate, plus a separate area for CTF participants. They also discuss interactive badges, challenge coins, and other activities designed to make the village more engaging.

### 00:42:36 · BBV Agenda

The hosts highlight talks and panels spanning AI security, hackbots, platform perspectives, and other bug bounty research topics. The organizers explain how the two talk tracks divide hands-on sessions from shorter presentations and panels.

### 01:10:57 · Harley's Hackbot

Harley explains at a high level how his AI-assisted research system grew to include specialized agents and processes for reviewing potential findings. He emphasizes that automation does not transfer responsibility: researchers need safeguards around authorization, scope, and actions taken by their agents.

## Key takeaways

- Financial and account-management features should enforce authorization at the transaction level, with testing designed to verify that one user cannot initiate actions for another.
- Autonomous research systems need clear scope boundaries and checks that confirm activity remains authorized; the human operator remains accountable for agent behavior.
- Useful bug bounty reports should explain reproducible steps, impact, and supporting evidence, rather than relying on a terse claim or demonstration alone.
- Community events can strengthen research practice by combining technical learning, collaboration, and constructive feedback from experienced triagers.

## Reference concepts

- **Bug Bounty Village**: A DEF CON community space organized around bug bounty talks, hands-on activities, a CTF, and opportunities for researchers to connect.
- **AI-assisted research governance**: The oversight practices needed when AI agents assist security research, including authorization awareness, scope limits, and human accountability.
- **Report quality and triage**: The practice of communicating findings with clear reproduction steps, evidence, and impact so reviewers can assess them effectively.
- **Community-led security learning**: A model of learning that brings researchers, platforms, and program representatives together for shared discussion and practical feedback.

## Source

[Critical Thinking Bug Bounty Podcast: Episode 185, show notes and transcript](https://www.criticalthinkingpodcast.io/harley-ariel-your-guide-to-bug-bounty-village-2026/)
