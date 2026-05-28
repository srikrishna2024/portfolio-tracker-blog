---
title: "Security and Privacy in Personal Portfolio Tracker: Local Data, Verifiable Proof"
subtitle: "How the app ensures your financial data stays on your machine — and how you can verify it"
tags: ["personal finance", "privacy", "security", "local-first", "india"]
coverImage: ""
---

Privacy claims are easy to make. "We take your security seriously" appears in the terms of service of every company that has suffered a breach.

Personal Portfolio Tracker takes a different approach: the privacy properties are verifiable by the user, not just asserted by the developer. This post explains how.

---

## The Baseline: No Cloud Infrastructure

Most financial apps route your data through their servers. They have to — the app logic runs server-side, the database is hosted somewhere, and your browser talks to their API.

Personal Portfolio Tracker has no server to route through. The architecture is:

- **Database**: PostgreSQL running locally on your machine, on port 5432
- **App server**: Python (Streamlit) running locally on your machine, on port 8501
- **Browser**: your browser connects to `http://localhost:8501` — not to the internet

There is no backend server. There is no API you're connecting to. Your browser and the Python process are on the same machine. The data goes nowhere.

This is verifiable. The Privacy Audit page (Admin → Privacy Audit) shows you live network connections for the running app. You can watch it in real time and confirm that no connections are being made to external hosts.

---

## The Privacy Audit Page

The Privacy Audit page provides four categories of live evidence:

### 1. Active Network Connections

Shows every active TCP connection from the Python process, with the remote host and port. While the app is running without AI features:

- Port 5432 (PostgreSQL): one local connection — your own database
- Port 8501 (Streamlit): one local connection — your browser talking to the app server

No connections to `api.anthropic.com`, no connections to analytics services, no connections to any external host. The page captures this and displays it.

### 2. Data Storage Locations

Shows exactly where your data lives: the local PostgreSQL database on this machine. No cloud sync paths, no shadow copies, no data written to temporary folders accessible by third parties.

### 3. Code Scan

Scans the running app code for network-making calls. Reports every `requests.get()`, `httpx.post()`, and similar call it finds, with the URL it's calling. For the core app logic (non-AI path), the only external calls are:

- AMFI's public API (to download fund NAV prices when you run the Data Pipeline)
- Anthropic's API (only if AI features are enabled, only on explicit user action)

Both are disclosed, scoped, and optional.

### 4. Code Integrity

Verifies that the app files on your machine match the SHA256 fingerprint published in your purchase email. If any file has been modified since distribution — by malware, by an incomplete download, or by anything else — the mismatch shows up here.

This section works fully offline.

---

## AI Features: What Gets Sent and When

AI features are optional and off by default. If you enable them:

- Data is sent to Anthropic's Claude API **only when you explicitly trigger an AI action** (clicking "Generate Recommendations", asking a question in Portfolio Chat, etc.)
- What is sent: fund names, fund codes, portfolio values, goal names, goal amounts, holding periods — portfolio structure, not identity
- What is **never** sent: account numbers, folio numbers, PAN, passwords, bank details
- The app uses the `claude-sonnet-4-6` model via Anthropic's API
- Anthropic's API is GDPR-compliant; refer to their privacy policy for data retention details

If AI is off, the Anthropic API is never contacted. Zero bytes leave your machine.

---

## Security Audit Page

The Security Audit page (Admin → Security Audit) runs a local scan of the app's own code looking for:

- **Package CVEs**: checks installed Python packages against the CVE database for known vulnerabilities
- **Hardcoded secrets**: scans for API keys, passwords, or tokens that might have been accidentally committed to code (there should be none — all secrets are loaded from `.env` at runtime)
- **SQL injection patterns**: looks for raw string interpolation in database queries (the app uses parameterised queries with `%s` placeholders throughout)
- **Sensitive file exposure**: verifies that `.env`, backup files, and private keys are not accessible via the web server

This is the same kind of scan a security auditor would run. You can run it yourself at any time.

---

## Integrity Verification

Every release ships with a `checksums.sha256` file. This file contains the SHA256 hash of every file in the distribution. The final line of the file is the SHA256 of the manifest itself — the fingerprint.

This fingerprint is printed in the purchase confirmation email.

To verify your copy:

