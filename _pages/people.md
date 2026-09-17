---
layout: page
permalink: /people/
title: People
description: Members of CIS Lab.
nav: true
nav_order: 2
---

{% comment %}
  This page renders from _data/people.yml. Do not hand-edit names here.
  A field that is missing from the YAML is simply not shown, so an
  incomplete entry degrades to just a name rather than to an empty label.
{% endcomment %}

{% assign groups = "faculty,phd,ms,undergrad" | split: "," %}
{% assign labels = "Faculty,Ph.D. &amp; Integrated Students,M.S. Students,Undergraduate Students" | split: "," %}

{% for g in groups %}
  {% assign members = site.data.people[g] %}
  {% if members and members.size > 0 %}
<h3 class="people-group">{{ labels[forloop.index0] }}</h3>
<div class="people-grid">
    {% for m in members %}
  <div class="person">
    {% if m.image %}
    <img class="person-avatar"
         src="{{ '/assets/img/people/' | append: m.image | relative_url }}"
         alt="{{ m.name }}">
    {% else %}
    <div class="person-avatar person-avatar--blank" aria-hidden="true">{{ m.name | slice: 0 }}</div>
    {% endif %}
    <div class="person-body">
      <h5 class="person-name">{{ m.name }}</h5>
      {% if m.role %}<div class="person-role">{{ m.role }}{% if m.year %} · since {{ m.year }}{% endif %}</div>{% endif %}
      {% if m.topic %}<p class="person-topic">{{ m.topic }}</p>{% endif %}
      <p class="person-links">
        {% if m.email %}<a href="mailto:{{ m.email }}">{{ m.email }}</a>{% endif %}
        {% if m.homepage %} &middot; <a href="{{ m.homepage }}" target="_blank" rel="noopener">homepage</a>{% endif %}
        {% if m.scholar %} &middot; <a href="https://scholar.google.com/citations?user={{ m.scholar }}" target="_blank" rel="noopener">scholar</a>{% endif %}
        {% if m.github %} &middot; <a href="https://github.com/{{ m.github }}" target="_blank" rel="noopener">github</a>{% endif %}
      </p>
    </div>
  </div>
    {% endfor %}
</div>
  {% endif %}
{% endfor %}

{% if site.data.people.alumni and site.data.people.alumni.size > 0 %}
<h3 class="mt-5">Alumni</h3>
<ul class="alumni-list">
  {% for m in site.data.people.alumni %}
  <li class="alumni-item">
    <span class="alumni-name">{{ m.name }}</span>
    {% if m.degree %}<span class="alumni-degree">{{ m.degree }}</span>{% endif %}
    {% if m.now %}<span class="alumni-now">{{ m.now }}</span>{% endif %}
  </li>
  {% endfor %}
</ul>
{% endif %}

---

Interested in joining? Write to <a href="mailto:hskwon@inha.ac.kr">hskwon@inha.ac.kr</a>.
