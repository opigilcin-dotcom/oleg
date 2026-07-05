"""Telegram bot: /analyze <symbol> <timeframe> [crypto|forex] -> chart + confluence signal.

Educational tool only. The signal is a historical indicator confluence
summary, not a prediction of future price movement or trading advice.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from ta_bot import data_crypto, data_forex
from ta_bot.chart import render_chart
from ta_bot.config import CRYPTO_TIMEFRAMES, FOREX_TIMEFRAMES, TELEGRAM_BOT_TOKEN
from ta_bot.indicators import add_indicators, confluence_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISCLAIMER = (
    "⚠️ Educational tool. This is a historical indicator pattern-match, "
    "not financial advice or a prediction of future price movement."
)

HELP_TEXT = (
    "/analyze <symbol> <timeframe> [crypto|forex]\n\n"
    "Examples:\n"
    "/analyze BTCUSDT 5m crypto\n"
    "/analyze EUR/USD 15min forex\n\n"
    f"Crypto timeframes: {', '.join(sorted(CRYPTO_TIMEFRAMES))}\n"
    f"Forex timeframes: {', '.join(sorted(FOREX_TIMEFRAMES))}"
)


def format_signal_text(symbol: str, timeframe: str, signal: dict) -> str:
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
    lines.append(DISCLAIMER)
    return "\n".join(lines)


async def cmd_start(message: Message) -> None:
    await message.answer(f"Hi! This bot does educational technical analysis.\n\n{HELP_TEXT}")


async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


async def cmd_analyze(message: Message) -> None:
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer(f"Usage:\n{HELP_TEXT}")
        return

    symbol = parts[1]
    timeframe = parts[2]
    market = parts[3].lower() if len(parts) > 3 else "crypto"

    try:
        if market == "forex":
            if timeframe not in FOREX_TIMEFRAMES:
                await message.answer(f"Unknown forex timeframe. Use one of: {', '.join(sorted(FOREX_TIMEFRAMES))}")
                return
            df = data_forex.fetch_candles(symbol, timeframe)
        else:
            if timeframe not in CRYPTO_TIMEFRAMES:
                await message.answer(f"Unknown crypto timeframe. Use one of: {', '.join(sorted(CRYPTO_TIMEFRAMES))}")
                return
            df = data_crypto.fetch_candles(symbol, timeframe)
    except Exception as exc:  # noqa: BLE001 - surface any data-fetch error to the user
        await message.answer(f"Couldn't fetch data for {symbol}: {exc}")
        return

    df_ind = add_indicators(df)
    signal = confluence_signal(df_ind)

    chart_buf = render_chart(df_ind.tail(100), title=f"{symbol} {timeframe}")
    photo = BufferedInputFile(chart_buf.read(), filename="chart.png")

    await message.answer_photo(photo, caption=format_signal_text(symbol, timeframe, signal))


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_analyze, Command("analyze"))
    return dp


async def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Put it in .env (get one from @BotFather).")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = build_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
