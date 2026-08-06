import random
import time
import json
from datetime import datetime

TICKERS = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]
prices = {t: random.uniform(100, 500) for t in TICKERS}


def generate_tick():
    ticker = random.choice(TICKERS)
    current_price = prices[ticker]
    pct_change = random.gauss(0, 0.002)

    if random.random() < 0.05:
        shock = random.choice([-1, 1]) * random.uniform(0.03, 0.08)
        pct_change += shock

    new_price = round(current_price * (1 + pct_change), 2)
    prices[ticker] = new_price

    return {
        "ticker": ticker,
        "price": new_price,
        "timestamp": datetime.utcnow().isoformat(),
        "pct_change": round(pct_change * 100, 4),
    }


def stream(n=None, delay=0.5):
    count = 0
    while n is None or count < n:
        tick = generate_tick()
        yield tick
        count += 1
        time.sleep(delay)


if __name__ == "__main__":
    for tick in stream(n=10, delay=0.1):
        print(json.dumps(tick))