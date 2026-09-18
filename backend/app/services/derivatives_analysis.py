import yfinance as yf
import pandas as pd
from typing import Dict, Any

def get_options_data(symbol: str) -> Dict[str, Any]:
    """
    Fetches the nearest options chain (calls and puts) for a given symbol.
    """
    ticker = yf.Ticker(symbol)
    
    # Check if options are available
    if not ticker.options:
        return {"error": f"No options data available for {symbol}"}
        
    # Get the closest expiration date
    expiration = ticker.options[0]
    opt_chain = ticker.option_chain(expiration)
    
    # Function to clean and convert DataFrame to dict
    def clean_options_df(df: pd.DataFrame):
        df = df.replace({float('nan'): None})
        # Select key columns
        cols = ['contractSymbol', 'strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'inTheMoney']
        available_cols = [c for c in cols if c in df.columns]
        return df[available_cols].to_dict(orient='records')
        
    calls = clean_options_df(opt_chain.calls)
    puts = clean_options_df(opt_chain.puts)
    
    try:
        current_price = ticker.info.get('currentPrice', ticker.history(period='1d')['Close'].iloc[-1])
    except:
        current_price = 0.0

    return {
        "symbol": symbol,
        "expiration": expiration,
        "underlying_price": current_price,
        "calls": calls,
        "puts": puts
    }
