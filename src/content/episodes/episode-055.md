---
title: "Popping WordPress Plugins — Methodology Braindump"
episode: 55
---


# Episode 55 Popping WordPress Plugins — Methodology Braindump

**Guest:** Ram Gall (Wordfence)
**Format:** Full transcript (feed)

### TL;DR
- Ram Gall from Wordfence walks the entire WordPress plugin vulnerability assessment methodology — sources, sinks, hooks, and escalations
- Elementor subscriber RCE via custom Ajax listener with nonce-only access control — arbitrary PHP file upload from subscriber role
- Deep taxonomy of WordPress attack surface: `add_action`, `add_filter`, `register_rest_routes`, shortcodes, and page-related code
- Nonce leaking, page-now manipulation for cross-admin-page access control bypass
- WordPress core still uses MD5-based password hashing (many rounds)

### Key Takeaways
- Audit plugins for `add_action('admin_init', …)` — triggers on any WP-admin page, even unauthenticated; no built-in CSRF or access control
- Nonces are NOT access control — they are CSRF tokens; never assume a nonce is unreachable
- `check_admin_referer` doesn't check referer header, only nonce
- `is_admin()` checks if the request originated from an admin page, NOT if the user is an admin
- Shortcode XSS is the most common in-scope vuln — contributor+ roles can trigger stored XSS that editors/admins see on review
- `register_rest_routes` lacks default CSRF but requires nonce; permission_callback is where auth goes — missing it = unauthenticated access
- `update_option` can set `users_can_register=1` and `default_role=administrator` for instant privilege escalation
- `update_user_meta` can set `wp_capabilities` to administrator — seen in membership plugins at registration

### Bugs and Findings

#### Elementor Subscriber+ RCE
- **Target/context:** Elementor (5M+ installs, likely 10M+)
- **Root cause:** Custom Ajax listener in onboarding module ran on `admin_init` (any admin page), checked only `wp_verify_nonce`, no capability check
- **Technique / how found:** Code review; the action was intended to upload the Pro upgrade zip but didn't validate the zip contents
- **Exploitation steps:**
  1. As a subscriber, navigate to any WP-admin page to grab the nonce (generated on `admin_init`)
  2. POST to the custom Ajax endpoint with the nonce and a malicious zip containing a PHP webshell
  3. The plugin's upload handler installs the zip (intended for Pro upgrade)
  4. Access the uploaded PHP file → RCE
- **Impact:** Full server compromise from subscriber account
- **Obstacles & how solved:** N/A — the nonce was the sole gate

