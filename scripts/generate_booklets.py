#!/usr/bin/env python3
"""
Generate educational booklets from episode summaries.
Reads each episode markdown, parses structured sections,
and appends a teaching booklet that explains concepts.
"""

import os
import re
import sys
from pathlib import Path

SRC_DIR = Path("src/content/episodes")
TEMPLATE = """---

### 📘 Episode Booklet

#### 1. Episode in one sentence
{one_liner}

#### 2. What you should learn
{learning_outcomes}

#### 3. Core concepts explained
{core_concepts}

#### 4. Techniques and tactics
{techniques}

#### 5. Good Quotes
{quotes}

#### 6. Mental models
{mental_models}

#### 7. Real-world application
{real_world}

#### 8. Red flags and pitfalls
{pitfalls}

#### 9. Vocabulary
{vocabulary}

#### 10. Self-test
{self_test}

#### 11. The practical takeaway
{takeaway}
"""


def parse_episode(content: str) -> dict:
    """Parse an episode markdown into structured sections."""
    # Remove frontmatter
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]

    sections = {
        "title": "",
        "tldr": [],
        "key_takeaways": [],
        "bugs": [],
        "techniques": [],
        "tools": [],
        "advice": [],
        "ai_takeaway": "",
        "guests": [],
        "full_text": body,
    }

    lines = body.split("\n")
    current_section = None
    current_subsection = None

    for line in lines:
        stripped = line.strip()

        # Detect section headers
        if stripped.startswith("# ") or stripped.startswith("## "):
            if "title" not in sections or not sections["title"]:
                sections["title"] = stripped.lstrip("# ").strip()
            continue

        if "### TL;DR" in stripped or "### Tldr" in stripped.lower():
            current_section = "tldr"
            continue
        if "### Key Takeaways" in stripped or "### Key takeaways" in stripped:
            current_section = "key_takeaways"
            continue
        if "### Bugs and Findings" in stripped:
            current_section = "bugs"
            current_subsection = None
            continue
        if "### Techniques and Primitives" in stripped:
            current_section = "techniques"
            continue
        if "### Tooling and Resources" in stripped:
            current_section = "tools"
            continue
        if "### Suggestions" in stripped or "### Advice" in stripped:
            current_section = "advice"
            continue
        if "### AI Takeaway" in stripped:
            current_section = "ai_takeaway"
            continue
        if "### Guests" in stripped or "**Guests" in stripped:
            current_section = "guests"
            continue
        if "### 📖 Reference Booklet" in stripped or "### 📘" in stripped:
            current_section = None  # Stop before appended booklet
            continue
        if stripped.startswith("---") and current_section:
            current_section = None
            continue

        # Collect content for current section
        if current_section == "tldr" and stripped.startswith("- "):
            sections["tldr"].append(stripped[2:])
        elif current_section == "key_takeaways" and (stripped.startswith("- ") or stripped.startswith("**")):
            sections["key_takeaways"].append(stripped.lstrip("- ").lstrip("*").rstrip("*").strip())
        elif current_section == "techniques" and stripped.startswith("- "):
            sections["techniques"].append(stripped[2:])
        elif current_section == "tools" and stripped.startswith("- "):
            sections["tools"].append(stripped[2:])
        elif current_section == "advice" and stripped.startswith("- "):
            sections["advice"].append(stripped[2:].strip('"').strip('"').strip('"'))
        elif current_section == "ai_takeaway" and stripped:
            sections["ai_takeaway"] += stripped + " "
        elif current_section == "bugs" and (stripped.startswith("#### ") or stripped.startswith("- ")):
            if stripped.startswith("#### "):
                sections["bugs"].append({"title": stripped[5:], "details": []})
            elif sections["bugs"]:
                sections["bugs"][-1]["details"].append(stripped)
        elif current_section == "guests" and stripped:
            sections["guests"].append(stripped)

    return sections


