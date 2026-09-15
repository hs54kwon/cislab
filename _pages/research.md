---
layout: page
permalink: /research/
title: Research
description: What we work on, and why.
nav: true
nav_order: 1
---

Our questions tend to start the same way. A security mechanism gets standardized and then widely deployed, at which point everyone assumes it works well. We go and check whether it does.

The work below spans measurement, formal analysis, and attack construction. Which of the three a project uses depends on what would actually settle the question.

---

## The TLS and PKI ecosystem

HTTPS rests on certificates that many independent parties issue, log, validate and revoke. That makes the system hard to reason about from the specification alone, and it is where most of our published work has gone.

We have studied **certificate transparency**, where public logging is meant to make misissuance detectable, and what it costs the parties who have to take part. We have surveyed **certificate revocation**, whose mechanisms have accumulated decades of partial fixes. And we have measured **certificate validation in in-app browsers**, the embedded webviews inside messaging and social apps, where a large share of mobile browsing actually happens and where validation turns out to be weaker than in the real browser beside it.

Earlier work in this line showed how cookie security flags could be stripped over HTTPS, letting an attacker take session cookies the flags were meant to protect.

## Web session and authorization security

A newer line looks at what happens to session material once it reaches the browser. Modern single-page applications built on OAuth 2.1 can be deployed in several architectures, and that choice decides which credentials remain in the browser and what protects them. We are studying it against an adversary holding a privileged position inside the browser itself, and asking what stays reachable when every protection mechanism is working as designed.

The work combines formal verification of the protocol conditions with experiments against real deployments.

## Software supply chain security

Installing a package means trusting a chain of parties nobody has audited. Registries have responded with signing and attestation, and a growing number of ecosystems now let a publisher attach evidence about where a package came from.

We ask what that evidence actually establishes. Our study across ecosystems found that the guarantee differs a great deal between them, and that a badge reading "verified provenance" can mean substantially less than a developer would reasonably assume.

## Security of AI coding agents

Coding agents run build systems, test runners and other development tooling against repositories nobody has inspected yet, and they do it with the developer's own permissions. A repository can therefore get code executed before the agent has read any of it.

We are studying what an untrusted repository can lead such an agent to do, how that depends on what the repository looks like, and how far the behaviour differs between agents that are meant to be comparable. Findings that affect deployed products go to the vendors before they go anywhere else.

## Side channels in shared hardware

GPUs are increasingly shared between tenants that are not supposed to learn anything about each other. Scheduling is a recently recognized source of leakage in that setting, and most of what is known about it comes from environments far cleaner than a real multi-tenant machine.

We are looking at what scheduling behaviour leaks once the noise of co-running workloads is taken seriously rather than assumed away.

## Mobile forensics

In-app browsers keep browsing activity inside each host application rather than in one browser. That scatters the evidence an investigator would need and makes it hard to attribute an action to the application that produced it.

Building on our measurement work on these browsers, we are developing methods to recover browsing activity on Android, attribute it to the application it came from, and reconstruct a timeline out of fragmented traces.

## Encrypted data and learning-based analysis

Data handed to a cloud provider should stay confidential from that provider while remaining queryable. This line designs constructions supporting range queries, similarity search and deduplication directly over encrypted data, with attention to what each one leaks and how key management survives users joining and leaving.

Alongside it, we apply deep learning to the security analysis of network traffic, where the content is unavailable and the question is what can still be inferred from what remains visible.

---

## How we work

Most projects here start by building something: a measurement tool, a formal model, or a working attack. Students end up writing a fair amount of code, reading specifications closely, and arguing about whether a result means what it appears to mean. If that sounds like your kind of work, write to <a href="mailto:hskwon@inha.ac.kr">hskwon@inha.ac.kr</a>.
