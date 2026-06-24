import re, os, json

SRC = "src/content/episodes"
DATA = "src/data/booklet-data.json"

with open(DATA) as f:
    data = json.load(f)

# Build lookups
tools_by_ep = {}
for t in data["techniques"]:
    ep = t["episode"]
    if ep not in tools_by_ep:
        tools_by_ep[ep] = set()
    tools_by_ep[ep].add(t["name"])

guests_by_ep = {}
for g in data["guests"]:
    for ep in g["episodes"]:
        if ep not in guests_by_ep:
            guests_by_ep[ep] = []
        guests_by_ep[ep].append(g["name"])

bugs_by_ep = {}
for bug_type, bugs in data["bugs_by_type"].items():
    for b in bugs:
        ep = b["episode"]
        if ep not in bugs_by_ep:
            bugs_by_ep[ep] = []
        bugs_by_ep[ep].append({"type": bug_type, "title": b["title"]})

suggestions_by_ep = {}
for s in data["suggestions"]:
    ep = s["episode"]
    if ep not in suggestions_by_ep:
        suggestions_by_ep[ep] = []
    suggestions_by_ep[ep].append(s["text"])

for fname in sorted(os.listdir(SRC)):
    m = re.match(r"episode-(\d+)\.md", fname)
    if not m:
        continue
    ep = int(m.group(1))
    path = os.path.join(SRC, fname)

    with open(path) as f:
        content = f.read()

    # Strip frontmatter to get body
    body = content
    fm = ""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[0] + "---" + parts[1] + "---\n"
            body = parts[2]

    # Check if Darsnameh already appended
    if "### 📖 Darsnameh" in body or "### Darsnameh" in body:
        print(f"  SKIP {fname} — already has Darsnameh")
        continue

    # Build reference section
    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 📖 Darsnameh")
    lines.append("")

    has_any = False

    # Guests
    ep_guests = guests_by_ep.get(ep, [])
    if ep_guests:
        has_any = True
        lines.append("**Guests:**")
        for gname in ep_guests:
            # Find all episodes for this guest
            geps = []
            for g in data["guests"]:
                if g["name"] == gname:
                    geps = g["episodes"]
                    break
            refs = ", ".join(f"[#{e:03d}](/episodes/{e})" for e in sorted(geps))
            lines.append(f"- **{gname}** — also appears in {refs}")
        lines.append("")

    # Bug types
    ep_bugs = bugs_by_ep.get(ep, [])
    if ep_bugs:
        has_any = True
        # Deduplicate by type
        seen_types = set()
        unique_bugs = []
        for b in ep_bugs:
            if b["type"] not in seen_types:
                seen_types.add(b["type"])
                unique_bugs.append(b)
        lines.append("**Bugs & Vulnerabilities:**")
        for b in unique_bugs[:8]:
            search_link = f"[search](/search?q={b['type'].replace(' ', '%20')})"
            lines.append(f"- **{b['type']}** — {b['title']} ({search_link})")
        if len(unique_bugs) > 8:
            lines.append(f"- *+{len(unique_bugs) - 8} more bug types*")
        lines.append("")

    # Techniques
    ep_tools = tools_by_ep.get(ep, set())
    if ep_tools:
        has_any = True
        lines.append("**Techniques:**")
        for tname in sorted(ep_tools)[:10]:
            tech_entry = data.get("techniques_by_name", {}).get(tname, [])
            refs = ", ".join(f"[#{e:03d}](/episodes/{e})" for e in sorted(tech_entry[:5]))
            if refs:
                lines.append(f"- **{tname}** — also in {refs}")
            else:
                lines.append(f"- **{tname}**")
        if len(ep_tools) > 10:
            lines.append(f"- *+{len(ep_tools) - 10} more techniques*")
        lines.append("")

    # Advice
    ep_advice = suggestions_by_ep.get(ep, [])
    if ep_advice:
        has_any = True
        lines.append("**Advice:**")
        for a in ep_advice[:3]:
            lines.append(f"- *\"{a}\"*")
        if len(ep_advice) > 3:
            lines.append(f"- *+{len(ep_advice) - 3} more pieces of advice*")
        lines.append("")

    if not has_any:
        lines.append("*No structured reference data available for this episode.*")
        lines.append("")

    # Append to file
    darsnameh = "\n".join(lines)
    with open(path, "w") as f:
        f.write(fm + body.rstrip() + darsnameh + "\n")

    print(f"  ✓ {fname} — Darsnameh appended ({len(ep_guests)} guests, {len(unique_bugs)} bugs, {len(ep_tools)} techniques)")

print("\nDone!")