def generate_one_liner(data: dict) -> str:
    """Generate a one-sentence summary of the episode."""
    tldr = data["tldr"]
    if tldr:
        # Combine first TL;DR point as the core lesson
        return tldr[0].strip()
    title = data.get("title", "")
    if title:
        return f"Episode {title} covers practical bug bounty techniques and security research insights."
    return "This episode covers practical bug bounty techniques and security research insights."


def generate_learning_outcomes(data: dict) -> str:
    """Generate learning outcomes from key takeaways."""
    outcomes = []
    for item in data["key_takeaways"][:5]:
        # Clean up markdown formatting
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', item)
        clean = clean.strip().rstrip(".")
        if clean:
            outcomes.append(f"- Understand **{clean.lower()}**")

    if not outcomes and data["tldr"]:
        for item in data["tldr"][:5]:
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', item)
            clean = clean.strip().rstrip(".")
            if clean:
                outcomes.append(f"- Learn about **{clean.lower()}**")

    if not outcomes:
        outcomes = [
            "- Understand the vulnerability classes discussed",
            "- Learn practical exploitation techniques",
            "- Know which tools are useful for this type of research",
        ]

    return "\n".join(outcomes)


def generate_core_concepts(data: dict) -> str:
    """Generate core concept explanations from bugs and techniques."""
    sections = []

    for bug in data["bugs"][:3]:
        title = re.sub(r'\*\*([^*]+)\*\*', r'\1', bug["title"])
        sections.append(f"**{title}**")
        # Explain what the bug class is
        if "SSRF" in title.upper():
            sections.append("- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.")
            sections.append("- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.")
            sections.append("- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.")
        elif "XSS" in title.upper():
            sections.append("- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.")
            sections.append("- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.")
            sections.append("- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.")
        elif "IDOR" in title.upper():
            sections.append("- **What it is:** Insecure Direct Object Reference — accessing resources by manipulating identifiers (IDs, filenames) in API calls without proper authorization checks.")
            sections.append("- **Why it matters:** IDOR is one of the most common and bountiful vulnerability classes in bug bounty. It's often simple to find and exploit.")
            sections.append("- **Common mistake:** Only testing sequential IDs — also try UUIDs, encoded values, and name-based references.")
        elif "RCE" in title.upper() or "DESERIALIZATION" in title.upper():
            sections.append("- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.")
            sections.append("- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).")
            sections.append("- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.")
        elif "CSRF" in title.upper():
            sections.append("- **What it is:** Cross-Site Request Forgery — tricking a victim's browser into making unwanted requests to a site where they're authenticated.")
            sections.append("- **Why it matters:** CSRF can change email, password, or perform actions on behalf of the victim.")
            sections.append("- **Common mistake:** Only testing GET-based CSRF — POST and PUT endpoints with CSRF tokens may still be vulnerable if tokens are predictable.")
        elif "OPEN REDIRECT" in title.upper():
            sections.append("- **What it is:** An application redirects users to an attacker-controlled URL, often used in phishing or to bypass OAuth flows.")
            sections.append("- **Why it matters:** Open redirects are building blocks for credential theft and OAuth token theft chains.")
            sections.append("- **Common mistake:** Dismissing open redirects as low severity — they're critical links in high-impact attack chains.")
        elif "NOSQL" in title.upper():
            sections.append("- **What it is:** NoSQL injection — exploiting MongoDB/Redis/CouchDB query syntax to bypass authentication, extract data, or execute commands.")
            sections.append("- **Why it matters:** NoSQL databases are widely used. Injection techniques differ from SQL but can be equally devastating.")
            sections.append("- **Common mistake:** Assuming NoSQL means no injection — operators like $gt, $ne, $regex can bypass authentication.")
        else:
            sections.append(f"- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.")
        sections.append("")

    for tech in data["techniques"][:3]:
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', tech.split("—")[0] if "—" in tech else tech.split("-")[0] if "-" in tech else tech)
        clean = clean.strip()
        if clean:
            sections.append(f"**{clean}**")
            if "—" in tech:
                explanation = tech.split("—", 1)[1].strip() if "—" in tech else ""
                sections.append(f"- {explanation}")
            else:
                sections.append(f"- A technique discussed in this episode for security research and bug bounty hunting.")
            sections.append("")

    if not sections:
        sections = [
            "**Vulnerability Classes Discussed**",
            "This episode covers specific vulnerability classes with real-world examples. Review the bugs section for detailed exploitation paths.",
            "",
            "**Reconnaissance and Discovery**",
            "The techniques discussed focus on finding attack surface and identifying vulnerable endpoints through systematic testing.",
            "",
        ]

    return "\n".join(sections)


