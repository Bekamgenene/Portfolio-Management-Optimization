import pandas as pd
import numpy as np
import os
try:
    import yfinance as yf
except Exception:
    yf = None

def load_and_combine_adj_close(tickers):
    """
    Loads raw data for a list of tickers from the 'data/raw/' directory,
    extracts the appropriate closing price, and combines them into a single DataFrame.

    This version intelligently searches for 'adj close' first, then falls back
    to 'close' if the former is not available.
    """
    adj_close_list = []
    for ticker in tickers:
        file_path = f'data/raw/{ticker.lower()}_raw.csv'
        try:
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
            df.columns = [col.lower() for col in df.columns]
        except FileNotFoundError:
            # Attempt to download missing raw file if yfinance is available
            print(f"Raw data file for {ticker} not found at {file_path}. Trying to download via yfinance...")
            if yf is None:
                print("yfinance is not installed; please run the ingestion script or install yfinance.")
                return pd.DataFrame()
            # ensure data/raw exists
            os.makedirs('data/raw', exist_ok=True)
            try:
                downloaded = yf.download(ticker, start='2015-01-01', end='2026-01-15', progress=False, threads=False)
                if downloaded is None or downloaded.empty:
                    print(f"yfinance returned no data for {ticker}.")
                    return pd.DataFrame()
                downloaded.to_csv(file_path)
                df = downloaded
                df.columns = [col.lower() for col in df.columns]
                print(f"Downloaded and saved raw data for {ticker} to {file_path}")
            except Exception as e:
                print(f"Failed to download data for {ticker}: {e}")
                return pd.DataFrame()

        # --- FIX: Intelligently find the correct price column ---
        price_col_to_use = None
        if 'adj close' in df.columns:
            price_col_to_use = 'adj close'
        elif 'close' in df.columns:
            price_col_to_use = 'close'

        if price_col_to_use:
            adj_close_df = df[[price_col_to_use]].rename(columns={price_col_to_use: ticker})
            adj_close_list.append(adj_close_df)
        else:
            print(f"Error: Neither 'Adj Close' nor 'Close' column found in {file_path}.")
            print(f"Available columns are: {df.columns.tolist()}")
            continue
    
    if not adj_close_list:
        print("Could not load any data. Please check the file paths and column names.")
        return pd.DataFrame()

    combined_df = pd.concat(adj_close_list, axis=1)
    
    combined_df.ffill(inplace=True)
    combined_df.dropna(inplace=True)
    
    return combined_df

def calculate_daily_returns(prices_df):
    """Calculates the daily percentage change in prices."""
    return prices_df.pct_change().dropna()

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.0):
    """Calculates the annualized Sharpe Ratio for a set of daily returns."""
    mean_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()
    annualized_return = mean_daily_return * 252
    annualized_volatility = std_daily_return * np.sqrt(252)
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    return sharpe_ratio

def calculate_value_at_risk(daily_returns, confidence_level=0.95):
    """Calculates the Value at Risk (VaR) at a given confidence level."""
    return daily_returns.quantile(1 - confidence_level)

def calculate_rolling_volatility(daily_returns_df, window=30):
    """Calculates the rolling standard deviation of daily returns."""
    return daily_returns_df.rolling(window=window).std().dropna()