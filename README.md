# Multi-Timeframe Market Forecasting & Trade Execution Bot

A Python research bot that fetches market data across multiple timeframes, builds
statistical price-prediction models, generates directional signals, and (optionally)
executes live orders on Binance Futures and MetaTrader 5 / Exness.

**Author:** Mahmoud Osama Anwar · Cairo, Egypt
**Status:** Research / learning project — actively under development.

> ⚠️ **Disclaimer:** This is an educational research project, not financial advice
> and not a production trading system. It can place real orders on live accounts.
> Run it only against a demo/testnet account. Trading carries real risk of loss.

---

## What it does

- Pulls OHLC candle data from **Binance Futures** (REST klines), **yfinance** (stocks),
  and **MetaTrader 5** (forex / commodities via Exness).
- Engineers features and fits regression models to forecast each candle's
  **High / Low / Close**, plus logistic / random-forest models for up/down direction.
- Scores predictions with a broad set of statistical metrics.
- Derives a **BUY / SELL** signal from the forecast and, when enabled, submits
  signed limit orders (Binance Futures over WebSocket) or market orders with
  stop-loss / take-profit (MetaTrader 5).
- Runs on a candle-aligned schedule (logic for 5- and 15-minute cycles).

## Tech stack

| Area | Tools |
|------|-------|
| Language | Python 3.x |
| Data / numeric | pandas, NumPy, SciPy |
| Modeling | scikit-learn (LinearRegression, LogisticRegression, RandomForestClassifier, RegressorChain), statsmodels |
| Market data | python-binance, yfinance, MetaTrader5 |
| Execution | Binance Futures WebSocket API (RSA-signed), MetaTrader5 `order_send` |
| Utilities | requests, websocket-client, cryptography, APScheduler |

## How it works

```
fetch candles ──> feature prep ──> fit models ──> predict H/L/C ──> derive signal
                                                                        │
                          schedule next run <── execute order (opt.) <──┘
```

1. **Data ingestion** — `get_data` / `get_stock_data` pull recent candles per timeframe.
2. **Modeling** — `predictions_test`, `some_other_factors`, and the logistic helpers
   fit models and produce point forecasts plus a binary directional signal.
3. **Evaluation** — metrics are collected per run (see below).
4. **Decision & execution** — `new_trading_behaviour` / `new_stock_bejaviour` compare
   the forecast to the last close and place an order if a threshold is met.
5. **Scheduling** — `do_trade_analysis` aligns the next evaluation to the candle clock.

## Evaluation metrics

MAE · MAPE (with zero-division handling) · MSE · RMSE · R² · Adjusted R² ·
Explained Variance · Median Absolute Error · Durbin–Watson (residual autocorrelation) ·
5-fold cross-validation MSE.

## Setup

```bash
git clone https://github.com/<your-username>/<repo>.git
cd <repo>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Credentials (never hard-code these)

All keys and passwords are read from environment variables. Create a `.env` file
(which is git-ignored) based on `.env.example`:

```bash
# .env  — DO NOT COMMIT
BINANCE_API_KEY=your_key_here
BINANCE_PRIVATE_KEY_PATH=/path/to/private_key.pem
MT5_LOGIN=12345678
MT5_PASSWORD=your_password
MT5_SERVER=Exness-MT5Trial
```

Make sure your `.gitignore` contains:

```
.env
*.pem
__pycache__/
*.csv
```

## Usage

```bash
python new_price_predictions.py
```

Edit the configuration block at the bottom of the script to set the symbol,
timeframe, quantity, and whether to target crypto (Binance) or a stock/forex
symbol (yfinance / MT5).

## Limitations & lessons learned

I'm keeping this section honest because the reasoning matters more than the result:

- **Predicting price levels is misleading.** The current models forecast a candle's
  High/Low/Close largely from the *same candle's Open*. Because intrabar OHLC values
  are highly correlated, this produces a very high R² that does **not** reflect real
  predictive power. The correct approach — which I'm migrating toward — is to predict
  **forward returns** (a stationary target) from **past-only** features.
- **Validation needs to be leak-free.** A simple chronological split isn't enough for
  time series; the roadmap is purged / walk-forward validation.
- **Costs decide everything.** Any apparent edge must survive spread, slippage, and
  commission. Net PnL after costs is the only metric that counts, and it isn't yet
  measured here.
- **Code needs refactoring.** The logic currently lives in one large script; splitting
  it into data / features / model / execution modules is in progress.

## Roadmap

- [ ] Reframe targets as forward returns with lagged, past-only features
- [ ] Leak-free (purged / walk-forward) validation
- [ ] Backtest with realistic transaction costs and a PnL report
- [ ] Refactor the monolith into modules + unit tests
- [ ] Configuration via file/CLI instead of in-code edits

## License

MIT