def generate_techniques(data: dict) -> str:
    """Generate actionable technique explanations."""
    sections = []
    for tech in data["techniques"][:5]:
        parts = tech.split("—", 1)
        name = re.sub(r'\*\*([^*]+)\*\*', r'\1', parts[0]).strip()
        desc = parts[1].strip() if len(parts) > 1 else ""

        sections.append(f"**{name}**")
        if desc:
            sections.append(f"- **What it is:** {desc}")
        else:
            sections.append(f"- **What it is:** A technique for security research discussed in this episode.")
        sections.append(f"- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.")
        sections.append(f"- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.")
        sections.append("")

    if not sections:
        sections = [
            "**Systematic Testing Approach**",
            "- **What it is:** Methodical testing of application features for vulnerability classes",
            "- **When to use it:** Always — systematic testing catches bugs that ad-hoc testing misses",
            "- **What can go wrong:** Spending too much time on low-probability paths",
            "",
        ]

    return "\n".join(sections)


def generate_quotes(data: dict) -> str:
    """Generate good quotes from the episode with attribution."""
    sections = []
    for quote in data["advice"][:6]:
        # Clean up the quote - remove markdown formatting
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', quote)
        clean = clean.strip().strip('"').strip('"').strip('"')
        
        # Try to extract speaker attribution
        # Patterns: "quote" — Name on topic, "quote" - Name, quote — Name
        speaker = ""
        quote_text = clean
        
        # Check for em dash attribution
        if "—" in clean:
            parts = clean.split("—", 1)
            quote_text = parts[0].strip().strip('"').strip('"').strip('"')
            speaker = parts[1].strip()
        elif " - " in clean:
            parts = clean.split(" - ", 1)
            quote_text = parts[0].strip().strip('"').strip('"').strip('"')
            speaker = parts[1].strip()
        
        if quote_text and len(quote_text) > 5:
            if speaker:
                sections.append(f'- *"{quote_text}"* — **{speaker}**')
            else:
                sections.append(f'- *"{quote_text}"*')
    
    if not sections:
        sections = [
            '- *"The best bugs come from persistence and deep understanding of the target"*',
            '- *"Always think about what the worst thing that could happen is"*',
            '- *"Don\'t be afraid to spend time on a single target"*',
        ]
    
    return "\n".join(sections)


def generate_mental_models(data: dict) -> str:
    """Generate mental models from advice and techniques."""
    models = []
    for advice in data["advice"][:3]:
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', advice).strip().strip('"')
        if clean and len(clean) > 10:
            models.append(f"- **{clean[:60]}** — This mindset helps you find bugs others miss by approaching the problem from a different angle.")

    if not models:
        models = [
            "- **Think like an attacker** — Always consider the worst-case impact of a vulnerability. What would a malicious actor do with this access?",
            "- **Persistence pays off** — The best bugs often come from spending deep time on a single target rather than skimming many targets.",
            "- **Follow the data** — Track how user input flows through the application. Sources (inputs) lead to sinks (dangerous operations).",
        ]

    return "\n".join(models)


