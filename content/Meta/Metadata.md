---
title: "Metadata"
enableToc: true
tags:
  - topic/meta/writing_guidelines
type: article
status: complete
---

> [!abstract] [[Meta/Meta|Meta]]
> *This article is part of a series on the Encyclopedia's [[Meta/Writing Guidelines|Writing Guidelines]]*.

> [!danger] Warning
> **There may be some data on this page which is not visible when viewing this page from the Encyclopedia Mysenvaria website!**

Every article begins with a block of [YAML](https://yaml.org/) front matter. This block is inaccessible to the average reader and is not intended to be viewed or accessed by them. Instead, this block provides necessary data to [Quartz](https://quartz.jzhao.xyz/) to build and deploy the Encyclopedia's articles. YAML blocks may also provide optional information that scripts made for the Encyclopedia can use.

The following is the required YAML data for each article on the Encyclopedia:

```yaml
---
title: "Example Article" # The title of the article.
aliases: # A list of aliases for the title.
  - "Example"
link: "page_link" # Optional. If not included it defaults to the generic wikilink for the article. Programs use this to refer to the page in generated articles.
enableToc: true # Whether or not to render a Table of Contents on the article.
type: article # The type of article. Defaults to `article`. Accepts: `article`, `index`, `archive`, `overview`, `ledger`, `project`, `addenda`, or `template`.
status: empty # The current status of the article. Defaults to `empty`. Accepts: `empty`, `stub`, `incomplete`, `touch-up`, `update`, or `complete`.
future: none # How this article may fare in the future. Defaults to `none`. Accepts: `update`, `rewrite`, `review`, or `auto-generated`.
has: # `has` and `need` are an array of items which allow writers or editors to know what articles need what media. Both are optional. Accepts: `infobox`, `image`, `video`, `graphics`, `featured_data`, `archive`, and `addenda`.
  - example
needs:
  - example
---
%%
"page_link": "[[Meta/Metadata|Metadata]]"
%%
```
# Dates
Anytime a `date` is asked for it is written as `[year,day]`, where day can be omitted for less precision. Day is any number between 1 and 360 (As a single year in Mysenvar consists of 360 days) and year can be any number, including negatives. For example, `[-360,56]` means the 56th day of the year 360 BT (Before Treaty), whereas `[360,56]` means the 56th day of the year 360 AT (After Treaty).
# Tags
Tags are broken into two groups: **topics** and **subjects**. Topics are broad and overarching, but also straightforward in what articles they should apply to. Every article should have *at least one* topic tag. Subjects are more narrow in the topics which they cover. Not every article is required to have a subject tag.
## Topics

```yaml
---
tags:
# These are meta tags: they are used to tag articles which cover meta topics.
  - topic/meta # This article covers a general meta topic.
  - topic/meta/writing_guidelines # This article covers something relating to the Encyclopedia's writing guidelines.
  - topic/meta/ledger # This article is a Lore Ledger; a changelog for the Encyclopedia.
  - topic/meta/addenda # This article is an addenda; articles providing meta information on non-meta pages.
# These are the art tags:
  - topic/art # This article covers a topic relating to the arts.
  - topic/art/game # This article covers something related to the art of games.
  - topic/art/music # This article covers something related to the art of music.
  - topic/art/cuisine # This article covers something related to the art of food.
  - topic/art/literature # This article covers something related to the art of literary works.
  - topic/art/literature/non-fiction # This article covers something related to the art of non-fiction literary works.
  - topic/art/literature/fiction # This article covers something related to the art of fictional literary works.
  - topic/art/performance # This article covers something related to the art of performative arts.
  - topic/art/sport # This article covers something related to the art of sports.
# These are the biology tags:
  - topic/biology # This article covers a topic relating to biology.
  - topic/biology/plant # This article covers a specific taxon of plant.
  - topic/biology/animal # This article covers a specific taxon of animal.
  - topic/biology/disease # This page covers a specific disease or affliction.
# These are the culture tags:
  - topic/culture # This article covers a topic relating to the humanities.
  - topic/culture/belief # This article covers a certain belief system.
  - topic/culture/ethnicity # This article covers a certain ethnic group.
  - topic/culture/holiday # This article covers a certain holiday or group of holidays.
  - topic/culture/language # This article covers a certain language or language family.
  - topic/culture/occupation # This article covers a certain occupation.
  - topic/culture/organization # This article covers a certain organization.
# These are the geography tags:
  - topic/geography # This article covers a topic relating to the Plane's geography.
  - topic/geography/natural # This article covers a certain natural geographical feature or phenomenon.
  - topic/geography/abstract # This article covers a certain abstract geographical feature or phenomenon.
  - topic/geography/artificial # This article covers a certain artificial geographical feature or phenomenon.
  - topic/geography/astrography # This article covers a particular star or star system.
# These are the history tags:
  - topic/history # This article covers a topic relating to history.
  - topic/history/god-war_era # This article covers events which occurred during the God-War Era.
  - topic/history/post-war_era # This article covers events which occurred during the Post-War Era.
  - topic/history/golden_age # This article covers events which occurred during the Golden Age.
  - topic/history/modern_era # This article covers events which occurred during the Modern Era.
  - topic/history/biography # This article covers the lives of a particular person or persons.
  - topic/history/decade # This article covers a specific decade of history.
  - topic/history/century # This article covers a specific century of history.
# These are the science tags:
  - topic/science # This article covers a topic relating to the sciences.
  - topic/science/branch # This article covers a particular scientific branch.
  - topic/science/phenomena # This article covers a specific scientific phenomenon.
  - topic/science/model # This article covers a specific scientific model.
  - topic/science/technology # This article covers a particular technology.
---
```
## Subjects
```yaml
---
tags:
# These tags are used for articles which cover information regaring Gods.
  - subject/god # This article covers information regarding Gods.
  - subject/god/higher-god # This article covers information regarding higher-Gods.
  - subject/god/lesser-god # This article covers information regarding lesser-Gods.
  - subject/god/compound_god # This article covers information regarding Gods of the chemical compounds.
  - subject/god/elemental_god # This article covers information regarding Gods of the elements.
  - subject/god/energy_god # This article covers information regarding Gods of energies.
  - subject/god/reaction_god # This article covers information regarding Gods of chemical reactions.
  - subject/god/phenomena_god # This article covers information regarding Gods of phenomena.
  - subject/god/silent_god # This article covers information regarding Gods who haven't published a star.
  - subject/god/outspoken_god # This article covers information regarding Gods who have published stars.
# These tags are used for articles which cover information regarding stars. 
  - subject/star # This article covers information regarding stars.
  - subject/star/host # This article covers information regarding the host of a star system.
  - subject/star/child # This article covers information regarding a child star in a star system.
  - subject/star_system # This article covers information regarding a star system.
# These tags are used for articles which cover information relating to the Plane's sophonts.
  - subject/sophont # This article covers information regarding an aspect of sophonts.
  - subject/sophont/human # This article covers information regarding an aspect of humans.
  - subject/sophont/elf # This article covers information regarding an aspect of elves.
  - subject/sophont/dwarf # This article covers information regarding an aspect of dwarves.
# These tags are used for articles covering literary works.
  - subject/literature # This article covers information regarding a literary work.
  - subject/literature/non-fiction # This article covers a literary work of the genre: fiction.
  - subject/literature/fiction # This article covers a literary work of the genre: non-fiction.
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
  - subject/literature/ # This article covers a literary work of the genre: .
# These tags are used for misc. subjects.
  - subject/old_world # This article covers information which occurred in the Old World.
  - subject/new_world # This article covers information which occurred in the New World.
  - subject/war # This article covers information regarding a war.
  - subject/linguistics # This article covers information regarding the study of linguistics
---
```
# Subpage Example
```yaml
---
subpage: # An array, so you can list multiple subpages per page. Each subpage is treated exactly the same as a regular page.
  - title: "Example Subpage 1"
	link: "example_link1"
	type: article
	status: empty
  - title: "Example Subpage 2"
	link: "example_link2"
	type: article
	status: empty
---
%%
"example_link1": "[[Meta/Example|Example]]"
"example_link2": "Example"
%%
```
# Event Example
```yaml
---
event: # This is an array, so it can handle multiple events per-page.
  - start_desc: "start_desc_example" # The program will search through the page that the event is provided on to find a string matching this. That string should provide the description for the event.
    end_desc: "end_desc_example" 
    start_date: [] # Dates are written in a unique format covered elsewhere in the meta pages of the Encyclopedia.
    end_date: [] 
    major_event: true # Determines whether or not the event should be listed on certain pages.
---
%%
start_desc_example: This is the description for the start of the event. The program will search all hidden comments across the page to see if it can find the referenced string.
end_desc_example: This is the description for the end of the event, if it has one.
%%
```
# Star Example
```yaml
---
star: # This is an array, so it can handle multiple stars per-page.
  - name: "Example Star"
    desc: "star_desc"
    star_type: "legal" # `legal`, `documentary`, or `index`. Optional. No default.
    parent: "parent_star" # Optional. Defines if the star is a child and who its parent is.
    coordinates: [] # The coordinate location of the star. Optional. No default.
    orbital: # For data relating to the stars orbit.
	    center_mode: "explicit" # Either `coordinates` or `explicit`. Used to define the central coordinate of the star's orbit. 
	    center: [] # Used if `center_mode` is set to explicit.
	    radius: 1 # The distance the star orbits from its center in meters.
	    eccentricity: 0 # The eccentricity of the star's orbit. Optional. Defaults to 0.
	    tilt: 1 # The tilt of the star's orbital plane. Optional. Defaults to 0.
	    periapsis_deg: 1 # Which direction the periapsis is at. Optional. Defaults to 0.
	    periapsis_distance: 1 # The distance of the periapsis. Optional. Defaults to 0.
	    period: 90 # The number of days it takes to make a complete orbit.
	    phase_start: 23 # What part of the period the star starts at on day 0. Optional. Defaults to 0.
	translations: # An array of events detailing each translation of the star.
	  - translators: ["translator_example"]
	    date: []
	    desc: "translation_description_example"
	    major_event: true # Determines whether or not the event should be listed on certain pages.
    publications: # An array of events detailing each publication of the star.
      - publishers: ["publisher_example"]
        date: []
        desc: "publish_description_example"
        major_event: true # Determines whether or not the event should be listed on certain pages.
---
%%
star_desc: A short description of the star itself.
parent_star: May be a wikilink to the parent star.
translator_example: May be a wikilink to the translators page.
translation_description_example: A short description of the event relating to this star's translation.
publisher_example: May be a wikilink to the publishers page.
publish_description_example: A short description of the event relating to this star's publication.
%%
```
# Person Example
```yaml
---
person: # This is an array, so it can handle multiple people per-page.
  - name: "Example Person"
    birth_location: "location_example"
    birth_date: []
    birth_desc: "birth_description_example"
    death_date: []
    death_desc: "death_description_example"
    parents: ["parent_example"]
    children: ["child_example"]
    spouses:
      - name: "spouse_example"
        start_date: []
        end_date: [] # Optional. Defines if there was a divorce.
        major_event: true # Determines whether or not the wedding and divorce should be listed on certain pages.
    major_event: false # Determines whether or not their birth and death should be listed on certain pages.
---
%%
location_example: May be a wikilink to the location of the person's birth.
birth_description_example: A short description of the person's birth.
death_description_example: A short description of the person's death.
parent_example: May be a wikilink to the person's parent.
child_example: May be a wikilink to the person's child.
spouse_example: May be a wikilink to the person's spouse.
%%
```
# Index Example
```yaml
---
index: # This is an array, so it can handle multiple indexes per-page.
  - header_name: "Example" # The name of the header wherein the index will be placed. Text in this header section will be replaced.
    included_data: # An array of YAML data. Article's with matching YAML will be included in the index. Special logic is applied to any data containing the word `date`. Supports `gt`, `lt`, `gte`, and `lte` arguments.
      - event[].start_date: {gte: 609, lte: 1214} # In this example, articles which have an event listed which takes place on 609AT, 1214AT, or between these dates, will be included in the index.
      - tags: [topic/example] # In this example, articles with the `topic/example` tag will be included in the index.
    excluded_data: # An array of YAML data. Article's with matching YAML will be excluded from the index. Special logic is applied to any data containing the word `date`. Supports `gt`, `lt`, `gte`, and `lte` arguments.
      - type: example # In this example, articles with the `example` type will be excluded.
    sort: # An array of data which determines how the index will be sorted. The first entry in the array is used for sort all data: any matching data or outliers will then be sorted via the next entry. This repeats until no entries are left.
      - by: title # Pointer to the piece of metadata which the article should be indexed by.
        method: standard_forward # The method by which the program should sort the data. Accepts `standard_forward`, `standard_backward`, `natural_forward`, `natural_backward`, and `unique`.
        subheaders:
          generate: true # Whether or not to generate a subheader during this sort.
          method: first_character # The method by which to generate the subheader. Accepts `value` (Creates a subheader for each unique value), `first_character` (Creates a subheader for each unique first character), and `floor_x` (Works only for numbers, creates a subheader at each interval of x).
          format: "{value}'s Example" # Optional. Tells the program how to format the subheader. 
---
```
# Ledger Data Example
```yaml
---
ledger_data:
  week: 1 # The week the ledger was published.
  year: 2020 # The year the ledger was published.
---
```
# Featured Example
```yaml
---
featured_data:
  featured_desc: "featured_description_example"
  featured_image: "featured_image_example" # Can feature a wikilink to an image.
  fun_facts: ["fun_fact1"]
---
%%
featured_description_example: A short and concise description of the article's contents.
featured_image_example: ![[Media/Images/example.png|example.png]]
fun_fact1: A short fun fact relating to the article's contents. Should be formated to be followed by "Did you know...".
%%
```
# Archive Example
```yaml
---
archived_work:
  title: "Example Work"
  authors: ["author_example"] # An array of any authors who are known to have worked on the work.
  language: "language_example" # The original language the work was published in.
  publication_date: [] # Date of the work's original publication.
  medium: unknown # The medium the work was originally published in. Accepts: `unknown`, `stone`, `clay`, `papyrus`, `wax`, `wood`, `parchment`, `vellum`, or `paper`.
  status: complete # The current status of the archived work. Accepts: `complete`, `fragmented`, `censored`, `restored`, or `lost`.
---
%%
author_example: May be a wikilink to the work's author.
language_example: May be a wikilink to the work's original language.
%%
```