1. Open **Admin → Privacy Audit**
2. Scroll to **Section 4: Code Integrity**
3. Compare the fingerprint shown to the one in your email

If the fingerprints match, the files on your machine are exactly the files that were distributed. No file has been added, removed, or modified.

This works fully offline — the verification is a local computation, not a lookup against a server.

---

## License System

The app validates a license key on startup. The license key is an HMAC-SHA256 of your email address, signed with a secret key that only the developer holds. This means:

- Keys are deterministic: given your email, the same key is always generated
- Keys are unforgeable: without the signing secret, you can't generate a valid key
- Revocation is instant: a key can be added to the revoked list and blocked on the next app update, without touching your data

The license check happens locally. There is no activation server, no phone-home, and no key that expires unless explicitly revoked.

---

## The Antivirus False Positive (Resolved)

One security concern that came up after launch: some antivirus engines flagged the app's compiled files as malware. This was a false positive, and **BitDefender's Malware Research Team has since confirmed the file is clean** — the detection will be removed in their next signature update.

Here's the background. The app's core logic (calculations, analytics engine, tax engine) is compiled into native binary files using Nuitka before distribution. Nuitka translates Python to C and compiles it to a `.pyd` binary. These binaries protect the source code — buyers can't read the algorithms.

The false positive arose because certain antivirus engines use heuristic detection: they flag files based on structural patterns rather than known malicious signatures. Nuitka-compiled binaries have a specific structure that triggers these heuristics.

The affected engines were **BitDefender** and ~7 products that share its signature database: ALYac, Arcabit, Emsisoft, eScan, GData, VIPRE.

**Current VirusTotal status:** 59 out of 67 engines clean. The clean engines include Windows Defender, Kaspersky, Sophos, McAfee, ESET, Avast, AVG, and all major scanners.

**If you use BitDefender and still see the warning:** open BitDefender → Settings → Update → **Check for Updates** to pull the latest definitions, which will include the fix.

**If any AV is still blocking the app:** add the app folder as an exclusion — this is a standard AV feature and takes about 30 seconds:

- **Windows Defender**: Settings → Windows Security → Virus & threat protection → Manage settings → Exclusions → Add an exclusion → Folder → select your app folder
- **BitDefender**: Open BitDefender → Protection → Antivirus → Settings → Manage Exceptions → Add Exception → your app folder
- **Other AV products**: look for "Exclusions" or "Whitelist" in your AV settings

If your AV has already quarantined files, open the Quarantine section, restore them, and then add the exclusion.

---

## What Is Not in the Distribution

The distribution zip that buyers receive does not contain:

- Source code (compiled to `.pyd` binaries)
- Developer tooling (`build_dist.py`, `generate_checksums.py`, `generate_license.py`)
- Git history (`.git/`)
- Development documentation (`docs/`, `CLAUDE.md`, `CHANGELOG.md`)
- Test files (`tests/`)
- `.env` file or any credentials

The `distribution_manifest.toml` in the developer repository explicitly lists what ships and what doesn't. A safety check in `build_dist.py` scans the zip before finalising and aborts the build if any never-ship file appears in the archive.

---

## Backup Security

Your database backup (created via Admin → Backup) is a PostgreSQL dump file — a plain-text SQL dump of all your tables. It contains your complete financial history: every transaction, every goal, every NAV update.

It does **not** contain passwords, API keys, or license credentials — those live in `.env`, which is never included in backups.

The backup file should be treated like a financial document — copy it to a second location (Google Drive, OneDrive, encrypted USB) after every backup, and consider encrypting it if you're storing it in a shared location.

---

## Summary

| Property | Status |
|----------|--------|
| Data stored locally only | ✅ PostgreSQL on your machine |
| No cloud sync | ✅ Verified via Privacy Audit |
| AI data sharing | ✅ Opt-in only, scoped to portfolio structure |
| File integrity verification | ✅ SHA256 fingerprint, fully offline |
| License system | ✅ HMAC, no activation server |
| Antivirus false positives | ⚠️ BitDefender family — add exclusion |
| Source code protection | ✅ Nuitka-compiled binaries |
| Security audit tool | ✅ Built into the app |

Privacy is not a promise in the terms of service. It's a property you can verify yourself, in the app, right now.
