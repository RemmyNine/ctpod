import os
import re
import json

SRC = "src/content/episodes"
OUT = "src/data/search-index.json"

index_data = []

for fname in sorted(os.listdir(SRC)):
    if not fname.endswith(".md"):
        continue
    m = re.match(r"episode-(\d+)\.md", fname)
    if not m:
        continue
    ep_num = int(m.group(1))

    with open(os.path.join(SRC, fname), "r", encoding="utf-8") as f:
        raw = f.read()

    # Extract frontmatter title
    title = f"Episode {ep_num}"
    fm_match = re.search(r'^---\s*\n(.*?)\n---', raw, re.DOTALL)
    if fm_match:
        title_match = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', fm_match.group(1), re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

    # Body without frontmatter
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]

    # Create snippet (first ~300 chars of TL;DR or body text)
    tldr_match = re.search(r'(?m)^#{2,3} TL;DR\s*\n(.*?)(?=\n#{2,3} |\n---|\Z)', body, re.DOTALL)
    if tldr_match:
        tldr_text = re.sub(r'[\r\n]+', ' ', tldr_match.group(1)).strip()
        tldr_text = re.sub(r'\s+', ' ', tldr_text)
        snippet = f"Episode {ep_num} {title} TL;DR {tldr_text[:250]}"
    else:
        clean_body = re.sub(r'[#\*`_]', '', body)
        clean_body = re.sub(r'\s+', ' ', clean_body).strip()
        snippet = f"Episode {ep_num} {title} {clean_body[:250]}"

    # Keywords (extract techniques, bold items, headers, bug types)
    keywords = []
    bold_items = re.findall(r'\*\*(.*?)\*\*', body)
    for b in bold_items:
        b_clean = b.strip()
        if b_clean and len(b_clean) > 2 and len(b_clean) < 60 and b_clean not in keywords:
            keywords.append(b_clean)

    index_data.append({
        "episode": ep_num,
        "title": title,
        "snippet": snippet,
        "keywords": keywords[:20]
    })

# Preserve existing structure if original file had detailed keywords for earlier eps
if os.path.exists(OUT):
    try:
        with open(OUT, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing_map = {item["episode"]: item for item in existing}
        for item in index_data:
            if item["episode"] not in existing_map:
                existing_map[item["episode"]] = item
            else:
                # Update title & snippet if changed, keep existing keywords if rich
                existing_map[item["episode"]]["title"] = item["title"]
                existing_map[item["episode"]]["snippet"] = item["snippet"]
                if len(existing_map[item["episode"]].get("keywords", [])) < 5:
                    existing_map[item["episode"]]["keywords"] = item["keywords"]
        index_data = [existing_map[k] for k in sorted(existing_map.keys())]
    except Exception as e:
        print(f"Warning loading existing search index: {e}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)

print(f"Search index written to {OUT} with {len(index_data)} episodes.")
