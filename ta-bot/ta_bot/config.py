import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TWELVEDATA_API_KEY = os.environ.get("TWELVEDATA_API_KEY", "")

# Binance kline intervals this bot accepts as a "timeframe" argument.
CRYPTO_TIMEFRAMES = {"1m", "5m", "15m", "30m", "1h", "4h", "1d"}

# twelvedata interval strings for forex pairs.
FOREX_TIMEFRAMES = {"1min", "5min", "15min", "30min", "1h", "4h", "1day"}

CANDLES_LOOKBACK = 200  # how many candles to pull per request
