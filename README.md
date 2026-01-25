# 📈 Time Series Forecasting & Portfolio Optimization

![alt text](https://img.shields.io/badge/python-3.10+-blue.svg)
![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

An end-to-end quantitative analysis project to enhance portfolio management strategies for Guide Me in Finance (GMF) Investments. This repository documents the process of fetching financial data, developing predictive time series models, and constructing an optimal investment portfolio based on Modern Portfolio Theory (MPT).

---

## 🎯 Project Overview

As a Financial Analyst at GMF Investments, the objective is to leverage data-driven insights to optimize client portfolios. This project utilizes historical financial data for three key assets with distinct risk profiles:

- **Tesla (TSLA):** High-growth, high-volatility stock.
- **S\&P 500 ETF (SPY):** Diversified, moderate-risk market benchmark.
- **Vanguard Total Bond Market ETF (BND):** Stable, low-risk bond fund.

By forecasting future trends and understanding asset correlations, we aim to build a portfolio that maximizes returns for a given level of risk, grounded in proven financial theories.

---

## ✨ Key Features

- 📦 **Automated Data Ingestion** – Fetches over a decade of financial data using the `yfinance` API.
- 📊 **In-Depth EDA** – Analysis of price trends, volatility, return distributions, and risk metrics.
- 🤖 **Advanced Time Series Forecasting** – ARIMA and LSTM models for predictive analysis.
- ⚙️ **Portfolio Optimization (MPT)** – Efficient Frontier, Maximum Sharpe Ratio, and Minimum Volatility portfolios.
- 🧪 **Backtesting** – Compare optimized portfolio performance with a benchmark strategy.

---

## 🚀 Project Roadmap

### ✅ Completed: Task 1 – Preprocessing & Exploration

- Ingested, cleaned, and analyzed historical data (2015-01-01 – 2026-01-15).
- Key EDA insights:
  - TSLA shows explosive growth and volatility.
  - SPY is stable, upward-trending.
  - BND is low volatility, portfolio stabilizer.
  - VaR (95%) of equally weighted portfolio: **-3.12%**.

### ➡️ Next Steps:

#### 🧠 Task 2: Time Series Forecasting

- Build ARIMA and LSTM models for TSLA price forecasting.
- Evaluate with RMSE & MAE.

#### 🔮 Task 3: Forecast Future Market Trends

- Use best-performing model for 6–12 month forecast.
- Include confidence intervals.

#### 🎯 Task 4: Portfolio Optimization

- Combine TSLA forecast returns with historical SPY & BND.
- Use covariance matrix + MPT for Efficient Frontier.
- Identify max Sharpe ratio and min volatility portfolios.

#### 📜 Task 5: Backtesting

- Compare optimized portfolio vs 60/40 SPY/BND benchmark.
- Assess performance improvement.

---

## 🔍 EDA Highlights

- **Price Trends & Volatility:**
  TSLA volatility spikes (esp. 2020–2021) are much higher than SPY and BND.

- **Return Distributions:**
  All assets have fat-tailed return distributions.
  TSLA’s is widest (high risk), BND’s is narrowest (low risk).

- **Value at Risk (VaR):**
  95% VaR of -3.12% for equally weighted portfolio.

---

## 🗂 Project Structure

```
gmf-portfolio-optimization-analysis/
│
├── .github/              # GitHub Actions for CI/CD
├── data/
│   └── raw/              # Raw data from yfinance
│
├── notebooks/            # Jupyter Notebooks for analysis
│   └── 1.0-data-exploration.ipynb
│
├── reports/              # Final reports & figures
│
├── src/                  # Source code
│   ├── data_ingestion.py # Script to fetch data
│   └── utils.py          # Helper functions
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠 Setup & Installation

1. **Clone Repository**

```bash
git clone https://github.com/Bekamgenene/Portfolio-Management-Optimization.git
cd Portfolio-Management-Optimization
```

2. **Create Virtual Environment**

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\Activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

**Step 1 – Data Ingestion:**

```bash
python scripts/run_ingest.py
```

This populates `data/raw/` with CSV files for TSLA, SPY, and BND covering 2015-01-01 to 2026-01-15.

**Step 2 – Run Analysis:**

```bash
jupyter lab
```

Open `notebooks/1.0-data-exploration.ipynb` and run cells.

---

## 💻 Technologies Used

- **Python 3.10+**
- **Libraries:**
  - Data: `pandas`, `numpy`, `yfinance`
  - Visualization: `matplotlib`, `seaborn`
  - Time Series: `statsmodels`, `pmdarima`, `tensorflow`
  - Optimization: `PyPortfolioOpt`
  - Utilities: `scikit-learn`
