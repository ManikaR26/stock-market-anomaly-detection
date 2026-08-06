import sqlite3
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

DB_PATH = "market_data.db"
OUTPUT_HTML = "dashboard.html"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM ticks ORDER BY id", conn)
    conn.close()
    return df


def build_dashboard(df):
    tickers = df["ticker"].unique()
    fig = make_subplots(
        rows=len(tickers), cols=1,
        subplot_titles=[f"{t} — Price & Anomalies" for t in tickers],
        shared_xaxes=False,
    )

    for i, ticker in enumerate(tickers, start=1):
        sub = df[df["ticker"] == ticker].reset_index(drop=True)
        anomalies = sub[sub["is_anomaly"] == 1]

        fig.add_trace(
            go.Scatter(x=sub.index, y=sub["price"], mode="lines",
                       name=f"{ticker} price", line=dict(width=1.5)),
            row=i, col=1,
        )
        fig.add_trace(
            go.Scatter(x=anomalies.index, y=anomalies["price"], mode="markers",
                       name=f"{ticker} anomaly", marker=dict(color="red", size=9, symbol="x")),
            row=i, col=1,
        )

    fig.update_layout(
        height=300 * len(tickers),
        title_text="Real-Time Stock Pipeline — Price Trends & Detected Anomalies",
        showlegend=False,
    )

    fig.write_html(OUTPUT_HTML)
    print(f"Dashboard written to {OUTPUT_HTML}")

    total = len(df)
    n_anom = df["is_anomaly"].sum()
    print(f"\nSummary: {total} ticks processed, {n_anom} anomalies flagged ({n_anom/total*100:.2f}% of ticks).")


if __name__ == "__main__":
    df = load_data()
    build_dashboard(df)