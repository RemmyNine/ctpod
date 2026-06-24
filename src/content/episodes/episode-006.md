---
title: "Mobile Hacking Attack Vectors with Teknogeek (Joel Margolis)"
episode: 6
---


# Episode 6 Mobile Hacking Attack Vectors with Teknogeek (Joel Margolis)

### TL;DR
- Android intent filters, activities, and exported components — attack surface for external apps and browsers
- URL schemes, app links, and intent URLs: how to launch Android activities from the browser
- WebViews: content provider access, JavaScript interfaces, file access — massive attack surface
- Content providers: insecurely configured providers can be accessed via `content://` URIs from WebViews
- Broadcast receivers: exported receivers can be triggered by malicious apps
- SSL pinning bypass with universal Frida script
- Chrome `chrome://inspect` to debug WebViews on connected devices

### Key takeaways
- `AndroidManifest.xml` lists activities, services, broadcast receivers, content providers — check `android:exported` and intent filters
- Activities with intent filters and no explicit `android:exported="false"` are implicitly exported (pre-Android 12)
- URL schemes defined in intent filter `<data>` elements specify `scheme`, `host`, `port`, `path`
- App links = HTTP/HTTPS only, verified server-side; scheme URLs = any custom scheme
- Intent URLs (`intent://...`) from Chrome: requires activity to have `android.intent.category.BROWSABLE`
- WebViews: by default have `setAllowContentAccess(true)` and `setAllowFileAccess(true)` (Android <10)
- JavaScript interfaces exposed via `addJavascriptInterface()` with `@JavascriptInterface` decorator
- Content providers: can be accessed via `content://authority/path/id` from WebViews
- Use `scrcpy` (screen copy) to mirror Android device screen on computer over USB
- Use `adb reverse tcp:8080 tcp:8080` to proxy through USB

### Bugs and Findings

#### Shopify Point-of-Sale App — WebSocket Key Reset → Session Takeover
- **Target/context:** Shopify POS app — customer/shop-owner pairing via QR code
- **Root cause:** In the message handler, if an unknown message type was received, it reset the rolling public key handshake. Attacker could send bogus message → key reset → inject own public key
- **Technique / how found:**
  1. Analyzed QR code pairing — discovered it used plain WS (not WSS) connecting to local IP
  2. Read app source code (decompiled with JADX + VSCode)
  3. Renamed obfuscated functions to understand flow
  4. Noticed `setReceiverPublicKey` function called in the message handler as fallback for unknown message types
- **Exploitation steps:**
  1. ARP spoof on local network to intercept pairing communication
  2. Send unknown message type → device resets public key to attacker's key
  3. Send crafted messages as the shop owner → control cart/session
- **Key technical details:** WS (not WSS); rolling key handshake; `setReceiverPublicKey` fallback on unknown message types
- **Impact / severity / bounty:** Session/device takeover; triaged immediately once engineer saw the code reference
- **Obstacles & how solved:** Obfuscated code made analysis hard; solved by JADX deobfuscation flags + VSCode rename refactoring

#### [Episode 6] Red App WebView Cookie Bypass — Authentication Bypass
- **Target/context:** Android app requiring re-auth on resume
- **Root cause:** Forgot password webview injected user's session cookies. Clicking company logo in the webview navigated to homepage → bypassed re-auth screen
- **Technique / how found:** Proxied app through Burp; noticed cookies being injected into the forgot-password webview
- **Key technical details:** WebView class extended with custom cookie injection; forgot password → logo link → homepage with valid session

### Techniques and Primitives
- **Activity enumeration** — parse `AndroidManifest.xml` for exported activities/services/broadcast-receivers
- **GetSchemas** — Joel's tool to parse Android XML and list accessible URL schemes
- **JADX deobfuscation** — rename methods below threshold length; then VSCode refactoring to rename everywhere
- **WebView audit checklist** — check `setAllowContentAccess`, `setAllowFileAccess`, `addJavascriptInterface`, `setJavaScriptEnabled`
- **Chrome inspect for WebViews** — `chrome://inspect` on desktop shows debuggable WebViews on connected device
- **scrcpy** — mirror physical Android device to desktop via USB

