import yfinance as yf
import os
import time
from datetime import datetime


def _fetch_with_history_fallback(ticker, start_date, end_date):
    """Attempt to fetch data using yf.download, then fallback to Ticker.history.
    Also try chunked downloads by year if a full-range download fails.
    Returns a DataFrame or None.
    """
    # Try a single call first
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False, threads=False)
        if data is not None and not data.empty:
            return data
    except Exception:
        data = None

    # Fallback to Ticker.history
    try:
        tk = yf.Ticker(ticker)
        data = tk.history(start=start_date, end=end_date)
        if data is not None and not data.empty:
            return data
    except Exception:
        data = None

    # As a last resort, attempt chunked downloads by year to avoid timeouts
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        parts = []
        year = start_dt.year
        while year <= end_dt.year:
            chunk_start = datetime(year, 1, 1).strftime('%Y-%m-%d')
            chunk_end = datetime(year + 1, 1, 1).strftime('%Y-%m-%d')
            try:
                chunk = yf.download(ticker, start=chunk_start, end=chunk_end, progress=False, threads=False)
                if chunk is not None and not chunk.empty:
                    parts.append(chunk)
            except Exception:
                pass
            year += 1
        if parts:
            full = parts[0].append(parts[1:]) if len(parts) > 1 else parts[0]
            return full
    except Exception:
        pass

    return None


def fetch_and_save_yfinance_data(tickers, start_date, end_date, max_retries=4, backoff=5):
    """
    Fetches historical financial data for a list of tickers using yfinance
    and saves the raw data to the 'data/raw/' directory.

    Implements retry logic and multiple fallbacks to improve robustness
    against transient network errors and API glitches.
    """
    print(f"Starting sequential download for {tickers}...")

    # Create directory if it doesn't exist
    if not os.path.exists('data/raw'):
        os.makedirs('data/raw')
        print("Created directory: data/raw/")

    for ticker in tickers:
        print(f"--- Downloading data for {ticker} from {start_date} to {end_date} ---")
        attempt = 0
        success = False
        last_err = None
        while attempt < max_retries and not success:
            attempt += 1
            try:
                data = _fetch_with_history_fallback(ticker, start_date, end_date)
                if data is None or data.empty:
                    last_err = f"No data fetched (attempt {attempt})"
                    print(last_err)
                    time.sleep(backoff * attempt)
                    continue

                output_path = f'data/raw/{ticker.lower()}_raw.csv'
                data.to_csv(output_path)
                print(f"Successfully saved raw data for {ticker} to {output_path}")
                success = True
            except Exception as e:
                last_err = str(e)
                print(f"Attempt {attempt} failed for {ticker}: {e}")
                time.sleep(backoff * attempt)

        if not success:
            print(f"Failed to fetch data for {ticker} after {max_retries} attempts. Last error: {last_err}")

    print("\nAll downloads complete.")


if __name__ == '__main__':
    TICKERS = ['TSLA', 'SPY', 'BND']
    # Use the project-specified date range
    START_DATE = '2015-01-01'
    END_DATE = '2026-01-15'

    fetch_and_save_yfinance_data(TICKERS, START_DATE, END_DATE)
import yfinance as yf
import os

def fetch_and_save_yfinance_data(tickers, start_date, end_date):
    """
    Fetches historical financial data for a list of tickers using yfinance
    and saves the raw data to the 'data/raw/' directory. This version
    downloads tickers sequentially to avoid database locking errors.
    
    This script is intended to be run once from the command line.
    """
    print(f"Starting sequential download for {tickers}...")

    # Create directory if it doesn't exist
    if not os.path.exists('data/raw'):
        os.makedirs('data/raw')
        print("Created directory: data/raw/")

    for ticker in tickers:
        print(f"--- Downloading data for {ticker} from {start_date} to {end_date} ---")
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if data.empty:
                print(f"No data fetched for {ticker}. Skipping.")
                continue

            output_path = f'data/raw/{ticker.lower()}_raw.csv'
            data.to_csv(output_path)
            print(f"Successfully saved raw data for {ticker} to {output_path}")
        except Exception as e:
            print(f"An error occurred while fetching data for {ticker}: {e}")
    
    print("\nAll downloads complete.")

if __name__ == '__main__':
    TICKERS = ['TSLA', 'SPY', 'BND']
    # Use the project-specified date range
    START_DATE = '2015-01-01'
    END_DATE = '2026-01-15'

    fetch_and_save_yfinance_data(TICKERS, START_DATE, END_DATE)