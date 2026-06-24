import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  output: "static",
  adapter: cloudflare(),
  site: "https://ctbbp-summaries.pages.dev",
  vite: {
    resolve: {
      conditions: ["browser", "module"],
    },
  },
});
