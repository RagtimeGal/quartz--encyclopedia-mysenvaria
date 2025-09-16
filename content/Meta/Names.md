---
title: "Names"
enableToc: true
tags:
  - topic/meta
type: article
status: complete
---

> [!abstract] [[Meta/Meta|Meta]]
> *This article is part of a series on the encyclopedia's [[Meta/Writing Guidelines|Writing Guidelines]]*.

Mysenvar is an ever-evolving setting, and while swathes of its lore remain incomplete there are still articles which cover that lore. Some of this lore needs names, for characters and locations, but names aren't just arbitrary. Names emerge from language, history, and culture, and that's lore which may not be complete yet, and so strategies are employed to temporarily fill those gaps until lore catches up. There's two primary strategies employed:
- *Name Code* is a standardized placeholder system which ensures consistency, no overlap, and enables easy searching for placeholders;
- Eponyms are placeholders borrowed from real-world figures and places.

Name Code is preferred over the use of eponyms as it is safer and more friendly to editors.
# Eponyms
Eponyms, names formed after real people or places, are strongly discouraged. They should only be used in select cases where Name Code cannot be reasonably employed. If an eponym is used it must fall into one of these two categories:
- The thing being named must loosely fit the description of the fictional or antique figure which they are being named after.
- The placeholder will only be used in personal drafts that will not be published to the encyclopedia publicly.

These rules should not be broken. Failure to follow these rules is considered a violation of the encyclopedia's [[Meta/Contributing#Standards|Code of Conduct]] and will be treated as such.
# Name Code
Name code is a standardized string of characters constructed using information regarding the character or location which it is referring to. The string is formatted as such: `<CATEGORY>.<DATE>.<UID>`.

`CATEGORY` is a three-character code which defines what the name code is referencing. `DATE` is determined by the category and is written in EDTF format. `CATEGORY` can be any of the following:
- `CHR`: for characters. `DATE` is the birth and death date of the character.
- `LAN`: for languages. `DATE` is the advent of the language.
- `ETH`: for ethnicities. `DATE` is the advent of the ethnic group.
- `CUL`: for cultures. `DATE` is the advent of the cultural group.
- `ORG`: for organizations. `DATE` is the founding of the organization.
- `NAT`: for nations. `DATE` is the founding of the nation.
- `CTY`: for cities, towns, or villages. Places where people live. `DATE` is the founding of the locality.
- `FTR`: for geographical features. `DATE` is the creation of the locality.

`UID` is a custom ID generated using the UID Generator [[Meta/Scripts|program]], seeded using the incomplete name code string.