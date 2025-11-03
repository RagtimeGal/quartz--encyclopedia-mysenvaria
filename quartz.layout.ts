import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "Home": "https://mysenvaria.ragno.wiki/",
      "Meta": "https://mysenvaria.ragno.wiki/Meta/Meta",
      "Contributors": "https://mysenvaria.ragno.wiki/Meta/Contributors",
      "Code of Conduct": "https://github.com/RagtimeGal/quartz--encyclopedia-mysenvaria/blob/v4/CODE_OF_CONDUCT.md",
      "GitHub": "https://github.com/RagtimeGal/quartz--encyclopedia-mysenvaria",
      "Blog": "https://ragnois.gay",
      "Discord": "https://discord.gg/2yUDZ5j",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode()},
      ],
    }),
    Component.Explorer()
  ],
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Comments(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode()},
      ],
    }),
    Component.Explorer()
  ],
  right: [],
}
