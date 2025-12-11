---
layout: single
title: "Photo Album (by Date)"
permalink: /photos/date-album/
author_profile: false
toc: true
toc_label: "Years"
toc_icon: "calendar"
---

Welcome to our photo album organized by date! Browse through photos grouped by year and month.

{% assign photos_json = site.data.photos.by-date %}
{% assign photos_by_year = photos_json.photos | group_by: "year" | sort: "name" | reverse %}

{% for year_group in photos_by_year %}
## {{ year_group.name }}

{% assign photos_by_month = year_group.items | group_by: "month_name" %}
{% for month_group in photos_by_month %}
### {{ month_group.name }} {{ year_group.name }}

<div class="photo-gallery">
{% for photo in month_group.items %}
  <div class="photo-item" style="display: inline-block; margin: 10px; text-align: center; vertical-align: top; width: 300px;">
    <a href="{{ photo.path }}" title="{{ photo.title }}">
      <img src="{{ photo.thumbnail }}" alt="{{ photo.title }}" style="max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    </a>
    <p style="margin-top: 8px; font-size: 0.9em; color: #666;">
      <strong>{{ photo.title }}</strong><br>
      <small>{{ photo.date }}</small>
    </p>
  </div>
{% endfor %}
</div>

{% endfor %}
{% endfor %}

---

<div style="background-color: #f0f0f0; padding: 20px; border-radius: 8px; margin-top: 40px;">
<h3 style="margin-top: 0;">About This Album</h3>
<p>This photo album contains {{ photos_json.total_count }} photos organized by date. Photos are automatically grouped by year and month for easy browsing.</p>
<p><small>Last updated: {{ photos_json.generated_at | date: "%B %d, %Y" }}</small></p>
</div>

<style>
.photo-gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 10px;
  margin-bottom: 30px;
}

.photo-item img {
  transition: transform 0.2s ease;
}

.photo-item img:hover {
  transform: scale(1.05);
}
</style>
