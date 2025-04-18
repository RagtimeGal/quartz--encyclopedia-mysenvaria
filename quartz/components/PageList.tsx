import { useState } from "react"
import { GlobalConfiguration } from "../cfg"
import { QuartzPluginData } from "../plugins/vfile"
import { FullSlug, isFolderPath, resolveRelative } from "../util/path"
import { Date, getDate } from "./Date"
import { QuartzComponent, QuartzComponentProps } from "./types"

export type SortFn = (f1: QuartzPluginData, f2: QuartzPluginData) => number

export function byDateAndAlphabetical(cfg: GlobalConfiguration): SortFn {
  return (f1, f2) => {
    if (f1.dates && f2.dates) {
      return getDate(cfg, f2)!.getTime() - getDate(cfg, f1)!.getTime()
    } else if (f1.dates && !f2.dates) {
      return -1
    } else if (!f1.dates && f2.dates) {
      return 1
    }
    const f1Title = f1.frontmatter?.title.toLowerCase() ?? ""
    const f2Title = f2.frontmatter?.title.toLowerCase() ?? ""
    return f1Title.localeCompare(f2Title)
  }
}

export function byDateAndAlphabeticalFolderFirst(cfg: GlobalConfiguration): SortFn {
  return (f1, f2) => {
    const f1IsFolder = isFolderPath(f1.slug ?? "")
    const f2IsFolder = isFolderPath(f2.slug ?? "")
    if (f1IsFolder && !f2IsFolder) return -1
    if (!f1IsFolder && f2IsFolder) return 1

    if (f1.dates && f2.dates) {
      return getDate(cfg, f2)!.getTime() - getDate(cfg, f1)!.getTime()
    } else if (f1.dates && !f2.dates) {
      return -1
    } else if (!f1.dates && f2.dates) {
      return 1
    }
    const f1Title = f1.frontmatter?.title.toLowerCase() ?? ""
    const f2Title = f2.frontmatter?.title.toLowerCase() ?? ""
    return f1Title.localeCompare(f2Title)
  }
}

type Props = {
  limit?: number
  sort?: SortFn
} & QuartzComponentProps

export const PageList: QuartzComponent = ({ cfg, fileData, allFiles, limit, sort }: Props) => {
  const sorter = sort ?? byDateAndAlphabeticalFolderFirst(cfg)
  let list = allFiles.sort(sorter)
  if (limit) {
    list = list.slice(0, limit)
  }

  const [openFolders, setOpenFolders] = useState<Record<string, boolean>>({})

  const toggleFolder = (slug: string) => {
    setOpenFolders(prev => ({ ...prev, [slug]: !prev[slug] }))
  }

  const isChildOf = (childSlug: string, parentSlug: string) => {
    return childSlug.startsWith(parentSlug) && childSlug !== parentSlug
  }

  return (
    <ul class="section-ul">
      {list.map((page) => {
        const title = page.frontmatter?.title
        const tags = page.frontmatter?.tags ?? []
        const slug = page.slug ?? ""
        const isFolder = isFolderPath(slug)

        if (isFolder) {
          const isOpen = openFolders[slug] ?? false
          const children = allFiles.filter(p => isChildOf(p.slug ?? "", slug))

          return (
            <li class="section-li" key={slug}>
              <div class="section">
                <p class="meta">
                  {page.dates && <Date date={getDate(cfg, page)!} locale={cfg.locale} />}
                </p>
                <div class="desc">
                  <h3>
                    <button
                      class="internal folder-name"
                      onClick={() => toggleFolder(slug)}
                    >
                      {title}
                    </button>
                  </h3>
                </div>
                {isOpen && (
                  <ul class="child-pages">
                    {children.map(child => (
                      <li key={child.slug}>
                        <a
                          href={resolveRelative(fileData.slug!, child.slug!)}
                          class="internal"
                        >
                          {child.frontmatter?.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </li>
          )
        } else {
          return (
            <li class="section-li" key={slug}>
              <div class="section">
                <p class="meta">
                  {page.dates && <Date date={getDate(cfg, page)!} locale={cfg.locale} />}
                </p>
                <div class="desc">
                  <h3>
                    <a href={resolveRelative(fileData.slug!, slug)} class="internal">{title}</a>
                  </h3>
                </div>
                <ul class="tags">
                  {tags.map((tag) => (
                    <li key={tag}>
                      <a
                        class="internal tag-link"
                        href={resolveRelative(fileData.slug!, `tags/${tag}` as FullSlug)}
                      >
                        {tag}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </li>
          )
        }
      })}
    </ul>
  )
}

PageList.css = `
.section h3 {
  margin: 0;
}

.section > .tags {
  margin: 0;
}

.folder-name {
  background: none;
  border: none;
  font: inherit;
  color: inherit;
  text-align: left;
  padding: 0;
  cursor: pointer;
  opacity: 0.85;
  font-style: italic;
}

.folder-name:hover {
  text-decoration: underline;
}

.child-pages {
  margin-left: 1.5rem;
  margin-top: 0.5rem;
  list-style-type: disc;
}
`
