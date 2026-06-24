import re, os, json
from collections import defaultdict

SRC = "src/content/episodes"
OUT = "src/data/booklet-data.json"

bugs_by_type = defaultdict(list)
techniques = []
tools_set = set()
guests = []
hosts_seen = set()
guests_seen = set()
all_episodes = []
suggestions = []

for fname in sorted(os.listdir(SRC)):
    if not fname.endswith(".md"):
        continue
    m = re.match(r"episode-(\d+)\.md", fname)
    if not m:
        continue
    num = int(m.group(1))
    with open(os.path.join(SRC, fname), "r") as f:
        raw = f.read()

    # Strip frontmatter
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        body = parts[2] if len(parts) >= 3 else raw

    ep_data = {
        "num": num,
        "bugs": [],
        "techniques": [],
        "tools": [],
        "guests": [],
    }

    # --- GUESTS / HOSTS ---
    # Look in the first 15 lines for the guest/host metadata line
    header = "\n".join(body.split("\n")[:15])
    gh_match = re.search(r'\*\*Guests/Hosts:\*\*\s*(.+)', header)
    if gh_match:
        raw_names = gh_match.group(1)
        # Split on ), ( or ,
        names = re.split(r'[,;]', raw_names)
        for n in names:
            n = n.strip().strip("*").strip()
            if not n:
                continue
            # Identify hosts vs guests
            if "Justin" in n or "Joel" in n or "Gardner" in n or "Margolis" in n:
                if n not in hosts_seen:
                    hosts_seen.add(n)
            else:
                # Extract just the name part before parenthetical
                main_name = re.sub(r'\s*\(.*?\)', '', n).strip()
                if main_name and main_name not in guests_seen:
                    guests_seen.add(main_name)
                    guests.append({"name": main_name, "episodes": [num]})
                elif main_name:
                    for g in guests:
                        if g["name"] == main_name:
                            g["episodes"].append(num)
                            break
                ep_data["guests"].append(main_name)
    # Also try "Guests:" or "Hosts:" separately
    if not gh_match:
        g_match = re.search(r'\*\*Guests?:\*\*\s*(.+)', header)
        if g_match:
            for n in re.split(r'[,;]', g_match.group(1)):
                n = n.strip().strip("*").strip()
                if n and n not in guests_seen:
                    guests_seen.add(n)
                    guests.append({"name": n, "episodes": [num]})
                    ep_data["guests"].append(n)

    # --- BUGS ---
    bug_sections = re.split(r'(?m)^####\s+', body)
    for bs in bug_sections[1:]:
        lines = bs.split("\n")
        title_line = lines[0].strip()
        bug_type_raw = ""
        type_sep = re.search(r'[—–\-]\s*(.+?)$', title_line)
        if type_sep:
            bug_type_raw = type_sep.group(1).strip()
        target = ""
        tm2 = re.search(r'\*\*Target/context:\*\*\s*(.+)', bs)
        if tm2:
            target = tm2.group(1).strip()
        root_cause = ""
        rc2 = re.search(r'\*\*Root cause:\*\*\s*(.+)', bs)
        if rc2:
            root_cause = rc2.group(1).strip()
        technique = ""
        tech2 = re.search(r'\*\*Technique(?: / how found)?:\*\*\s*(.+)', bs)
        if tech2:
            technique = tech2.group(1).strip()
        impact = ""
        imp2 = re.search(r'\*\*Impact / severity / bounty:\*\*\s*(.+)', bs)
        if imp2:
            impact = imp2.group(1).strip()
        steps = ""
        steps_match = re.search(r'\*\*Exploitation steps:\*\*\s*(.+?)(?=\n\*\*|\n\n|\Z)', bs, re.DOTALL)
        if steps_match:
            steps = steps_match.group(1).strip()

        bug_entry = {
            "title": title_line,
            "type": bug_type_raw,
            "target": target,
            "root_cause": root_cause,
            "technique": technique,
            "impact": impact,
            "steps": steps[:200] if steps else "",
        }

        # Categorize by type
        types = re.split(r'[,/]', bug_type_raw)
        for t in types:
            t = t.strip()
            if t:
                bugs_by_type[t].append({"episode": num, "title": title_line, "target": target, "root_cause": root_cause, "impact": impact})
        ep_data["bugs"].append(bug_entry)

    # --- TECHNIQUES ---
    tech_section = re.search(r'(?m)^### Techniques and Primitives\n(.+?)(?=\n### |\n---|\Z)', body, re.DOTALL)
    if tech_section:
        for line in tech_section.group(1).split("\n"):
            ls = line.strip()
            if ls.startswith("- **"):
                tcm = re.match(r'- \*\*(.+?)\*\*\s*[—–\-:]\s*(.*)', ls)
                if tcm:
                    name = tcm.group(1).strip()
                    desc = tcm.group(2).strip()
                    techniques.append({"episode": num, "name": name, "description": desc})
                    ep_data["techniques"].append(name)

    # --- TOOLS ---
    tool_section = re.search(r'(?m)^### Tooling and Resources\n(.+?)(?=\n### |\n---|\Z)', body, re.DOTALL)
    if tool_section:
        for line in tool_section.group(1).split("\n"):
            ls = line.strip()
            if ls.startswith("- "):
                tool = ls[2:].strip()
                # Clean up leading/trailing
                tool = re.sub(r'\s*[—–\-]\s*.*$', '', tool).strip().strip("*")
                if tool and len(tool) > 2:
                    tools_set.add(tool)

    # --- SUGGESTIONS ---
    adv_section = re.search(r'(?m)^### Suggestions and Advices from Hunter\n(.+?)(?=\n---|\Z)', body, re.DOTALL)
    if adv_section:
        for line in adv_section.group(1).split("\n"):
            ls = line.strip()
            if ls.startswith("- "):
                suggestions.append({"episode": num, "text": ls[2:].strip()})

    all_episodes.append(ep_data)

# --- Build final structure ---
bug_type_counts = {k: len(v) for k, v in sorted(bugs_by_type.items(), key=lambda x: -len(x[1]))}

# Create technique index by name
technique_by_name = defaultdict(list)
for t in techniques:
    technique_by_name[t["name"]].append(t["episode"])

data = {
    "bug_type_counts": bug_type_counts,
    "bugs_by_type": {k: v for k, v in sorted(bugs_by_type.items())},
    "techniques": techniques,
    "techniques_by_name": {k: sorted(v) for k, v in sorted(technique_by_name.items())},
    "tools": sorted(tools_set),
    "guests": sorted(guests, key=lambda g: g["name"]),
    "suggestions_count": len(suggestions),
    "suggestions": suggestions[:100],  # top 100
    "total_episodes": len(all_episodes),
    "total_bugs": sum(len(ep["bugs"]) for ep in all_episodes),
    "total_techniques": len(techniques),
    "total_tools": len(tools_set),
    "total_guests": len(guests),
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Booklet data written to {OUT}")
print(f"  Episodes: {len(all_episodes)}")
print(f"  Bug types: {len(bug_type_counts)}")
print(f"  Total bugs found: {sum(len(v) for v in bugs_by_type.values())}")
print(f"  Techniques: {len(techniques)}")
print(f"  Tools: {len(tools_set)}")
print(f"  Guests: {len(guests)}")
print(f"  Suggestions: {len(suggestions)}")
print(f"\nTop bug types:")
for t, c in list(bug_type_counts.items())[:15]:
    print(f"  {t}: {c}")
