"""Telegram bot: pick a symbol and timeframe from buttons -> chart + confluence signal.

Educational tool only. The signal is a historical indicator confluence
summary, not a prediction of future price movement or trading advice.
A power-user text command (/analyze) is also available.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from ta_bot import data_crypto, data_forex
from ta_bot.chart import render_chart
from ta_bot.config import CRYPTO_TIMEFRAMES, FOREX_TIMEFRAMES, TELEGRAM_BOT_TOKEN
from ta_bot.indicators import add_indicators, confluence_signal, historical_accuracy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISCLAIMER = (
    "⚠️ Educational tool. This is a historical indicator pattern-match, "
    "not financial advice or a prediction of future price movement."
)

HELP_TEXT = (
    "Tap a symbol below, or use the text command:\n"
    "/analyze <symbol> <timeframe> [crypto|forex]\n\n"
    "Examples:\n"
    "/analyze BTCUSDT 5m crypto\n"
    "/analyze EUR/USD 15min forex"
)

# Small, fixed lists keep the button flow simple — no OTC pairs, no expiry timers.
CRYPTO_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
FOREX_SYMBOLS = ["EUR/USD", "GBP/USD", "USD/JPY"]
CRYPTO_TF_CHOICES = ["5m", "15m", "1h"]
FOREX_TF_CHOICES = ["15min", "1h", "1day"]


def symbol_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"₿ {s}", callback_data=f"sym|crypto|{s}") for s in CRYPTO_SYMBOLS],
        [InlineKeyboardButton(text=f"💱 {s}", callback_data=f"sym|forex|{s}") for s in FOREX_SYMBOLS],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def timeframe_keyboard(market: str, symbol: str) -> InlineKeyboardMarkup:
    choices = CRYPTO_TF_CHOICES if market == "crypto" else FOREX_TF_CHOICES
    row = [InlineKeyboardButton(text=tf, callback_data=f"tf|{market}|{symbol}|{tf}") for tf in choices]
    return InlineKeyboardMarkup(inline_keyboard=[row])


def format_signal_text(symbol: str, timeframe: str, signal: dict, history: dict) -> str:
    lines = [
        f"<b>{symbol}</b> ({timeframe})",
        f"Last close: {signal['last_close']:.5f}",
        f"Confluence: <b>{signal['overall'].upper()}</b> "
        f"({signal['bullish_votes']} bullish / {signal['bearish_votes']} bearish "
        f"of {signal['total_indicators']} indicators)",
        "",
    ]
    for name, direction, detail in signal["details"]:
        lines.append(f"- {name}: {direction} ({detail})")
    lines.append("")
    if history["total"] > 0:
        lines.append(
            f"Historical accuracy of this signal on {symbol} {timeframe} "
            f"over the last {history['total'] + 60} candles: "
            f"{history['accuracy_pct']:.1f}% ({history['correct']}/{history['total']})"
        )
        lines.append("(Backward-looking hit rate on this sample — not a forward-looking probability.)")
        lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


async def run_analysis(symbol: str, timeframe: str, market: str):
    """Fetch candles, compute the signal, and render the chart. Returns (photo_bytes, caption)."""
    if market == "forex":
        df = data_forex.fetch_candles(symbol, timeframe)
    else:
        df = data_crypto.fetch_candles(symbol, timeframe)

    df_ind = add_indicators(df)
    signal = confluence_signal(df_ind)
    history = historical_accuracy(df_ind)

    chart_buf = render_chart(df_ind.tail(100), title=f"{symbol} {timeframe}")
    caption = format_signal_text(symbol, timeframe, signal, history)
    return chart_buf.read(), caption


async def cmd_start(message: Message) -> None:
    await message.answer(
        f"Hi! This bot does educational technical analysis.\n\nPick a symbol:\n\n{HELP_TEXT}",
        reply_markup=symbol_keyboard(),
    )


async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=symbol_keyboard())


async def on_symbol_chosen(callback: CallbackQuery) -> None:
    _, market, symbol = callback.data.split("|")
    await callback.message.edit_text(
        f"{symbol} — pick a timeframe:",
        reply_markup=timeframe_keyboard(market, symbol),
    )
    await callback.answer()


async def on_timeframe_chosen(callback: CallbackQuery) -> None:
    _, market, symbol, timeframe = callback.data.split("|")
    await callback.answer("Crunching the numbers...")
    await callback.message.edit_text(f"Analyzing {symbol} ({timeframe})...")

    try:
        photo_bytes, caption = await run_analysis(symbol, timeframe, market)
    except Exception as exc:  # noqa: BLE001 - surface any data-fetch error to the user
        await callback.message.answer(f"Couldn't fetch data for {symbol}: {exc}")
        return

    photo = BufferedInputFile(photo_bytes, filename="chart.png")
    await callback.message.answer_photo(photo, caption=caption)


async def cmd_analyze(message: Message) -> None:
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer(f"Usage:\n{HELP_TEXT}", reply_markup=symbol_keyboard())
        return

    symbol = parts[1]
    timeframe = parts[2]
    market = parts[3].lower() if len(parts) > 3 else "crypto"

    valid_timeframes = FOREX_TIMEFRAMES if market == "forex" else CRYPTO_TIMEFRAMES
    if timeframe not in valid_timeframes:
        await message.answer(f"Unknown {market} timeframe. Use one of: {', '.join(sorted(valid_timeframes))}")
        return

    try:
        photo_bytes, caption = await run_analysis(symbol, timeframe, market)
    except Exception as exc:  # noqa: BLE001 - surface any data-fetch error to the user
        await message.answer(f"Couldn't fetch data for {symbol}: {exc}")
        return

    photo = BufferedInputFile(photo_bytes, filename="chart.png")
    await message.answer_photo(photo, caption=caption)


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_analyze, Command("analyze"))
    dp.callback_query.register(on_symbol_chosen, F.data.startswith("sym|"))
    dp.callback_query.register(on_timeframe_chosen, F.data.startswith("tf|"))
    return dp


async def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Put it in .env (get one from @BotFather).")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = build_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
