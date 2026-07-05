"""Backtest the confluence signal against historical candles.

Usage:
    python backtest.py BTCUSDT 5m --market crypto --candles 500

Reports how often the signal's direction matched the next candle's direction.
This is a simple historical accuracy check, not a guarantee of future results:
past performance on one dataset does not predict future price movement.
"""

import argparse

from ta_bot import data_crypto, data_forex
from ta_bot.indicators import add_indicators, historical_accuracy


def run_backtest(symbol: str, timeframe: str, market: str, candles: int) -> None:
    if market == "forex":
        df = data_forex.fetch_candles(symbol, timeframe, limit=candles)
    else:
        df = data_crypto.fetch_candles(symbol, timeframe, limit=candles)

    df_ind = add_indicators(df)
    result = historical_accuracy(df_ind)

    if result["total"] == 0:
        print("No non-neutral signals were generated in this window.")
        return

    print(f"{symbol} {timeframe} ({market}): {result['correct']}/{result['total']} correct ({result['accuracy_pct']:.1f}%)")
    print("Educational stat only — historical accuracy on this sample, not a forward-looking guarantee.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol")
    parser.add_argument("timeframe")
    parser.add_argument("--market", choices=["crypto", "forex"], default="crypto")
    parser.add_argument("--candles", type=int, default=500)
    args = parser.parse_args()

    run_backtest(args.symbol, args.timeframe, args.market, args.candles)
