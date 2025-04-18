import { classNames } from "../util/lang"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const TagList: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const tags = fileData.frontmatter?.tags
  if (tags && tags.length > 0) {
    return (
      <ul class={classNames(displayClass, "tags")}>
        {tags.map((tag) => (
          <li>
            <span class="tag-box">#{tag}</span>
          </li>
        ))}
      </ul>
    )
  } else {
    return null
  }
}

TagList.css = `
.tags {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 1rem 0;
  padding-left: 0;
}

.tags > li {
  white-space: nowrap;
  margin: 0;
}

.tag-box {
  display: inline-block;
  border-radius: 8px;
  background-color: var(--highlight);
  padding: 0.2rem 0.4rem;
  font-size: 0.9em;
  color: inherit;
}
`

export default (() => TagList) satisfies QuartzComponentConstructor
