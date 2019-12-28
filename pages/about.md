---
layout: page
title: About
description: 咖啡生活
keywords: java, scala, dubbo, springcloud, scala 
comments: true
menu: 关于
permalink: /about/
---

优雅编程。

选择大于努力，坚持改变人生

## 联系

{% for website in site.data.social %}
* {{ website.sitename }}：[@{{ website.name }}]({{ website.url }})
{% endfor %}

## Skill Keywords

{% for category in site.data.skills %}
### {{ category.name }}
<div class="btn-inline">
{% for keyword in category.keywords %}
<button class="btn btn-outline" type="button">{{ keyword }}</button>
{% endfor %}
</div>
{% endfor %}
