import { defineCollection, z } from "astro:content";

const episodes = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    episode: z.number(),
  }),
});

export const collections = { episodes };
