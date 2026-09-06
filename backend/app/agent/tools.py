from langchain.tools import tool
from ..services.stock_api import get_stock_data
from ..services.technical_analysis import calculate_technical_indicators
from ..services.sentiment import analyze_sentiment

@tool
def fetch_stock_price(symbol: str) -> str:
    """Fetch current stock price and basic info for a given ticker symbol (e.g., RELIANCE.NS, AAPL)."""
    try:
        data = get_stock_data(symbol, period="1d")
        return f"Symbol: {symbol}\nCurrent Price: {data.get('current_price')}\nMarket Cap: {data.get('market_cap')}"
    except Exception as e:
        return f"Error fetching data for {symbol}: {str(e)}"

@tool
def technical_analysis_tool(symbol: str) -> str:
    """Calculates RSI and Moving Averages for a stock to determine trend."""
    try:
        data = get_stock_data(symbol, period="3mo")
        history = data.get("history", {})
        
        # Format for technical analysis service
        formatted_data = []
        for date_str, metrics in history.items():
            formatted_data.append({
                "close": metrics.get("Close"),
                "high": metrics.get("High"),
                "low": metrics.get("Low"),
                "volume": metrics.get("Volume")
            })
            
        result = calculate_technical_indicators(formatted_data)
        if "error" in result:
             return f"Analysis error: {result['error']}"
             
        return f"Technical Analysis for {symbol}:\nRSI (14): {result.get('rsi_14')}\nSMA 20: {result.get('sma_20')}\nSMA 50: {result.get('sma_50')}\nTrend: {result.get('trend')}"
    except Exception as e:
        return f"Error calculating technicals for {symbol}: {str(e)}"

@tool
def analyze_financial_sentiment(text: str) -> str:
    """Analyzes the sentiment of a given financial text or news headline."""
    result = analyze_sentiment([text])
    if result and "error" not in result[0]:
        return f"Sentiment: {result[0]['label']}, Confidence: {result[0]['score']:.2f}"
    return "Could not analyze sentiment."
