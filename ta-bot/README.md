# TA Bot — учебный телеграм-бот с техническим анализом

Личный образовательный инструмент: считает индикаторы (RSI, MACD, EMA, Bollinger, Stochastic) по свечам крипты (Binance, публичный API) и форекса (twelvedata, бесплатный тариф) и присылает график + сводный сигнал прямо в Telegram.

**Это не финансовая рекомендация и не предсказание будущей цены.** Сигнал — это просто historical pattern-match по нескольким индикаторам на последней свече. Скрипт `backtest.py` честно показывает % угадываний на исторических данных — не завышенную гарантию.

## Установка

1. `pip install -r requirements.txt`
2. Скопируй `.env.example` в `.env` и заполни:
   - `TELEGRAM_BOT_TOKEN` — получи у [@BotFather](https://t.me/BotFather) в Telegram (команда `/newbot`).
   - `TWELVEDATA_API_KEY` — нужен только для форекса, бесплатный ключ на [twelvedata.com](https://twelvedata.com).
3. `python -m ta_bot.bot`

## Использование

В Telegram, в чате с ботом:
```
/analyze BTCUSDT 5m crypto
/analyze EUR/USD 15min forex
```

Бот пришлёт свечной график (EMA20/EMA50 наложены) и текст вида:
```
BTCUSDT (5m)
Last close: 67 812.30000
Confluence: BULLISH (3 bullish / 1 bearish of 4 indicators)

- RSI: bullish (RSI 28.4 (oversold))
- MACD: bullish (MACD above signal line)
- EMA: bullish (EMA20 above EMA50)
- Stochastic: bearish (%K 82.1 (overbought))
```

## Бэктест

```
python backtest.py BTCUSDT 5m --market crypto --candles 500
```
Прогоняет сигнал по истории и считает, как часто направление сигнала совпадало с направлением следующей свечи.

## Ограничения (честно)

- На коротких таймфреймах (1-5 мин) движение цены в основном шум — устойчивого предсказательного преимущества у стандартных индикаторов там нет, это подтверждено множеством академических бэктестов. Инструмент полезен для ОБУЧЕНИЯ (как индикаторы вообще ведут себя), не для реальной торговли.
- Данные TradingView напрямую не используются (у них нет публичного API для этого) — график рисуется через `mplfinance` на данных Binance/twelvedata, визуально похоже, но это не тот же источник.
- Besplatные тарифы twelvedata сильно лимитированы по количеству запросов в минуту.
