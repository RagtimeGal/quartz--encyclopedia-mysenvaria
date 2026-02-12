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

Anytime a `date` is asked for it is written as \[year]\["-"]\[day], where day can be omitted for less precision. Day is any number between 1 and 360 (As a single year in Mysenvar consists of 360 days) and year can be any number, including negatives. For example, "-360-56" means the 56th day of the year 360 BT (Before Treaty), whereas "360-56" means the 56th day of the year 360 AT (After Treaty).

The following is a list of all YAML node keys—and examples of their values—used across the encyclopedia:
- **title**: The title of the article, written as a string.
- **enableToc**: Whether or not the article should list a Table of Contents. `true` or `false`.
- **tags**: For the list of applicable tags see the tags portion of this article.
- **type**: The type of article. `article`, `index`, `table`, `overview`, `ledger`, `project`, `addenda`, or `template`.
- **status**: The current status of the article. `empty`, `stub`, `incomplete`, `touch-up`, `update`, or `complete`.
- **future**: How this article might fare for the future. `update`, `rewrite`, or `review`.
- **has**: A list of items[^possible_page_items] which the article has.
- **needs**: A list of items[^possible_page_items] which could improve the article.
- **event**: Data for any event dates regarding the article. For information regarding the formatting of dates see the applicable portion of this article.
- **star**: Data for pages regarding stars. Used by scripts to generate certain pages.
- **person**: Data for pages regarding specific characters or people. Used by scripts to generate certain pages.
- **animal**: JSON-style data for pages regarding animals. Used by scripts to format infoboxes on specific pages.
- **index**: An array of data for index pages. Used by scripts to automatically generate indexes.
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
		- `topic/art/literature/non-fiction`: This page covers a piece of non-fiction literature.
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
- `subject/war`: This page covers information regarding a war.
# Event
- **start_desc**: This is not optional, it provides a description of the event as a string. Wikilinks may be included. May point to hidden text in the article.
- **end_desc**: This is optional, it provides a description of the event as a string. Wikilinks may be included. May point to hidden text in the article.
- **start_date**: The date the event began, this is not optional.
- **end_date**: If the event has a defined end it may be included as a date here.
- **major_event**: Boolean. True means the event is listed on certain major pages.
# Star
- **name**: The name of the star, not optional.
- **publications**: An array of data detailing each publication of the star. Stars can fall and be republished, which is why this is an array. It is not optional.
	- **publishers**: This can be an array of strings, or simply just one. It accepts wiki-links too. It is not optional, there must be at least one string. May point to hidden text in the article.
	- **date**: The date that this publication took place. This is not optional.
	- **desc**: This is not optional, it provides a description of the publication event as a string. Wikilinks may be included. May point to hidden text in the article.
	- **major_event**: Boolean. True means the event is listed on certain major pages.
- **desc**: A short non-optional description of the star. May include wiki-links. May point to hidden text in the article.
- **coordinates**: The coordinates of the star in Altitude, Azimuth, & Elevation as a string. Optional.
- **orbital**: Defines the orbital data of the star.
	- **center_mode**: `coordinates` uses the previously defined coordinates as the base of the star. Otherwise `explicit` then `center` data is required. Not optional.
	- **center**: The coordinates of the star's orbital center, only required if `center_mode` is `explicit`.
	- **radius**: The distance the star orbits from the center. Not optional if the star has an orbit.
	- **eccentricity**: The eccentricity of the star's orbit. Optional. Defaults to 0.
	- **tilt**: The tilt of the orbital plane. Optional. Defaults to 0.
	- **periapsis_deg**: Which direction the periapsis is at. Optional. Defaults to 0.
	- **periapsis_distance**: The distance of the periapsis. Optional. Defaults to 0.
	- **period**: How man days it takes to make a complete orbit. Not optional.
	- **phase_start**: What part of the period the star starts at on day 0. Optional. Defaults to 0.
- **translations**: An array of data detailing each translation of the star. Multiple people over history may translate the star at different times, and so this is an array. This is optional.
	- **translators**: This can be an array of strings, or simply just one. It accepts wiki-links too. It is not optional, there must be at least one string. May point to hidden text in the article.
	- **date**: The date that this translation was published. This is not optional.
	- **desc**: Optionally provides a description of the translation event as a string. Wikilinks may be included. May point to hidden text in the article.
	- **major_event**: Boolean. True means the event is listed on certain major pages.
- **parent**: A string which names the parent to this star, it is optional and may include a wiki-link. May point to hidden text in the article.
- **misc_data**: various other data for the star.
	- **type**: Accepts `legal`, `index`, `documentary`, ``
# Person
- **name**: The name of the character, not optional.
- **birth_date**: The date of the character's birth, this is optional if the date of their birth is unknown.
- **birth_location**: The location of the characters birth as a string, this accepts wiki-links and is optional. May point to hidden text in the article.
- **death_date**: The date of the character's passing, this is optional if the character has not passed away or if the date of their death is unknown.
- **spouses**: An array of data detailing each spouse the character has ever had. This is optional data.
	- **name**: The name of the character, not optional. It accepts wiki-links. May point to hidden text in the article.
	- **start_date**: The date the characters married. Optional if unknown.
	- **end_date**: The date the characters divorced. Optional if this never occurred or is unknown.
- **children**: An array of strings, or simply just one. It accepts wiki-links too. It is optional. May point to hidden text in the article.
- **parents**: An array of strings, or simply just one. It accepts wiki-links too. It is optional. May point to hidden text in the article.
- **birth_desc**: Optionally provides a description of the persons birth as a string. Wikilinks may be included. May point to hidden text in the article.
- **death_desc**: Optionally provides a description of the persons birth as a string. Wikilinks may be included. May point to hidden text in the article.
- **major_event**: Boolean. True means the event is listed on certain major pages.
# Index
- **header_name**: The name of the header wherein the index will be placed. This is not optional. If a primary header is not found matching the string then the index is not generated. If there is any text between the specified header and the next primary header or callout then the text is replaced in the generation of the index.
- **included_data**: An array of YAML data which will be compared to all pages across the encyclopedia. Pages which have matching data will be included in this index. Special logic is applied to any data containing the word `date`. Supports `gt`, `lt`, `gte`, and `lte` arguments.
- **excluded_data**: An array of YAML data which will be compared to all pages included in this index. Pages which have matching data will be excluded from the index. Special logic is applied to any data containing the word `date`. Supports `gt`, `lt`, `gte`, and `lte` arguments.
- **sort**: An array of data detailing how the program should sort the indexed pages. The program will attempt to use the first entry to sort all data. Any matching data or outliers will then be sorted via the next entry. This repeats until no entries are left. (For instance, if you sort by date first and there are items with matching dates you may then want these matching items to be sorted by name.)
	- **by:** A pointer to the piece of metadata which the articles should be indexed by.
	- **method**: The method by which the program should sort the data. Accepts: `standard_forward`, `standard_backward`, `natural_forward`, `natural_backward`, `unique`. 
	- **subheaders**: Subheader data.
		- **generate**: Boolean. Whether or not to generate a subheader for this sort.
		- **method**: The method by which to generate the subheader. Accepts:  `value` (creates a subheader for each unique value), `first_character` (creates a subheader for each unique first character), and `floor_x` (works only for numbers, creates a subheader at each interval of x).
		- **format**: Optional string that tells the program how to format the subheader. `{value}` in the string is replaced with the value correlating to the group placed under the subheader.
# Animal


[^possible_page_items]: Possible items listed here include: `infobox`, `image`, `video`, `graphics`, and `addenda`.