---
layout: post
title: "Your Financial Data Stays on Your Machine. Here's How"
subtitle: "How Personal Portfolio Tracker keeps your data private and how you can verify it yourself"
date: 2026-05-29
tags: [personal finance, privacy, security, local-first, india]
---

Privacy claims are easy to make. This post explains what Personal Portfolio Tracker actually does. You can verify it yourself rather than taking it on trust.

---

## No Cloud, No Server

Personal Portfolio Tracker is desktop software that runs entirely on your Windows or Mac computer. There is no mobile app, no backend server, no database hosted somewhere else, and no company storing your transactions. Your browser connects to `localhost`, your own machine, not to the internet.

This means:

- Your data is never at risk from a company data breach
- There is no account that can be hacked, suspended, or deleted
- Your financial history doesn't disappear if the developer shuts down or changes pricing
- No one can sell your portfolio data or use it to train models

---

## The Privacy Audit Page

The software includes a built-in Privacy Audit page (under Admin) that gives you live evidence of what's happening on your machine while it runs.

It shows you the active network connections from the software. When AI features are off, the only connections are between your browser and your own computer. You can watch this in real time. There is nothing to take on faith.

---

## AI Features: Strictly Opt-In

If you enable AI features, Personal Portfolio Tracker can answer questions about your portfolio and generate recommendations. Here is exactly what gets sent to the AI:

- Fund names and category
- Portfolio values and goal amounts
- Goal names and timelines

What is **never** sent:

- Account numbers or folio numbers
- PAN or Aadhaar
- Bank details or passwords

These details are never stored in the database to begin with, so they cannot be transmitted anywhere.

AI features are off by default. If you never enable them, no data leaves your machine.

---

## File Integrity Verification

Every release ships with a fingerprint, a unique code that represents the exact files in that release. This fingerprint is printed in your purchase confirmation email.

The Privacy Audit page lets you verify that the files on your machine match that fingerprint. If anything had been tampered with after distribution, the numbers wouldn't match. This check runs entirely offline. It doesn't contact any server.

---

## Antivirus Notice

The software has been scanned by all major antivirus engines — 0 out of 67 flagged it on VirusTotal. If your AV still flags the file, update your AV definitions and re-scan.

---

## Your Backup, Your Control

Your data backup is a file you create and store wherever you choose: your own hard drive, an encrypted USB, Google Drive. There is no automatic sync to any service. You decide where your financial history lives.

---

Personal Portfolio Tracker is available for Windows and Mac. Setup takes about 20 minutes.
