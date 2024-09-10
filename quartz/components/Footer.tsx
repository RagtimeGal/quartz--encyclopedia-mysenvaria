import { version } from "../../package.json"
import style from "./styles/footer.scss"
import { QuartzComponentConstructor, QuartzComponentProps } from "./types"

interface Options {
  links: Record<string, string>
}

export default ((opts?: Options) => {
  function Footer({ displayClass }: QuartzComponentProps) {
    const year = new Date().getFullYear()
    const links = opts?.links ?? []
    return (
      <footer class={`${displayClass ?? ""}`}>
        <div class="giscus" style={{ marginTop: "5rem" }}></div>
        <hr />
        <p>
          Created with <a href="https://quartz.jzhao.xyz/">Quartz v{version}</a>, © {year}
        </p>
        <p>
          Encyclopedia Mysenvaria © 2024 by Ragno is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>.
        </p>
        <p>
          The website's backend is powered by Quartz and is licensed under the <a href="https://opensource.org/licenses/MIT">MIT License</a>.
        </p>
        <ul>
          {Object.entries(links).map(([text, link]) => (
            <li>
              <a href={link}>{text}</a>
            </li>
          ))}
        </ul>
      </footer>
    )
  }

  Footer.css = style
  return Footer
}) satisfies QuartzComponentConstructor
