// A file-mode build for previews hosted under an arbitrary URL prefix, including
// hosts that do not resolve directory requests to index.html automatically.
// Keep the standard Astro/Cloudflare build and its public URLs unchanged.
import { cp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { dirname, posix } from "node:path";
import { fileURLToPath } from "node:url";

const source = fileURLToPath(new URL("../dist/", import.meta.url));
const output = fileURLToPath(new URL("../dist-portable/", import.meta.url));
const entries = new Set();

async function inventory(folder = "") {
  for (const entry of await readdir(`${source}${folder}`, { withFileTypes: true })) {
    const file = posix.join(folder, entry.name);
    if (entry.isDirectory()) await inventory(file);
    else if (entry.isFile()) entries.add(file);
  }
}

await inventory();
if (!entries.has("index.html")) throw new Error("Build the Astro project before packaging.");
await rm(output, { recursive: true, force: true });
await cp(source, output, { recursive: true });

function targetFor(url) {
  const [, bare, suffix] = url.match(/^\/([^?#]*)(.*)$/);
  const filename = [bare, posix.join(bare, "index.html")].find((name) => entries.has(name));
  return filename && { filename, suffix };
}

await Promise.all([...entries].filter((file) => file.endsWith(".html")).map(async (file) => {
  const html = await readFile(`${output}${file}`, "utf8");
  const portable = html.replace(/(\b(?:href|src|action)=")(\/(?!\/)[^"]*)"/g, (match, attr, url) => {
    const to = targetFor(url);
    if (!to) return match;
    let path = posix.relative(dirname(file), to.filename);
    if (!path.startsWith(".")) path = `./${path}`;
    return `${attr}${path}${to.suffix}"`;
  });
  if (portable !== html) await writeFile(`${output}${file}`, portable);
}));

console.log(`Packaged ${entries.size} files for prefix-based preview hosting.`);
