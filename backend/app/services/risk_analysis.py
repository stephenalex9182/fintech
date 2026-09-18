import yfinance as yf
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from .. import models

def calculate_portfolio_risk(portfolio_id: int, db: Session):
    """
    Calculates portfolio risk metrics (VaR, Volatility, Beta, Sharpe Ratio).
    """
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio or not portfolio.holdings:
        return None

    # Gather holdings
    holdings_dict = {h.symbol: h.shares for h in portfolio.holdings}
    symbols = list(holdings_dict.keys())

    # Download historical data (1 year for risk metrics)
    data = yf.download(symbols, period="1y", group_by='ticker')
    
    if len(symbols) == 1:
        closes = pd.DataFrame({symbols[0]: data['Close']})
    else:
        closes = pd.DataFrame()
        for symbol in symbols:
            if symbol in data and 'Close' in data[symbol]:
                closes[symbol] = data[symbol]['Close']
            elif 'Close' in data and isinstance(data.columns, pd.MultiIndex):
                closes[symbol] = data['Close'][symbol]

    # Fill forwards then backwards to handle missing data
    closes = closes.ffill().bfill()
    
    # Calculate daily returns
    returns = closes.pct_change().dropna()
    
    # Get latest prices to calculate weights
    latest_prices = closes.iloc[-1]
    portfolio_value = 0
    weights = {}
    for symbol, shares in holdings_dict.items():
        if symbol in latest_prices:
            value = shares * latest_prices[symbol]
            weights[symbol] = value
            portfolio_value += value
            
    if portfolio_value == 0:
        return None
        
    # Normalize weights
    for symbol in weights:
        weights[symbol] /= portfolio_value
        
    # Create weight array aligned with returns columns
    weight_array = np.array([weights.get(col, 0) for col in returns.columns])
    
    # Portfolio daily returns
    portfolio_returns = returns.dot(weight_array)
    
    # Metrics
    # 1. Total Returns (annualized)
    total_returns = portfolio_returns.mean() * 252
    
    # 2. Volatility (annualized)
    volatility = portfolio_returns.std() * np.sqrt(252)
    
    # 3. Sharpe Ratio (assuming 2% risk free rate)
    risk_free_rate = 0.02
    sharpe_ratio = (total_returns - risk_free_rate) / volatility if volatility != 0 else 0
    
    # 4. Value at Risk (VaR) 95% historical
    var_95 = np.percentile(portfolio_returns, 5) * portfolio_value
    
    # 5. Beta (approximation against equal weight portfolio if no benchmark provided)
    # Ideally against SPY, let's fetch SPY for Beta
    try:
        spy_data = yf.download("SPY", period="1y")['Close']
        spy_returns = spy_data.pct_change().dropna()
        # Align dates
        aligned_returns = pd.concat([portfolio_returns, spy_returns], axis=1).dropna()
        aligned_returns.columns = ['Portfolio', 'SPY']
        cov = aligned_returns.cov().iloc[0, 1]
        var = aligned_returns['SPY'].var()
        beta = cov / var if var != 0 else 1
    except Exception:
        beta = 1.0 # fallback

    return {
        "portfolio_id": portfolio_id,
        "portfolio_value": float(portfolio_value),
        "total_returns": float(total_returns),
        "volatility": float(volatility),
        "sharpe_ratio": float(sharpe_ratio),
        "value_at_risk_95": float(var_95),
        "beta": float(beta)
    }
