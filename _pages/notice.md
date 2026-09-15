---
layout: page
permalink: /notice/
title: Notice
description: Announcements from the lab.
nav: true
nav_order: 4
---

{% comment %}
  Every entry in _news/ appears here, newest first.

  Two kinds of entry, set by `inline:` in the file's front matter:
    inline: true   short, one or two sentences, shown in full right here.
                   These are the ones that also appear on the home page.
    inline: false  longer notice. Needs a `title:`; it gets its own page and
                   is linked from here by that title.

  The home page shows only the five most recent entries; this page shows all.
{% endcomment %}

{% assign notices = site.news | sort: 'date' | reverse %}

{% if notices.size == 0 %}

Nothing posted yet.

{% else %}
<ul class="notice-list">
  {% for item in notices %}
  <li class="notice-item">
    <div class="notice-date">{{ item.date | date: '%B %-d, %Y' }}</div>
    <div class="notice-body">
      {% if item.inline %}
        {{ item.content | remove: '<p>' | remove: '</p>' }}
      {% else %}
        <a class="notice-title" href="{{ item.url | relative_url }}">{{ item.title }}</a>
        {% if item.description %}<div class="notice-desc">{{ item.description }}</div>{% endif %}
      {% endif %}
    </div>
  </li>
  {% endfor %}
</ul>
{% endif %}
