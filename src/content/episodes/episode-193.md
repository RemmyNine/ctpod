---
title: "Browser Logic Errors & XS-Leaks with Jorian Woltjer"
episode: 193
date: "2026-09-24"
source: "https://www.criticalthinkingpodcast.io/browser-logic-errors-xs-leaks-with-jorian-woltjer/"
description: "A technical field guide to browser edge cases, cross-site leaks, redirect behavior, DNS rebinding defenses, and the risks new HTML features pose to sanitizers."
---

**Guests:** Jorian Woltjer

## TL;DR

- Woltjer recounts a CTFd research finding that used differences in browser-observable responses to illustrate how small status and history behaviors can create cross-site information leaks.
- An inconsistent script-loading result led to an ORB investigation: service-worker behavior changed request metadata, revealing an interaction between browser components.
- The discussion surveys obscure navigation and pop-up behaviors that can undermine assumptions in OAuth flows and user-interface protections.
- Browser local-network protections complicate DNS-rebinding risks, while newer HTML parsing features raise fresh questions for sanitizers.

## Chapter notes

### 00:04:19 · CTFd status-code XS-Leak

Woltjer describes a research finding in which distinct response outcomes could be observed through browser behavior, creating a way to infer information. The discussion emphasizes how browser history and styling behavior can become privacy-relevant signals, and notes that browser changes such as history partitioning affect the surrounding assumptions.

### 00:18:05 · Research journey and an ORB mystery

Woltjer traces his path from CTFs and penetration testing to a security-research role, then explains how a community question about inconsistent script-loading behavior prompted investigation. Comparing network observations with service-worker behavior and browser source code exposed an interaction involving request destination metadata and ORB.

### 00:33:39 · Stopping redirects

The discussion examines cases where an in-progress navigation, an automatic form submission, or browser limits can interfere with an expected redirect. Woltjer frames these behaviors as useful research clues and as reasons to test complete browser flows, particularly where redirects and OAuth handling affect security assumptions.

### 00:58:55 · DNS rebinding in the browser

Woltjer distinguishes browser-based DNS-rebinding concerns from server-side filtering issues, including the possibility of a browser reaching local or internal services. He describes Local Network Access protections and points to host-header validation as one defensive check used by local applications.

### 01:24:33 · Declarative partial updates

The conversation explores new HTML mechanisms that can defer and insert content, creating parsing states that server-side processors and sanitizers may not anticipate. Woltjer also discusses browser-managed cloning in select elements and recounts a DOMPurify bypass that was fixed within hours of its discovery.

## Key takeaways

- Treat browser-observable differences, such as navigation outcomes, load events, history state, and focus changes, as potential privacy signals during security reviews.
- When behavior varies across browsers or sites, isolate variables systematically; inspect service workers, request metadata, and browser implementation details before attributing it to a local anomaly.
- Test security-sensitive flows as complete browser interactions, including redirects, automatic submissions, pop-ups, and focus transitions, rather than validating only server responses.
- Local services should validate expected hosts and origins, and browser local-network protections should be considered an additional layer rather than the only safeguard.

## Reference concepts

- **Cross-site leaks (XS-Leaks)**: Information inference through browser-observable differences, even when an attacker cannot directly read a cross-origin response.
- **Visited-link privacy**: Browser history and link styling can expose state that websites may not intend to disclose; partitioning and careful browser behavior reduce this risk.
- **Opaque Response Blocking (ORB)**: A browser mechanism that blocks certain cross-origin responses from being used in contexts such as scripts; its interactions with service workers can produce surprising outcomes.
- **Service-worker request mediation**: Service workers can intercept and forward requests, potentially changing request metadata in ways that affect downstream browser handling.

## Source

[Critical Thinking Bug Bounty Podcast: Episode 193, show notes and transcript](https://www.criticalthinkingpodcast.io/browser-logic-errors-xs-leaks-with-jorian-woltjer/)
