import sqlite3
from collections import defaultdict, deque
from statistics import mean, stdev
from data_generator import stream

DB_PATH = "market_data.db"
WINDOW_SIZE = 20
Z_SCORE_THRESHOLD = 3.0


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            price REAL NOT NULL,
            pct_change REAL NOT NULL,
            timestamp TEXT NOT NULL,
            is_anomaly INTEGER NOT NULL DEFAULT 0,
            z_score REAL
        )
    """)
    conn.commit()
    return conn


def detect_anomaly(history, pct_change):
    if len(history) < WINDOW_SIZE:
        return False, None

    mu = mean(history)
    sigma = stdev(history) if len(set(history)) > 1 else 0.0001

    z = (pct_change - mu) / sigma
    is_anomaly = abs(z) > Z_SCORE_THRESHOLD
    return is_anomaly, round(z, 3)


def run_pipeline(n_ticks=None, delay=0.1, verbose=True):
    conn = init_db()
    cur = conn.cursor()
    history = defaultdict(lambda: deque(maxlen=WINDOW_SIZE))

    for tick in stream(n=n_ticks, delay=delay):
        ticker = tick["ticker"]
        pct_change = tick["pct_change"]

        is_anomaly, z = detect_anomaly(list(history[ticker]), pct_change)

        cur.execute(
            """INSERT INTO ticks (ticker, price, pct_change, timestamp, is_anomaly, z_score)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (ticker, tick["price"], pct_change, tick["timestamp"], int(is_anomaly), z),
        )
        conn.commit()
        history[ticker].append(pct_change)

        if verbose:
            if is_anomaly:
                print(f"ANOMALY  {ticker:6s} price={tick['price']:>8} change={pct_change:+.2f}%  z={z}")
            else:
                print(f"   ok      {ticker:6s} price={tick['price']:>8} change={pct_change:+.2f}%")

    conn.close()


if __name__ == "__main__":
    run_pipeline(n_ticks=200, delay=0.05)