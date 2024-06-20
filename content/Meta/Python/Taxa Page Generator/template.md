---
title: {{ name }}
enableToc: true
tags:
  - biology/taxa{% if tags == "family" %}
  - biology/taxa/{{ tags }}{% endif %}{% if tags == "species" and root_ancestor == "Animal" %}
  - biology/animal{% endif %}{% if tags == "species" and root_ancestor == "Plant" %}
  - biology/plant{% endif %}{% if extinct %}
  - biology/extinct{% endif %}
  - stub
---

> [!note]
> This page is a stub and has more information that can be added.

> [!summary] {{ name }}
> > [!info] Relation{% if predecessor %}
> > ### Succeeds:
> > [[Encyclopedia Mysenvaria/Biology/Taxa/{{ predecessor }}|{{ predecessor }}]]{% endif %}{% if successors %}
> > ### Supersedes {% for successor in successors %}
> > [[Encyclopedia Mysenvaria/Biology/Taxa/{{ successor.name }}|{{ successor.name }}]]{% endfor %}{% endif %}
>
> > [!info] Creation Date
> > c. BT {{ date }}

{{ body }}

# See Also
- [[Encyclopedia Mysenvaria/Indexes/Biology/Taxa/Lists of Taxa|Lists of Taxa]]{% if root_ancestor == "Plant" %}
- [[Encyclopedia Mysenvaria/Indexes/Biology/Plants/Lists of Plants|Lists of Plants]]
{% endif %}{% if root_ancestor == "Animal" %}
- [[Encyclopedia Mysenvaria/Indexes/Biology/Animals/Lists of Animals|Lists of Animals]]
{% endif %}{% if tags == "biology/taxa/family" %}
- [[Encyclopedia Mysenvaria/Indexes/Biology/Taxa/List of Family Taxa|List of Phylogenetic Families]]
{% endif %}