def generate_real_world(data: dict) -> str:
    """Generate practical application guidance."""
    items = []
    for tk in data["key_takeaways"][:4]:
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', tk).strip()
        if clean:
            items.append(f"- **Try this:** {clean}")

    if not items:
        items = [
            "- **Try this:** Pick a bug class from this episode and find 3 real examples on HackerOne bug reports",
            "- **Practice:** Set up a local vulnerable application (DVWA, Juice Shop) and practice the exploitation techniques",
            "- **Watch for:** Similar patterns in your own targets — the vulnerability classes discussed are common across web applications",
        ]

    return "\n".join(items)


def generate_pitfalls(data: dict) -> str:
    """Generate red flags and pitfalls."""
    pitfalls = []
    for bug in data["bugs"][:2]:
        details = bug.get("details", [])
        for d in details:
            if "obstacle" in d.lower() or "solved" in d.lower() or "blocked" in d.lower():
                clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', d).strip()
                pitfalls.append(f"- {clean}")

    if not pitfalls:
        pitfalls = [
            "- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked",
            "- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones",
            "- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface",
        ]

    return "\n".join(pitfalls)


def generate_vocabulary(data: dict) -> str:
    """Generate glossary of key terms."""
    terms = []
    seen = set()

    all_text = " ".join(data["tldr"] + data["key_takeaways"] + [t for t in data["techniques"]])

    # Common security terms to define
    term_defs = {
        "SSRF": "Server-Side Request Forgery — server makes requests on behalf of attacker",
        "XSS": "Cross-Site Scripting — injecting JavaScript into web pages viewed by other users",
        "IDOR": "Insecure Direct Object Reference — accessing resources by manipulating identifiers",
        "CSRF": "Cross-Site Request Forgery — tricking users into making unwanted requests",
        "RCE": "Remote Code Execution — running arbitrary code on a target server",
        "SQLi": "SQL Injection — inserting SQL queries through user input",
        "API": "Application Programming Interface — structured endpoints for data exchange",
        "JWT": "JSON Web Token — compact token format for authentication",
        "OAuth": "Open standard for authorization — delegated access without sharing passwords",
        "CORS": "Cross-Origin Resource Sharing — browser mechanism for cross-domain requests",
        "DNS": "Domain Name System — translates domain names to IP addresses",
        "WAF": "Web Application Firewall — filters and monitors HTTP traffic",
        "Burp": "Burp Suite — popular web application security testing proxy",
        "recon": "Reconnaissance — systematic discovery of target attack surface",
        "fuzzing": "Sending unexpected or malformed data to discover vulnerabilities",
        "deserialization": "Converting serialized data back into objects — dangerous if attacker-controlled",
        "Redis": "In-memory data store — often exploitable via SSRF or injection",
        "SSRF": "Server-Side Request Forgery — server makes HTTP requests on attacker's behalf",
        "AWS metadata": "Cloud instance metadata service at 169.254.169.254 — contains IAM credentials",
        "prompt injection": "Tricking an LLM into ignoring its instructions by injecting malicious input",
        "agent": "AI system that can use tools and make decisions autonomously",
        "LLM": "Large Language Model — AI system trained on text data for generation and understanding",
        "meta-prompting": "Using a prompt to rewrite another prompt for better results",
        "tree-of-thought": "Prompting technique that explores multiple reasoning paths",
        "embeddings": "Mathematical representations of text for similarity search",
        "0-day": "Vulnerability unknown to the vendor — no patch available",
        "1-day": "Vulnerability with a patch available but not yet applied",
        "ACL": "Access Control List — permissions defining who can access what",
        "BOLA": "Broken Object Level Authorization — accessing objects without proper checks",
        "XXE": "XML External Entity — injecting XML that references external resources",
        "SSTI": "Server-Side Template Injection — injecting template syntax that executes on server",
    }

    for term, definition in term_defs.items():
        if term.lower() in all_text.lower() and term.lower() not in seen:
            terms.append(f"- **{term}** — {definition}")
            seen.add(term.lower())

    if not terms:
        terms = [
            "- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities",
            "- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure",
            "- **Attack Surface** — All points where an unauthorized user can try to enter or extract data",
        ]

    return "\n".join(terms)


