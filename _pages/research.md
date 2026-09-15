---
layout: page
permalink: /research/
title: research
description: What we work on, and why.
nav: true
nav_order: 1
---

Our questions tend to start the same way: a security mechanism has been standardized, shipped, and widely adopted, and everyone assumes it works. We go and check.

---

## The TLS and PKI ecosystem

HTTPS rests on a certificate system that is large, distributed, and run by many independent parties. That makes it very hard to reason about from the specification alone, and it is where most of our work has gone.

We have looked at **certificate transparency**, where public logging of certificates is supposed to make misissuance detectable, and asked what it costs the parties who have to participate ([TDSC 2023]({{ '/publications/' | relative_url }})). We have surveyed **certificate revocation**, where the mechanisms that are supposed to withdraw a compromised certificate have accumulated decades of partial fixes ([ACM CSUR 2026]({{ '/publications/' | relative_url }})). And we have measured **certificate validation in in-app browsers**, the embedded webviews inside messaging and social apps, where a large fraction of mobile browsing actually happens and where validation turns out to be weaker than in the real browser next to it ([ACM CCS 2025]({{ '/publications/' | relative_url }})).

Earlier work in this line showed how cookie security flags could be stripped over HTTPS, letting an attacker steal session cookies that the flags were meant to protect ([IEEE TIFS 2020]({{ '/publications/' | relative_url }})).

---

## Software supply chain security

When you install a package, you are trusting a chain of parties you have never audited. Ecosystems have responded with signing and attestation: PyPI, npm, crates.io, Maven, NuGet, RubyGems and others now let a publisher attach evidence about where a package came from.

We ask what that evidence actually establishes. Our study across ecosystems found that the guarantee varies a great deal between them, and that a badge indicating "verified provenance" can mean substantially less than a developer would reasonably assume ([IEEE S&P 2027]({{ '/publications/' | relative_url }})).

We are extending this to the assurance that build and release infrastructure can offer in the first place, and to what a consumer of a package can check on their own.

---

## Searching and querying encrypted data

Data moved to a cloud provider should stay confidential from that provider, but it still has to be queryable. This line of our work designs constructions that allow range queries, similarity search and deduplication directly over encrypted data, with attention to what each one leaks and how key management survives users joining and leaving.

Recent work covers order-revealing encryption for range queries that span separate databases ([IJIS 2026]({{ '/publications/' | relative_url }})), multiwriter/multireader similarity search ([IEEE Access 2022]({{ '/publications/' | relative_url }})), and key management for secure deduplication ([IEEE CLOUD 2017]({{ '/publications/' | relative_url }})).

---

## How we work

Most of our projects involve building a measurement tool, pointing it at a real ecosystem, and dealing with what comes back. Students end up writing a fair amount of code, reading specifications closely, and arguing about whether a result means what it appears to mean. If that sounds like your kind of work, see [Join us]({{ '/join/' | relative_url }}).
