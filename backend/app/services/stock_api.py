import yfinance as yf
import pandas as pd
from fastapi import HTTPException
from ..database import cache_get, cache_set

def get_stock_data(symbol: str, period: str = "1mo") -> dict:
    """Fetch stock data using yfinance with Redis caching."""
    cache_key = f"stock:{symbol}:{period}"
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return cached_data

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="Stock data not found")
        
        # Convert to dictionary and handle timestamps
        hist.index = hist.index.strftime('%Y-%m-%d')
        data = hist.to_dict(orient='index')
        
        # Add basic info
        info = ticker.info
        result = {
            "symbol": symbol,
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "history": data
        }
        
        cache_set(cache_key, result, expire_seconds=3600) # Cache for 1 hour
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")
