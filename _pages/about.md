---
layout: about
title: home
permalink: /
subtitle: Computer & Intelligence Security Lab · Department of Computer Engineering · <a href="https://www.inha.ac.kr">Inha University</a>

profile:
  align: right
  # No lab photo yet. Add one to assets/img/ and set `image:` here; until then
  # the block shows the address only, which is better than a placeholder box.
  more_info: >
    <p>Room #1110, Inha Hi-Tech Center</p>
    <p>100 Inha-ro, Michuhol-gu</p>
    <p>Incheon 22212, Korea</p>

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
---

Software that is supposed to be secure very often is not, once it is deployed at scale. A browser accepts a certificate it should have rejected. A revoked certificate keeps working for weeks. A package arrives with a signature that proves less than it appears to prove. **CIS Lab studies that gap between what a security mechanism promises on paper and what it actually delivers in the field.**

We work mostly by measurement. We collect what is really out there, at the scale of the whole ecosystem rather than a handful of samples, and we report what we find. Recent work has covered the TLS and PKI ecosystem (certificate transparency, revocation, certificate validation in in-app browsers) and the software supply chain (what package attestation across ecosystems actually attests to). Alongside this we design cryptographic constructions for querying encrypted data.

Our results have appeared at IEEE S&P, ACM CCS, USENIX Security, IEEE TDSC, IEEE TIFS, and ACM Computing Surveys.

**We are recruiting.** Graduate and undergraduate students interested in this kind of work should read the [Join us]({{ '/join/' | relative_url }}) page.
