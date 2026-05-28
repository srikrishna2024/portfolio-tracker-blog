---
title: "What Personal Portfolio Tracker Actually Does: A Module-by-Module Walkthrough"
subtitle: "From CAMS import to goal health score — every feature explained"
tags: ["personal finance", "mutual funds", "india", "portfolio tracker", "goal planning"]
coverImage: ""
---

This post walks through every module in Personal Portfolio Tracker. If you've already read the introduction and want to know exactly what you're getting, this is that post.

The app is organised into sections. Here's what each one does.

---

## Data Import

Before the app can do anything useful, it needs your transaction history. There are three import paths.

### Equity Import

This handles mutual fund transactions from CAMS or MF Central.

- **CAMS PDF**: download your Consolidated Account Statement from camsonline.com, upload the PDF, and the app parses it automatically. Transactions, switch-ins, switch-outs, and redemptions are all handled.
- **MF Central PDF**: same process, different format.
- **MF Central Excel**: the full CAS download in Excel format — useful for large portfolios where PDFs get unwieldy.

The parser extracts every transaction with the correct date, units, NAV, and amount. After import, you get a preview with a row count and the option to confirm or discard before anything hits the database.

### Debt Import

This is the part most apps skip. EPF, NPS, PPF, and Superannuation don't appear in CAMS statements — they're separate instruments with separate data sources.