### Tooling and Resources
- APKTool
- JADX / JADX-GUI
- VSCode with deobfuscation flags
- GetSchemas (Joel's tool)
- Frida + universal unpin script (Joel's script)
- scrcpy (screen copy)
- Android SDK emulator
- `adb reverse` / `adb forward`

### Suggestions and Advices from Hunter
- "If you see a WebView, look for JavaScript interfaces — they can be really dangerous" — Joel
- "If you can get your URL open inside a WebView, you have a launchpad for other attacks" — Joel
- "If you find an app that forces re-auth, try the forgot password flow — it might inject cookies into a WebView" — Justin
- "For obfuscated Android code, use JADX deobfuscation flags + VSCode rename refactoring" — Joel

### AI Takeaway
The Android WebView attack surface is enormous and under-audited. Three defaults to check: `setAllowContentAccess` (true by default pre-Android 10), `setAllowFileAccess` (true pre-Android 10), and JavaScript interfaces (custom bridge with `@JavascriptInterface`). Even a single XSS in a WebView can become full app compromise via the JavaScript bridge.
---

### 📘 Episode Booklet

#### 1. Episode in one sentence
Android intent filters, activities, and exported components — attack surface for external apps and browsers

#### 2. What you should learn
- Understand **`androidmanifest.xml` lists activities, services, broadcast receivers, content providers — check `android:exported` and intent filters**
- Understand **activities with intent filters and no explicit `android:exported="false"` are implicitly exported (pre-android 12)**
- Understand **url schemes defined in intent filter `<data>` elements specify `scheme`, `host`, `port`, `path`**
- Understand **app links = http/https only, verified server-side; scheme urls = any custom scheme**
- Understand **intent urls (`intent://...`) from chrome: requires activity to have `android.intent.category.browsable`**

#### 3. Core concepts explained
**Shopify Point-of-Sale App — WebSocket Key Reset → Session Takeover**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**[Episode 6] Red App WebView Cookie Bypass — Authentication Bypass**
- This vulnerability class is discussed in the episode. Review the technical details for exploitation steps and mitigation strategies.

**Activity enumeration**
- parse `AndroidManifest.xml` for exported activities/services/broadcast-receivers

**GetSchemas**
- Joel's tool to parse Android XML and list accessible URL schemes

**JADX deobfuscation**
- rename methods below threshold length; then VSCode refactoring to rename everywhere


#### 4. Techniques and tactics
**Activity enumeration**
- **What it is:** parse `AndroidManifest.xml` for exported activities/services/broadcast-receivers
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**GetSchemas**
- **What it is:** Joel's tool to parse Android XML and list accessible URL schemes
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**JADX deobfuscation**
- **What it is:** rename methods below threshold length; then VSCode refactoring to rename everywhere
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**WebView audit checklist**
- **What it is:** check `setAllowContentAccess`, `setAllowFileAccess`, `addJavascriptInterface`, `setJavaScriptEnabled`
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.

**Chrome inspect for WebViews**
- **What it is:** `chrome://inspect` on desktop shows debuggable WebViews on connected device
- **When to use it:** Apply this when testing targets with similar technology stacks or vulnerability patterns.
- **What can go wrong:** Technique may not work on all targets — adapt based on specific application behavior and WAF rules.


#### 5. Good Quotes
- *"If you see a WebView, look for JavaScript interfaces"* — **they can be really dangerous" — Joel**
- *"If you can get your URL open inside a WebView, you have a launchpad for other attacks"* — **Joel**
- *"If you find an app that forces re-auth, try the forgot password flow"* — **it might inject cookies into a WebView" — Justin**
- *"For obfuscated Android code, use JADX deobfuscation flags + VSCode rename refactoring"* — **Joel**

#### 6. Mental models
- **If you see a WebView, look for JavaScript interfaces — they ** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you can get your URL open inside a WebView, you have a la** — This mindset helps you find bugs others miss by approaching the problem from a different angle.
- **If you find an app that forces re-auth, try the forgot passw** — This mindset helps you find bugs others miss by approaching the problem from a different angle.

#### 7. Real-world application
- **Try this:** `AndroidManifest.xml` lists activities, services, broadcast receivers, content providers — check `android:exported` and intent filters
- **Try this:** Activities with intent filters and no explicit `android:exported="false"` are implicitly exported (pre-Android 12)
- **Try this:** URL schemes defined in intent filter `<data>` elements specify `scheme`, `host`, `port`, `path`
- **Try this:** App links = HTTP/HTTPS only, verified server-side; scheme URLs = any custom scheme

#### 8. Red flags and pitfalls
- - Obstacles & how solved: Obfuscated code made analysis hard; solved by JADX deobfuscation flags + VSCode rename refactoring

#### 9. Vocabulary
- **Bug Bounty** — Program where companies reward researchers for finding security vulnerabilities
- **Responsible Disclosure** — Reporting vulnerabilities to vendors before public disclosure
- **Attack Surface** — All points where an unauthorized user can try to enter or extract data

#### 10. Self-test
1. **Recall:** What is the root cause of the vulnerability in Shopify Point-of-Sale App — WebSocket Key Reset → Session Takeover?
2. **Application:** If you found a similar pattern in a different application, what would your first test be?
3. **Reasoning:** Why is this technique effective against the target? What makes it work?
4. **Application:** How would you adapt this technique if the target had a WAF blocking obvious payloads?
5. **Recall:** Name three tools mentioned in this episode and their primary use case.
6. **Reasoning:** What obstacles might you encounter when applying these techniques in a real engagement?
7. **Application:** Design a testing workflow that combines multiple techniques from this episode.

#### 11. The practical takeaway
1. **Android intent filters, activities, and exported components — attack surface for**
2. **`AndroidManifest.xml` lists activities, services, broadcast receivers, content p**
3. **Activities with intent filters and no explicit `android:exported="false"` are im**
