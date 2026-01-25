import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Make sure the project root is on sys.path so `src` can be imported during tests
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src import utils


def test_calculate_daily_returns():
    idx = pd.date_range('2020-01-01', periods=3, freq='D')
    prices = pd.DataFrame({'A': [100.0, 110.0, 121.0], 'B': [200.0, 220.0, 242.0]}, index=idx)
    returns = utils.calculate_daily_returns(prices)
    # Both series have consistent 10% returns
    assert np.allclose(returns['A'].values, [0.10, 0.10])
    assert np.allclose(returns['B'].values, [0.10, 0.10])


def test_calculate_sharpe_ratio_and_rolling_vol():
    # Create simple daily returns with small variance
    idx = pd.date_range('2020-01-01', periods=252, freq='B')
    series = pd.Series(0.001 + 0.001 * np.random.randn(len(idx)), index=idx)
    df = pd.DataFrame({'X': series})

    sharpe = utils.calculate_sharpe_ratio(df)
    assert 'X' in sharpe.index
    # Sharpe ratio should be a finite number
    assert np.isfinite(sharpe['X'])

    roll = utils.calculate_rolling_volatility(df, window=5)
    assert not roll.empty


def test_calculate_value_at_risk():
    returns = pd.Series([-0.05, -0.02, 0.01, 0.02, 0.03])
    var_95 = utils.calculate_value_at_risk(returns, confidence_level=0.95)
    # With these values the 5th percentile is approximately -0.05
    assert np.isclose(var_95, returns.quantile(0.05))
