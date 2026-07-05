"""Fetch OHLC candles for forex pairs via the twelvedata API (free tier, rate-limited)."""

import pandas as pd
from twelvedata import TDClient

from ta_bot.config import CANDLES_LOOKBACK, TWELVEDATA_API_KEY


def fetch_candles(symbol: str, interval: str, limit: int = CANDLES_LOOKBACK) -> pd.DataFrame:
    """Return a DataFrame of OHLC candles for a forex pair, e.g. EUR/USD."""
    if not TWELVEDATA_API_KEY:
        raise RuntimeError(
            "TWELVEDATA_API_KEY is not set. Get a free key at twelvedata.com and put it in .env"
        )
    td = TDClient(apikey=TWELVEDATA_API_KEY)
    ts = td.time_series(symbol=symbol.upper(), interval=interval, outputsize=limit).as_pandas()
    ts = ts.rename(columns={"open": "open", "high": "high", "low": "low", "close": "close"})
    ts = ts.sort_index()
    if "volume" not in ts.columns:
        ts["volume"] = 0.0
    return ts[["open", "high", "low", "close", "volume"]]
