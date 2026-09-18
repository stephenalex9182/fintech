import yfinance as yf
import pandas as pd
from typing import List, Dict

def analyze_multiple_assets(symbols: List[str], period: str = "1y") -> Dict:
    """
    Analyzes multiple assets and returns a correlation matrix and comparative performance.
    """
    if not symbols:
        return {"error": "No symbols provided"}

    # Download historical data
    data = yf.download(symbols, period=period, group_by='ticker')
    
    # Handle single symbol case vs multi symbol case for yfinance download
    if len(symbols) == 1:
        # If single symbol, yf.download returns a flat dataframe
        closes = pd.DataFrame({symbols[0]: data['Close']})
    else:
        # For multiple symbols, we need to extract the 'Close' column for each
        closes = pd.DataFrame()
        for symbol in symbols:
            if symbol in data and 'Close' in data[symbol]:
                closes[symbol] = data[symbol]['Close']
            elif 'Close' in data and isinstance(data.columns, pd.MultiIndex):
                # Another format yf might return
                closes[symbol] = data['Close'][symbol]
    
    # Drop any rows with NA that might mess up calculations
    closes.dropna(inplace=True)
    
    # Calculate daily returns
    returns = closes.pct_change().dropna()
    
    # Correlation matrix
    correlation = returns.corr().to_dict()
    
    # Calculate annualized return and volatility
    stats = {}
    for symbol in symbols:
        if symbol in returns.columns:
            annual_return = returns[symbol].mean() * 252
            annual_volatility = returns[symbol].std() * (252 ** 0.5)
            stats[symbol] = {
                "annual_return": annual_return,
                "annual_volatility": annual_volatility
            }
            
    return {
        "correlation_matrix": correlation,
        "performance_stats": stats
    }