def generate_self_test(data: dict) -> str:
    """Generate self-test questions."""
    questions = []

    if data["bugs"]:
        bug_title = re.sub(r'\*\*([^*]+)\*\*', r'\1', data["bugs"][0]["title"])
        questions.append(f"1. **Recall:** What is the root cause of the vulnerability in {bug_title}?")
        questions.append(f"2. **Application:** If you found a similar pattern in a different application, what would your first test be?")

    if data["techniques"]:
        questions.append("3. **Reasoning:** Why is this technique effective against the target? What makes it work?")
        questions.append("4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?")

    questions.append("5. **Recall:** Name three tools mentioned in this episode and their primary use case.")
    questions.append("6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?")
    questions.append("7. **Application:** Design a testing workflow that combines multiple techniques from this episode.")

    if len(questions) < 7:
        questions.append("8. **Reflection:** What would you do differently if you had to redo this testing from scratch?")

    return "\n".join(questions[:8])


def generate_takeaway(data: dict) -> str:
    """Generate the practical takeaway."""
    items = []
    bold_pattern = re.compile(r'\*\*([^*]+)\*\*')
    if data["tldr"]:
        items.append(f"1. **{data['tldr'][0][:80]}**")
    if data["key_takeaways"]:
        clean_tk = bold_pattern.sub(r'\1', data['key_takeaways'][0])[:80]
        items.append(f"2. **{clean_tk}**")
    if len(data["key_takeaways"]) > 1:
        clean_tk2 = bold_pattern.sub(r'\1', data['key_takeaways'][1])[:80]
        items.append(f"3. **{clean_tk2}**")

    if not items:
        items = [
            "1. **Understand the vulnerability class** — Know how it works and why it matters",
            "2. **Master the exploitation technique** — Practice the specific steps to exploit it",
            "3. **Apply the mental model** — Use the thinking patterns to find similar bugs in other targets",
        ]

    return "\n".join(items)


def process_episode(filepath: Path) -> bool:
    """Process a single episode and append booklet."""
    content = filepath.read_text(encoding="utf-8")

    # Skip if booklet already exists
    if "### 📘 Episode Booklet" in content:
        return False

    data = parse_episode(content)

    # Generate booklet sections
    booklet = TEMPLATE.format(
        one_liner=generate_one_liner(data),
        learning_outcomes=generate_learning_outcomes(data),
        core_concepts=generate_core_concepts(data),
        techniques=generate_techniques(data),
        quotes=generate_quotes(data),
        mental_models=generate_mental_models(data),
        real_world=generate_real_world(data),
        pitfalls=generate_pitfalls(data),
        vocabulary=generate_vocabulary(data),
        self_test=generate_self_test(data),
        takeaway=generate_takeaway(data),
    )

    # Remove the old Reference Booklet section if it exists
    # (replaced by the new educational booklet)
    if "### 📖 Reference Booklet" in content:
        idx = content.index("### 📖 Reference Booklet")
        content = content[:idx].rstrip()

    # Append the new booklet
    content = content.rstrip() + "\n" + booklet
    filepath.write_text(content, encoding="utf-8")
    return True


def main():
    if not SRC_DIR.exists():
        print(f"Error: {SRC_DIR} not found")
        sys.exit(1)

    episodes = sorted(SRC_DIR.glob("episode-*.md"))
    print(f"Found {len(episodes)} episodes")

    processed = 0
    skipped = 0

    for ep in episodes:
        try:
            if process_episode(ep):
                processed += 1
                print(f"  ✓ {ep.name}")
            else:
                skipped += 1
                print(f"  — {ep.name} (already has booklet)")
        except Exception as e:
            print(f"  ✗ {ep.name}: {e}")

    print(f"\nDone: {processed} processed, {skipped} skipped")


if __name__ == "__main__":
    main()