- **EPF**: upload the UMANG app PDF (your EPF passbook). The parser handles both the standard UMANG format and the older per-FY format.
- **NPS**: upload the NSDL CRA CSV (the SOA you download from NSDL's website). Tier I is fully supported; the parser handles all CRA formats.
- **PPF**: upload your PPF account statement PDF (ICICI format and similar).
- **Superannuation**: upload the statement PDF from your provider — six provider variants are supported.
- **Manual entry**: if your provider isn't supported, you can enter balances and yearly contributions manually using a plain CSV format the app defines.

After import, all these instruments appear alongside your mutual funds in the Debt & Fixed Income view, with projected values calculated forward to your retirement date.

### Stocks Import

Upload your stock transaction CSV. XIRR analysis and Ulcer Index are available for stock holdings in the Stock Portfolio section.

---

## NAV Data Manager

The app maintains a local copy of NAV history for every fund in the AMFI database. This is what makes all the historical analysis possible — returns, rolling returns, portfolio value history — without a live internet connection.

### Data Pipeline

The one-click workflow page. Two modes:

- **Weekly Maintenance**: downloads the full scheme list and historical NAV prices. Run this once after setup (~10–15 minutes) and once a week after that.
- **Daily Refresh**: updates just today's prices for funds you hold (2–5 minutes). Run this at the start of each day.

The pipeline runs in steps with a progress bar and shows you which step succeeded or failed. If a step fails, it retries automatically from a secondary source.

---

## My Portfolio

Once your data is in, these pages are your primary views.

### Equity Portfolio

Your current holdings in equity mutual funds. Each fund shows:
- Current value (live NAV × units)
- Invested amount
- Unrealised gain/loss in rupees and percentage
- XIRR since first purchase

Transaction history is filterable by fund and date range.

### Debt & Fixed Income

All your debt instruments — EPF, NPS, PPF, Superannuation, FDs, bonds — in one place. Shows current balance, projected value at retirement, and yearly contribution history.

For instruments with projected returns (PPF, FDs), you can set the expected interest rate and the app projects the balance forward.

### Portfolio Analysis

The aggregate view. Tabs covering:
- Portfolio composition by fund and asset class
- Overall XIRR
- Annual performance vs the NIFTY 50 TRI benchmark
- Equity vs debt allocation over time

### Rolling Returns

Returns across multiple time horizons: 1Y, 3Y, 5Y, 10Y rolling windows. Plotted as distributions so you can see not just the average but the spread of outcomes across different entry points.

### Portfolio Chat

Ask questions about your portfolio in plain English. The app fetches the relevant data and generates a response with supporting charts. Examples:

- *"Which fund has the highest XIRR?"*
- *"How much have I invested in the last 12 months?"*
- *"What's my allocation to mid-cap funds?"*

This requires AI features to be enabled in Setup Wizard.

### Portfolio Report

Generates a printable PDF report of your portfolio — holdings, goal progress, health score, and XIRR. Useful for the annual review or for sharing with a financial advisor.

---

## Goal Planning

This is the distinctive part of the app. Most portfolio tools show you what your portfolio is worth. This section tells you whether your portfolio is doing what you need it to do.

### Create a Goal

Describe a financial goal in plain English:
- *"Save ₹50 lakhs for my daughter's college in 12 years"*
- *"Build a ₹2 crore retirement corpus in 20 years"*
- *"Buy a house for ₹1.5 crore in 5 years — I already have ₹30 lakhs saved"*

If AI is enabled, Claude reads the description and fills in the structured fields (target amount, timeline, current value, monthly SIP). You review and edit everything before saving. Without AI, you fill in the form directly.

### Goal Fund Manager

Maps your equity funds to goals. One fund can serve multiple goals (split by percentage). After mapping, every calculation — health score, SIP requirement, K4/K8 — is goal-specific, not portfolio-wide.

### Goal Dashboard

The most-used page in the app. Shows:

- **Portfolio Health Score** (0–100): a composite of goal progress, fund tracking quality, and concentration risk.
- Per-goal progress cards: current corpus, required corpus, gap, and recommended monthly SIP.
- AI-generated recommendations: if AI is enabled, the dashboard can generate specific, actionable suggestions — fund replacements, SIP adjustments, rebalancing steps.

### Goal Diagnostics

The quarterly review page. Shows two proprietary metrics per goal:

**K4 (Weighted Tracking Error)**: How consistently do the funds in this goal track their benchmark? A low K4 means reliable benchmark exposure. A high K4 means the fund is unpredictable relative to the index — for better or worse.

**K8 (Required CAGR Safety Margin)**: Given your goal's current shortfall and remaining time, what's the minimum CAGR your portfolio needs? K8 compares this to the worst-case rolling CAGR seen historically. If K8 > 1, you're in margin territory. If K8 < 0.77, you're in a risk zone — the historical worst case is uncomfortably close to what you need.

These metrics are tracked quarterly so you can see trends over time.

### Decision Log

Records investment decisions with their rationale: why you bought a fund, why you rebalanced, why you held during a crash. Each entry has a decision type (BUY/SELL/HOLD/REBALANCE/SWITCH), a linked goal, and a free-text rationale.

Outcomes can be linked back to prior decisions. With AI enabled, the app can surface behavioural patterns across your decision history — e.g., "you tend to add lump sum during market highs" or "your hold decisions have a better outcome rate than your switch decisions."

### Annual Review

A structured April review — meant to be run once a year after the financial year closes. Covers:
- Portfolio health score year-on-year
- Goal progress vs 12 months ago
- SIP adequacy (are your SIPs sufficient given the gap?)
- Funds underperforming their benchmark by more than 3% over 3 years
- LTCG harvesting opportunities for the coming year
- K4/K8 status across all goals
- AI-generated prioritised action list (if AI enabled)

### Fund Managers

Tracks fund manager continuity for funds in your active goals. Flags funds where the manager has changed in the last 12 months — a meaningful risk factor that most screeners ignore. Manager data is entered manually from AMFI or AMC websites (no automated source exists for this data).

---

## Retirement Planning

### Retirement Planner

Enter your current age, retirement age, expected monthly expenses at retirement, inflation assumption, and current portfolio value. The planner:
- Calculates the corpus required at retirement
- Shows the monthly SIP required to reach it
- Projects the corpus value year by year

Also has an early retirement mode and a corpus longevity calculator (how long does a given corpus last given monthly withdrawals?).

### Bucket Strategy Simulator

Models the bucket approach to retirement withdrawals. You define three buckets (cash/short-term, balanced, equity) with different return assumptions. The simulator runs a year-by-year drawdown showing:
- How long each bucket lasts
- When refills happen (from equity → balanced → cash)
- Whether the corpus survives to a given age

Supports glide-path allocation (automatically shifting from equity to debt as you age) and inflation-adjusted expenses.

---

## Fund Analysis

### Fund Analysis

Head-to-head comparison of any two funds. Overlaid NAV charts, rolling return comparison, drawdown comparison, and correlation.

### Fund Performance

A six-tab analysis suite:
- Rolling returns distribution
- Risk-return scatter (returns vs standard deviation)
- Consistency score (how often does the fund beat the benchmark in each rolling window?)
- Downside capture and upside capture
- Category screener — all funds in a category ranked by rolling 3Y return

### Volatility Clustering

Identifies volatility regimes in a fund's history — periods of persistently high or low volatility. Useful for understanding whether recent volatility is unusual or part of a recurring pattern.

### Risk Analysis (Ulcer Index)

Four tabs:
- **Ulcer Index**: a risk metric that weights depth and duration of drawdowns, not just variance. Lower is better.
- **Drawdown stats**: worst drawdown, average drawdown, time to recovery.
- **Maximum drawdown timeline**: where the worst drawdowns occurred.
- **Antifragile fund finder**: identifies funds that have historically gained or held value during equity crashes.

### Factor Analysis

Verifies whether a fund's actual behaviour matches its stated style. For each fund, calculates:
- **R²**: how much of the fund's movement is explained by the benchmark. High R² with high expense ratio = closet indexer.
- **Tracking error**: how much the fund deviates from the benchmark.
- **Alpha**: excess return vs benchmark (annualised).
- **Upside/downside capture**: how much of benchmark gains/losses the fund captures.

Produces a scatter plot (R² vs tracking error) that places each fund in one of four quadrants: true index fund, closet indexer, active, or high-noise.

---

## Portfolio Lab

### Portfolio Builder

Simulate adding funds to your portfolio before committing. Enter a hypothetical allocation, and the app calculates the impact on diversification, expected return, and correlation with your existing holdings.

### Crash Simulator

Stress-tests your portfolio against historical crashes (2008 global financial crisis, 2020 COVID crash, 2015–2016 midcap drawdown). Shows how your current corpus would have fared, and whether your goals would have survived a poor-sequence event early in the accumulation phase.

### K4/K8 Optimizer

Helps you find the optimal fund weight split for a goal. You adjust fund weights using sliders (constrained to sum to 100%), and the app recalculates K4 (tracking error) and K8 (safety margin) in real time. There's also a grid search that finds the weight split that minimises K4 while keeping K8 above the 0.77 safety threshold.

---

## Tax Corner

### Tax Corner

Three tabs in one page:
- **MF Tax**: FIFO-based LTCG and STCG calculation for equity and debt funds. Shows taxable gains for the current financial year.
- **Stock Tax**: same calculation for stock holdings.
- **Advanced planning**: scenario modelling — what if you redeem X units of fund Y? What's the tax impact?

The FIFO engine handles the ₹1.25 lakh LTCG exemption, grandfathering (for pre-2018 units), and correct treatment of switch transactions.

### Tax Optimizer

Identifies tax harvesting opportunities: units you can redeem to book LTCG within the ₹1.25 lakh annual exemption, minimising future tax liability. Also flags STCG positions approaching 12 months (potential conversion to LTCG with a short wait).

### Arbitrage Tracker

Tracks your arbitrage fund positions. Arbitrage funds have equity tax treatment (LTCG at 10% after 12 months) despite near-debt-fund volatility — the tracker helps you manage the 12-month hold requirement and shows the effective post-tax return.

---

## Alerts & Monitoring

### Alert Center

Automated portfolio-wide alerts:
- **Goal drift**: a goal's trajectory has shifted significantly since the last review
- **Concentration**: more than 40% of a goal's value in one fund or one AMC
- **Tax deadline**: STCG positions approaching the 12-month mark
- **Stale NAV**: funds whose NAV hasn't updated in more than 2 days

Alerts are prioritised by severity and include a one-line explanation of what to do.

### Behaviour Analytics

Analyses your transaction history to infer investor behaviour patterns:
- **SIP discipline**: are you investing consistently or irregularly?
- **Timing quality**: are your lump sum additions correlated with market dips (good) or highs (bad)?
- **Crash response**: did you stop SIPs, continue, or add during major corrections?
- **Idle capital**: periods of large cash holdings not being deployed

With AI enabled, generates a coaching note based on the patterns found.

---

## Ask Freefincal

Answers questions about personal finance grounded in Freefincal's published articles — a large, well-regarded corpus of Indian personal finance writing. Two modes:

- **Ask mode**: ask any question about mutual funds, goal planning, or investment strategy
- **Portfolio review mode**: the app compares your portfolio against Freefincal's published guidelines and highlights gaps

---

## What's Next

The next post covers the security and privacy architecture — how the app proves your data never leaves your machine, how the integrity verification works, and what the antivirus false positive situation is about.