#### Subscriber SSRF via REST Route (Gutenberg Blocks plugin)
- **Target/context:** "Get with Gutenberg Blocks" plugin
- **Root cause:** Registered REST route `get_remote_content` with permission callback `current_user_can('read')` — subscribers have this; the route took a URL, called `wp_remote_get()`, base64-decoded the response, and echoed it back
- **Technique / how found:** REST route enumeration at `/wp-json/` via `?rest_route=/`
- **Exploitation steps:**
  1. Authenticate as subscriber
  2. Craft JSON request to the REST endpoint with URL pointing to `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
  3. Response contains EC2 IMDSv1 credentials
- **Impact:** Full AWS account compromise via IMDS credential theft
- **Key technical details:** `wp_remote_get()` uses cURL; `wp_safe_remote_get()` exists but was not used; JSON body accepted for all HTTP methods
- **Obstacles & how solved:** Nonce required (subscriber has it); no CSRF possible

#### Unauthenticated Stored XSS via User-Agent Header (Security Plugin)
- **Target/context:** A security plugin (unnamed)
- **Root cause:** User-Agent header from blocked requests was stored in logs and rendered unescaped in the admin dashboard
- **Technique / how found:** Send a request that triggers a block with a malicious User-Agent containing `<script>alert(1)</script>`
- **Exploitation steps:**
  1. Craft HTTP request to the target site with XSS payload in User-Agent header
  2. Request gets blocked/logged by security plugin
  3. Admin visits the blocked-requests log page → payload executes
- **Impact:** Stored XSS in admin context → full site takeover (add admin user, edit plugins)
- **Obstacles & how solved:** N/A — output was not escaped

### Techniques and Primitives
- **Nonce Leakage + Nonce-as-Access-Control:** Generate/reuse nonces from accessible pages (admin bar, profile page) to call privileged Ajax handlers
- **Page-now / PHP_SELF manipulation:** Append `?page=admin.php` on a profile page to trick WordPress into generating nonces for a different admin page (NGINX-specific, uses `PHP_SELF`)
- **`$_REQUEST` vs `$_GET` discrepancy:** WordPress merges GET and POST into `$_REQUEST`, giving POST priority; pass correct page in GET parameter for access check, payload in POST body for echo
- **WP Handle Upload overrides:** Second parameter can disable MIME/type validation — grep for `'test_form' => false`
- **Labeled printf in wpdb::prepare:** `%1$s` doesn't add quotes (backward compat) → character-based SQL injection without string escape

### Tooling and Resources
- Wordfence Common WordPress Vulnerabilities and Prevention PDF (linked in show notes)
- `github.com/wordpressplugindirectory` — Justin's mirror of all WP SVN plugins, enabling code search and diff monitoring
- `wp_safe_remote_get()` vs `wp_remote_get()`

### Suggestions and Advices
- **Ram Gall:** "Never use nonce as the sole form of access control." / "If you can get Xdebug set up on a Docker container and step through basic Ajax actions, you'll get a much better sense."
- Shortcode XSS is the most common in-scope vuln — contributors must submit posts for review, ensuring an editor/admin sees the payload
- Ram recommends auditing "low install count authentication plugins" as they are "full" of bugs

### AI Takeaway
The WordPress hook system (`add_action`/`add_filter`) is a massive, poorly-documented attack surface where any hook + callback combo may be reachable from unexpected contexts. The gap between WordPress's naming conventions and actual behavior (`admin_init` reachable unauthenticated, `is_admin()` checks admin-page-origin not role) is a perpetual source of access control bugs.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Ram Gall from Wordfence walks the entire WordPress plugin vulnerability assessment methodology — sources, sinks, hooks, and escalations

#### 2. What you should learn
- Understand **audit plugins for `add_action('admin_init', …)` — triggers on any wp-admin page, even unauthenticated; no built-in csrf or access control**
- Understand **nonces are not access control — they are csrf tokens; never assume a nonce is unreachable**
- Understand **`check_admin_referer` doesn't check referer header, only nonce**
- Understand **`is_admin()` checks if the request originated from an admin page, not if the user is an admin**
- Understand **shortcode xss is the most common in-scope vuln — contributor+ roles can trigger stored xss that editors/admins see on review**

#### 3. Core concepts explained
**Elementor Subscriber+ RCE**
- **What it is:** Remote Code Execution via deserialization — attacker-controlled data is deserialized by the server, triggering code execution through object injection or gadget chains.
- **Why it matters:** Deserialization RCE is typically critical severity. It often requires chaining multiple primitives (object injection → Redis injection → RCE).
- **Common mistake:** Giving up when direct exploitation is blocked — look for pivoting techniques like Redis SLAVEOF replication.

**Subscriber SSRF via REST Route (Gutenberg Blocks plugin)**
- **What it is:** Server-Side Request Forgery — the server makes HTTP requests on behalf of the attacker, reaching internal services, cloud metadata, or other resources not meant to be exposed.
- **Why it matters:** SSRF can lead to internal network scanning, cloud credential theft (AWS metadata at 169.254.169.254), and in some cases full RCE.
- **Common mistake:** Assuming SSRF is only about reading responses — even blind SSRF can be exploited via timing or out-of-band techniques.

**Unauthenticated Stored XSS via User-Agent Header (Security Plugin)**
- **What it is:** Cross-Site Scripting — injecting malicious JavaScript that runs in a victim's browser session, allowing session theft, phishing, or further attacks.
- **Why it matters:** XSS remains one of the most common and impactful web vulnerabilities. Stored XSS can affect every user who views the page.
- **Common mistake:** Focusing only on reflected XSS and missing stored XSS in profile fields, file uploads, or message boards.

****Nonce Leakage + Nonce**
- A technique discussed in this episode for security research and bug bounty hunting.

****Page**
- A technique discussed in this episode for security research and bug bounty hunting.

**`$_REQUEST` vs `$_GET` discrepancy: WordPress merges GET and POST into `$_REQUEST`, giving POST priority; pass correct page in GET parameter for access check, payload in POST body for echo**
- A technique discussed in this episode for security research and bug bounty hunting.


#### 4. Techniques and tactics
**Nonce Leakage + Nonce-as-Access-Control: Generate/reuse nonces from accessible pages (admin bar, profile page) to call privileged Ajax handlers**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Page-now / PHP_SELF manipulation: Append `?page=admin.php` on a profile page to trick WordPress into generating nonces for a different admin page (NGINX-specific, uses `PHP_SELF`)**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**`$_REQUEST` vs `$_GET` discrepancy: WordPress merges GET and POST into `$_REQUEST`, giving POST priority; pass correct page in GET parameter for access check, payload in POST body for echo**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WP Handle Upload overrides: Second parameter can disable MIME/type validation**
- **What it is:** grep for `'test_form' => false`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Labeled printf in wpdb::prepare: `%1$s` doesn't add quotes (backward compat) → character-based SQL injection without string escape**
- **What it is:** A technique for security research discussed in this episode.
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"Ram Gall: "Never use nonce as the sole form of access control." / "If you can get Xdebug set up on a Docker container and step through basic Ajax actions, you'll get a much better sense."*
- *"Shortcode XSS is the most common in-scope vuln"* — **contributors must submit posts for review, ensuring an editor/admin sees the payload**
- *"Ram recommends auditing "low install count authentication plugins" as they are "full" of bugs"*

#### 6. Mental models
- **Ram Gall: "Never use nonce as the sole form of access contro** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Shortcode XSS is the most common in-scope vuln — contributor** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **Ram recommends auditing "low install count authentication pl** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** Audit plugins for `add_action('admin_init', …)` — triggers on any WP-admin page, even unauthenticated; no built-in CSRF or access control
- **Try this:** Nonces are NOT access control — they are CSRF tokens; never assume a nonce is unreachable
- **Try this:** `check_admin_referer` doesn't check referer header, only nonce
- **Try this:** `is_admin()` checks if the request originated from an admin page, NOT if the user is an admin

#### 8. Red flags and pitfalls
- - Obstacles & how solved: N/A — the nonce was the sole gate
- - Obstacles & how solved: Nonce required (subscriber has it); no CSRF possible

#### 9. Vocabulary
- **XSS** — Cross-Site Scripting — injecting JavaScript into web pages viewed by other users
- **CSRF** — Cross-Site Request Forgery — tricking users into making unwanted requests
- **RCE** — Remote Code Execution — running arbitrary code on a target server

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Elementor Subscriber+ RCE?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Ram Gall from Wordfence walks the entire WordPress plugin vulnerability assessme**
2. **Audit plugins for `add_action('admin_init', …)` — triggers on any WP-admin page,**
3. **Nonces are NOT access control — they are CSRF tokens; never assume a nonce is un**
