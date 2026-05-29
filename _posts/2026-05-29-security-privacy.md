---
layout: post
title: "Your Financial Data Stays on Your Machine — Here's How"
subtitle: "How the app keeps your data private and how you can verify it yourself"
date: 2026-05-29
tags: [personal finance, privacy, security, local-first, india]
---

Privacy claims are easy to make. This post explains what the app actually does — and how you can verify it yourself rather than taking it on trust.

---

## No Cloud, No Server

The app runs entirely on your computer. There is no backend server, no database hosted somewhere else, and no company storing your transactions. Your browser connects to `localhost` — your own machine — not to the internet.

This means:

- Your data is never at risk from a company data breach
- There is no account that can be hacked, suspended, or deleted
- Your financial history doesn't disappear if the developer shuts down or changes pricing
- No one can sell your portfolio data or use it to train models

---

## The Privacy Audit Page

The app includes a built-in Privacy Audit page (under Admin) that gives you live evidence of what's happening on your machine while the app runs.

It shows you the active network connections from the app — and when AI features are off, the only connections are between your browser and your own computer. You can watch this in real time. There is nothing to take on faith.

---

## AI Features: Strictly Opt-In

If you enable AI features, the app can answer questions about your portfolio and generate recommendations. Here is exactly what gets sent to the AI:

- Fund names and category
- Portfolio values and goal amounts
- Goal names and timelines

What is **never** sent:

- Account numbers or folio numbers
- PAN or Aadhaar
- Bank details or passwords

AI features are off by default. If you never enable them, no data leaves your machine.

---

## File Integrity Verification

Every release ships with a fingerprint — a unique code that represents the exact files in that release. This fingerprint is printed in your purchase confirmation email.

The Privacy Audit page lets you verify that the files on your machine match that fingerprint. If anything had been tampered with after distribution, the numbers wouldn't match. This check runs entirely offline — it doesn't contact any server.

---

## Antivirus Notice

Some antivirus programs flag the app's compiled files as suspicious when you first unzip it. This is a confirmed false positive — BitDefender's Malware Research Team has reviewed the files and confirmed they are clean. The detection will be removed in their next signature update.

If you see a warning, update your antivirus definitions. The Setup Wizard inside the app has step-by-step instructions for adding the app folder as an exclusion in Windows Defender, BitDefender, and other AV products.

---

## Your Backup, Your Control

Your data backup is a file you create and store wherever you choose — your own hard drive, an encrypted USB, Google Drive. There is no automatic sync to any service. You decide where your financial history lives.

---

The app is available for purchase for Windows and Mac. Setup takes about 20 minutes.
