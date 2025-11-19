import { QuartzEmitterPlugin } from "../types"
import fs from "fs"
import chalk from "chalk"

export function extractDomainFromBaseUrl(baseUrl: string) {
  const url = new URL(`https://${baseUrl}`)
  return url.hostname
}

export const CNAME: QuartzEmitterPlugin = () => ({
  name: "CNAME",
  async emit({ argv, cfg }) {
    if (!cfg.configuration.baseUrl) {
      console.warn(chalk.yellow("CNAME emitter requires `baseUrl` to be set in your configuration"))
      return []
    }
    const content = extractDomainFromBaseUrl(ctx.cfg.configuration.baseUrl)
    if (!content) {
      return []
    }

    const path = await write({
      ctx,
      content,
      slug: "CNAME" as FullSlug,
      ext: "",
    })
    return [path]
  },
  async *partialEmit() {},
})
