---
title: "Cloud Hacking w/ Nick Copi"
episode: 200
date: "2026-11-12"
source: "https://www.criticalthinkingpodcast.io/cloud-hacking-w-nick-copi/"
description: "JD and Nick Copi examine cloud-service threat models, tenant boundaries, identity permissions, storage behavior, and research practices for assessing provider-side risk."
---

**Guests:** Nick Copi

## TL;DR

- A cloud service’s custom integration code can create security risks that are easy to miss without understanding the service’s architecture and trust boundaries.
- Cloud assessments should distinguish customer-controlled weaknesses from provider failures, especially failures that undermine tenant isolation.
- Identity permissions, service-to-service trust, and shared storage can connect otherwise separate parts of a cloud environment.
- The episode emphasizes validating impact within program scope and treating AI as a research aid rather than a substitute for threat modeling.

## Chapter notes

### 00:03:16 · A Client-Side Cloud Service Bug

Copi describes finding an unsafe command-handling flaw in custom code for a deployed cloud service, where access to the instance made its implementation inspectable. The discussion highlights how a seemingly narrow application weakness can have broader consequences when the service carries cloud permissions.

### 00:13:38 · Cloud Provider Dashboards

The hosts distinguish provider dashboards from deployed services and discuss how rich configuration interfaces create different kinds of attack surface. Copi stresses learning how a service is built and how its credentials are scoped, rather than assuming all provider pages or services share the same security properties.

### 00:24:08 · Larger Cloud Threat Model

Copi frames cloud security around shared responsibility and the boundary between customer data processing and provider orchestration. A key concern is whether permissions or trusted connections associated with a customer-facing instance could expose provider resources or weaken tenant isolation.

### 00:37:33 · Approach to Hacking Providers that use the Cloud

The conversation favors understanding a service’s architecture and testing its customer-facing components before drawing conclusions about provider impact. Copi discusses using focused research and AI assistance to examine complex integrations, while emphasizing that access to one’s own instance does not by itself establish a provider vulnerability.

### 00:59:53 · Identity Services & S3 Buckets

The hosts explore how cloud identities and role delegation can create confused-deputy risks when users or jobs receive broader permissions than intended. They also discuss object-storage behaviors, including how shared buckets and response metadata may affect the security of applications that consume stored content.

## Key takeaways

- Design customer-facing services with the assumption that a tenant may inspect or control its own data-plane environment; do not rely on that environment remaining opaque.
- Apply least privilege to service identities, temporary credentials, and delegated roles, and review permissions as service architecture changes.
- Keep provider control-plane operations isolated from customer-controlled workloads, and validate tenant boundaries through authorized, non-destructive testing.
- Separate provider security failures from customer configuration issues when triaging reports, and make program scope and safe validation expectations clear to researchers.

## Reference concepts

- **Shared responsibility model**: The division of security responsibilities between a cloud provider and the customer using its services.
- **Data plane and control plane**: The data plane processes customer workloads; the control plane provisions, manages, and records cloud resources.
- **Confused deputy**: A trust-boundary failure in which a service with greater authority performs an action for a less-privileged user without adequate permission checks.
- **Managed identity**: A cloud-provided identity used by a workload to access other services; its permissions should be narrowly scoped.

## Source

[Critical Thinking Bug Bounty Podcast: Episode 200, show notes and transcript](https://www.criticalthinkingpodcast.io/cloud-hacking-w-nick-copi/)
