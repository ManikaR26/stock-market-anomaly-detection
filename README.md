# Stock Market Data Pipeline & Anomaly Detection

A Python-based pipeline that ingests streaming stock price data, applies rolling statistical analysis to detect abnormal price movements in real time, and visualizes results in an interactive dashboard.

![Dashboard Screenshot](dashboard_screenshot.png)

## Overview

This project simulates a continuous stock market data feed across five tickers (AAPL, GOOGL, TSLA, MSFT, AMZN) and processes each price tick through an anomaly detection pipeline. Abnormal price movements — sudden spikes or drops — are automatically flagged using a rolling z-score model, stored alongside the raw data, and visualized on an interactive dashboard.

## Features

- **Streaming data simulation** — generates realistic tick-by-tick price data with occasional injected shocks to mimic real market volatility
- **Rolling anomaly detection** — calculates a per-ticker rolling mean and standard deviation over a 20-tick window, flagging any price change beyond 3 standard deviations
- **Persistent storage** — every tick, along with its anomaly status and z-score, is stored in a SQLite database for later analysis
- **Interactive visualization** — generates an HTML dashboard (Plotly) plotting price trends per ticker with anomalies marked

## Tech Stack

Python · SQLite · Plotly · Pandas

## How It Works

1. `data_generator.py` simulates a live tick feed, producing a price update for a random ticker on each call
2. `pipeline.py` consumes the feed, computes a rolling z-score for each incoming tick against that ticker's recent history, flags anomalies, and writes everything to `market_data.db`
3. `dashboard.py` reads the database and generates `dashboard.html`, an interactive chart per ticker with anomalies marked in red

## Setup & Usage

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/stock-market-anomaly-detection.git
cd stock-market-anomaly-detection

# Install dependencies
pip install -r requirements.txt

# Run the pipeline (generates 200 simulated ticks)
python pipeline.py

# Generate the dashboard
python dashboard.py
```

Open `dashboard.html` in your browser to view the results.

## Sample Output

```
   ok      AAPL   price=  408.53 change=+0.08%
   ok      GOOGL  price=  374.72 change=-0.28%
ANOMALY    GOOGL  price=   353.9 change=-5.76%  z=-24.705
   ok      MSFT   price=  235.03 change=-0.11%
```

## Anomaly Detection Logic

For each ticker, the pipeline maintains a rolling window of the last 20 percentage price changes. Once enough history exists, each new tick's z-score is computed as:

```
z = (current % change - rolling mean) / rolling standard deviation
```

Any tick with `|z| > 3` is flagged as anomalous. This approach adapts to each ticker's own typical volatility rather than relying on a single fixed threshold across all stocks.

## Possible Extensions

This project currently runs as a single-process simulation. A natural next step toward a production-grade real-time system would be:
- **Apache Kafka** for streaming ingestion across multiple concurrent producers/consumers
- **Apache Spark Structured Streaming** for distributed rolling computations at scale
- **MySQL/PostgreSQL** in place of SQLite for concurrent multi-user access
- **Grafana** for live-updating dashboards instead of a static HTML export

## Author

Manika Rattan
[LinkedIn](https://linkedin.com/in/manika-rattan) · [GitHub](https://github.com/ManikaR26)
