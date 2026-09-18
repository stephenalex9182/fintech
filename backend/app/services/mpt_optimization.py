import yfinance as yf
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import List

def optimize_portfolio(symbols: List[str], risk_free_rate: float = 0.02) -> dict:
    """
    Optimizes portfolio weights to maximize the Sharpe Ratio using Modern Portfolio Theory.
    """
    if len(symbols) < 2:
        return {"error": "Need at least 2 symbols to optimize."}
        
    data = yf.download(symbols, period="2y", group_by='ticker')
    
    closes = pd.DataFrame()
    for symbol in symbols:
        if symbol in data and 'Close' in data[symbol]:
            closes[symbol] = data[symbol]['Close']
        elif 'Close' in data and isinstance(data.columns, pd.MultiIndex):
            closes[symbol] = data['Close'][symbol]
            
    closes = closes.ffill().bfill()
    returns = closes.pct_change().dropna()
    
    # Expected Returns and Covariance
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    num_assets = len(symbols)
    
    # Define optimization functions
    def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights)
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return std, returns
        
    def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
        p_var, p_ret = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        return - (p_ret - risk_free_rate) / p_var

    # Constraints and bounds
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    
    # Initial guess
    initial_weights = num_assets * [1. / num_assets,]
    
    result = minimize(neg_sharpe_ratio, initial_weights, args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
                        
    if not result.success:
        return {"error": "Optimization failed"}
        
    optimized_weights = result.x
    opt_vol, opt_ret = portfolio_annualised_performance(optimized_weights, mean_returns, cov_matrix)
    opt_sharpe = (opt_ret - risk_free_rate) / opt_vol
    
    weights_dict = {symbols[i]: float(optimized_weights[i]) for i in range(num_assets)}
    
    return {
        "optimal_weights": weights_dict,
        "expected_return": float(opt_ret),
        "expected_volatility": float(opt_vol),
        "sharpe_ratio": float(opt_sharpe)
    }
