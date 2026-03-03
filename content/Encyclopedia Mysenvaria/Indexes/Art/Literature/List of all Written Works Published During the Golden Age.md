---
title: "List of all Written Works Published During the Golden Age"
enableToc: true
tags:
  - topic/art/literature
type: index
status: update
index:
  - header_name: "Works Published During the Golden Age"
    included_data: 
      - tags: [topic/art/literature/*]
      - event[].start_date: {gte: 609, lte: 1214}
    excluded_data: 
      - type: index
      - type: template
    sort:
      - by: event[].start_date
        method: standard_forward
        subheaders: 
          generate: true
          method: floor_10
          format: "{value}s AT"
      - by: title
        method: standard_forward
        subheaders:
          generate: false
---

The following is an index of all articles across the encyclopedia describing [[Encyclopedia Mysenvaria/Arts/Art#Literature|literary works]] which were published during the [[Encyclopedia Mysenvaria/History/Golden Age/Golden Age|Golden Age]], organized by decade of publication.
# Works Published During the Golden Age

> [!note] [[Meta/Meta|Meta]] || [[Meta/Callouts#Update|Update]]
> This article is always growing! As the encyclopedia and setting continue to grow, so too does this page! You can help expand it by commenting or suggesting an edit through [GitHub issues](https://github.com/RagtimeGal/quartz--encyclopedia-mysenvaria/issues/new/choose)!
