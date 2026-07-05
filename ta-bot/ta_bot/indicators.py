"""Compute technical indicators and turn them into a simple confluence signal.

This is an educational heuristic, not a prediction of future price movement.
Short-timeframe price direction is dominated by noise; treat any signal here
as a labeled historical pattern-match, not a guarantee.
"""

import pandas as pd
import pandas_ta as ta


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["rsi14"] = ta.rsi(out["close"], length=14)
    macd = ta.macd(out["close"])
    out = out.join(macd)
    out["ema20"] = ta.ema(out["close"], length=20)
    out["ema50"] = ta.ema(out["close"], length=50)
    bb = ta.bbands(out["close"], length=20)
    out = out.join(bb)
    stoch = ta.stoch(out["high"], out["low"], out["close"])
    out = out.join(stoch)
    return out


def confluence_signal(df_with_indicators: pd.DataFrame) -> dict:
    """Score the latest candle across several indicators. Returns a summary dict."""
    last = df_with_indicators.iloc[-1]
    votes = []

    if pd.notna(last.get("rsi14")):
        if last["rsi14"] < 30:
            votes.append(("RSI", "bullish", f"RSI {last['rsi14']:.1f} (oversold)"))
        elif last["rsi14"] > 70:
            votes.append(("RSI", "bearish", f"RSI {last['rsi14']:.1f} (overbought)"))
        else:
            votes.append(("RSI", "neutral", f"RSI {last['rsi14']:.1f}"))

    macd_col = next((c for c in df_with_indicators.columns if c.startswith("MACD_")), None)
    signal_col = next((c for c in df_with_indicators.columns if c.startswith("MACDs_")), None)
    if macd_col and signal_col and pd.notna(last.get(macd_col)) and pd.notna(last.get(signal_col)):
        if last[macd_col] > last[signal_col]:
            votes.append(("MACD", "bullish", "MACD above signal line"))
        else:
            votes.append(("MACD", "bearish", "MACD below signal line"))

    if pd.notna(last.get("ema20")) and pd.notna(last.get("ema50")):
        if last["ema20"] > last["ema50"]:
            votes.append(("EMA", "bullish", "EMA20 above EMA50"))
        else:
            votes.append(("EMA", "bearish", "EMA20 below EMA50"))

    stoch_k_col = next((c for c in df_with_indicators.columns if c.startswith("STOCHk_")), None)
    if stoch_k_col and pd.notna(last.get(stoch_k_col)):
        k = last[stoch_k_col]
        if k < 20:
            votes.append(("Stochastic", "bullish", f"%K {k:.1f} (oversold)"))
        elif k > 80:
            votes.append(("Stochastic", "bearish", f"%K {k:.1f} (overbought)"))
        else:
            votes.append(("Stochastic", "neutral", f"%K {k:.1f}"))

    bullish = sum(1 for _, v, _ in votes if v == "bullish")
    bearish = sum(1 for _, v, _ in votes if v == "bearish")

    if bullish > bearish:
        overall = "bullish"
    elif bearish > bullish:
        overall = "bearish"
    else:
        overall = "neutral"

    return {
        "overall": overall,
        "bullish_votes": bullish,
        "bearish_votes": bearish,
        "total_indicators": len(votes),
        "details": votes,
        "last_close": last["close"],
    }
