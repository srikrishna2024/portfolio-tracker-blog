---
title: "Personal Portfolio Tracker: Your Finances, Your Machine"
subtitle: "A local-first financial planning app for serious Indian investors — no cloud, no subscriptions, no data sharing"
tags: ["personal finance", "mutual funds", "india", "portfolio tracker", "privacy"]
coverImage: ""
---

Most financial apps make a quiet bargain with you: convenience in exchange for your data. Your portfolio lives on someone else's server, gets used to train models, and disappears if the company shuts down or changes its pricing.

**Personal Portfolio Tracker is built on the opposite assumption.** Every number you enter — every transaction, every goal, every NAV price — stays on your own computer. The database runs locally on PostgreSQL. The app runs locally on Python. Nothing leaves your machine unless you explicitly choose to enable AI features.

This post is the start of a series where I document exactly what the app does, how it works, and why it was built this way.

---

## Who This Is For

The app is built for the Indian investor who:

- Holds mutual funds across CAMS or MF Central — equity, debt, ELSS, hybrid
- Also has EPF, NPS, PPF, and Superannuation that don't show up in those statements
- Has financial goals — retirement, children's education, house purchase — and wants to track progress rigorously
- Has used CAGR calculators and realised that's not enough
- Is tired of explaining their portfolio to a wealth manager who earns from product sales

If you're the kind of person who has a spreadsheet but wishes it had proper database-backed history and AI analysis, this is what that spreadsheet would have become.

---

## The Core Idea: Local-First

"Local-first" means the app works entirely offline. Your data is stored in a PostgreSQL database on your own machine. The app itself is a web interface served by Python (Streamlit) — it opens in your browser, but it's talking to localhost, not the internet.

What this means practically:

- No internet required after the initial setup
- No account to create, no password to forget
- Your data persists across upgrades — it's in a proper database, not a JSON file
- You can back it up, restore it, and move it to a new machine
- There is no third party who can lose your data, sell your data, or lock you out

The app has AI features (Claude by Anthropic) that can generate goal analysis and portfolio recommendations. These are strictly opt-in. If you enable them, some portfolio information (fund names, values, goal names — no account numbers or passwords) is sent to Anthropic's API. If you leave AI off, no data leaves your machine. Ever.

---

## Why This Isn't Just Another CAGR Calculator

Mutual fund apps and calculators have a common blind spot: they treat each fund as independent and each metric as standalone.

The question they answer: *"What has this fund returned?"*

The questions this app answers: *"Is this fund actually doing the job I hired it for?"* and *"Given where I am today, what does this mean for the goal I'm trying to reach?"*

That shift — from fund-centric to goal-centric — is the design principle behind every module.

### Example: The Health Score

When you open the Goal Dashboard, you see a number: your Portfolio Health Score. It's not just XIRR. It's a composite of:

- Whether your current corpus is on the trajectory needed to hit each goal
- Whether the funds in each goal are tracking their benchmarks tightly (K4 — weighted tracking error)
- Whether your portfolio can survive a poor-sequence year and still meet the goal (K8 — worst-case CAGR safety margin)
- Whether you have concentration risk in any single fund or sector

A 10% XIRR can still produce a poor health score if the money isn't mapped to a goal with a concrete timeline, or if the funds are unreliable benchmark trackers. That nuance is what the app is designed to surface.

---

## What the App Covers

Here's a plain-English summary of what the app does. I'll go deep on each in separate posts.

**Data Import**
Import your portfolio from CAMS PDF statements, MF Central PDF/Excel, or by uploading a CSV. EPF, NPS, PPF, and Superannuation statements (PDF or NSDL CRA CSV) import automatically — no manual re-typing.

**Portfolio Tracking**
Live holdings, transaction history, XIRR, rolling returns, debt-to-equity breakdown, and annual performance vs benchmark. All your mutual funds plus EPF/NPS/PPF in one view.

**Goal Planning**
Create goals in plain English (*"₹50 lakhs for daughter's college in 12 years"*) and map your funds to them. The app tracks progress, shows whether your SIP is sufficient, and warns you when a goal is at risk.

**Retirement Planning**
Corpus projector, retirement planner, bucket strategy simulator. The numbers are goal-linked, not abstract.

**Fund Analysis**
Compare funds, check rolling returns, screen for risk (Ulcer Index, drawdown), verify whether a fund's style matches its label (Factor Analysis), and identify closet indexers.

**Tax Corner**
FIFO-based LTCG and STCG calculation. Tax harvesting optimizer. Arbitrage tracker.

**Alerts and Monitoring**
Automated alerts for goal drift, portfolio concentration, stale NAV data, and tax deadlines.

**AI Features (Optional)**
Ask the app questions about your portfolio in plain English. Get AI-generated annual review summaries. Use Claude to analyse fund replacements and generate rebalancing recommendations.

---

## How It's Built

The app is written entirely in Python. The database backend is PostgreSQL. The UI is Streamlit. The AI layer uses Anthropic's Claude API.

The core logic — calculations, analytics, tax engine — is compiled into protected binary files before distribution. Buyers don't get source code; they get a working software.

This has one known side effect: the compiled files trigger a false positive in a small number of antivirus engines. All 67 antivirus engines engines on VirusTotal flagged it — a completely clean result, including Windows Defender, Kaspersky, Sophos, McAfee, and BitDefender. Every release ships with a SHA256 integrity fingerprint so buyers can verify the files are untampered.

---

## What's Next

The next post covers every module in detail — what it does, what inputs it needs, and what you learn from it.

After that: how the privacy and security model works, including the Privacy Audit page that gives you live proof your data isn't leaving the machine.

If you've been managing your portfolio in a spreadsheet and you're ready for something more rigorous, the app is available for purchase. Setup takes about 20 minutes and works on Windows and Mac.
