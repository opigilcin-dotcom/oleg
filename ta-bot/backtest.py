"""Backtest the confluence signal against historical candles.

Usage:
    python backtest.py BTCUSDT 5m --market crypto --candles 500

Reports how often the signal's direction matched the next candle's direction.
This is a simple historical accuracy check, not a guarantee of future results:
past performance on one dataset does not predict future price movement.
"""

import argparse

from ta_bot import data_crypto, data_forex
from ta_bot.indicators import add_indicators, confluence_signal


def run_backtest(symbol: str, timeframe: str, market: str, candles: int) -> None:
    if market == "forex":
        df = data_forex.fetch_candles(symbol, timeframe, limit=candles)
    else:
        df = data_crypto.fetch_candles(symbol, timeframe, limit=candles)

    df_ind = add_indicators(df)

    correct = 0
    total = 0
    warmup = 60  # skip early rows before indicators have enough history

    for i in range(warmup, len(df_ind) - 1):
        window = df_ind.iloc[: i + 1]
        signal = confluence_signal(window)
        if signal["overall"] == "neutral":
            continue

        next_close = df_ind["close"].iloc[i + 1]
        this_close = df_ind["close"].iloc[i]
        actual_direction = "bullish" if next_close > this_close else "bearish"

        total += 1
        if signal["overall"] == actual_direction:
            correct += 1

    if total == 0:
        print("No non-neutral signals were generated in this window.")
        return

    accuracy = correct / total * 100
    print(f"{symbol} {timeframe} ({market}): {correct}/{total} correct ({accuracy:.1f}%)")
    print("Educational stat only — historical accuracy on this sample, not a forward-looking guarantee.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol")
    parser.add_argument("timeframe")
    parser.add_argument("--market", choices=["crypto", "forex"], default="crypto")
    parser.add_argument("--candles", type=int, default=500)
    args = parser.parse_args()

    run_backtest(args.symbol, args.timeframe, args.market, args.candles)
