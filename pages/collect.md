---
layout: page
title: Collect
description: 咖啡生活
keywords: java, scala, dubbo, springcloud, scala 
comments: true
menu: 收藏
permalink: /collect/
---

收集优秀网站，优秀开源软件

选择大于努力，坚持改变人生

## 开源软件

{% for website in site.data.github %}
* {{ website.sitename }}：[@{{ website.name }}]({{ website.url }})
{% endfor %}

<!-- ## Skill Keywords

{% for category in site.data.skills %}
### {{ category.name }}
<div class="btn-inline">
{% for keyword in category.keywords %}
<button class="btn btn-outline" type="button">{{ keyword }}</button>
{% endfor %}
</div>
{% endfor %} -->
