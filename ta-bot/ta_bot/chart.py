"""Render a candlestick chart with EMA overlays to a PNG, for sending via Telegram."""

import io

import mplfinance as mpf
import pandas as pd


def render_chart(df_with_indicators: pd.DataFrame, title: str) -> io.BytesIO:
    plot_df = df_with_indicators[["open", "high", "low", "close", "volume"]].copy()

    addplots = []
    if "ema20" in df_with_indicators.columns:
        addplots.append(mpf.make_addplot(df_with_indicators["ema20"], color="orange", width=1.0))
    if "ema50" in df_with_indicators.columns:
        addplots.append(mpf.make_addplot(df_with_indicators["ema50"], color="blue", width=1.0))

    buf = io.BytesIO()
    mpf.plot(
        plot_df,
        type="candle",
        style="charles",
        title=title,
        volume=True,
        addplot=addplots if addplots else None,
        savefig=dict(fname=buf, dpi=150, bbox_inches="tight"),
    )
    buf.seek(0)
    return buf
