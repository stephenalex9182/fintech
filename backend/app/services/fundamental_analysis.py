import yfinance as yf
from sqlalchemy.orm import Session
from .. import models

def get_fundamental_data(symbol: str, db: Session = None):
    """
    Fetches fundamental data for a given symbol from yfinance.
    Optionally updates the database if db session is provided.
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    fundamentals = {
        "symbol": symbol,
        "pe_ratio": info.get("trailingPE"),
        "debt_to_equity": info.get("debtToEquity"),
        "revenue_growth": info.get("revenueGrowth"),
        "profit_margins": info.get("profitMargins"),
        "free_cashflow": info.get("freeCashflow"),
        "beta": info.get("beta")
    }
    
    if db:
        # Check if exists
        existing_data = db.query(models.FundamentalData).filter(models.FundamentalData.symbol == symbol).first()
        if existing_data:
            existing_data.pe_ratio = fundamentals["pe_ratio"]
            existing_data.debt_to_equity = fundamentals["debt_to_equity"]
            existing_data.revenue_growth = fundamentals["revenue_growth"]
            existing_data.profit_margins = fundamentals["profit_margins"]
            existing_data.free_cashflow = fundamentals["free_cashflow"]
            existing_data.beta = fundamentals["beta"]
        else:
            new_data = models.FundamentalData(**fundamentals)
            db.add(new_data)
        db.commit()
        
    return fundamentals
