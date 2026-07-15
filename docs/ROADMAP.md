# Daily Market Tracker Roadmap

## Project Vision

Daily Market Tracker is an automated market monitoring system that records the overnight state of six core financial indicators, generates a standardized **Market Fingerprint** visualization, archives historical data, and publishes an interactive dashboard.

The project is **not intended to predict the market**. Instead, it provides a consistent, automated framework for observing market conditions over time.

The long-term goal is to build a continuously growing market state database that supports visualization, statistical analysis, market regime detection, clustering, and future research.

Daily Market Tracker uses Yahoo Finance daily OHLC data as the canonical market data source for all instruments. No instrument-specific session adjustments are applied in v1.0.
---

# Design Principles

## Single Source of Truth (SSOT)

The entire project is built around a single historical database:

```
data/history.csv
```

Every visualization, dashboard, and future analysis should be generated from this file.

There should never be multiple independent versions of the same data.

---

# System Architecture

```
Yahoo Finance
        │
        ▼
GitHub Actions (Daily)
        │
        ├── Fetch market data
        ├── Calculate overnight gaps
        ├── Update history.csv
        ├── Generate Market Fingerprint
        ├── Commit changes
        └── Push to GitHub
                │
                ▼
GitHub Repository
                │
                ▼
Streamlit Cloud
```

No local computer should be required.

Everything should run automatically.

---

# Repository Structure

```
Daily_Market_Tracker/

├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── app.py
│
├── data/
│   └── history.csv
│
├── figures/
│   ├── 2026-07-15.png
│   ├── 2026-07-16.png
│   └── ...
│
├── scripts/
│   ├── fetch_data.py
│   ├── generate_fingerprint.py
│   └── daily_pipeline.py
│
├── demo/
│   ├── Overnight_Market_Fingerprint.py
│   ├── Overnight_Market_Fingerprint.ipynb
│   ├── Overnight_Market_Fingerprint.csv
│   └── Overnight_Market_Fingerprint.xlsx
│
├── docs/
│   └── ROADMAP.md
│
└── .github/
    └── workflows/
        └── daily_market.yml
```

---

# Development Phases

## Phase 0

- Repository setup
- Folder structure
- Prototype visualization
- Project roadmap

---

## Phase 1

- Automatic Yahoo Finance data collection
- Historical database
- GitHub Actions automation

---

## Phase 2

- Automatic Market Fingerprint generation
- Automatic figure archiving

---

## Phase 3

- Streamlit dashboard
- Historical browsing
- Figure gallery

---

## Phase 4

- Statistical analysis
- Rolling percentile normalization
- Market regime detection
- Historical analytics

---

# Daily Workflow

Every trading day after the U.S. market closes:

1. Fetch market data from Yahoo Finance
2. Calculate overnight gaps
3. Append a new row to `history.csv`
4. Generate the daily Market Fingerprint
5. Save the figure
6. Commit new data
7. Push changes to GitHub
8. Streamlit automatically refreshes

If today's data already exists in `history.csv`, the workflow should exit without making changes.

---

# Data Sources

Yahoo Finance

Required indicators:

- S&P 500
- Nasdaq-100 Futures
- VIX
- U.S. 10-Year Treasury Yield
- U.S. Dollar Index
- WTI Crude Oil

For each indicator collect:

- Previous Close
- Open
- Overnight Gap
- Overnight Gap %

---

# Historical Database

The historical database contains one row per trading day.

Suggested columns:

```
Date,
SP500_GapPct,
NASDAQ100_GapPct,
VIX_GapPct,
TNX_GapPct,
DXY_GapPct,
WTI_GapPct
```

Future versions may include additional columns such as:

```
Previous Close
Open
Gap
Volume
```

All analyses should be derived from this single dataset.

---

# Daily Figure

Generate

```
figures/YYYY-MM-DD.png
```

Each figure includes:

- Market Shape (Radar Plot)
- Overnight Changes (Heatmap)
- Direction-adjusted Colorbar
- Automatic scaling
- Date
- Figure annotation

---

# GitHub Actions

Run automatically every weekday after the U.S. market closes.

Workflow:

1. Checkout repository
2. Install dependencies
3. Execute

```bash
python scripts/daily_pipeline.py
```

4. Commit updated files
5. Push changes back to GitHub

The workflow should skip execution if today's record already exists in `history.csv`.

---

# Streamlit Dashboard

Homepage

- Today's Market Fingerprint
- Today's Raw Data
- Overnight Heatmap
- Market Shape

Future pages

- Historical Table
- Figure Gallery
- Monthly Calendar View
- Market Statistics
- Interactive Dashboard

---

# Version Roadmap

## v1.0

- Automatic data collection
- Historical database
- Automatic figure generation
- GitHub Actions
- Streamlit dashboard

---

## v1.1

- Historical dashboard
- Calendar browser
- Figure gallery

---

## v1.2

- Rolling percentile normalization
- Market regime classification
- Risk-On / Risk-Off score

---

## v2.0

- Market clustering
- Similarity search
- PCA visualization
- Hidden market state detection
- Long-term statistical analysis

---

# Coding Principles

- Keep functions independent.
- Avoid duplicated code.
- Centralize configuration.
- Separate:
  - data collection
  - data processing
  - visualization
  - deployment
- Every module should have a single responsibility.
- `history.csv` is the Single Source of Truth.
- All figures and analyses should be reproducible from `history.csv`.

---

# Long-term Goal

Daily Market Tracker is designed to build a long-term, standardized historical record of the overnight market environment.

The objective is **observation**, not prediction.

By collecting consistent daily data over many years, the project will provide a reusable dataset for visualization, quantitative analysis, market research, and future machine learning applications.