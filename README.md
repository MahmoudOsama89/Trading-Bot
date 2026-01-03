# Financial Market Forecasting with Machine Learning

A comprehensive multi-timeframe price prediction system using scikit-learn for cryptocurrency and stock markets.

## 🎯 Project Overview

This project implements a production-ready machine learning system that forecasts financial market prices across multiple timeframes (1-minute to 1-month intervals) using ensemble methods and statistical modeling.

**Author:** Mahmoud Osama Anwar  
**Status:** Active Development  
**Use Case:** Financial forecasting, algorithmic trading research

---

## 🔧 Technical Implementation

### Machine Learning Approach

**Primary Models:**
- **Linear Regression** for continuous OHLC (Open, High, Low, Close) price prediction
- **Logistic Regression** for binary directional signals (up/down movement)
- **Random Forest Classifier** for enhanced signal generation with class balancing

**Key Features:**
- Multi-output prediction using `RegressorChain` methodology
- Time series-specific train/test splitting (70/30) to prevent data leakage
- K-fold cross-validation (5-fold) for robust performance estimation
- Real-time data processing with API integration

### Feature Engineering

Engineered 15+ predictive features from raw market data:

**Returns-based Features:**
- Multi-period returns (1h, 2h, 4h, 8h intervals)
- Percentage change calculations

**Volatility Features:**
- Rolling standard deviation (10-period, 20-period windows)
- Volatility ratios

**Technical Indicators:**
- Price-to-moving-average distances
- Rate of change indicators

**Statistical Features:**
- Candlestick body ratios
- Volume metrics

### Model Evaluation Framework

Comprehensive evaluation using 10+ statistical metrics:

| Metric | Purpose |
|--------|---------|
| MAE (Mean Absolute Error) | Average prediction error magnitude |
| MAPE (Mean Absolute Percentage Error) | Percentage-based error measurement |
| RMSE (Root Mean Squared Error) | Penalizes large errors |
| R² Score | Proportion of variance explained |
| Adjusted R² | R² adjusted for number of features |
| Durbin-Watson | Tests for autocorrelation in residuals |
| Explained Variance Score | Variance captured by model |
| Median Absolute Error | Robust to outliers |

**Probability Scoring System:**
- Closest Probability: Rolling window comparison
- Interval Probability: Normal distribution modeling using `scipy.stats.norm`

---

## 📊 Results

**Model Performance (Example - Update with your actual results):**
- Test Set R²: 0.XX
- Test Set MAE: $X.XX
- Classification Accuracy: XX%
- MAPE: X.X%

**Key Findings:**
- Multi-timeframe approach provides robust predictions
- Feature engineering significantly improved model performance
- Proper time-series validation critical for avoiding overfitting

---

## 🛠️ Technical Stack

**Core Technologies:**
```
Python 3.x
scikit-learn (RandomForestClassifier, LinearRegression, LogisticRegression)
pandas (Data manipulation)
NumPy (Numerical computing)
scipy (Statistical functions)
```

**Data Sources:**
- Binance Futures API (Cryptocurrency markets)
- yFinance API (Stock markets)
- MetaTrader5 API (Forex & Commodities)

**Key Libraries:**
```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import RegressorChain
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
```

---

## 🚀 Key Features

### 1. Multi-Timeframe Support
Supports 13 different timeframes:
- High frequency: 1-second, 1-minute, 3-minute, 5-minute
- Intraday: 15-minute, 30-minute, 1-hour, 4-hour
- Daily and above: 1-day, 3-day, 1-week, 1-month

### 2. Real-time Data Processing
- WebSocket integration for live data streaming
- Automated feature calculation pipeline
- Continuous prediction updates

### 3. Statistical Validation
- Time-series aware train/test splitting
- Cross-validation for robust performance estimation
- Comprehensive residual analysis

### 4. Automated Reporting
- CSV export with predictions and confidence metrics
- Statistical summaries (mean, median, std, min/max)
- Timestamp-based file organization

---

## 📁 Project Structure

```
financial-ml-forecasting/
├── src/
│   ├── predictor.py              # Main prediction engine
│   ├── feature_engineering.py    # Feature creation functions
│   └── model_evaluation.py       # Evaluation metrics
├── data/
│   └── sample_predictions.csv    # Example output
├── notebooks/
│   └── exploratory_analysis.ipynb
├── requirements.txt
└── README.md
```

---

## 🔬 Methodology

### Data Preprocessing
1. Time-series data fetching from multiple sources
2. Feature engineering pipeline
3. Handling missing values and outliers
4. Train/test temporal splitting (maintains chronological order)

### Model Training
1. Sequential train/test split (70% train, 30% test)
2. StandardScaler normalization
3. RegressorChain for multi-output predictions
4. Model fitting with cross-validation

### Prediction & Validation
1. Generate predictions on test set
2. Calculate comprehensive evaluation metrics
3. Compute confidence scores using statistical distributions
4. Export results with timestamp

---

## 💡 Innovations

**Custom MAPE Calculation:**
Handles zero-value edge cases in percentage error calculation:
```python
def calculate_mape(y_true, y_pred):
    non_zero_indices = y_true != 0
    return np.mean(np.abs((y_true[non_zero_indices] - y_pred[non_zero_indices]) 
                           / y_true[non_zero_indices])) * 100
```

**Bias Correction:**
Implements mean residual analysis for systematic bias correction:
```python
mean_error = np.mean(y_pred - y_test)
predictions_corrected = predictions - mean_error
```

**Probability Confidence Metrics:**
Uses normal distribution to quantify prediction uncertainty:
```python
from scipy.stats import norm
prob_interval = norm.cdf(actual + window, loc=mean, scale=std) - \
                norm.cdf(actual - window, loc=mean, scale=std)
```

---

## 📈 Future Enhancements

- [ ] Implement LSTM/GRU for sequential modeling
- [ ] Add XGBoost for gradient boosting comparison
- [ ] Hyperparameter optimization using GridSearchCV
- [ ] Feature importance visualization
- [ ] Interactive prediction dashboard
- [ ] Backtesting framework
- [ ] Model ensemble strategies

---

## 🎓 Learning Outcomes

This project demonstrates:
- End-to-end ML pipeline development
- Time series forecasting best practices
- Feature engineering for financial data
- Model evaluation and validation
- Production-ready code structure
- Real-time data processing

---

## 📫 Contact

**Mahmoud Osama Anwar**  
📧 Mahmoud.ossama89@gmail.com  
🔗 LinkedIn: [Your LinkedIn]  
📍 Cairo, Egypt

Open to remote Data Science opportunities globally.

---

## ⚖️ Disclaimer

This project is for educational and research purposes only. Not financial advice. Always conduct your own research before making investment decisions.

---

## 📝 License

MIT License - Feel free to use this code for learning and development purposes.

---

*Built with passion for data science and continuous learning* 🚀# Trading-Bot
Trading bot using python
