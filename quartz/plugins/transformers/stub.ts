import { QuartzTransformerPlugin } from "quartz/plugins/types";

interface Options {
  repoURL: string;
}

export const StubTransformer: QuartzTransformerPlugin<Options> = (opts: Options) => {
  return {
    name: "StubTransformer",
    textTransform(ctx, content) {
      const { repoURL } = opts;
      const frontmatterDelimiter = "---";
      const contentStr = content.toString();
      
      if (contentStr.includes("stub: true")) {
        const [_, frontmatter, body] = contentStr.split(frontmatterDelimiter);
        const newFrontmatter = `${frontmatter.trim()}\nmessage: "This page is incomplete, but you can help by adding to it"\ngithub_url: "${repoURL}"`;
        return `${frontmatterDelimiter}\n${newFrontmatter}\n${frontmatterDelimiter}\n${body}`;
      }

      return content;
    }
  };
};
