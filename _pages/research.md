---
layout: page
permalink: /research/
title: Research
description: What we work on.
nav: true
nav_order: 1
---

Our questions tend to start the same way. A security mechanism gets standardized and then widely deployed, at which point everyone assumes it works well. We go and check whether it does.

Depending on what would actually settle a question, a project may rest on large-scale measurement, on formal analysis, or on building the attack and seeing whether it runs.

---

## Web and PKI security

HTTPS rests on certificates that many independent parties issue, log, validate and revoke, which makes the system hard to reason about from the specification alone. Most of our published work sits here: certificate transparency, certificate revocation, certificate validation inside the embedded browsers of messaging and social apps, and cookie protection over HTTPS.

We also work on what happens to session and authorization material once it reaches the browser.

## Software supply chain security

Installing a package means trusting a chain of parties nobody has audited. Registries have answered with signing and attestation, and we ask what that evidence actually establishes. Our cross-ecosystem study found the guarantee behind a "verified provenance" indicator differs a great deal between registries.

## AI security

AI agents now act on developer machines and on code and data that nobody has inspected. We study what that exposure allows, and how far behaviour differs between systems that are meant to be comparable.

## Systems security and digital forensics

Two directions. One is side-channel leakage on hardware shared between tenants who are not supposed to learn anything about each other. The other is mobile forensics, where evidence of user activity is scattered across applications rather than held in one place.

## Applied cryptography and data analysis

Data handed to a cloud provider should stay confidential from that provider while remaining queryable. We design constructions for range queries, similarity search and deduplication over encrypted data, with attention to what each one leaks.

We also apply deep learning to network traffic analysis, where the content is unavailable and the question is what can still be inferred from what remains visible.

---

## How we work

Most projects here start by building something: a measurement tool, a formal model, or a working attack. Students end up writing a fair amount of code, reading specifications closely, and arguing about whether a result means what it appears to mean. If that sounds like your kind of work, write to <a href="mailto:hskwon@inha.ac.kr">hskwon@inha.ac.kr</a>.
