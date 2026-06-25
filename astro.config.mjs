import { defineConfig } from "astro/config";
import rehypeSanitize from "rehype-sanitize";

export default defineConfig({
  output: "static",
  site: "https://ctbbp-summaries.pages.dev",
  markdown: {
    rehypePlugins: [rehypeSanitize],
  },
});
