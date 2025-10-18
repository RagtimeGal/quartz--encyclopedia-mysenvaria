---
title: "Metadata"
enableToc: true
tags:
  - topic/meta/writing_guidelines
type: article
status: complete
---

> [!abstract] [[Meta/Meta|Meta]]
> *This article is part of a series on the encyclopedia's [[Meta/Writing Guidelines|Writing Guidelines]]*.

Every article begins with a block of [YAML](https://yaml.org/) front matter. This block is inaccessible to the average reader and is not intended to be viewed or accessed by them. Instead, this block provides necessary data to [Quartz](https://quartz.jzhao.xyz/) to build and deploy the encyclopedia's articles. YAML blocks may also provide optional information that scripts made for the encyclopedia can use.

The following is a list of all YAML node keys—and examples of their values—used across the encyclopedia:
- **title**: The title of the article, written as a string.
- **enableToc**: Whether or not the article should list a Table of Contents. `true` or `false`.
- **tags**: For the list of applicable tags see the tags portion of this article.
- **type**: The type of article. `article`, `index`, `table`, `overview`, `ledger`, `project`, `addenda`, or `template`.
- **status**: The current status of the article. `empty`, `stub`, `incomplete`, `touch-up`, `update`, or `complete`.
- **future**: How this article might fare for the future. `update`, `rewrite`, or `review`.
- **has**: A list of items[^possible_page_items] which the article has.
- **needs**: A list of items[^possible_page_items] which could improve the article.
- **dates**: JSON-style data array for any dates regarding the article. For information regarding the formatting of date's see the applicable portion of this article.
- **animal**: JSON-style data for pages regarding animals. Used by scripts to format infoboxes on specific pages.
- **uid**: The UID if applicable, determined by the encyclopedia's [[Meta/Names#Name Code|name code]].
# Tags
Tags are broken down into two types: topics and subjects. Topics are broad and overarching, every article should have at least one topic tag. These tags are very straightforward and help with finding articles over a broad area of information. Subjects are much more narrow in the topics they discuss. Not every article needs a subject tag. They help with finding very specific articles.
## Topics
- `topic/meta`: This page covers a meta topic for the encyclopedia.
	- `topic/meta/writing_guidelines`: This page covers the encyclopedia's writing guidelines.
	- `topic/meta/ledger`: This page is a Lore Ledger, a changelog for the encyclopedia.
	- `topic/meta/project`: This page covers an ongoing or complete Project regarding the completion of the encyclopedia.
	- `topic/meta/addenda`: Addenda are hidden pages which provide meta information, like author's notes and TTRPG stat blocks, for specific articles.
- `topic/art`: This page covers a topic relating to the arts.
	- `topic/art/game`: This page covers a topic relating to games.
	- `topic/art/music`: This page covers a topic relating to music.
	- `topic/art/cuisine`: This page covers a topic relating to food.
	- `topic/art/literature`: This page covers a topic relating to literature.
		- `topic/art/literature/fiction`: This page covers a piece of fiction literature.
		- `toqpic/art/literature/non-fiction`: This page covers a piece of non-fiction literature.
	- `topic/art/performance`: This page covers a topic relating to performative arts.
	- `topic/art/sport`: This page covers a topic relating to sports.
- `topic/biology`: This page covers a topic relating to biology.
	- `topic/biology/plant`: This page covers a specific taxon of plant.
	- `topic/biology/animal`: This page covers a specific taxon of animal.
	- `topic/biology/disease`: This page covers a specific disease.
- `topic/culture`: This page covers a topic relating to the humanities.
	- `topic/culture/belief`: This page covers a certain belief system.
	- `topic/culture/ethnicity`: This page covers a certain ethnic group.
	- `topic/culture/holiday`: This page covers a certain holiday or group of holidays.
	- `topic/culture/language`: This page covers a certain language or language family.
	- `topic/culture/occupation`: This page covers a certain occupation.
	- `topic/culture/organization`: This page covers a certain organization.
- `topic/geography`: This page covers a topic relating to the Plane's geography.
	- `topic/geography/natural`: This page covers a certain natural geographical phenomenon.
	- `topic/geography/abstract`: This page covers a certain abstract geographical phenomenon.
	- `topic/geography/artificial`: This page covers a certain artificial geographical phenomenon.
	- `topic/geography/astrography`: This page covers a star or star system.
- `topic/history`: This page covers a topic relating to history.
	- `topic/history/god-war_era`: This page covers events which occurred during the God-War Era.
	- `topic/history/post-war_era`: This page covers events which occurred during the Post-War Era.
	- `topic/history/golden_age`: This page covers events which occurred during the Golden Age.
	- `topic/history/modern_era`: This page covers events which occurred during the Modern Era.
	- `topic/history/biography`: This page covers the lives of specific people.
	- `topic/history/decade`: This page covers a specific decade of history.
	- `topic/history/century`: This page covers a specific century of history.
- `topic/science`: This page covers a topic relating to the sciences.
	- `topic/science/branch`: This page covers a specific scientific branch.
	- `topic/science/phenomena`: This page covers a specific scientific phenomenon.
	- `topic/science/model`: This page covers a specific scientific model.
	- `topic/science/technology`: This page covers a specific technology.
## Subjects
- `subject/god`: This page covers information regarding Gods.
	- `subject/god/higher-god`: This page covers information regarding higher-Gods.
	- `subject/god/lesser-god`: This page covers information regarding lesser-Gods.
	- `subject/god/compound_god`: This page covers information regarding Gods of chemical compound.
	- `subject/god/elemental_god`: This page covers information regarding Gods of elements.
	- `subject/god/energy_god`: This page covers information regarding Gods of energies.
	- `subject/god/reaction_god`: This page covers information regarding Gods of reactions.
	- `subject/god/phenomena_god`: This page covers information regarding Gods of phenomenon.
	- `subject/god/silent_god`: This page covers information regarding Gods who haven't published stars.
	- `subject/god/outspoken_god`: This page covers information regarding Gods who have published stars.
- `subject/star`: This page covers information regarding stars.
	- `subject/star/host`: This page covers information regarding the host star of a specific star system.
	- `subject/star/child`: This page covers information regarding a child star of a specific star system.
- `subject/star_system`: This page covers information regarding star systems.
- `subject/old_world`: This page covers information regarding the old world.
- `subject/new_world`: This page covers information regarding the new world.
- `subject/sophont`: This page covers information regarding an aspect of sophonts.
	- `subject/sophont/human`: This page covers information regarding an aspect of humans.
	- `subject/sophont/elf`: This page covers information regarding an aspect of elves.
	- `subject/sophont/dwarf`: This page covers information regarding an aspect of dwarves.
# Dates
Dates is an optional JSON-style array of dates which can be included in a files YAML. The following keys should be attached to each node in the array:
- **name**: The name of the event as a string.
- **desc**: A description of the event as a string. `{{name}}` may be included in the description, any scripts which build information will link back to the page with the date, using the name as the display for the wiki-link.
- **date**: A date string formatted as level 2 [EDTF](https://www.loc.gov/standards/datetime/). Quarters are used in the place of months.
# Animal
- ****


[^possible_page_items]: Possible items listed here include: `infobox`, `image`, `video`, `graphics`, and `addenda`.