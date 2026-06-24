---
title: "Archive Testing Methodology with Mathias Karlsson"
episode: 132
---


# Episode 132 Archive Testing Methodology with Mathias Karlsson

**Source:** Show notes (feed) — condensed.

### TL;DR
- Archive Alchemist tool for archive vulnerability testing.
- Three attack types: path traversal, symlinks, parser differentials.
- ZIP quirks: Unicode Path extension, CRC differentials, nullbyte truncation, path length truncation.
- 7-Zip treats empty entry as archive filename.
- Symlink + LD_PRELOAD for blind container RCE.

### Key takeaways
- [ ] Archive Alchemist: `archive-alchemist <archive> ls|cat|rm|add|replace` — ZIP, TAR, tar.gz.
- [ ] ZIP Unicode Path: third filename location. Windows Explorer ignores bad CRC, PowerShell rejects it.
- [ ] Nullbyte truncation: unzip/Python truncate on nullbyte — `file.exe\x00.txt` → `file.exe`.
- [ ] Path length truncation: unzip truncates at 4096 — padding + `.exe` changes extension.
- [ ] 7-Zip: empty entry = archive filename → `exploit.zip` extracts as `exploit.phar`.
- [ ] Symlink + overwrite = arbitrary file write.

### Bugs and Findings

#### ZIP Unicode Path Parser Differential — Filename confusion
- **Key detail:** Extra field ID `0x7075` = Unicode Path. CRC checks validity. Windows Explorer ignores bad CRC, PowerShell rejects.
- **Impact:** Same ZIP extracts different filenames on different parsers.

#### Unzip Path Length Truncation — Extension bypass
- **Technique:** 4090 chars padding + `.exe` → OS truncates at 4096 → `.exe` becomes real extension.
- **Impact:** Bypasses extension validation.

#### 7-Zip Empty Entry — Archive name reuse
- **Impact:** `payload.phar.zip` with empty entry extracts as `payload.phar`.

#### Symlink + LD_PRELOAD — RCE
- **Technique:**
  1. Symlink entry → `/etc/ld.so.preload`
  2. Overwrite same path → content: `/tmp/evil.so`
  3. Write shared object to `/tmp/evil.so`
  4. Next binary execution loads evil.so → RCE.
- **Key detail:** Only root can write `ld.so.preload`; containers often run as root.
- **Impact:** Silent RCE on next binary execution.

### Techniques and Primitives
- **Multiple filenames in ZIP** — Central directory, local header, Unicode Path extension.
- **CRC invalidation differential** — Invalid CRC = parser confusion between Explorer and PowerShell.
- **Nullbyte in archive** — Truncation at nullbyte.
- **Path length as oracle** — Error boundary at 4096 determines extraction directory length.
- **`<>` in filename as OS oracle** — Invalid on Windows, valid on Linux.
- **Polyglot archives** — Prepend arbitrary data to ZIP (offset-adjusted) or TAR (512-byte padded).

### Tooling and Resources
- Archive Alchemist (Mathias Karlsson)
- Ginwell's ZIP format talk
- SonarSource UTF-8 visualizer

### Suggestions and Advices from Hunter
- "Blind archive testing: create directory + file inside → if same as flat file, you have path traversal oracle."
- "Symlink testing: valid file → symlink to valid file → symlink to nonexistent file → error confirms symlink support."
- "`/proc/self/cwd` resolves current directory in arbitrary read."
- "`<>` in filename checks error vs success → Windows vs Linux fingerprint."
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Archive Alchemist tool for archive vulnerability testing.

#### 2. What you should learn
- Understand **[ ] archive alchemist: `archive-alchemist <archive> ls|cat|rm|add|replace` — zip, tar, tar.gz**
- Understand **[ ] zip unicode path: third filename location. windows explorer ignores bad crc, powershell rejects it**
- Understand **[ ] nullbyte truncation: unzip/python truncate on nullbyte — `file.exe\x00.txt` → `file.exe`**
- Understand **[ ] path length truncation: unzip truncates at 4096 — padding + `.exe` changes extension**
- Understand **[ ] 7-zip: empty entry = archive filename → `exploit.zip` extracts as `exploit.phar`**

#### 3. Core concepts explained
**ZIP Unicode Path Parser Differential — Filename confusion**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Unzip Path Length Truncation — Extension bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**7-Zip Empty Entry — Archive name reuse**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Multiple filenames in ZIP**
- Central directory, local header, Unicode Path extension.

**CRC invalidation differential**
- Invalid CRC = parser confusion between Explorer and PowerShell.

**Nullbyte in archive**
- Truncation at nullbyte.


#### 4. Techniques and tactics
**Multiple filenames in ZIP**
- **What it is:** Central directory, local header, Unicode Path extension.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**CRC invalidation differential**
- **What it is:** Invalid CRC = parser confusion between Explorer and PowerShell.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Nullbyte in archive**
- **What it is:** Truncation at nullbyte.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Path length as oracle**
- **What it is:** Error boundary at 4096 determines extraction directory length.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`<>` in filename as OS oracle**
- **What it is:** Invalid on Windows, valid on Linux.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Blind archive testing: create directory + file inside → if same as flat file, you have path traversal oracle."*
- *"Symlink testing: valid file → symlink to valid file → symlink to nonexistent file → error confirms symlink support."*
- *"`/proc/self/cwd` resolves current directory in arbitrary read."*
- *"`<>` in filename checks error vs success → Windows vs Linux fingerprint."*

#### 6. Mental models
- **Blind archive testing: create directory + file inside → if s** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Symlink testing: valid file → symlink to valid file → symlin** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **`/proc/self/cwd` resolves current directory in arbitrary rea** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** [ ] Archive Alchemist: `archive-alchemist <archive> ls|cat|rm|add|replace` — ZIP, TAR, tar.gz.
- **Try this:** [ ] ZIP Unicode Path: third filename location. Windows Explorer ignores bad CRC, PowerShell rejects it.
- **Try this:** [ ] Nullbyte truncation: unzip/Python truncate on nullbyte — `file.exe\x00.txt` → `file.exe`.
- **Try this:** [ ] Path length truncation: unzip truncates at 4096 — padding + `.exe` changes extension.

#### 8. Red flags and pitfalls
- **Giving up too early** — Many bugs require creative pivoting when initial exploitation paths are blocked
- **Ignoring blind vulnerabilities** — Blind SSRF, blind XSS, and timing-based attacks can be just as impactful as visible ones
- **Missing the forest for the trees** — Don't get tunnel vision on one vulnerability class; step back and consider the full attack surface

#### 9. Vocabulary
- **RCE** — Remote Code Execution — running arbitrary code on a target server
- **ACL** — Access Control List — permissions defining who can access what

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in ZIP Unicode Path Parser Differential — Filename confusion?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Archive Alchemist tool for archive vulnerability testing.**
2. **[ ] Archive Alchemist: `archive-alchemist <archive> ls|cat|rm|add|replace` — ZIP**
3. **[ ] ZIP Unicode Path: third filename location. Windows Explorer ignores bad CRC,**
