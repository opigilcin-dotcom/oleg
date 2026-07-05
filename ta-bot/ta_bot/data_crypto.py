"""Fetch OHLCV candles from Binance's public REST API (no API key needed for market data)."""

import pandas as pd
from binance.client import Client

from ta_bot.config import CANDLES_LOOKBACK

# Public market data endpoints don't require credentials.
_client = Client(api_key="", api_secret="")


def fetch_candles(symbol: str, interval: str, limit: int = CANDLES_LOOKBACK) -> pd.DataFrame:
    """Return a DataFrame of OHLCV candles for a Binance spot symbol, e.g. BTCUSDT."""
    raw = _client.get_klines(symbol=symbol.upper(), interval=interval, limit=limit)
    df = pd.DataFrame(
        raw,
        columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore",
        ],
    )
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = df[col].astype(float)
    df = df.set_index("open_time")
    return df[["open", "high", "low", "close", "volume"]]
