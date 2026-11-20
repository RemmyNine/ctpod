import { defineCollection, z } from "astro:content";

const episodes = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    episode: z.number(),
    date: z.coerce.date().optional(),
    source: z.string().url().optional(),
    description: z.string().optional(),
  }),
});

export const collections = { episodes };
